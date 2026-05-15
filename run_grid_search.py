# run_grid_search.py
import os
import json
import time
import gc
import torch
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig

import config

# --- EKSPERIMENTŲ PARAMETRŲ MATRICA ---
# Jei norite pradžioje ištestuoti tik vieną modelį, kitus galite užkomentuoti su #
MODELS_TO_TEST = [
    "meta-llama/Meta-Llama-3-8B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.2",
    "google/gemma-1.1-7b-it",
    "Qwen/Qwen2.5-7B-Instruct"
]

CHUNK_SIZES = [256, 512, 1024]
K_VALUES = [1, 3, 5, 10]
AUKSINIS_STANDARTAS = "auksinis_standartas.json"
# --------------------------------------

def load_json_documents_local(directory):
    documents = []
    json_path = os.path.join(directory, "cve_data.json")
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for entry in data:
            content = (f"CVE ID: {entry.get('cve_id')}\n"
                       f"Severity: {entry.get('severity')} (Score: {entry.get('score')})\n"
                       f"Product: {entry.get('affected_product')}\n"
                       f"Description: {entry.get('description')}")
            doc = Document(page_content=content, metadata={"source": "cve_data.json", "cve": entry.get('cve_id')})
            documents.append(doc)
    return documents

def build_faiss_db(chunk_size, overlap):
    db_path = f"vectorstore/db_faiss_{chunk_size}_{overlap}"
    if os.path.exists(db_path):
        print(f"   [!] DB jau egzistuoja ({db_path}), praleidžiame kūrimą.")
        return db_path

    print(f"   [*] Kuriama nauja DB: Chunk={chunk_size}")
    pdf_loader = PyPDFDirectoryLoader(config.DATA_DIR)
    all_documents = pdf_loader.load() + load_json_documents_local(config.DATA_DIR)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    chunks = text_splitter.split_documents(all_documents)
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_ID)
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(db_path)
    return db_path

def clear_vram():
    """Išvalo GPU atmintį, kad tilptų kitas modelis."""
    gc.collect()
    torch.cuda.empty_cache()

def run_grid_search():
    print(f"=== PRADEDAMAS MULTI-MODEL GRID SEARCH EKSPERIMENTAS ===")

    with open(AUKSINIS_STANDARTAS, 'r', encoding='utf-8') as f:
        klausimai = json.load(f)

    for model_id in MODELS_TO_TEST:
        print(f"\n==================================================")
        print(f"🚀 TESTUOJAMAS MODELIS: {model_id}")
        print(f"==================================================")

        safe_model_name = model_id.split("/")[-1]

        # 1. Krauname LLM modelį
        clear_vram()
        print("\n[1] Kraunamas LLM modelis į VRAM (4-bit)...")
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        )

        try:
            tokenizer = AutoTokenizer.from_pretrained(model_id, token=config.HF_TOKEN)
            model = AutoModelForCausalLM.from_pretrained(model_id, token=config.HF_TOKEN, quantization_config=bnb_config, device_map="auto")
            pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512, temperature=0.1, repetition_penalty=1.1, return_full_text=False)
            llm = HuggingFacePipeline(pipeline=pipe)
        except Exception as e:
            print(f"❌ KLAIDA KRAUNANT MODELĮ {model_id}: {e}")
            continue

            # ATNAUJINTAS ANGLIŠKAS PROMPT'AS
        template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a professional cybersecurity expert. Use strictly the provided context to answer the question. Answer clearly and concisely in English. If the answer is not contained in the context, output exactly: "Information not found in the provided context." Do not invent facts.<|eot_id|><|start_header_id|>user<|end_header_id|>

Context: {context}

Question: {question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
        PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])

        # 2. Vykdome parametrų paiešką šiam modeliui
        for chunk_size in CHUNK_SIZES:
            db_path = build_faiss_db(chunk_size, 100)
            embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_ID)
            db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)

            for k in K_VALUES:
                print(f"\n   >>> Testuojama k = {k} (Chunk = {chunk_size}) <<<")
                rezultatu_failas = f"rezultatai_{safe_model_name}_chunk{chunk_size}_k{k}.json"

                if os.path.exists(rezultatu_failas):
                    print(f"       [!] Failas {rezultatu_failas} jau yra, praleidžiame.")
                    continue

                retriever = db.as_retriever(search_kwargs={'k': k})
                qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True, chain_type_kwargs={"prompt": PROMPT})

                gauti_rezultatai = []
                for i, irasas in enumerate(klausimai):
                    q = irasas['klausimas']
                    print(f"       [{i+1}/{len(klausimai)}] {q[:40]}...", end="", flush=True)
                    start_time = time.time()
                    try:
                        response = qa_chain.invoke({"query": q})
                        gauti_rezultatai.append({
                            "klausimas": q,
                            "gautas_atsakymas": response['result'].strip(),
                            "gauti_saltiniai": [doc.metadata.get('source', '') for doc in response['source_documents']],
                            "trukme_sek": round(time.time() - start_time, 2)
                        })
                        print(f" (OK, {round(time.time() - start_time, 2)}s)")
                    except Exception as e:
                        print(f" (KLAIDA)")
                        gauti_rezultatai.append({"klausimas": q, "error": str(e)})

                with open(rezultatu_failas, 'w', encoding='utf-8') as f:
                    json.dump(gauti_rezultatai, f, ensure_ascii=False, indent=2)

        # 3. Ištriname modelį iš atminties prieš kraunant kitą
        del qa_chain
        del llm
        del pipe
        del model
        del tokenizer
        clear_vram()

    print("\n=== MULTI-MODEL GRID SEARCH SEKMINGAI BAIGTAS ===")

if __name__ == "__main__":
    run_grid_search()
# klausti.py
import torch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
from langchain.chains import RetrievalQA
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import config

# 1. Įdėjimų modelis ir DB
print(f"Kraunama duomenų bazė iš: {config.DB_FAISS_PATH}...")
embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_ID)
try:
    db = FAISS.load_local(config.DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
except RuntimeError:
    print("KLAIDA: Nerasta vektorinė DB. Pirmiausia paleiskite 'kurti_db.py'.")
    exit()

# Nustatome k=10
retriever = db.as_retriever(search_kwargs={'k': 10})

# 2. PROMPT PARINKIMAS
if "Llama-3" in config.MODEL_ID:
    print("   -> Naudojamas Llama 3 Prompt formatas.")
    template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a professional cybersecurity expert. Use strictly the provided context to answer the question. Answer clearly and concisely in English. If the answer is not contained in the context, output exactly: "Information not found in the provided context." Do not invent facts.<|eot_id|><|start_header_id|>user<|end_header_id|>

Context: {context}

Question: {question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
else:
    template = """[INST] ... [/INST]""" # (Senas kodas, jei reiktų)

PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])

# 3. Modelio paruošimas (OPTIMIZUOTA RTX 4060 8GB)
print(f"Kraunamas modelis: {config.MODEL_ID} (4-bit quantization)...")

# Konfigūracija, kad tilptų į 8GB VRAM
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16, # RTX 40 serija palaiko bfloat16 (greičiau)
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

tokenizer = AutoTokenizer.from_pretrained(config.MODEL_ID, token=config.HF_TOKEN)

model = AutoModelForCausalLM.from_pretrained(
    config.MODEL_ID,
    token=config.HF_TOKEN,
    quantization_config=bnb_config, # <-- Įjungiame 4-bit
    device_map="auto"
)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    temperature=0.1,
    repetition_penalty=1.1,
    return_full_text=False
)

llm = HuggingFacePipeline(pipeline=pipe)

# 4. RAG grandinė
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)

if __name__ == '__main__':
    # Testas
    res = qa_chain.invoke({"query": "Kas yra DDoS?"})
    print(res['result'])
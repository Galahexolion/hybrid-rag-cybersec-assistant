# kurti_db.py
import os
import json
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import config

def load_json_documents(directory):
    """Nuskaito JSON failus ir paverčia juos į LangChain dokumentus."""
    documents = []
    json_path = os.path.join(directory, "cve_data.json")

    if os.path.exists(json_path):
        print(f"   -> Rastas JSON failas: {json_path}")
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for entry in data:
                # Suformuojame tekstą, kurį "skaitys" ir supras AI
                content = (
                    f"CVE ID: {entry.get('cve_id')}\n"
                    f"Severity: {entry.get('severity')} (Score: {entry.get('score')})\n"
                    f"Product: {entry.get('affected_product')}\n"
                    f"Description: {entry.get('description')}"
                )
                # Pridedame metaduomenis (svarbu šaltinių atsekamumui)
                doc = Document(
                    page_content=content,
                    metadata={"source": "cve_data.json", "cve": entry.get('cve_id')}
                )
                documents.append(doc)
            print(f"   -> Sėkmingai įkelta {len(data)} CVE įrašų.")
        except Exception as e:
            print(f"   -> KLAIDA skaitant JSON: {e}")
    else:
        print("   -> JSON failų nerasta.")

    return documents

def create_vector_db():
    print(f"Nustatymai: Chunk={config.CHUNK_SIZE}, Overlap={config.CHUNK_OVERLAP}")

    # 1. Dokumentų įkėlimas (PDF + JSON)
    print("Įkeliami dokumentai...")

    # PDF
    print("   -> Ieškoma PDF failų...")
    pdf_loader = PyPDFDirectoryLoader(config.DATA_DIR)
    pdf_docs = pdf_loader.load()
    print(f"   -> Rasta PDF puslapių: {len(pdf_docs)}")

    # JSON (CVE)
    print("   -> Ieškoma JSON failų...")
    json_docs = load_json_documents(config.DATA_DIR)

    all_documents = pdf_docs + json_docs

    if not all_documents:
        print("KLAIDA: Nerasta jokių dokumentų.")
        return

    # 2. Segmentavimas
    print("Tekstas segmentuojamas...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(all_documents)

    # 3. Įdėjimų modelis
    print(f"Kraunamas įdėjimų modelis: {config.EMBEDDING_MODEL_ID}...")
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_ID)

    # 4. Kūrimas ir saugojimas
    print("Generuojama vektorinė duomenų bazė...")
    if not os.path.exists(os.path.dirname(config.DB_FAISS_PATH)):
        os.makedirs(os.path.dirname(config.DB_FAISS_PATH))

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(config.DB_FAISS_PATH)
    print(f"✅ Baigta! DB atnaujinta su PDF ir JSON duomenimis.")

if __name__ == '__main__':
    create_vector_db()
# config.py
import os

# Jūsų HuggingFace raktas (įklijuokite jį čia)
# HF_TOKEN = ""

# Pasirinktas modelis (galite atkomentuoti norimą)
# Senas modelis (prastai veikė su LT):
# MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"

# NAUJAS modelis (Llama 3 - daug geresnis lietuvių kalbai):
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"

# Įdėjimų modelis (kol kas paliekame BGE, vėliau galėsime pakeisti)
EMBEDDING_MODEL_ID = "BAAI/bge-small-en-v1.5"

# Parametrai
CHUNK_SIZE = 1024  # Galima bandyti 512, jei atsakymai bus netikslūs
CHUNK_OVERLAP = 100
DATA_DIR = "duomenys"
DB_FAISS_PATH = f"vectorstore/db_faiss_{CHUNK_SIZE}_{CHUNK_OVERLAP}"

# Nustatome aplinkos kintamąjį, kad bibliotekos matytų raktą
os.environ["HUGGING_FACE_HUB_TOKEN"] = HF_TOKEN
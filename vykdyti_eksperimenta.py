# vykdyti_eksperimenta.py
import json
import os
import time
from klausti import qa_chain
import config

# Išvalome modelio pavadinimą failui (kad nebūtų "/" simbolių)
safe_model_name = config.MODEL_ID.split("/")[-1]
# Rezultatas bus pvz.: rezultatai_Meta-Llama-3-8B-Instruct_k10.json
REZULTATU_FAILAS = f"rezultatai_{safe_model_name}_k10.json"
AUKSINIS_STANDARTAS = "auksinis_standartas.json"

def vykdyti_eksperimenta():
    print(f"PRADEDAMAS EKSPERIMENTAS SU MODELIU: {config.MODEL_ID}")

    # Užtikriname k=10
    qa_chain.retriever.search_kwargs['k'] = 10

    # -----------------------------------------------------------
    # DEBUG REŽIMAS: Nustatome kiek klausimų testuoti
    # Pakeiskite į None, kai norėsite pilno testo (15 klausimų)
    DEBUG_LIMIT = None
    # -----------------------------------------------------------

    safe_model_name = config.MODEL_ID.split("/")[-1]
    REZULTATU_FAILAS = f"rezultatai_{safe_model_name}_k10_DEBUG.json" # Pridedame _DEBUG prie failo vardo

    print(f"Parametrai: K=10, Modelis={safe_model_name}")
    print(f"TESTUOJAMA TIK {DEBUG_LIMIT} KLAUSIMŲ (Greitas patikrinimas)")
    print(f"Rezultatai bus saugomi į: {REZULTATU_FAILAS}")

    try:
        with open(AUKSINIS_STANDARTAS, 'r', encoding='utf-8') as f:
            klausimai = json.load(f)

        # ČIA YRA ESMINIS PAKEITIMAS - IMAME TIK PIMUS 3
        if DEBUG_LIMIT:
            klausimai = klausimai[:DEBUG_LIMIT]

    except FileNotFoundError:
        print(f"KLAIDA: Nerastas failas {AUKSINIS_STANDARTAS}")
        return

    gauti_rezultatai = []
    total = len(klausimai)

    for i, irasas in enumerate(klausimai):
        # ... (visas ciklas toliau lieka toks pat) ...
        klausimas = irasas['klausimas']
        print(f"\n[{i+1}/{total}] Klausimas: {klausimas}")

        start_time = time.time()
        try:
            response = qa_chain.invoke({"query": klausimas})
            atsakymas = response['result'].strip()
            saltiniai = [doc.metadata.get('source', '') for doc in response['source_documents']]

            rezultatas = {
                "klausimas": klausimas,
                "gautas_atsakymas": atsakymas,
                "gauti_saltiniai": saltiniai,
                "trukme_sek": round(time.time() - start_time, 2)
            }
            gauti_rezultatai.append(rezultatas)

            # Iškart parodome, ką rado, kad nereikėtų laukti failo
            print(f"   -> Atsakyta per {rezultatas['trukme_sek']}s.")
            print(f"   -> Rasti šaltiniai: {saltiniai}")

        except Exception as e:
            print(f"   -> KLAIDA: {e}")
            gauti_rezultatai.append({"klausimas": klausimas, "error": str(e)})

    with open(REZULTATU_FAILAS, 'w', encoding='utf-8') as f:
        json.dump(gauti_rezultatai, f, ensure_ascii=False, indent=2)

    print(f"\nDEBUG EKSPERIMENTAS BAIGTAS.")

if __name__ == "__main__":
    vykdyti_eksperimenta()
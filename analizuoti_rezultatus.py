import os
import json
import csv
import re

AUKSINIS_STANDARTAS = "auksinis_standartas.json"
REZULTATU_APLANKAS = "." # Jei failai tame pačiame aplanke
ISVESTIES_FAILAS = "galutiniai_rezultatai.csv"

def gauti_rezultatu_failus():
    failai = []
    for f in os.listdir(REZULTATU_APLANKAS):
        # Ieškome failų, atitinkančių mūsų struktūrą, ir ignoruojame DEBUG failus
        if f.startswith("rezultatai_") and f.endswith(".json") and "DEBUG" not in f:
            failai.append(f)
    return failai

def normalizuoti_kelia(kelias):
    """Panaikina skirtumus tarp pasvirųjų brūkšnių (\ ir /)"""
    return kelias.replace("\\", "/").lower()

def analizuoti():
    print("=== PRADEDAMA REZULTATŲ ANALIZĖ ===")

    # Uzkrauname etalonus
    with open(AUKSINIS_STANDARTAS, 'r', encoding='utf-8') as f:
        etalonai_data = json.load(f)

    # Sukuriame žodyną greitai paieškai: {klausimas: [etaloninis_saltinis_1, ...]}
    etalonai = {}
    for item in etalonai_data:
        etalonai[item['klausimas']] = [normalizuoti_kelia(s) for s in item['etaloniniai_saltiniai']]

    failai = gauti_rezultatu_failus()
    apdoroti_duomenys = []

    for failas in failai:
        # Iš failo pavadinimo ištraukiame parametrus
        # Pvz: rezultatai_Meta-Llama-3-8B-Instruct_chunk512_k5.json
        match = re.search(r"rezultatai_(.*)_chunk(\d+)_k(\d+)\.json", failas)
        if not match:
            continue

        modelis = match.group(1)
        chunk_size = int(match.group(2))
        k_value = int(match.group(3))

        with open(failas, 'r', encoding='utf-8') as f:
            rezultatai = json.load(f)

        is_viso_klausimu = len(rezultatai)
        teisingai_rasti = 0
        bendra_trukme = 0.0

        for rez in rezultatai:
            klausimas = rez['klausimas']
            gauti_saltiniai = [normalizuoti_kelia(s) for s in rez.get('gauti_saltiniai', [])]
            trukme = rez.get('trukme_sek', 0)
            bendra_trukme += trukme

            tikimi_saltiniai = etalonai.get(klausimas, [])

            # Tikriname, ar BENT VIENAS etaloninis šaltinis yra tarp gautų šaltinių (Recall)
            rasta = False
            for tikimas in tikimi_saltiniai:
                for gautas in gauti_saltiniai:
                    # Naudojame substring match, kad išvengtume pilno kelio neatitikimų
                    if tikimas in gautas or gautas in tikimas:
                        rasta = True
                        break
                if rasta:
                    break

            if rasta:
                teisingai_rasti += 1

        recall_proc = (teisingai_rasti / is_viso_klausimu) * 100 if is_viso_klausimu > 0 else 0
        vid_trukme = bendra_trukme / is_viso_klausimu if is_viso_klausimu > 0 else 0

        apdoroti_duomenys.append({
            "Modelis": modelis,
            "Chunk Dydis": chunk_size,
            "K Reikšmė": k_value,
            "Tikslumas (Recall %)": round(recall_proc, 2),
            "Vid. Laikas (sek)": round(vid_trukme, 2)
        })

    # Rūšiuojame rezultatus pagal Modelį, tada Chunk, tada K
    apdoroti_duomenys.sort(key=lambda x: (x['Modelis'], x['Chunk Dydis'], x['K Reikšmė']))

    # Saugome į CSV
    with open(ISVESTIES_FAILAS, 'w', newline='', encoding='utf-8') as csvfile:
        lauku_pavadinimai = ["Modelis", "Chunk Dydis", "K Reikšmė", "Tikslumas (Recall %)", "Vid. Laikas (sek)"]
        writer = csv.DictWriter(csvfile, fieldnames=lauku_pavadinimai)
        writer.writeheader()
        writer.writerows(apdoroti_duomenys)

    print(f"✅ Analizė baigta! Rezultatai išsaugoti į failą: {ISVESTIES_FAILAS}")

if __name__ == "__main__":
    analizuoti()
# vertinti.py
import json
import os

def normalizuoti_kelia(kelias):
    """
    Suvienodina failų kelius:
    1. Paima tik failo pavadinimą (atmeta aplankus).
    2. Pašalina '_puslapis_X' prierašą, jei toks yra.
    """
    # 1. Paimame tik failo pavadinimą (pvz., 'failas.pdf')
    pavadinimas = os.path.basename(kelias).strip()

    # 2. Jei pavadinime yra "_puslapis_", kerpame viską, kas po jo
    # Tai leis sulyginti "file.pdf_puslapis_0" su "file.pdf"
    if "_puslapis_" in pavadinimas:
        pavadinimas = pavadinimas.split("_puslapis_")[0]

    return pavadinimas

def apskaiciuoti_metrikas(etaloniniai_saltiniai, gauti_saltiniai):
    """Apskaičiuoja Precision, Recall ir F1 metrikas vienam klausimui."""

    # Normalizuojame kelius (išvalome nuo aplankų ir puslapių numerių)
    etalonine_aibe = {normalizuoti_kelia(s) for s in etaloniniai_saltiniai}
    gauta_aibe = {normalizuoti_kelia(s) for s in gauti_saltiniai}

    # Debugging (Galite atkomentuoti, jei norite matyti, kas lyginama)
    # print(f"Etalonas: {etalonine_aibe}")
    # print(f"Gauta:    {gauta_aibe}")

    tp = len(etalonine_aibe.intersection(gauta_aibe)) # Teisingai rasti
    fp = len(gauta_aibe.difference(etalonine_aibe))   # Rasti nereikalingi
    fn = len(etalonine_aibe.difference(gauta_aibe))   # Nerasti reikalingi

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {"precision": precision, "recall": recall, "f1": f1}

def pagrindinis_vertinimas(auksinio_standarto_failas, rezultatu_failas):
    print(f"Vertinamas failas: {rezultatu_failas}")

    try:
        with open(auksinio_standarto_failas, 'r', encoding='utf-8') as f:
            auksinis_standartas = json.load(f)
        with open(rezultatu_failas, 'r', encoding='utf-8') as f:
            rezultatai = json.load(f)
    except FileNotFoundError as e:
        print(f"KLAIDA: Nerastas failas – {e.filename}")
        return

    rezultatu_zemelapis = {item['klausimas']: item['gauti_saltiniai'] for item in rezultatai}
    visos_metrikos = []

    print("-" * 60)
    print(f"{'Klausimas (trumpintas)':<40} | {'F1':<6} | {'P':<6} | {'R':<6}")
    print("-" * 60)

    for irasas in auksinis_standartas:
        klausimas = irasas['klausimas']
        etaloniniai_saltiniai = irasas['etaloniniai_saltiniai']
        gauti_saltiniai = rezultatu_zemelapis.get(klausimas)

        if gauti_saltiniai is not None:
            metrikos = apskaiciuoti_metrikas(etaloniniai_saltiniai, gauti_saltiniai)
            visos_metrikos.append(metrikos)

            # Atvaizduojame kiekvieno klausimo rezultatą
            print(f"{klausimas[:37]+'...':<40} | {metrikos['f1']:.2f}   | {metrikos['precision']:.2f}   | {metrikos['recall']:.2f}")
        else:
            print(f"ĮSPĖJIMAS: Nerastas atsakymas į klausimą: '{klausimas[:20]}...'")

    if visos_metrikos:
        avg_precision = sum(m['precision'] for m in visos_metrikos) / len(visos_metrikos)
        avg_recall = sum(m['recall'] for m in visos_metrikos) / len(visos_metrikos)
        avg_f1 = sum(m['f1'] for m in visos_metrikos) / len(visos_metrikos)

        print("-" * 60)
        print(f"REZULTATŲ SUVESTINĖ ({len(visos_metrikos)} klausimų)")
        print("-" * 60)
        print(f"Vidutinis Tikslumas (Precision): {avg_precision:.4f}")
        print(f"Vidutinis Atšaukimas (Recall):   {avg_recall:.4f}")
        print(f"Vidutinis F1 balas:              {avg_f1:.4f}")
        print("-" * 60)
    else:
        print("Nepavyko apskaičiuoti metrikų.")

if __name__ == '__main__':
    file_gold = "auksinis_standartas.json"
    file_results = "rezultatai_Meta-Llama-3-8B-Instruct_k10_DEBUG.json"

    pagrindinis_vertinimas(file_gold, file_results)
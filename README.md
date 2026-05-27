# Hybrid RAG Cybersecurity Assistant

Šis projektas yra magistro baigiamojo darbo metu sukurta hibridinė *Retrieval-Augmented Generation* (RAG) sistema, skirta kibernetinio saugumo konsultacijų automatizavimui. Sistema integruoja nestruktūrizuotus PDF dokumentus ir struktūrizuotus JSON (CVE) pažeidžiamumų įrašus, užtikrindama duomenų privatumą veikiant lokalioje aplinkoje.

## Pagrindinės funkcijos
* **Hibridinė paieška:** Semantinė paieška (FAISS) derinama su struktūrizuotais techniniais duomenimis (CVE).
* **Lokalus LLM vykdymas:** Pilnas duomenų privatumas naudojant atvirojo kodo modelius (*Meta-Llama-3*, *Mistral*, *Qwen*, *Gemma*).
* **Resursų optimizavimas:** Įdiegtas 4 bitų parametrų kvantavimas (`BitsAndBytes` / GGUF), leidžiantis sistemą paleisti su 8 GB VRAM.
* **Eksperimentinis vertinimas:** Automatinis hiperparametrų paieškos (*Grid Search*) ir modelių generavimo kokybės matavimas.

## Projekto struktūra

* **Pagrindiniai sistemos failai:**
  * `app.py` – Pagrindinė interaktyvi `Streamlit` vartotojo sąsaja.
  * `kurti_db.py` – Duomenų įkėlimo, segmentavimo ir FAISS vektorinės bazės kūrimo skriptas.
  * `config.py` – Centralizuotas sistemos parametrų konfigūracijos failas (rinkinių keliai, `CHUNK_SIZE`, modelių ID).
  * `klausti.py` – Užklausų vykdymo ir paieškos loginis modulis.

* **Eksperimentai ir vertinimas:**
  * `vykdyti_eksperimenta.py` – Pagrindinis eksperimentų vykdymo skriptas.
  * `run_grid_search.py` – Hiperparametrų optimizavimo (*Grid Search*) konvejeris.
  * `vertinti.py` – Informacijos atgaminimo (*Recall*) ir generavimo kokybės vertinimo logika.
  * `analizuoti_rezultatus.py` – Gautų eksperimentinių duomenų statistinė analizė.
  * `galutiniai_rezultatai.csv` – Sukaupti eksperimentų matavimų rezultatai.

* **Rezultatų vizualizacija (Grafikai):**
  * `braizyti_embeddings.py` – Įterpinių modelių efektyvumo grafikų braižymas.
  * `braizyti_grafikus.py` / `braizyti_grafika.py` – Rezultatų vizualizavimo skriptai.
  * `braizyti_kokybe.py` – LLM generavimo kokybės ir stabilumo grafikų generavimas.

* **Pagalbiniai įrankiai:**
  * `tikrinti_gpu.py` – CUDA ir VRAM prieinamumo patikrinimo skriptas.
  * `generuoti_cve.py` – Testinių CVE įrašų JSON formatu paruošimas.
  * `requirements.txt` – Projekto Python priklausomybių sąrašas.

## Reikalavimai
* Python 3.10+
* Nvidia GPU (Rekomenduojama bent 8 GB VRAM)
* CUDA Toolkit v12.8+
* Hugging Face token'as

## Diegimas

1. **Klonuoti repozitoriją:**
   ```bash
   git clone [https://github.com/Galahexolion/hybrid-rag-cybersec-assistant.git](https://github.com/Galahexolion/hybrid-rag-cybersec-assistant.git)
   cd hybrid-rag-cybersec-assistant
   ```

2. **Įdiegti priklausomybes:**
   ```bash
   pip install -r requirements.txt
   ```

## Naudojimo instrukcija

### 1. Duomenų paruošimas
Sukurkite aplanką (numatytasis kelias nurodytas `config.py`) ir į jį įkelkite:
* PDF formato dokumentus (mokslinius straipsnius, ataskaitas). Atsisiųskite duomenų rinkinį iš čia: [https://drive.google.com/drive/folders/1MJu6WEIjgkdzTVElGRQg18yIZAvLrxbG?usp=sharing]
* `cve_data.json` failą su struktūrizuotais CVE įrašais.

### 2. Vektorinės duomenų bazės sukūrimas
Prieš paleidžiant asistentą, būtina suindeksuoti dokumentus ir sukurti FAISS indeksą:
```bash
python kurti_db.py
```

### 3. Asistento paleidimas
Sistemos grafinės sąsajos paleidimas naudojant `Streamlit`:
```bash
streamlit run app.py
```

### 4. Eksperimentinio tyrimo pakartojimas
Norint paleisti pilną hiperparametrų optimizavimo ciklą ir sugeneruoti tyrimo rezultatus:
```bash
python run_grid_search.py
python vykdyti_eksperimenta.py
python vertinti.py
```
Grafikų atnaujinimui paleiskite vizualizacijos skriptus (pvz., `python braizyti_grafikus.py`).

## Tyrimo rezultatai
Projekto aplanke esantys grafikai vizualizuoja magistro darbe aprašytus eksperimentus:
* `4_5_pav_Embeddings.png` – Įterpinių modelių efektyvumo palyginimas.
* `4_5_pav_Recall.png` – Paieškos gylio ($k$) įtaka informacijos atgaminimui.
* `4_6_pav_Greitis.png` – 4 bitų kvantavimo įtaka generavimo spartai.
* `4_7_pav_Kokybe.png` – LLM modelių stabilumo ir instrukcijų laikymosi analizė.

## Autorius
Edvinas Merkevičius – Vytauto Didžiojo universitetas, Informatikos fakultetas.

## Licencija
Šis projektas platinamas pagal MIT licenciją.

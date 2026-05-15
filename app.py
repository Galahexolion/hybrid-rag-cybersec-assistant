# app.py

import streamlit as st
import time
# Importuojame jau paruoštą grandinę iš jūsų failo 'klausti.py'
# Tai automatiškai užkraus modelį, FAISS ir konfigūraciją.
from klausti import qa_chain
import config

# ---------------------------------------------------------
# PUSLAPIO KONFIGŪRACIJA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Kibernetinio Saugumo Asistentas",
    page_icon="🛡️",
    layout="wide"
)

# ---------------------------------------------------------
# ŠONINĖ JUOSTA (SIDEBAR) - INFO APIE SISTEMĄ
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/cyber-security.png", width=80)
    st.title("Sistemos Parametrai")

    st.info(f"🧠 **LLM Modelis:**\n{config.MODEL_ID.split('/')[-1]}")
    st.info(f"🔍 **Paieškos gylis (k):** 10")
    st.info(f"📚 **Žinių bazė:**\nPDF Straipsniai + JSON (CVE)")

    st.markdown("---")
    st.caption("Magistro baigiamasis darbas")
    st.caption("© Edvinas Merkevičius, 2025")

# ---------------------------------------------------------
# PAGRINDINIS LANGAS
# ---------------------------------------------------------
st.markdown("# 🛡️ Kibernetinio Saugumo Žinių Asistentas")
st.markdown("### *Retrieval-Augmented Generation (RAG) Prototipas*")
st.markdown("---")

# Vartotojo įvestis
query = st.text_input(
    "Užduokite klausimą (pvz.: Koks yra CVE-2023-XYZ kritiškumo lygis?)",
    placeholder="Rašykite klausimą čia..."
)

# Mygtukas paieškai
if st.button("Ieškoti ir Generuoti", type="primary"):
    if not query:
        st.warning("Prašome įvesti klausimą.")
    else:
        # RAG Vykdymas
        with st.spinner('Vykdoma semantinė paieška hibridinėje duomenų bazėje ir generuojamas atsakymas...'):
            try:
                start_time = time.time()

                # Kviečiame jūsų RAG grandinę
                response = qa_chain.invoke({"query": query})

                end_time = time.time()
                duration = round(end_time - start_time, 2)

                # Ištraukiame rezultatus
                answer = response['result']
                source_docs = response['source_documents']

                # -----------------------------------------------------
                # 1. ATSAKYMO ATVAIZDAVIMAS
                # -----------------------------------------------------
                st.success(f"Generavimas baigtas per {duration} s.")
                st.markdown("### 🤖 Generuotas Atsakymas:")
                st.write(answer)

                st.markdown("---")

                # -----------------------------------------------------
                # 2. "SEARCH ENGINE" REZULTATAI (XAI - Explainability)
                # -----------------------------------------------------
                st.subheader(f"📚 Rasti Šaltiniai ({len(source_docs)} dokumentai):")
                st.markdown("*Čia pateikiami tikslūs fragmentai, kuriais rėmėsi modelis (Skaidrumo užtikrinimas)*")

                for i, doc in enumerate(source_docs):
                    # Paimame metaduomenis (failo pavadinimą, CVE ID ir t.t.)
                    source_name = doc.metadata.get("source", "Nežinomas šaltinis")
                    cve_id = doc.metadata.get("cve", "")

                    # Jei tai CVE įrašas iš JSON, pridedame ID prie pavadinimo
                    title_display = f"{i+1}. Šaltinis: {source_name}"
                    if cve_id:
                        title_display += f" (CVE: {cve_id})"

                    # Atvaizduojame išskleidžiamame lange
                    with st.expander(title_display):
                        st.markdown(f"**Failo kelias:** `{source_name}`")
                        st.text_area("Fragmento turinis:", doc.page_content, height=150)

            except Exception as e:
                st.error(f"Įvyko klaida vykdant užklausą: {e}")
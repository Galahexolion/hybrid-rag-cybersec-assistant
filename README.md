\# Hibridinis RAG kibernetinio saugumo asistentas



Ši repozitorija skirta magistro baigiamajam darbui „Hibridinės informacijos paieška grįsto generavimo (RAG) sistemos projektavimas ir optimizavimas kibernetinio saugumo srityje“ (VDU, 2026).



\## Apie projektą

Tai RAG prototipas, suprojektuotas apdoroti tiek nestruktūrizuotus PDF mokslinius dokumentus, tiek linearizuotus CVE pažeidžiamumų įrašus. Sistema naudoja 4-bit kvantuotą `Meta-Llama-3-8B-Instruct` modelį lokaliam ir konfidencialiam generavimui.



\## Naudotos technologijos

\* \*\*Python 3.10+\*\*

\* \*\*LangChain\*\* (grandinių valdymas)

\* \*\*FAISS\*\* (vektorinė duomenų bazė)

\* \*\*BGE-small-en-v1.5\*\* (įterpinių modelis)

\* \*\*Streamlit\*\* (grafinė vartotojo sąsaja)



\## Kaip paleisti sistemą lokaliai



1\. Klonuokite repozitoriją:

&#x20;  ```bash

&#x20;  git clone \[https://github.com/JusuVardas/hybrid-rag-cybersec-assistant.git](https://github.com/JusuVardas/hybrid-rag-cybersec-assistant.git)


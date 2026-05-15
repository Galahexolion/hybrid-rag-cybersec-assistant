import matplotlib.pyplot as plt
import numpy as np

# Jūsų gauti duomenys iš vertinti.py
metrics = ['Tikslumas (Precision)', 'Atšaukimas (Recall)', 'F1-Balas']
values = [0.2057, 1.0000, 0.3319]

# Grafiko nustatymai
fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(metrics, values, color=['#d9534f', '#5cb85c', '#5bc0de'], width=0.6)

# Pridedame reikšmes virš stulpelių
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.02, f"{yval:.4f}", ha='center', va='bottom', fontsize=12, fontweight='bold')

# Ašių pavadinimai ir antraštė
ax.set_ylabel('Reikšmė (0-1)', fontsize=12)
ax.set_title('RAG Paieškos sistemos (Retriever) efektyvumas (k=10)', fontsize=14, fontweight='bold')
ax.set_ylim(0, 1.1)  # Kad būtų vietos viršuje
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Išsaugome
plt.savefig('grafikas_retriever_metrics.png', dpi=300)
print("Grafikas išsaugotas: grafikas_retriever_metrics.png")
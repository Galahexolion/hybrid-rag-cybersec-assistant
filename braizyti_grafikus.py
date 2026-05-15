import matplotlib.pyplot as plt
import numpy as np

def braizyti_recall_grafika():
    """
    Braižo 4.5 pav.: Paieškos sistemos efektyvumas (Recall %)
    """
    # Duomenys iš Jūsų analizės
    k_values = ['k=1', 'k=3', 'k=5', 'k=10']
    chunk_256 = [43.33, 50.00, 53.33, 66.67]
    chunk_512 = [36.67, 40.00, 60.00, 70.00]
    chunk_1024 = [46.67, 63.33, 66.67, 76.67]

    x = np.arange(len(k_values))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))

    # Stulpeliai
    rects1 = ax.bar(x - width, chunk_256, width, label='256 žetonai', color='#A9C4EB')
    rects2 = ax.bar(x, chunk_512, width, label='512 žetonų', color='#5C8CD0')
    rects3 = ax.bar(x + width, chunk_1024, width, label='1024 žetonai', color='#1D4E89')

    # Ašių ir pavadinimų nustatymai
    ax.set_ylabel('Atšaukimas (Recall %)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Paieškos gylis (k)', fontsize=12, fontweight='bold')
    ax.set_title('4.5 pav. Paieškos posistemės atgaminimo tikslumas', fontsize=14, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(k_values, fontsize=11)
    ax.set_ylim(0, 100)
    ax.legend(fontsize=11)

    # Pridedame reikšmes virš stulpelių
    ax.bar_label(rects1, padding=3, fmt='%.1f%%')
    ax.bar_label(rects2, padding=3, fmt='%.1f%%')
    ax.bar_label(rects3, padding=3, fmt='%.1f%%')

    # Tinklelis geresniam skaitomumui
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.7)

    # Išsaugome aukšta raiška
    plt.tight_layout()
    plt.savefig('4_5_pav_Recall.png', dpi=300)
    print("✅ Išsaugotas grafikas: 4_5_pav_Recall.png")


def braizyti_greicio_grafika():
    """
    Braižo 4.6 pav.: Modelių generavimo greičio palyginimas (Chunk=1024, k=10)
    """
    # Duomenys iš CSV (tik optimaliausiems parametrams Chunk=1024, K=10)
    modeliai = ['Google\nGemma-1.1', 'Meta\nLlama-3-8B', 'Qwen 2.5-7B', 'Mistral-7B-v0.2']
    laikas_sek = [3.54, 7.96, 11.81, 13.60]

    # Spalvos: Gemmai (raudona - klaidinga), Llama (žalia - ideali), kitiems (geltona/mėlyna)
    spalvos = ['#E74C3C', '#2ECC71', '#F1C40F', '#3498DB']

    fig, ax = plt.subplots(figsize=(10, 6))
    stulpeliai = ax.bar(modeliai, laikas_sek, color=spalvos, width=0.5)

    ax.set_ylabel('Vidutinis generavimo laikas (sekundėmis)', fontsize=12, fontweight='bold')
    ax.set_title('4.6 pav. Kalbos modelių atsakymų generavimo greitis (k=10, 1024 žetonai)', fontsize=14, pad=15)

    # Pridedame reikšmes virš stulpelių
    ax.bar_label(stulpeliai, padding=3, fmt='%.2f s', fontsize=11, fontweight='bold')

    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.7)

    plt.tight_layout()
    plt.savefig('4_6_pav_Greitis.png', dpi=300)
    print("✅ Išsaugotas grafikas: 4_6_pav_Greitis.png")

if __name__ == "__main__":
    # Jei neturite matplotlib bibliotekos, terminale įrašykite: pip install matplotlib
    braizyti_recall_grafika()
    braizyti_greicio_grafika()
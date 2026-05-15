import matplotlib.pyplot as plt

def braizyti_embeddings_grafika():
    """
    Braižo 4.5 pav.: Įdėjimų modelių Recall palyginimas pradiniame teste.
    """
    modeliai = ['all-MiniLM-L6-v2', 'BGE-small-en-v1.5']
    recall_reiksmes = [63.33, 100.00]

    # Spalvos: pilka silpnesniam, mėlyna nugalėtojui
    spalvos = ['#95A5A6', '#2980B9']

    fig, ax = plt.subplots(figsize=(8, 5))
    stulpeliai = ax.bar(modeliai, recall_reiksmes, color=spalvos, width=0.5)

    ax.set_ylabel('Atšaukimas (Recall %)', fontsize=12, fontweight='bold')
    ax.set_title('4.5 pav. Įdėjimų modelių efektyvumo palyginimas (parengiamasis etapas)', fontsize=13, pad=15)
    ax.set_ylim(0, 110) # Šiek tiek vietos viršuje tekstui

    # Pridedame reikšmes virš stulpelių
    ax.bar_label(stulpeliai, padding=3, fmt='%.2f%%', fontsize=12, fontweight='bold')

    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.7)

    plt.tight_layout()
    plt.savefig('4_5_pav_Embeddings.png', dpi=300)
    print("✅ Išsaugotas grafikas: 4_5_pav_Embeddings.png")

if __name__ == "__main__":
    braizyti_embeddings_grafika()
import matplotlib.pyplot as plt
import numpy as np

def braizyti_kokybes_grafika():
    """
    Braižo 4.7 pav.: Atsakymų pasiskirstymas pagal kokybės kategorijas.
    Pastaba: Duomenys aproksimuoti remiantis JSON failų analize (iš 30 užklausų).
    """
    modeliai = ['Meta\nLlama-3', 'Qwen 2.5', 'Mistral\nv0.2', 'Google\nGemma-1.1']

    # Iš 30 klausimų (apytiksliai pagal mūsų atradimus JSON failuose)
    sekmingi = [30, 0, 0, 0] # Llama 100% sėkminga
    su_klaidom = [0, 30, 30, 18] # Qwen (kilpos), Mistral (prompt bleeding), Gemma (HTML šiukšlės)
    nuluze = [0, 0, 0, 12] # Gemma grąžino daug tuščių "" atsakymų

    width = 0.6
    fig, ax = plt.subplots(figsize=(10, 6))

    # Braižome "Stacked bar chart" (vienas ant kito)
    p1 = ax.bar(modeliai, sekmingi, width, label='Sėkmingi (akademinė struktūra)', color='#2ECC71')
    p2 = ax.bar(modeliai, su_klaidom, width, bottom=sekmingi, label='Sisteminės/formatavimo klaidos', color='#F1C40F')
    p3 = ax.bar(modeliai, nuluze, width, bottom=np.array(sekmingi)+np.array(su_klaidom), label='Nulūžę (tušti) atsakymai', color='#E74C3C')

    ax.set_ylabel('Užklausų skaičius (iš 30)', fontsize=12, fontweight='bold')
    ax.legend(loc='upper right', bbox_to_anchor=(1.05, 1.15), fontsize=10)
    ax.set_ylim(0, 35)

    # Pridedame tinkleli
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.7)

    plt.tight_layout()
    plt.savefig('4_7_pav_Kokybe.png', dpi=300)
    print("✅ Išsaugotas grafikas: 4_7_pav_Kokybe.png")

if __name__ == "__main__":
    braizyti_kokybes_grafika()
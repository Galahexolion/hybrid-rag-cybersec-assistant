import torch

if torch.cuda.is_available():
    print("✅ GPU yra prieinama!")
    print(f"GPU Įrenginio pavadinimas: {torch.cuda.get_device_name(0)}")
else:
    print("❌ GPU neprieinama. PyTorch naudos CPU.")

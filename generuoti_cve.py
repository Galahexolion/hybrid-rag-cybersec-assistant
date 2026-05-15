# generuoti_cve.py
import json
import random

# Jūsų pradiniai 3 įrašai
pradiniai_cve = [
    {
        "cve_id": "CVE-2024-1234",
        "description": "Critical SQL Injection vulnerability in SecureLogin 5.0 allowing attackers to bypass authentication via crafted payload.",
        "severity": "HIGH",
        "score": 9.8,
        "affected_product": "SecureLogin 5.0"
    },
    {
        "cve_id": "CVE-2023-9876",
        "description": "Buffer overflow in WebServerPro version 2.1 handling large headers, leading to potential remote code execution.",
        "severity": "CRITICAL",
        "score": 10.0,
        "affected_product": "WebServerPro 2.1"
    },
    {
        "cve_id": "CVE-2024-5555",
        "description": "Cross-Site Scripting (XSS) vulnerability in UserForum app allows stealing session cookies.",
        "severity": "MEDIUM",
        "score": 5.4,
        "affected_product": "UserForum 3.2"
    }
]

produktai = ["Apache Server", "Nginx", "Windows 11", "Ubuntu Linux", "Cisco Router", "MySQL", "PostgreSQL", "React", "WordPress", "Docker"]
pažeidžiamumai = ["Cross-Site Scripting (XSS)", "SQL Injection", "Buffer Overflow", "Remote Code Execution (RCE)", "Authentication Bypass", "Denial of Service (DoS)", "Path Traversal"]

sugeneruoti_cve = []

# Generuojame 500 sintetinių įrašų
for i in range(1, 501):
    metai = random.choice([2021, 2022, 2023, 2024])
    cve_id = f"CVE-{metai}-{random.randint(10000, 99999)}"
    produktas = f"{random.choice(produktai)} {random.randint(1, 15)}.{random.randint(0, 9)}"
    tipas = random.choice(pažeidžiamumai)

    score = round(random.uniform(3.0, 10.0), 1)
    if score >= 9.0: severity = "CRITICAL"
    elif score >= 7.0: severity = "HIGH"
    elif score >= 4.0: severity = "MEDIUM"
    else: severity = "LOW"

    description = f"{tipas} in {produktas} allows unauthorized attackers to cause unexpected behavior or compromise the system."

    sugeneruoti_cve.append({
        "cve_id": cve_id,
        "description": description,
        "severity": severity,
        "score": score,
        "affected_product": produktas
    })

# Sujungiame ir išsaugome
visi_cve = pradiniai_cve + sugeneruoti_cve

with open("duomenys/cve_data.json", "w", encoding="utf-8") as f:
    json.dump(visi_cve, f, indent=2)

print(f"Sėkmingai sugeneruota ir išsaugota {len(visi_cve)} CVE įrašų failan duomenys/cve_data.json!")
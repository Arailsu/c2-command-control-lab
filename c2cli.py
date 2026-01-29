import os
import argparse
import requests
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from rich.table import Table
from rich.console import Console

load_dotenv()
console = Console()

SERVER_URL = os.getenv("C2_SERVER_URL", "http://127.0.0.1:5000")
C2_KEY = os.getenv("C2_SHARED_KEY")

if not C2_KEY:
    console.print("[red]Erro: C2_SHARED_KEY não definida[/red]")
    exit(1)

fernet = Fernet(C2_KEY.encode())

#  Listar agentes
def list_agents():
    resp = requests.get(f"{SERVER_URL}/agents")
    data = resp.json()

    table = Table(title="Agentes Conectados")
    table.add_column("Agent ID", style="cyan")
    table.add_column("Último contato", style="green")
    table.add_column("Comandos pendentes", justify="center")
    table.add_column("Resultados", justify="center")

    for aid, info in data.items():
        table.add_row(aid, info["last_seen"], str(info["queue"]), str(info["results"]))

    console.print(table)

#  Enviar comando
def send_command(agent_id, command):
    data = {
        "agent_id": agent_id,
        "command": command
    }
    r = requests.post(f"{SERVER_URL}/sendcommand", json=data)
    if r.status_code == 200:
        console.print(f"[green]Comando enviado para {agent_id}[/green]")
    else:
        console.print(f"[red]Erro ao enviar comando[/red]")

#  Ver resultados descriptografados
def view_results(agent_id):
    r = requests.get(f"{SERVER_URL}/results/{agent_id}")
    if r.status_code != 200:
        console.print(f"[red]Agente {agent_id} não encontrado[/red]")
        return

    results = r.json()
    table = Table(title=f"Resultados de {agent_id}")
    table.add_column("Nº", justify="center")
    table.add_column("Resultado Descriptografado")

    for idx, enc in enumerate(results):
        try:
            result = fernet.decrypt(enc.encode()).decode()
        except:
            result = "[Erro ao descriptografar]"
        table.add_row(str(idx + 1), result)

    console.print(table)

# CLI principal
parser = argparse.ArgumentParser(description="CLI para interagir com C2")
subparsers = parser.add_subparsers(dest="command")

# Subcomandos
parser_list = subparsers.add_parser("list-agents", help="Listar todos os agentes")
parser_send = subparsers.add_parser("send-cmd", help="Enviar comando a um agente")
parser_send.add_argument("agent_id", help="ID do agente")
parser_send.add_argument("command", help="Comando a enviar")
parser_view = subparsers.add_parser("view-results", help="Ver resultados de um agente")
parser_view.add_argument("agent_id", help="ID do agente")

args = parser.parse_args()

if args.command == "list-agents":
    list_agents()
elif args.command == "send-cmd":
    send_command(args.agent_id, args.command)
elif args.command == "view-results":
    view_results(args.agent_id)
else:
    parser.print_help()


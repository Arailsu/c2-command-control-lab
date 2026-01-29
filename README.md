# 📁 Custom C2

### 💻 Projeto: Command & Control Personalizado

Este projeto é um sistema C2 (Command & Control) funcional, feito com Python, composto por:

- 🛰️ **Agente (`agent.py`)**  
- 🧠 **Servidor Flask (`server.py`)**  

Suporta múltiplos agentes, criptografia de comandos e resultados com `Fernet`, e uma fila de comandos por agente.

---

## 🚀 Funcionalidades

✅ Registro automático de agentes  
✅ Polling para recebimento de comandos  
✅ Execução de comandos reais com `subprocess`  
✅ Criptografia de ponta a ponta com `Fernet`  
✅ Resultados criptografados e armazenados  
✅ Fila de comandos por agente  
✅ Logs salvos em `c2_log.txt`

---

## 🔐 Requisitos

- Python 3.8+
- Bibliotecas:

```bash
pip install flask requests python-dotenv cryptography
```

---

## 🔧 Como usar

### 1. Gere uma chave para criptografia:

```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 2. Crie um arquivo `.env` com a chave:

```
C2_SHARED_KEY=COLE_AQUI_A_CHAVE
```

---

### 3. Inicie o servidor

```bash
python3 server.py
```

---

### 4. Inicie o agente

```bash
python3 agent.py
```

> O agente se registra e salva seu `agent_id` em `.agent_id`

---

## 🛠️ Estrutura do Projeto

```
custom_c2/
├── agent.py         # Agente que executa comandos
├── server.py        # Servidor Flask (C2)
├── c2_log.txt       # Log de eventos
├── .env             # Chave C2_SHARED_KEY
└── .agent_id        # Persistência do agente
```

---

## 🧱 Endpoints do servidor

| Método | Rota            | Função                             |
|--------|------------------|-------------------------------------|
| POST   | `/register`      | Registra novo agente               |
| GET    | `/getcommand`    | Entrega comando ao agente          |
| POST   | `/submit_result` | Recebe resultado do comando        |
| POST   | `/sendcommand`   | Envia comando ao agente            |
| GET    | `/agents`        | Lista agentes e status             |

---

## 📌 TODO (Próximas melhorias)

- [ ] Corrigir e reintroduzir CLI (`c2cli.py`)
- [ ] Persistência de `agents` e `commands` em disco
- [ ] Painel web com Flask + JS
- [ ] Módulo de autenticação HMAC por agente
- [ ] C2 via DNS ou canais covertos

---

## ⚠️ Aviso legal

Este projeto é para fins **educacionais e de pesquisa em ambientes controlados**.  
**Nunca use este sistema em redes, dispositivos ou sistemas sem autorização explícita.**

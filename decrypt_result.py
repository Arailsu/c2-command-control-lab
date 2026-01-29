from cryptography.fernet import Fernet
import os

# Pegue a chave do mesmo lugar onde você definiu (ou use dotenv)
key = os.getenv("C2_SHARED_KEY")
fernet = Fernet(key.encode())

# Cole aqui o resultado recebido no log
encrypted = "gAAAAABpe3TzXsmTLn8NIe3yd3c1RbB4ptLUcnfuCrW3_-EGmijjZYMO8ZL-TWCUnq99vXOWakPjpana_XSjclWQFwb5KCD1Qg=="

# Decripta e imprime
print("Resultado:", fernet.decrypt(encrypted.encode()).decode())

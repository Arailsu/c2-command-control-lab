# c2-command-control-lab
Meu take em um C2 para fins educacionais, Desenvolvido usando Python/Flask

## KEY C2
Para definir as keys entre o agent e o server é necessário criar um arquivo .env e gerar a key usando o comando

> python3 - <<EOF
  from cryptography.fernet import Fernet
  print(Fernet.generate_key().decode())
  EOF
esse .env terá a key nele usando a variável C2_SHARED_KEYS = <KEY AQUI>

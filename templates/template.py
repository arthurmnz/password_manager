import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from models.password import Password
from views.password_views import FernetHasher

key, path = FernetHasher.create_key(archive=True)
print('Sua chave foi criada com sucesso, salve-a com cuidado. ELA DARÁ ACESSO PARA SUAS SENHAS\n\n')
print(f'Chave:  {key.decode('utf-8')}',end='\n\n\n')
if path:
    print('Chave salva no arquivo, lembre-se de remover o arquivo após o tranferir o local')
    print(f"Caminho:  {path}")

while True:
    choice = input('''
__Gerenciador de senha__
[1] Adicionar senha
[2] Ver senha
[3] Gerador de senhas
[4] sair
    
- ''')

    match choice:
        case '1':
            key = input('Digite sua chave usada para criptografia, use sempra a mesma chave: ')
                
            domain = input("Domínio: ")
            password = input("Senha: ")
            try:    
                fernet_user = FernetHasher(key)
            except:
                print('key invalida')
                continue
            p1 = Password(domain=domain, password=fernet_user.encrypt(password).decode('utf-8'))
            p1.save()
            
            
        case '2':
            key = input('key: ')
            try:    
                fernet_user = FernetHasher(key)
            except:
                print('key invalida')
                continue   
            data = Password.get()
            if len(data)== 0:
                print('Nâo tem nenhuma senha cadastrada.')
                continue
            choice = input('''
__ver senhas__
[1] ver todas
[2] ver apenas uma

- \n''')
            match choice:
                case '1':
                    for passwords in data:
                        print(f'Domínio: {passwords['domain']} | Senha: {fernet_user.decrypt(passwords['password'])}')
                case '2':
                    print('__Escolha o domínio__')
                    for n,passwords in enumerate(data):
                        print(f'[{n+1}] {passwords['domain']}')
                    domain_choice = input('- ')
                    for i in data:
                        if domain_choice in i['domain']:
                            password = fernet_user.decrypt(i['password'])
                    if password:
                        print(f'Sua senha: {password}')
                    else:
                        print('Nenhuma senha cadastrada.')    
            
        case '3':
            nivel = input('''

__Nivel da senha__                          
[1] fraca (15 caracteres)
[2] media (20 caracteres)
[3] forte (25 caracteres)
[4] Escolha o número
                         
- ''')
            match nivel:
                case '1':
                    n = 15
                case '2':
                    n = 20
                case '3':
                    n = 25
                case '4':
                    n = int(input('Digite a quantidade de caracteres: '))
                    
            print(f'Senha: {FernetHasher._get_random_string(length = n)}')
            
        case '4':
            break 
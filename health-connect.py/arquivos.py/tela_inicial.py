import subprocess
import json

while True:
    print('=-' * 25 + 'SEJA BEM VINDO(A) AO HEALTH CONNECT!' + '=-' * 25)
    print('0 - Encerrar programa')
    print('1 - Login')
    print('2 - Cadastrar')
    resposta_usuario = input('Selecione uma das opcoes acima: ')
    if resposta_usuario == '0':
        print('Finalizando programa...')
        break
    if resposta_usuario == '1':
        subprocess.run(['python', 'login.py'])
        try:
            with open('login.json', 'r') as arquivo:
                login_status = json.load(arquivo)
                if login_status['login'] == True:
                    if login_status['tipo_de_conta'] == 'usuario_comum':
                        subprocess.run(['python', 'pagina_principal_usuarios.py'])
                    elif login_status['tipo_de_conta'] == 'usuario_profissional':
                        subprocess.run(['python', 'pagina_principal_profissionais.py'])
                else:
                    print('Login nao realizado')
        except:
            print('Ocorreu um erro ao tentar acessar o status de Login')
    elif resposta_usuario == '2':
        print('=-' * 25)
        print('0 - Cadastrar como usuario comum')
        print('1 - Cadastrar como profissional da saude')
        while True:
            resposta_usuario2 = input('Selecione uma das opcoes acima: ')
            if resposta_usuario2 == '0':
                subprocess.run(['python', 'cadastro_usuario_comum.py'])
                break
            elif resposta_usuario2 == '1':
                subprocess.run(['python', 'cadastro_profissionais.py'])
                break
            else:
                print('Digite somente 0 ou 1!')
    else:
        print('Digite somente 0 ou 1!')

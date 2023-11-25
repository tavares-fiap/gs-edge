import json
import getpass

print("=-" * 25)

def campo_de_cpf() -> bool:
	'''Campo para CPF e validacao de CPF (somente para usuarios comuns)'''
	while True:
		cpf_inserido = input('Digite seu CPF: ')
		if len(cpf_inserido) == 11 and cpf_inserido.isdigit():	# Validacao
			break
		else:
			print('O CPF inserido deve possuir 11 dígitos e conter apenas números.')

	try:
		arquivo = open('usuario_comum.json', 'r', encoding='utf-8')
		cadastros_existentes = json.load(arquivo)
	except:
		print('Arquivo JSON vazio, nao existem usuarios comuns cadastrados')
		return False

	lista_cpfs_cadastrados = []
	for keys in cadastros_existentes.keys():
		lista_cpfs_cadastrados.append(keys)

	# Busca binaria para identificar o cadastro equivalente ao CPF inserido
	lista_cpfs_cadastrados.sort()

	inicio = 0
	fim = len(lista_cpfs_cadastrados) - 1
	
	while inicio <= fim:
		meio = (inicio + fim) // 2
		if lista_cpfs_cadastrados[meio] == cpf_inserido:
			print(f"Este CPF esta associado a conta de: {cadastros_existentes[cpf_inserido]['nome']}")
			confirma_cpf = input('E voce? (s ou n) : ')
			confirma_cpf = confirma_cpf.upper()
			if confirma_cpf == 'S':
				return cpf_inserido
			elif confirma_cpf == 'N':
				return confirma_cpf
			else:
				print('Digite somente S ou N!')
			return True
		elif cpf_inserido > lista_cpfs_cadastrados[meio]:
			inicio = meio + 1
		else:
			fim = meio - 1
	arquivo.close()
	print("Nao encontramos nenhum cadastro de Usuario Comum com esse CPF")
	return False

def campo_de_id() -> bool:
	'''Campo para ID e validacao de ID (Somente para profissionais da saude)'''
	while True:
		id_inserido = input('Digite seu ID que foi fornecido durante o cadastro: ')
		if id_inserido.isdigit():
			break
		else:
			print('O ID inserido deve conter apenas números.')

	try:
		arquivo = open('profissionais.json', 'r', encoding='utf-8')
		cadastros_existentes = json.load(arquivo)
	except:
		print('Arquivo JSON vazio, nao existem usuarios profissionais cadastrados')
		return False

	lista_ids_cadastrados = []
	for keys in cadastros_existentes.keys():
		lista_ids_cadastrados.append(keys)

	# Busca binaria para identificar o cadastro equivalente ao ID inserido
	lista_ids_cadastrados.sort()

	inicio = 0
	fim = len(lista_ids_cadastrados) - 1
	
	while inicio <= fim:
		meio = (inicio + fim) // 2
		if lista_ids_cadastrados[meio] == id_inserido:
			while True:
				print(f"Este ID esta associado a conta do profissional: {cadastros_existentes[id_inserido]['nome']}")
				confirma_id = input('E voce? (s ou n) : ')
				confirma_id = confirma_id.upper()
				if confirma_id == 'S':
					return id_inserido
				elif confirma_id == 'N':
					return confirma_id
				else:
					print('Digite somente S ou N!')
		elif id_inserido > lista_ids_cadastrados[meio]:
			inicio = meio + 1
		else:
			fim = meio - 1
	arquivo.close()
	print("Nao encontramos nenhum cadastro de Usuario Comum com esse CPF")
	return False

def campo_de_senha_usuarios(cpf_inserido : str) -> bool:
	'''Validacao de senha para contas do tipo usuario_comum'''
	try:
		arquivo = open('usuario_comum.json', 'r', encoding='utf-8')
		cadastros_existentes = json.load(arquivo)
	except:
		print('Arquivo JSON vazio, nao existem usuarios comuns cadastrados')
		return False
	
	senha_usuario = cadastros_existentes[cpf_inserido]['senha']
	while True:
		senha_inserida = getpass.getpass("Digite sua senha: ")

		if senha_inserida == senha_usuario:
			return True
		else:
			print('Senha Incorreta')

def campo_de_senha_profissionais(id_inserido : str) -> bool:
	'''Validacao de senha para contas do tipo profissionais'''
	try:
		arquivo = open('profissionais.json', 'r', encoding='utf-8')
		cadastros_existentes = json.load(arquivo)
	except:
		print('Arquivo JSON vazio, nao existem usuarios comuns cadastrados')
		return False
	
	senha_usuario = cadastros_existentes[id_inserido]['senha']
	while True:
		senha_inserida = getpass.getpass("Digite sua senha: ")

		if senha_inserida == senha_usuario:
			return True
		else:
			print('Senha Incorreta')
			
def mudar_status_do_login_para_true(cpf_ou_id_inserido : str, login : bool, tipo_de_conta : str) -> bool:
	'''Muda status do login caso as validacoes tenham sido bem sucedidas'''
	arquivo = open('login.json', 'r', encoding='utf-8')	
	status_login = json.load(arquivo)

	if login == True:
		status_login["tipo_de_conta"] = tipo_de_conta
		status_login["login"] = login
		status_login["usuario"] = cpf_ou_id_inserido
		with open('login.json', 'w', encoding='utf-8') as arquivo:
				json.dump(status_login, arquivo, indent=2, ensure_ascii=False)
		print("Login realizado com sucesso!")

	else:
		print('O login nao foi realizado')
		return False



# ------------------------------- PRINCIPAL ------------------------
while True:
	print("0 - para logar como usuario comum")
	print("1 - para logar como usuario profissional")
	opcao_usuario = input("Selecione uma das opcoes acima: ")
	if opcao_usuario == '0':
		print("=-" * 25 + "LOGIN Usuario Comum" + "=-" * 25)
		cpf_inserido = campo_de_cpf()
		if cpf_inserido == 'N':
			print('Tente novamente...')
			continue
		elif cpf_inserido == False:
			break
		senha_inserida = campo_de_senha_usuarios(cpf_inserido)
		if senha_inserida == True:
			login = True
			mudar_status_do_login_para_true(cpf_inserido, login, tipo_de_conta='usuario_comum')
			break
	elif opcao_usuario == '1':
		print("=-" * 25 + "LOGIN Usuario Profissional" + "=-" * 25)
		id_inserido = campo_de_id()
		if id_inserido == 'N':
			print('Nao encontramos outra conta para esse CPF.\nTente novamente...')
			continue
		elif id_inserido == False:
			break
		senha_inserida = campo_de_senha_profissionais(id_inserido)
		if senha_inserida == True:
			login = True
			mudar_status_do_login_para_true(id_inserido, login, tipo_de_conta='usuario_profissional')
			break
	else:
		print('Somente 0 ou 1!')
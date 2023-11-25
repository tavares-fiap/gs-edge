import getpass
import requests
import json

def obter_nome() -> str:
	'''Obtem nome do usuario'''
	while True:
		nome = input('Digite seu nome completo: ')
		nome_formatado = nome.lower().title()
		if not nome.isdigit(): # Validacao
			return nome_formatado
		else:
			print('O nome deve conter apenas letras.')

def obter_idade() -> str:
	'''Obtem idade do usuario'''
	while True:
		idade = input('Digite sua idade: ')
		if idade.isdigit(): # Validacao
			return int(idade)
		else:
			print('A idade deve conter apenas números.')

def obter_cpf() -> str:
	'''Obtem cpf do usuario'''
	while True:
		cpf = input('Digite seu CPF: ')
		if len(cpf) == 11 and cpf.isdigit(): # Validacao
			return cpf
		else:
			print('O CPF deve possuir 11 dígitos e conter apenas números.')

def obter_cep() -> str:
	'''Obtem cep do usuario'''
	while True:
		cep = input('Digite seu CEP: ')
		if len(cep) == 8 and cep.isdigit(): # Validacao
			return cep
		else:
			print('O CEP deve possuir 8 dígitos e conter apenas números.')

def obter_celular() -> str:
	'''Obtem numero de celular do usuario'''
	while True:
		celular = input('Digite numero de celular com DDD: ')
		if len(celular) == 11 and celular.isdigit(): # Validacao
			return celular
		else:
			print('O numero de celular com DDD deve possuir 11 dígitos e conter apenas números.')

def criar_senha() -> str:
	'''usuario cria senha'''
	while True:
		senha = getpass.getpass(prompt='Crie uma senha: ')
		confirmar_senha = getpass.getpass("Confirme sua senha: ")
		if confirmar_senha == senha: # Validacao
			return senha
		else:
			print('As senhas nao coincidem!')

def busca_cep(cep : str) -> dict:
	'''Busca CEP do usuario na API ViaCep'''

	url_api_cep = f"http://viacep.com.br/ws/{cep}/json/"
	try:
		response_cep = requests.get(url_api_cep)

		if response_cep.status_code == 200:
			print('Solicitacao de CEP concluida com sucesso!')
			try:
				dados_cep = response_cep.json()

				print("CEP:", dados_cep["cep"])
				print("Logradouro:", dados_cep["logradouro"])
				print("Complemento:", dados_cep["complemento"])
				print("Bairro:", dados_cep["bairro"])
				print("Cidade:", dados_cep["localidade"])
				print("Estado:", dados_cep["uf"])
			except:
				print('Ocorreu um erro. Talvez CEP incorreto?')
				cep = obter_cep()
				dados_cep = busca_cep(cep)
				return dados_cep
			
			while True:
				confirma_dados = input('Esses dados estao corretos? (Digite S para sim, N para nao): ')
				confirma_dados = confirma_dados.upper()
				if confirma_dados == 'S':
					return dados_cep
				elif confirma_dados == 'N':
					cep = obter_cep()
					dados_cep = busca_cep(cep)
					return dados_cep
				else:
					print('Digite somente S ou N!')

		elif response_cep.status_code == 404:
			print('Nao foi possivel encontrar o endereco passado como parametro')
		elif response_cep.status_code == 500:
			print('Ocorreu algum erro no servidor')	
		else:
			print("Erro ao obter dados do CEP.")

	except ConnectionError:
		print('Ocorreu um erro de conexao')
	except Exception:
		print('ERRO DESCONHECIDO')

def mudar_status_do_login_para_false() -> str:
	'''Altera arquivo login.json para realizar o logout'''
	with open('login.json', 'r', encoding='utf-8') as arquivo:
		try:	
			status_login = json.load(arquivo)
		except Exception as e:
			print(f'Ocorreu um erro ao tentar acessar o status de login durante o logout. Codigo do erro: {e}')
	status_login["login"] = False
	status_login["tipo_de_conta"] = ''
	status_login["usuario"] = ''

	with open('login.json', 'w', encoding='utf-8') as arquivo:
			json.dump(status_login, arquivo, indent=2, ensure_ascii=False)
	return 'LOGOUT realizado com sucesso'
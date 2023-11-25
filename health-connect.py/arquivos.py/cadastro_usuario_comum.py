import json
from  modulo import obter_nome, obter_idade, obter_cep, obter_cpf, busca_cep, criar_senha, obter_celular

def verifica_cpf_no_sistema(cpf : str):
	'''Realiza busca binaria para verificar se o CPF inserido ja tem cadastro no sistema'''
	try:
		arquivo = open('usuario_comum.json', 'r', encoding='utf-8')
		cadastros_existentes = json.load(arquivo)
	except:
		print('Arquivo JSON vazio, esse e o primeiro cadastro de Usuario Comum')
		return False

	lista_cpfs_cadastrados = []   # Transforma CPFs cadastrados em lista para fazer busca binaria
	for keys in cadastros_existentes.keys():
		lista_cpfs_cadastrados.append(keys)

	lista_cpfs_cadastrados.sort()

	inicio = 0
	fim = len(lista_cpfs_cadastrados) - 1
	
	while inicio <= fim:
		meio = (inicio + fim) // 2
		if lista_cpfs_cadastrados[meio] == cpf:
			print(f"Este CPF ja esta associado a conta de: {cadastros_existentes[cpf]['nome']}")
			return True
		elif cpf > lista_cpfs_cadastrados[meio]:
			inicio = meio + 1
		else:
			fim = meio - 1

	arquivo.close()
	return False

def cadastrando_paciente_no_sistema(nome : str, idade : str, cpf : str, dados_cep : dict, celular : str, senha : str):
	'''Escreve o novo cadastro no arquivo usuario_comum.json'''
	try:
		with open('usuario_comum.json', 'r', encoding='utf-8') as arquivo:
			try:
				cadastros_existentes = json.load(arquivo)
			except:
				cadastros_existentes = {}

		# Adiciona cadastro
		cadastros_existentes[cpf] = {
			"nome": nome,
			"idade": idade,
			"endereco": dados_cep,
			"celular" : celular,
			"senha": senha,
			"ocorrencias_ativas" : {},
			"ocorrencias" : {}
		}

		with open('usuario_comum.json', 'w', encoding='utf-8') as arquivo:
			json.dump(cadastros_existentes, arquivo, indent=2, ensure_ascii=False)
		print("Cadastro realizado com sucesso!")
	except Exception as e:
		print(f"Erro ao escrever no arquivo JSON: {e}")



# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=MENU CADASTRO=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
while True:
	try:
		print('=-' * 25 + 'CADASTRO USUARIO COMUM' + '=-' * 25)

		nome = obter_nome()

		idade = obter_idade()

		cpf = obter_cpf()

		cpf_ja_existe = verifica_cpf_no_sistema(cpf)
		if cpf_ja_existe == True:
			raise ValueError
		
		cep = obter_cep()

		dados_cep = busca_cep(cep)

		celular = obter_celular()

		senha = criar_senha()

		cadastrando_paciente_no_sistema(nome, idade, cpf, dados_cep, celular, senha)

		break

	except ValueError:
		continue
	except Exception as e:
		print(f'Ocorreu um erro desconhecido: {e}')
		continue
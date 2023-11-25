import json
from  modulo import obter_nome, obter_idade, obter_cep, obter_cpf, busca_cep, criar_senha, obter_celular

def obter_hospital_de_atuacao_do_profissional() -> str:
	'''Obtem hospital de atuacao do profissional'''
	while True:
		nome_hospital = input('Digite o hospital em que trabalha hoje ou trabalhou pela ultima vez: ')
		nome_hospital_formatado = nome_hospital.lower().title()
		return nome_hospital_formatado

def verifica_cpf_no_sistema_profissionais(cpf: str) -> bool:
    '''Realiza busca binaria para verificar se o CPF inserido já tem cadastro no sistema'''
    try:
        arquivo = open('profissionais.json', 'r', encoding='utf-8')
        cadastros_existentes = json.load(arquivo)
    except:
        print('Arquivo JSON vazio, esse é o primeiro cadastro')
        return False

    lista_cpfs_cadastrados = list(cadastros_existentes.keys())  # Transforma CPFs cadastrados em lista para fazer busca binaria

    inicio = 0
    fim = len(lista_cpfs_cadastrados) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        if lista_cpfs_cadastrados[meio] == cpf:
            print(f"Este CPF já está associado à conta de: {cadastros_existentes[cpf]['nome']}")
            return True
        elif cpf > lista_cpfs_cadastrados[meio]:
            inicio = meio + 1
        else:
            fim = meio - 1

    arquivo.close()
    return False

def cadastrando_profissional_no_sistema(nome: str, idade: str, cpf: str, dados_cep: dict, hospital : str, celular : str, senha : str):
	'''Escreve o novo cadastro no arquivo profissionais.json'''
	try:
		with open('profissionais.json', 'r', encoding='utf-8') as arquivo:
			try:
				cadastros_existentes = json.load(arquivo)
			except:
				print('Esse e o primeiro cadastro! Criando dicionario...')
				cadastros_existentes = {}

		# Cria numero de identificacao ao profissional da saude
		id_do_profissional = int(list(cadastros_existentes.keys())[-1]) + 1 if cadastros_existentes else 1


		cadastros_existentes[str(id_do_profissional)] = {
			"nome": nome,
			"idade": idade,
			"cpf" : cpf,
			"endereco": dados_cep,
			"hospital": hospital,
			"celular" : celular,
			"senha" : senha,
			"ocorrencias" : {}
		}

		with open('profissionais.json', 'w', encoding='utf-8') as arquivo:
			json.dump(cadastros_existentes, arquivo, indent=2, ensure_ascii=False)
		print("Cadastro realizado com sucesso!")
		print('=-' * 25 + 'ATENCAO' + '=-' * 25)
		print(f"Seu ID: {id_do_profissional}")
		print("GUARDE MUITO BEM SEU ID, ELE E USADO NO LOGIN")
	except Exception as e:
		print(f"Erro ao escrever no arquivo JSON: {e}")



# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=MENU CADASTRO PROFISSIONAIS DA SAUDE=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
while True:
	try:
		print('=-' * 25 + 'CADASTRO DE PROFISSIONAIS DA SAUDE' + '=-' * 25)

		nome = obter_nome()

		idade = obter_idade()

		cpf = obter_cpf()

		cpf_ja_existe = verifica_cpf_no_sistema_profissionais(cpf)
		if cpf_ja_existe == True:
			raise ValueError
		cep = obter_cep()

		dados_cep = busca_cep(cep)

		hospital = obter_hospital_de_atuacao_do_profissional()
		
		celular = obter_celular()

		senha = criar_senha()

		cadastrando_profissional_no_sistema(nome, idade, cpf, dados_cep, hospital, celular, senha)

		break

	except ValueError:
		continue
	except Exception as e:
		print(f'Ocorreu um erro desconhecido: {e}')
		continue
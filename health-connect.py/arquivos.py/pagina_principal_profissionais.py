import json
from modulo import mudar_status_do_login_para_false

def buscar_historico_de_ocorrencias(id_usuario_atual : str) -> dict:
	'''Busca o historico de ocorrencias atendidas pelo usuario atual'''
	try:
		with open("profissionais.json", 'r', encoding='utf-8') as arquivo:
			profissionais_json = json.load(arquivo)
	except Exception as e:
		print(f'Erro ao obter dados do "usuario_comum.json". Erro: {e}')
		return False
	try:
		hist_ocorrencias = profissionais_json[id_usuario_atual]['ocorrencias']
	except Exception as e:
		print(f'Ocorreu um erro ao tentar localizar o historico de ocorrencias. Codigo do erro: {e}')	
		return False
	return hist_ocorrencias


def cadastrar_ocorrencia_do_zero(profissionais_json: dict, id_usuario_atual : str) -> str:
	'''Permite que o profissional cadastre o atendimento de um paciente do zero'''
	while True:
		nome_paciente = input('Digite o nome compelto do paciente: ')
		nome_formatado = nome_paciente.lower().title()
		if not nome_paciente.isdigit():
			break
		else:
			print('O nome deve conter apenas letras.')

	while True:
		idade_paciente = input('Digite a idade do paciente: ')
		if idade_paciente.isdigit():
			idade_paciente = int(idade_paciente)
			break
		else:
			print('A idade deve conter apenas números.')

	while True:
		cpf_paciente = input('Digite o CPF do paciente: ')
		if len(cpf_paciente) == 11 and cpf_paciente.isdigit():
			break
		else:
			print('O CPF deve possuir 11 dígitos e conter apenas números.')

	try:
		while True:
			nivel_de_emergencia = int(input('Digite o nivel de emergencia (de 1 a 5): '))
			if nivel_de_emergencia < 1 or nivel_de_emergencia > 5:
				print('Digite somente numeros de 1 a 5!')
			else:
				break
	except:
		print('Digite apenas numeros de 1 a 5!')

	descricao_ocorrencia = input('Descreva a ocorrencia: ')

	# Utiliza mesmo metodo de gerar IDs para gerar um numero para a ocorrencia
	numero_da_ocorrencia = int(list(profissionais_json[id_usuario_atual]['ocorrencias'].keys())[-1]) + 1 if profissionais_json[id_usuario_atual]['ocorrencias'] else 1
	
	profissionais_json[id_usuario_atual]['ocorrencias'][numero_da_ocorrencia] = {
		"nome_paciente" : nome_formatado,
		"idade_paciente" : idade_paciente,
		"cpf_paciente" : cpf_paciente,
		"nivel_de_emergencia" : nivel_de_emergencia,
		"descricao_ocorrencia" : descricao_ocorrencia,
		"status" : "solucionada"
	}
	try:
		with open("profissionais.json", 'w', encoding='utf-8') as arquivo:
			json.dump(profissionais_json, arquivo, indent=2, ensure_ascii=False)
	except Exception as e:
		print(f'Ocorreu um erro ao tentar escrever a ocorrencia no banco de dados. Erro: {e}')
	
	return "Ocorrencia cadastrada com sucesso no seu historico!"


def buscar_ocorrencias_ativas() -> list:
	'''Busca ocorrencias ativas de usuarios comuns'''
	with open("usuario_comum.json", "r", encoding="utf-8") as arquivo:
		cadastros_usuarios_comuns = json.load(arquivo)

	ocorrencias_ativas = []
	for keys, values in cadastros_usuarios_comuns.items():
		if values['ocorrencias_ativas']:
			ocorrencias_ativas_usuario = values['ocorrencias_ativas']
			if 'celular' in values:
				celular_paciente = values['celular']

				ocorrencias_ativas.append({
					'cpf_paciente': keys,
					'celular_paciente': celular_paciente,
					'ocorrencia': ocorrencias_ativas_usuario
				})
			
	
	return ocorrencias_ativas
		

try:
	
	with open('login.json', 'r') as arquivo:
		login_status_atual = json.load(arquivo)
		id_usuario_atual = login_status_atual['usuario']

	with open('profissionais.json', 'r') as arquivo2:
		profissionais_json = json.load(arquivo2)
except Exception as e:
	print(f"Ocorreu um erro ao tantar acessar o status do login, ou as informacoes de cadastro no banco de dados. Codigo do erro: {e}")



while True:
	print(f"{'=-' * 15} Seja bem-vindo(a) {profissionais_json[id_usuario_atual]['nome'].split(' ')[0]} {'=-' * 15}")
	print('0 - LOGOUT')
	print('1 - Historico de ocorrencias')
	print('2 - Nova ocorrencia')
	escolha = input('Escolha uma das opcoes acima: ')
	if escolha == '0':
		print(mudar_status_do_login_para_false())
		break

	elif escolha == '1':
		historico_de_ocorrencias = buscar_historico_de_ocorrencias(id_usuario_atual)
		if not historico_de_ocorrencias:
			print('Voce nao tem ocorrencias no historico')
		else:
			print('Essas foram todas as ocorrencias atendidas por voce ate hoje:')
			for keys, values in historico_de_ocorrencias.items():
				print(f'\n{keys}: Nome do Paciente: {values["nome_paciente"]}, Descrição da Ocorrência: {values["descricao_ocorrencia"]}')
			while True:
				try:
					escolha3 = input('\nDigite o numero da ocorrencia que voce deseja obter mais detalhes ou digite 0 para voltar: ')
				except Exception as e:
					print(f'Digite apenas o numero da ocorrencia ou 0! Codigo do erro:{e}')
					continue
				if escolha3 == '0':
					break
				try:				
					print(f"\nNome paciente: {profissionais_json[id_usuario_atual]['ocorrencias'][escolha3]['nome_paciente']}")
					print(f"CPF paciente: {profissionais_json[id_usuario_atual]['ocorrencias'][escolha3]['cpf_paciente']}")
					print(f"Idade paciente: {profissionais_json[id_usuario_atual]['ocorrencias'][escolha3]['idade_paciente']}")
					print(f"Detalhes da ocorrencia: {profissionais_json[id_usuario_atual]['ocorrencias'][escolha3]['descricao_ocorrencia']}")
				except Exception as e:
					print(f'Impossivel acessar detalhes da ocorrencia, por favor, tente novamente. Erro: {e}')

	elif escolha == '2':
		while True:
			print('\n0 - Voltar')
			print('1 - Buscar ocorrencias ativas')
			print('2 - Cadastrar ocorrencia do zero')
			escolha2 = input("Escolha uma das opcoes acima: ")
			if escolha2 == '2':
				print(cadastrar_ocorrencia_do_zero(profissionais_json, id_usuario_atual))
			elif escolha2 == '1':
				ocorrencias_ativas = buscar_ocorrencias_ativas()
				if not ocorrencias_ativas:
					print('\nNao existem ocorrencias ativas no momento')
				else:
					print('\nAs seguintes ocorrencias estao ativas no momento:')
					for ocorrencia in ocorrencias_ativas:
						try:
							print(f'\nCPF do Paciente: {ocorrencia["cpf_paciente"]}')
							print(f'Telefone do Paciente: {ocorrencia["celular_paciente"]}')
							print('Detalhes da Ocorrencia:')
							print(ocorrencia["ocorrencia"]["descricao_ocorrencia"])
						except Exception as e:
							print(f'Ocorreu um erro ao tentar acessar dados dos pacientes, por favor, tente novamente. Erro: {e}')
					print('\nEntre em contato com o paciente pelo numero de telefone para que a ocorrencia possa ser solucionada.')
					print('Apenas o paciente pode mudar o status da ocorrencia para "Solucionada"\n')
			elif escolha2 == '0':
				break
			else:
				print('Escolha somente 0, 1 ou 2!')
	else:
		print('Escolha somente uma das opcoes acima!')
		
import json
from modulo import mudar_status_do_login_para_false
import subprocess


def buscar_historico_de_ocorrencias_usuario_comum(cpf_usuario_atual : str) -> dict:
	'''Busca o historico de ocorrencias do usuario atual que ja foram solucionadas'''
	try:
		with open("usuario_comum.json", 'r', encoding='utf-8') as arquivo:
			usuarios_json = json.load(arquivo) # Atualiza o arquivo JSON toda vez que a funcao e chamada para garantir que todas as ocorrencias estejam nos devidos lugares
	except Exception as e:
		print(f'Erro ao obter dados do "usuario_comum.json". Erro: {e}')
		return False
	try:
		hist_ocorrencias = usuarios_json[cpf_usuario_atual]['ocorrencias']
	except Exception as e:
		print(f'Ocorreu um erro ao tentar localizar o historico de ocorrencias. Codigo do erro: {e}')	
		return False
	return hist_ocorrencias

def gerenciar_ocorrencias_ativas(cpf_usuario_atual : str, usuarios_json : dict, profissionais_json : dict):
	'''Permite que usuario mude o status de sua ocorrencia ativa para solucionada'''
	if not usuarios_json[cpf_usuario_atual]['ocorrencias_ativas']:
		return "Nenhuma ocorrencia ativa localizada!"		
		
	print('Voce possui uma ocorrencia ativa:')
	print(f"\nDetalhes da ocorrencia: {usuarios_json[cpf_usuario_atual]['ocorrencias_ativas']['descricao_ocorrencia']}\nStatus da ocorrencia: {usuarios_json[cpf_usuario_atual]['ocorrencias_ativas']['status']}")
	while True:
		escolha = input('\nDeseja marcar essa ocorrencia como solucionada? (S para sim, N para nao): ')
		escolha = escolha.upper()
		if escolha == 'N':
			return False
		elif escolha == 'S':
			break
		else:
			print('Digite somente S ou N')
	while True:
		id_do_medico = input('Cole aqui o ID do medico que solucionou seu problema (Caso nao saiba, basta pergunta-lo): ')	# Solicita ID do medico para que ocorrencia seja adicionada tambem em seu historico
		if not id_do_medico.isdigit():
			print('Digite somente numeros!')
		else:
			break
	try:
		nome_medico = profissionais_json[id_do_medico]['nome']
		print(f'Medico encontrado com sucesso: {nome_medico}')
	except Exception as e:
		print(f'Ocorreu um erro ao tentar localizar o medico. Codigo do erro: {e}')
		return False

	# Utiliza metodo de gerar IDs para gerar numero na ocorrencia para o usuario
	numero_da_ocorrencia_usuario = int(list(usuarios_json[cpf_usuario_atual]['ocorrencias'].keys())[-1]) + 1 if usuarios_json[cpf_usuario_atual]['ocorrencias'] else 1

	# Salva no historico do usuario comum
	usuarios_json[cpf_usuario_atual]['ocorrencias'][numero_da_ocorrencia_usuario] = {
		"nome_medico" : nome_medico,
		"id_medico" : id_do_medico,
		"descricao_ocorrencia" : usuarios_json[cpf_usuario_atual]["ocorrencias_ativas"]["descricao_ocorrencia"],
		"status" : "solucionada"
	}
	# Utiliza metodo de gerar IDs para gerar numero na ocorrencia para o profissional
	numero_da_ocorrencia_medico = int(list(profissionais_json[id_do_medico]['ocorrencias'].keys())[-1]) + 1 if profissionais_json[id_do_medico]['ocorrencias'] else 1

	# Salva no historico do proissional
	profissionais_json[id_do_medico]['ocorrencias'][numero_da_ocorrencia_medico] = {
		"nome_paciente" : usuarios_json[cpf_usuario_atual]["nome"],
		"idade_paciente" : usuarios_json[cpf_usuario_atual]["idade"],
		"cpf_paciente" : cpf_usuario_atual,
		"descricao_ocorrencia" : usuarios_json[cpf_usuario_atual]["ocorrencias_ativas"]["descricao_ocorrencia"]
	}
	# Zera ocorrencias ativas do usuario
	usuarios_json[cpf_usuario_atual]['ocorrencias_ativas'] = {}
	try:
		with open("usuario_comum.json", 'w', encoding='utf-8') as arquivo:
			json.dump(usuarios_json, arquivo, indent=2, ensure_ascii=False)
	except Exception as e:
		print(f'Ocorreu um erro ao tentar escrever a ocorrencia no historico do paciente. Erro: {e}')

	try:
		with open("profissionais.json", 'w', encoding='utf-8') as arquivo:
			json.dump(profissionais_json, arquivo, indent=2, ensure_ascii=False)
	except Exception as e:
		print(f'Ocorreu um erro ao tentar escrever a ocorrencia no historico do medico. Erro: {e}')
	
	return "Ocorrencia cadastrada com sucesso no seu historico! A ocorrencia nao esta mais ativa."


def cadastrar_nova_ocorrencia_usuario(cpf_usuario_atual : str, usuarios_json : dict) -> str:
	'''Permite que o usuario realize uma ocorrencia'''
	if usuarios_json[cpf_usuario_atual]['ocorrencias_ativas']:
		print('Impossivel cadastrar nova ocorrencia enquanto ja existe uma ocorrencia ativa! Marque a ocorrencia atual como Solucionada antes de cadastrar uma nova ocorrencia!')
		return False
	while True:
		descricao = input('Descreva em detalhes a ocorrencia: ')
		escolha = input('Deseja confirmar e enviar a ocorrencia para um medico? (S para sim, N para nao): ')
		escolha = escolha.upper()
		if escolha == 'N':
			while True:
				escolha2 = input('Digite 1 para reescrever a descricao ou 0 para voltar ao menu: ')
				if escolha2 == '1':
					break
				elif escolha2 == '0':
					return False
				else:
					print('Somente 0 ou 1!')
		elif escolha == 'S':
			break
		else:
			print('Digite somente S ou N!')		

	# Cadastra ocorrencia ativa
	usuarios_json[cpf_usuario_atual]['ocorrencias_ativas'] = {
		"descricao_ocorrencia" : descricao,
		"status" : "ativa"
	}

	try:
		with open("usuario_comum.json", 'w', encoding='utf-8') as arquivo:
			json.dump(usuarios_json, arquivo, indent=2, ensure_ascii=False)
	except Exception as e:
		print(f'Ocorreu um erro ao tentar escrever a ocorrencia no banco de dados. Erro: {e}')
	
	return "Ocorrencia postada com sucesso! Logo medicos entrarao em contato!"
		
	

		

	



try:	
	with open('login.json', 'r') as arquivo:
		login_status_atual = json.load(arquivo)
		cpf_usuario_atual = login_status_atual['usuario']

	with open('usuario_comum.json', 'r') as arquivo2:
		usuarios_json = json.load(arquivo2)
except Exception as e:
	print(f"Ocorreu um erro ao tentar acessar o status do login, ou as informacoes de cadastro no banco de dados. Codigo do erro: {e}")

try:
	with open('profissionais.json', 'r') as arquivo3:
		profissionais_json = json.load(arquivo3)

except Exception as e:
	profissionais_json = {}
	print(f"Ocorreu um erro ao tentar acessar o informacoes dos Medicos Disponiveis. Codigo do erro: {e}")



while True:
	print(f"{'=-' * 15} Seja bem-vindo(a) {usuarios_json[cpf_usuario_atual]['nome'].split(' ')[0]} {'=-' * 15}")
	print('0 - LOGOUT')
	print('1 - Historico de ocorrencias')
	print('2 - Gerenciar Ocorrencias Ativas')
	print('3 - Nova ocorrencia')
	print('4 - Monitoramento de temperatura')
	escolha = input('Escolha uma das opcoes acima: ')
	if escolha == '0':
		print(mudar_status_do_login_para_false())
		break
	
	elif escolha == '1':
		historico_de_ocorrencias = buscar_historico_de_ocorrencias_usuario_comum(cpf_usuario_atual)
		if not historico_de_ocorrencias:
			print('Voce nao tem ocorrencias no historico')
		else:
			print('Essas foram todas as ocorrencias solicitadas por voce ate hoje:')
			for keys, values in historico_de_ocorrencias.items():
				print(f'\n{keys}: Nome do Medico: {values["nome_medico"]}, ID do Medico: {values["id_medico"]}, Descrição da Ocorrência: {values["descricao_ocorrencia"]}')
			while True:
				try:
					escolha3 = input('\nDigite o numero da ocorrencia que voce deseja obter mais detalhes ou digite 0 para voltar: ')
				except Exception as e:
					print(f'Digite apenas o numero da ocorrencia ou 0! Erro: {e}')
					continue
				if escolha3 == '0':
					break
				try:
					print(f"\nNome do medico: {historico_de_ocorrencias[escolha3]['nome_medico']}")
					print(f"ID do medico: {historico_de_ocorrencias[escolha3]['id_medico']}")
					print(f"Descricao da ocorrencia: {historico_de_ocorrencias[escolha3]['descricao_ocorrencia']}")
					print(f"Status: {historico_de_ocorrencias[escolha3]['status']}")
				except Exception as e:
					print(f'Impossivel acessar detalhes da ocorrencia, por favor, tente novamente. Erro: {e}')
					continue
				
	elif escolha == '2':
		print(gerenciar_ocorrencias_ativas(cpf_usuario_atual, usuarios_json, profissionais_json))
	elif escolha == '3':
		print(cadastrar_nova_ocorrencia_usuario(cpf_usuario_atual, usuarios_json))
	elif escolha == '4':
		subprocess.run(['python', 'get_postman.py'])

	else:
		print('Escolha somente uma das opcoes acima!')
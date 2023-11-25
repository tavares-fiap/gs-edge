import json
import requests
import subprocess
from time import sleep

url = 'http://46.17.108.113:1026/v2/entities/urn:ngsi-ld:Hc:034/attrs/identity'

def get_postman_function(url : str, headers : dict) -> dict:
		# Fazendo a solicitação GET
	try:
		response = requests.get(url, headers=headers)

	# Verifica se a solicitação foi bem-sucedida (código de status 200)
		if response.status_code == 200:
			print('Solicitação GET realizada com sucesso!')
			# Conteúdo da resposta
			data = response.json()  # Para decodificar JSON
			print(f"Temperatura : {data['value']} \nUltimo registro : {data['metadata']['TimeInstant']['value']}")
			return data

		else:
			print("Falha na solicitação GET. Código de status:", response.status_code)
			raise ValueError
		
	except ValueError:
		pass
	except:
		print('Ocorreu um erro desconhecido, tente novamente')

def cadastrar_ocorrencia_automaticamente(cpf_usuario_atual : str, usuarios_json : dict, estado_temperatura : float) -> str:
	'''Realize ocorrencia automatica'''
	if usuarios_json[cpf_usuario_atual]['ocorrencias_ativas']:
		print('Impossivel cadastrar nova ocorrencia enquanto ja existe uma ocorrencia ativa! Marque a ocorrencia atual como Solucionada antes de cadastrar uma nova ocorrencia!')
		return False
	
	descricao = estado_temperatura

	# Cadastra ocorrencia ativa automaticamente
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




print('=-'*10 + 'GET POSTMAN' + '=-'*10)

# Parametros definidos pelo PostMan
headers = {
	'fiware-service': 'smart' ,
	'fiware-servicepath': '/' ,
	'accept': 'application/json'
}

while True:
	data = get_postman_function(url, headers)
	# Informacoes necessarias
	try:
		temperatura = data['value'] # Temperatura do usuario
		date_time = data['metadata']['TimeInstant']['value'] # Horario em que foi medida a temperatura
	except:
		print('Nao foi possivel acessar os dados do POSTMAN.')

	if temperatura >= 35 and temperatura <= 37:
		sleep(2)
		continue
	else:
		print(f"Temperatura de risco detectada!: {data['value']}")
		break




try:	
	with open('login.json', 'r') as arquivo:
		login_status_atual = json.load(arquivo)
		cpf_usuario_atual = login_status_atual['usuario']

	with open('usuario_comum.json', 'r') as arquivo2:
		usuarios_json = json.load(arquivo2)
except Exception as e:
	print(f"Ocorreu um erro ao tentar acessar o status do login, ou as informacoes de cadastro no banco de dados. Codigo do erro: {e}")


if temperatura < 35:
	estado_temperatura = "Risco de HIPOTERMIA"
	print(estado_temperatura)
	print(cadastrar_ocorrencia_automaticamente(cpf_usuario_atual, usuarios_json, estado_temperatura))
	while True:
		escolha = input('Ditige 1 para continuar a leitura ou 0 para voltar: ')
		if escolha == '0':
			break
		elif escolha == '1':
			print('Continuando Leitura')
			subprocess.run(['python', 'get_postman.py'])
		else:
			print('Somente 0 ou 1')
elif temperatura > 37 and temperatura <= 38:
	estado_temperatura = "ESTADO FEBRIL"
	print(estado_temperatura)
	print(cadastrar_ocorrencia_automaticamente(cpf_usuario_atual, usuarios_json, estado_temperatura))
	while True:
		escolha = input('Ditige 1 para continuar a leitura ou 0 para voltar: ')
		if escolha == '0':
			break
		elif escolha == '1':
			print('Continuando Leitura')
			subprocess.run(['python', 'get_postman.py'])
		else:
			print('Somente 0 ou 1')
elif temperatura > 38 and temperatura <= 39:
	estado_temperatura = "RISCO DE FEBRE"
	print(estado_temperatura)
	print(cadastrar_ocorrencia_automaticamente(cpf_usuario_atual, usuarios_json, estado_temperatura))
	while True:
		escolha = input('Ditige 1 para continuar a leitura ou 0 para voltar: ')
		if escolha == '0':
			break
		elif escolha == '1':
			print('Continuando Leitura')
			subprocess.run(['python', 'get_postman.py'])
		else:
			print('Somente 0 ou 1')
elif temperatura > 39:
	estado_temperatura = "FEBRE ALTA!"
	print(estado_temperatura)
	print(cadastrar_ocorrencia_automaticamente(cpf_usuario_atual, usuarios_json, estado_temperatura))
	while True:
		escolha = input('Ditige 1 para continuar a leitura ou 0 para voltar: ')
		if escolha == '0':
			break
		elif escolha == '1':
			print('Continuando Leitura')
			subprocess.run(['python', 'get_postman.py'])
		else:
			print('Somente 0 ou 1')


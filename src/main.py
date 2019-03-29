import platform
from os import path, system

from ia_algoritimos import calc_trajeto
from ia_estruturas import PlanoCartesiano, PontoAStar, Ponto

try:
	from colorama import init
 
except ImportError:

	print("Instalando colorama...")

	if (platform.system().upper() != "WINDOWS"):
		system("pip install --user colorama 2>&1 >/dev/null")
		system("cls")

	else:
		system("pip3 install --user colorama /quiet")
		system("ls")

	from colorama import init

simb_obst_txt_arq = 1
__color_red = "\033[31m{}\033[m"
__color_green = "\033[32m{}\033[m"
__color_blue = "\033[34m{}\033[m"
__color_purple = "\033[35m{}\033[m"

def ler_plano_arquivo(path_arq: str, quadrante: int = 4) -> PlanoCartesiano:

	linhas = []

	with open(path_arq, mode="r") as arq:
		linhas = arq.readlines()

	qtd_colunas = len(linhas[0].split(" "))
	qtd_linhas = len(linhas)

	plano = PlanoCartesiano(qtd_linhas, qtd_colunas, quadrante)

	y = -1 if (quadrante == 3 or quadrante == 4) else 1
	x = -1 if (quadrante == 2 or quadrante == 3) else 1

	for i, linha in enumerate(linhas):
		pts = linha.strip().split(" ")

		for j, pt in enumerate(pts):
			ponto: PontoAStar = plano.get_pt(x*j, y*i)
			ponto.valor = int(pt)

	return plano

def __ler_path_arquivo():

	caminho = input("\nDigite ou cole o path do arquivo contendo o plano:\n")

	return caminho if path.isfile(caminho) else None

def __ler_ponto_teclado(pt_inicial: bool = False, pt_final: bool = False) -> PontoAStar:

	termo = ""

	if pt_inicial and not pt_final:
		termo = "INICIAL "

	elif pt_final and not pt_inicial:
		termo = "FINAL "

	ponto_str = input("\nEntre com o valor x, y do ponto {}(Ex.: '2 3'):\n".format(termo))

	ponto: PontoAStar = None

	# Se a entrada de fato for: dois inteiros separados por espaço, crie um ponto;
	try:
		ponto_split = ponto_str.split(" ")
		x, y = int(ponto_split[0]), int(ponto_split[1])
		ponto = PontoAStar(x, y)

	except:
		pass

	return ponto

def __validar_ponto_plano(ponto: Ponto, plano: PlanoCartesiano, simb_obst: object) -> bool:
	
	"""
	Verifica se um ponto é válido (não nulo, existente no plano, não obstáculo)
	em um plano.
	
	:param ponto: Ponto a ser validado.
	:param plano: Plano base para verificação do ponto.
	:param simb_obst: Símbolo usado como flag de obstáculos / barreiras.
	:return: True, se o ponto existir no plano e não for um obstáculo, senão, False.
	"""
	
	# Se a entrada do ponto for inválida, conter letras, caracteres não aceitos;
	if (not ponto):
		print("\nPonto digitado não é um ponto válido, corrija a entrada!")
		return False
	
	# Se o ponto não existir no plano;
	if (ponto not in plano):
		print("\nO ponto digitado não existe no plano! Tente outros valores.")
		return False
	
	# Se o ponto existir, mas for um obstáculo / barreira;
	if (plano.get_pt(ponto.x, ponto.y).valor == simb_obst):
		print("\nO ponto inicial existe no plano, porém é um OBSTÁCULO!")
		return False

	return True

def __validar_path(caminho: str) -> bool:
	
	"""
	Verifica se um path é válido para um arquivo texto.
	
	:param caminho: Caminho do arquivo a ser verificado.
	:return: True, se o caminho for de um arquivo texto existente, do contrário, False. 
	"""
	if not caminho:
		print("O caminho digitado não existe ou não é um arquivo!")
		return False

	if not caminho.lower().endswith(".txt"):
		print("O caminho digitado não pertence a um arquivo do TIPO TEXTO (.txt)!")
		return False

	return True

def ler_entrada() -> PlanoCartesiano:

	caminho = __ler_path_arquivo()
	
	while(not __validar_path(caminho)):
		caminho = __ler_path_arquivo()
	
	plano: PlanoCartesiano = ler_plano_arquivo(caminho)

	pt_inicial = __ler_ponto_teclado(pt_inicial=True)

	while(not __validar_ponto_plano(pt_inicial, plano, simb_obst_txt_arq)):
		pt_inicial = __ler_ponto_teclado(pt_inicial=True)

	pt_final = __ler_ponto_teclado(pt_final=True)

	while(not __validar_ponto_plano(pt_final, plano, simb_obst_txt_arq)):
		pt_final = __ler_ponto_teclado(pt_final=True)

	plano.pt_inicial = pt_inicial
	plano.pt_final = pt_final
	
	return plano

def imprimir_legenda(simb_pt_inic: object, simb_pt_final: object,
                     simb_pt_comum: object, simb_pt_obstaculo: object,
                     simb_pt_trajeto_final: object):

	print(__color_blue.format(simb_pt_inic.__str__() + ' - PONTO INICIAL'))
	print(__color_red.format(simb_pt_final.__str__() + ' - PONTO FINAL'))
	print(simb_pt_comum.__str__() + ' - PONTO COMUM')
	print(__color_purple.format(simb_pt_obstaculo.__str__() + ' - OBSTÁCULOS'))
	print(__color_green.format(simb_pt_trajeto_final.__str__() + ' - TRAJETO FINAL'))
	print()

	return 0

def main():

	init()

	# Defina os símbolos visuais que serão usados;
	esquerda = '◄'
	direita = '►'
	cima = '▲'
	baixo = '▼'
	obstaculo = '■'
	comum = '-'
	inicio = 'O'
	fim = 'O'

	# Aplique uma cor em cada símb de acordo c/ seu tipo (inicial, final,
	# obstáculo comum, trajeto)
	simb_inic = __color_blue.format(inicio)
	simb_final = __color_red.format(fim)

	simb_obst = __color_purple.format(obstaculo)

	simb_esq = __color_green.format(esquerda)
	simb_dir = __color_green.format(direita)
	simb_cima = __color_green.format(cima)
	simb_baixo = __color_green.format(baixo)

	# Leia o plano, ponto inicial e final;
	plano = ler_entrada()

	# Calcule o melhor trajeto;
	path = calc_trajeto(plano, plano.pt_inicial, plano.pt_final, simb_obst_txt_arq)

	# Estilize o plano para exibi-lo;
	plano.estilizar_trajeto(path, comum, simb_inic, simb_final, simb_obst,
	                        simb_cima, simb_baixo, simb_esq, simb_dir)
	print(plano)

	print(" ".join(["-"]*20))

	if len(path) > 0:
		print("PONTOS percorridos (X, Y):", [pt.to_tuple() for pt in path])
		print(" ".join(["-"] * 20))
		print("Distância: {}\n".format(len(path)))

	else:
		print("NÃO HÁ CAMINHOS POSSÍVEIS!!!\n")

	imprimir_legenda(simb_inic, simb_final, comum, simb_obst, simb_cima)

	return 0

main()

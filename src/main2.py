import platform
import os

try:
	from colorama import init
 
except ImportError:

	if (platform.system().upper() != "WINDOWS"):
		os.system("pip install --user colorama 2>&1 >/dev/null")

	else:
		os.system("pip3 install --user colorama /quiet")

	from colorama import init

import ia_random
from ia_algoritimos import calc_trajeto

def main():

	init()
	__color_red = "\033[31m{}\033[m"
	__color_green = "\033[32m{}\033[m"
	__color_yellow = "\033[33m{}\033[m"
	__color_blue = "\033[34m{}\033[m"
	__color_purple = "\033[35m{}\033[m"

	esquerda = '◄'
	direita = '►'
	cima = '▲'
	baixo = '▼'
	obstaculo = '■'
	comum = '+'
	inicio = 'O'
	fim = 'O'
        
	simb_esq = __color_green.format(esquerda)
	simb_dir = __color_green.format(direita)
	simb_cima = __color_green.format(cima)
	simb_baixo = __color_green.format(baixo)
	simb_obst = __color_purple.format(obstaculo)
	simb_inic = __color_blue.format(inicio)
	simb_final = __color_red.format(fim)

	plano = ia_random.gerar_plano_com_obstaculos(10, 8,
                                                     simb_pt_inic = simb_inic,
                                                     simb_pt_final = simb_final,
                                                     simb_obst = simb_obst,
                                                     simb_pt_comum = comum)
	path = calc_trajeto(plano, plano.pt_inicial, plano.pt_final, simb_obst)
	plano.estilizar_trajeto(path, simb_cima, simb_baixo, simb_esq, simb_dir)
	print(plano)

	print(" ".join(["-"]*10))

	if len(path) > 0:
		print("Distância: {}\n".format(len(path)))

	else:
		print("NÃO HÁ CAMINHOS POSSÍVEIS!!!\n")

	print(__color_blue.format(inicio + ' - PONTO INICIAL'))
	print(__color_red.format(fim + ' - PONTO FINAL'))
	print(comum + ' - PONTO COMUM')
	print(__color_purple.format(obstaculo + ' - OBSTÁCULOS'))
	print(__color_green.format(esquerda + ' - TRAJETO FINAL'))
	print()

	return 0

main()

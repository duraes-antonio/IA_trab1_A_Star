import ia_random
from ia_algoritimos import calc_trajeto

def main():
	__color_red = "\033[31m{}\033[m"
	__color_green = "\033[32m{}\033[m"
	__color_yellow = "\033[33m{}\033[m"
	__color_blue = "\033[34m{}\033[m"
	__color_purple = "\033[35m{}\033[m"

	simb_esq = __color_green.format('◀')
	simb_dir = __color_green.format('▶')
	simb_cima = __color_green.format('▲')
	simb_baixo = __color_green.format('▼')

	simb_obst = __color_purple.format('❚')
	simb_inic = __color_blue.format('●')

	plano = ia_random.gerar_plano_com_obstaculos(
		15, 7, simb_pt_inic=simb_inic, simb_obst=simb_obst)
	path = calc_trajeto(plano, plano.pt_inicial, plano.pt_final, simb_obst)
	plano.estilizar_trajeto(path, simb_cima, simb_baixo, simb_esq, simb_dir)
	print(plano)

	print(" ".join(["-"]*10))

	if len(path) > 0:
		print("Distância: {}\n".format(len(path) + 1))

	else:
		print("NÃO HÁ CAMINHOS POSSÍVEIS!!!\n")

	print(__color_blue.format('● - PONTO INICIAL'))
	print(__color_purple.format('❚ - OBSTÁCULOS'))
	print(__color_red.format('● - PONTO FINAL'))
	print(__color_green.format('◀ - TRAJETO FINAL'))

	print()

	return 0

main()

from ia_estruturas import *
from random import randint, choice

__color_red = "\033[31m{}\033[m"
__color_green = "\033[32m{}\033[m"
__color_blue = "\033[34m{}\033[m"

def gerar_plano_com_obstaculos(n_lin: int, n_col: int, n_obstaculos: int = None,
                               simb_pt_inic: str = None, simb_pt_final: str = None,
                               simb_pt_traj: str = None, simb_pt_comum: str = None,
                               simb_obst: str = None
                               ) -> PlanoCartesiano:

	simb_esq = simb_dir = simb_cima = simb_baixo = simb_pt_traj

	# Defina os símbolos do pt inicial e final, do trajeto percorrido
	# dos pt comuns e dos pts bloqueados;
	if not simb_pt_inic: simb_pt_inic = __color_red.format('●')
	if not simb_pt_final: simb_pt_final = __color_red.format('●')
	if not simb_pt_traj:
		simb_esq = __color_green.format('◀')
		simb_dir = __color_green.format('▶')
		simb_cima = __color_green.format('▲')
		simb_baixo = __color_green.format('▼')

	if not simb_pt_comum: simb_pt_comum = '+'
	if not simb_obst: simb_obst = __color_blue.format('✖')

	plano: PlanoCartesiano = PlanoCartesiano(n_lin, n_col, 4)

	# Se não receber o núm. de obstáculos, sorteie de
	# 0 até a qtd. de pontos - 2 (espaço para o ponto inicial e o final);
	if not n_obstaculos:
		n_obstaculos: int = randint(0, plano.n_pontos - 2)

	posicoes_pts = plano.get_posicoes_xy()

	# Preencha a quantidade de obstáculos
	for i in range(n_obstaculos):
		xy = choice(posicoes_pts)
		plano.get_pt(xy[0], xy[1]).valor = simb_obst
		posicoes_pts.remove(xy)

	# Estilize os pontos comuns
	for xy in posicoes_pts:
		plano.get_pt(xy[0], xy[1]).valor = simb_pt_comum

	# Escolha o ponto inicial e estilize-o
	xy = choice(posicoes_pts)
	plano.pt_inicial = plano.get_pt(xy[0], xy[1])
	plano.pt_inicial.valor = simb_pt_inic
	posicoes_pts.remove(xy)

	# Escolha o ponto final e estilize-o
	xy = choice(posicoes_pts)
	plano.pt_final = plano.get_pt(xy[0], xy[1])
	plano.pt_final.valor = simb_pt_final
	posicoes_pts.remove(xy)

	return plano
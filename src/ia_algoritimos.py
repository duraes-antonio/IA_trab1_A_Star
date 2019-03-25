from typing import List

from ia_estruturas import Ponto, PlanoCartesiano, PontoAStar


def calc_dist_manhattan(ponto_1: Ponto, ponto_2: Ponto) -> int:
	return abs(ponto_1.x - ponto_2.x) + abs(ponto_1.y - ponto_2.y)

def calc_dist_euclid(ponto_1: Ponto, ponto_2: Ponto) -> float:
	return ((ponto_1.x - ponto_2.x) ** 2 + (ponto_1.y - ponto_2.y) ** 2) ** (0.5)

def calc_trajeto(plano: PlanoCartesiano, pt_inicial: Ponto, pt_final: Ponto,
                 simbolo_bloqueio: str) -> List[PontoAStar]:

	# Defina como o primeiro ponto corrente, o ponto inicial recebido;
	pt_atual = pt_inicial

	# Armazene os nós já percorridos (p/ evitar laços s/ fim e mov. desnecessários)
	pts_fechados: List[PontoAStar] = []
	pts_abertos: List[PontoAStar] = [pt_atual]

	# Armazene os pontos que representam obstáculos;
	obstaculos = plano.get_pts_bloqueados(simbolo_bloqueio)

	encontrou = False

	# Enquanto houver pontos candidatos a serem verificados;
	while (pts_abertos):

		# Obtenha o pt da lista de abertos c/ o menor custo final;
		pts_abertos = sorted(pts_abertos, key=lambda pt: pt.f)
		pt_atual: PontoAStar = pts_abertos.pop(0)

		# Adicione o ponto atual na lista de pontos percorridos;
		pts_fechados.append(pt_atual)

		if pt_atual == pt_final:
			encontrou = True
			break

		# Obtenha os pontos vizinhos verticais e horizontais do ponto atual;
		vizinhos: List[PontoAStar] = plano.get_pts_adj_horiz_vert(pt_atual.x, pt_atual.y)

		# Remova os obstáculos dos pontos vizinhos;
		vizinhos = [pt for pt in vizinhos if pt not in obstaculos]

		# Remova os pontos já percorridos da lista de pontos vizinhos;
		vizinhos = [pt for pt in vizinhos if pt not in pts_fechados]

		# Para cada vizinho do ponto atual;
		for pt_viz in vizinhos:

			# Se o vizinho atual já estiver na lista de candidatos;
			if (pt_viz in pts_abertos):

				# Calcule a dist. G do ponto atual até o vizinho atual;
				g_dist = pt_atual.g + calc_dist_manhattan(pt_atual, pt_viz)

				# Se G do pt atual até o viz. for menor que o G antigo do viz;
				if (g_dist < pt_viz.g):
					# Defina o pt atual como pai do pt vizinho E atualize seu G;
					pt_viz.pt_pai = pt_atual
					pt_viz.g = g_dist

			# Senão, atualize as distâncias do pt vizinho e defina seu pt pai;
			else:

				pt_viz.pt_pai = pt_atual

				# Calcule sua distância (valor G) até o ponto atual;
				pt_viz.g = pt_atual.g + calc_dist_manhattan(pt_atual, pt_viz)

				# Calcule a dist. H do vizinho até o objetivo;
				pt_viz.h = calc_dist_manhattan(pt_viz, pt_final)

				pts_abertos.append(pt_viz)

	saida = []

	if encontrou:

		# Adicione o pai do ponto no trajeto final até que um ponto sem pai
		# seja encontrado;
		while (pt_atual.pt_pai):
			saida.append(pt_atual.pt_pai)
			pt_atual = pt_atual.pt_pai

		# Remova o ponto inicial do trajeto; Por fim inverta o trajeto;
		saida.remove(pt_inicial)
		saida.reverse()

	return saida

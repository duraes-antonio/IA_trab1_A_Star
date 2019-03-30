from typing import List


class Ponto:

	def __init__(self, x: int, y: int, valor: object = None):
		self._x = x
		self._y = y
		self._valor = valor

	@property
	def valor(self) -> object: return self._valor

	@valor.setter
	def valor(self, objeto: object): self._valor = objeto

	@property
	def x(self) -> int: return self._x

	@x.setter
	def x(self, valor_x: int): self._x = valor_x

	@property
	def y(self) -> int: return self._y

	@y.setter
	def y(self, valor_y: int): self._y = valor_y

	def __str__(self) -> str:
		return "X: {}; Y: {}; value: {}".format(self.x, self.y, self.valor)

	def __eq__(self, other) -> bool:
		if type(other) == type(self) and other.x == self.x and other.y == self.y:
			return True

		return False

	def to_tuple(self):
		return (self.x, self.y)

class PontoAStar(Ponto):

	def __init__(self, x: int, y: int, objeto: object = 0):
		self._f = 0
		self._g = 0
		self._h = 0
		self._pt_pai: PontoAStar = None
		super().__init__(x, y, objeto)

	@property
	def g(self) -> float:
		return self._g

	@g.setter
	def g(self, valor_g: float):

		if valor_g >= 0:
			self._g = valor_g
			self._f = self._g + self._h

		else:
			raise ValueError("O valor de G deve ser um valor flutuante não negativo.")

	@property
	def h(self) -> float:
		return self._h

	@h.setter
	def h(self, valor_h: float):

		if valor_h >= 0:
			self._h = valor_h
			self._f = self._g + self._h

		else:
			raise ValueError("O valor de H deve ser um valor flutuante não negativo.")

	@property
	def f(self) -> float:
		return self._f

	@property
	def pt_pai(self):
		return self._pt_pai

	@pt_pai.setter
	def pt_pai(self, ponto):
		self._pt_pai = ponto


class PlanoCartesiano:
	n_linhas: int
	n_colunas: int
	n_pontos: int
	quadrante: int
	__mapa: dict = {}

	_pt_inicial: PontoAStar
	_pt_final: PontoAStar
	__y_mult = 1
	__x_mult = 1

	def __init__(self, qtd_linhas: int, qtd_colunas: int, quadrante: int):
		self.n_linhas = qtd_linhas
		self.n_colunas = qtd_colunas
		self.n_pontos = qtd_colunas * qtd_linhas
		self.quadrante = quadrante
		self.__mapa = self.criar_mapa(qtd_linhas, qtd_colunas, quadrante)

	@property
	def pt_inicial(self) -> PontoAStar:
		return self._pt_inicial

	@pt_inicial.setter
	def pt_inicial(self, ponto: Ponto):
		self._pt_inicial = self.__mapa[(ponto.x, ponto.y)]

	@property
	def pt_final(self) -> PontoAStar:
		return self._pt_final

	@pt_final.setter
	def pt_final(self, ponto: Ponto):
		self._pt_final = self.__mapa[(ponto.x, ponto.y)]

	def criar_mapa(self, qtd_linhas: int, qtd_colunas: int, quadrante: int) -> dict:

		mapa: dict = {}

		if (quadrante == 2):
			self.__x_mult = -1

		elif (quadrante == 3):
			self.__y_mult = -1
			self.__x_mult = -1

		if (quadrante == 4):
			self.__y_mult = -1

		for i_lin in range(qtd_linhas):
			for i_col in range(qtd_colunas):
				ponto = (self.__x_mult * i_col, self.__y_mult * i_lin)
				mapa[ponto] = PontoAStar(ponto[0], ponto[1])

		return mapa

	def get_pt(self, x: int, y: int) -> PontoAStar:

		if (x, y) in self.__mapa: return self.__mapa[(x, y)]

		raise ValueError("O ponto com x = {} e y = {} não existe no plano!".format(x, y))

	def get_all(self) -> List[PontoAStar]:
		return [self.__mapa[chave] for chave in self.__mapa]

	def get_posicoes_xy(self) -> List[tuple]:
		return [chave for chave in self.__mapa]

	def get_pts_adj_horiz_vert(self, x: int, y: int) -> List[PontoAStar]:
		"""
		:param x: Posição X do ponto a ter os vizinhos buscados;
		:param y: Posição Y do ponto a ter os vizinhos buscados;
		:return: Lista c/ no máx 4 Pontos adjacentes horizontais e verticais;
		"""
		pts_saida = []

		# Se o ponto de entrada não existir no plano;
		if (x, y) not in self.__mapa:
			raise ValueError("O ponto(%d, %d) não existe no plano." % (x, y))

		if (x, y - 1) in self.__mapa: pts_saida.append(self.__mapa[(x, y - 1)])
		if (x - 1, y) in self.__mapa: pts_saida.append(self.__mapa[(x - 1, y)])
		if (x + 1, y) in self.__mapa: pts_saida.append(self.__mapa[(x + 1, y)])
		if (x, y + 1) in self.__mapa: pts_saida.append(self.__mapa[(x, y + 1)])

		return pts_saida

	def get_pts_adj(self, x: int, y: int) -> List[PontoAStar]:
		"""
		:param x: Posição X do ponto a ter os vizinhos buscados;
		:param y: Posição Y do ponto a ter os vizinhos buscados;
		:return: Lista com 8 Pontos adjacentes horizontais, verticais e diagonais;
		"""
		pts_saida = []

		if (x, y) not in self.__mapa: return pts_saida

		# Para os exemplos abaixo, tome como entrada o ponto (1, -1)
		# Obtém os 3 primeiros pts do eixo y, ex.: (0, -1), (1, -1), (2, -1)
		for _x in range(x - 1, x + 2, 1):
			if (_x, y + 1) in self.__mapa:
				pts_saida.append(self.get_pt(_x, y + 1))

		# Obtém os 2 pts laterais, ex.: (0, -2), (2, -2)
		if (x - 1, y) in self.__mapa: pts_saida.append(self.get_pt(x - 1, y))
		if (x + 1, y) in self.__mapa: pts_saida.append(self.get_pt(x + 1, y))

		# Obtém os 3 últimos pts do eixo y, ex.: (0, -3), (1, -3), (2, -3)
		for _x in range(x - 1, x + 2, 1):
			if (_x, y - 1) in self.__mapa:
				pts_saida.append(self.get_pt(_x, y - 1))

		return pts_saida

	def get_pts_bloqueados(self, simb_obstaculo: object) -> List[PontoAStar]:
		return [self.__mapa[xy] for xy in self.__mapa
		        if self.__mapa[xy].valor == simb_obstaculo]

	def listar_pontos(self) -> str:
		return "\n".join([str(self.__mapa[xy]) for xy in self.__mapa.keys()])

	def estilizar_trajeto(self, trajeto_final: List[PontoAStar],
	                      simb_pt_comum: str, simb_pt_inic: str,
	                      simb_pt_final: str, simb_obst: str, simb_cima: str,
	                      simb_baixo: str, simb_esq: str, simb_dir: str):

		# Altere os símbolos dos pontos OBSTÁCULOS / barreiras;
		pts_bloqueados: List[PontoAStar] = self.get_pts_bloqueados(1)

		for obstaculo in pts_bloqueados:
			obstaculo.valor = simb_obst

		# Altere os símbolos dos pontos comuns;
		pts_comuns = [pt for pt in self.get_all()
		              if (pt not in pts_bloqueados and pt not in trajeto_final)]

		for pt_comum in pts_comuns:
			pt_comum.valor = simb_pt_comum

		# Altere os símbolos do ponto INICIAL e do ponto FINAL;
		self.pt_inicial.valor = simb_pt_inic
		self.pt_final.valor = simb_pt_final

		ult_pt = self.pt_inicial

		for pt in trajeto_final:

			if (pt == self.pt_inicial or pt == self.pt_final): continue

			pt_plano = self.get_pt(pt.x, pt.y)

			if (pt.x, pt.y) not in self.__mapa:
				raise ValueError(
					"O ponto (x = {}, y = {}) não pertence ao plano!".format(pt.x, pt.y))

			if (pt.x > ult_pt.x or (pt == trajeto_final[-1] and pt.x < self.pt_final.x)):
				pt_plano.valor = simb_dir

			elif (pt.x < ult_pt.x or (pt == trajeto_final[-1] and pt.x > self.pt_final.x)):
				pt_plano.valor = simb_esq

			elif (pt.y < ult_pt.y or (pt == trajeto_final[-1] and pt.y > self.pt_final.y)):
				pt_plano.valor = simb_baixo

			elif (pt.y > ult_pt.y or (pt == trajeto_final[-1] and pt.y < self.pt_final.y)):
				pt_plano.valor = simb_cima

			ult_pt = pt

	def __str__(self) -> str:

		# Monte a linha c/ numeração das colunas
		n_dig_col = len(str(self.n_colunas))

		# Concatene o índice de cada coluna, separando-os por um tab;
		numeracao_col = "     X\t" + "\t".join(
			[str(i * self.__x_mult).zfill(n_dig_col)
			 for i in range(self.n_colunas)]
		)
		barras_num_col = " Y\t" + "".join(["_\t"] * self.n_colunas)

		mapa_str = "{}\n{}\n".format(numeracao_col, barras_num_col)

		# Monte a linha c/ numeração das linhas
		n_dig_lin = len(str(self.n_linhas))

		for i_linha in range(self.n_linhas):
			# Multiple o índice da linha pelo -1 ou 1, obtido pelo quadrante;
			const_y = i_linha * self.__y_mult

			# Adicione o índice da linha atual;
			temp_linha_str = "{}|\t".format(str(const_y if const_y != 0 else " 0").zfill(n_dig_lin))

			# Concatene os símbolos de todos os pts da linha, insira um tab entre eles;
			temp_linha_str += "\t".join(
				[str(self.get_pt(i_col * self.__x_mult, const_y).valor)
				 for i_col in range(self.n_colunas)]
			)
			mapa_str = "%s\n%s" % (mapa_str, temp_linha_str)

		return mapa_str

	def __contains__(self, ponto: Ponto):
		return (ponto.x, ponto.y) in self.__mapa

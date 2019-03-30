# IA_trab1_A_Star
### Primeiro trabalho semestral da disciplina de Inteligência Artificial do IFES campus Serra.<br><br>

## DESCRIÇÃO
### OBJETIVO
<p align="justify"/>
Desenvolver uma aproximação do algorítimo encontrador de caminhos (pathfinding) chamado "A Estrela" ("A Star" ou "A *").

<p align="justify"/>
A ideia é, dado um plano 2D contendo uma lista de pontos com coordenadas X e Y, um ponto de partida e um ponto de chegada, e até mesmo obstáculos (pontos inacessíveis), encontrar a lista de pontos que formam o trajeto mais curto entre o ponto de início e o fim, desviando das barreiras.

### EXEMPLO
<p align="center">
  <img src="https://github.com/duraes-antonio/IA_trab1_A_Star/blob/master/doc/img/exemplo_1.png">
</p>
<br>

## 1. Explicação Teórica do Algoritmo

<p align="justify"/>
O Algoritmo A* tem como objetivo encontrar um caminho entre em pontos (nós ou vértices), fazendo uso de heurísticas para reduzir a quantidade de operações que serão necessárias para se ter um resultado e assim se pode tratar grandes quantidades de possibilidades de caminho em tempo hábil (computacionalmente), sendo este resultado, o caminho o mais próximo do que seria o melhor caminho. Por conta dessa heurística, não pode-se afirmar que o caminho escolhido é o melhor, pois para isso, seria necessário passar por todos caminhos possíveis e verificar o menor.
  <br>

<p align="justify"/>
O algoritmo cria um plano, representado como uma matriz ou grafo, e verifica qual o ponto adjacente (em relação ao atual) tem o menor peso, sendo este, calculado através da heurística escolhida.
Como heurística, usa-se para cada ponto, o custo de movimentação do ponto atual a outro ponto adjacente a ele, somado ou a distância a partir do ponto adjacente ao ponto final ou a distância a partir do ponto adjacente ao ponto atual. A distância pode ser calculada de duas formas: distância euclidiana ou distância de Manhattan.
<br>

## IMPLEMENTAÇÃO A STAR / A*
<br>

Foram implementados os dois tipos de cálculo de distância, apesar de ser usado apenas o de Manhattan, o outro cálculo pode ser usado caso queira.

```python
def calc_dist_manhattan(ponto_1: Ponto, ponto_2: Ponto) -> int:
   return abs(ponto_1.x - ponto_2.x) + abs(ponto_1.y – ponto_2.y)

def calc_dist_euclid(ponto_1: Ponto, ponto_2: Ponto) -> float:
   return ((ponto_1.x - ponto_2.x) ** 2 + (ponto_1.y - ponto_2.y) ** 2) ** (0.5)
```

<p align="justify"/>
A função “calc_trajeto” é realmente quem aplica o algoritmo A*. Ela recebe como parâmetro, o plano (um objeto do tipo PlanoCartesiano), o ponto inicial e final (objetos do tipo Ponto) e o símbolo que representa um bloqueio/obstáculo dentro do plano (importante para o algorítimo identificar quais pontos são obstáculos).

<br><p align="justify"/>
A primeira coisa a ser feita de fazer com que o ponto atual seja o ponto inicial, depois inicializa uma lista vazia que representa com os pontos em que todos os vizinhos já foram visitados (pts_fechados) e uma lista com os pontos que devem ser verificados (pts_abertos). Depois se pega a lista de pontos que são obstáculos e por fim define-se uma flag para saber se encontrou o caminho ao sair do loop ou não.

```python
def calc_trajeto(plano: PlanoCartesiano, pt_inicial: Ponto, pt_final: Ponto,
                 simbolo_bloqueio: object) -> List[PontoAStar]:

   # Defina como o primeiro ponto corrente, o ponto inicial recebido;
   pt_atual = pt_inicial

   # Armazene os nós já percorridos (p/ evitar laços s/ fim e mov. desnecessários)
   pts_fechados: List[PontoAStar] = []
   pts_abertos: List[PontoAStar] = [pt_atual]

   # Armazene os pontos que representam obstáculos;
   obstaculos = plano.get_pts_bloqueados(simbolo_bloqueio)
   encontrou = False
```

<p align="justify"/>
Chega-se então ao loop principal, que será executado enquanto existir pontos que devem ser verificados ou até se o ponto atual ser o ponto final. Dentro do loop é feita uma ordenação (crescente) dos pontos abertos em relação ao resultado da heurística de cada um, e então se atribui ao ponto atual o que possui o menor valor. Após isso, se adiciona o ponto atual a lista de pontos fechados e verifica se o ponto atual é igual ao ponto final, pois caso seja, muda-se a flag e quebra o loop.

<br><p align="justify"/>
Os três próximos passos são para se saber quem são os vizinhos do ponto atual, tanto na horizontal quanto na vertical, mas sem que eles sejam obstáculos ou estejam na lista de pontos fechados, pois isso evita loops infinitos e também a escolha de um obstáculo como um caminho.

```python
# Enquanto houver pontos candidatos a serem verificados;
while (pts_abertos):

   # Obtenha o ponto da lista de abertos c/ o menor custo final;
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
```

<p align="justify"/>
Logo em seguida, entra-se em um loop que passa por vizinho, e que é peça fundamental para se obter o melhor caminho. É neste momento que os pontos começarão a ter os valores de G e H calculados ou recalculados, e terão como pai o ponto atual, caso o G até ele seja o menor ou caso ele nunca tenha sido aberto antes.

```python
# Para cada vizinho do ponto atual;
for pt_viz in vizinhos:

   # Se o vizinho atual já estiver na lista de candidatos;
   if (pt_viz in pts_abertos):

      # Calcule a dist. G do ponto atual até o vizinho atual;
      g_dist = pt_atual.g + calc_dist_manhattan(pt_atual, pt_viz)

      # Se G do ponto atual até o viz. for menor que o G antigo do vizinho;
      if (g_dist < pt_viz.g):

         # Defina o ponto atual como pai do ponto vizinho E atualize seu G;
         pt_viz.pt_pai = pt_atual
         pt_viz.g = g_dist

   # Senão, atualize as distâncias do ponto vizinho e defina seu ponto pai;
   else:

      pt_viz.pt_pai = pt_atual

      # Calcule sua distância (valor G) até o ponto atual;
      pt_viz.g = pt_atual.g + calc_dist_manhattan(pt_atual, pt_viz)

      # Calcule a dist. H do vizinho até o objetivo;
      pt_viz.h = calc_dist_manhattan(pt_viz, pt_final)
      pts_abertos.append(pt_viz)
```

<p align="justify"/>
Após o loop principal finalizar, ele chega nesse trecho de código, que caso tenha sido encontrado um caminho, ele passa por todos pontos pais, a partir do último (que é o ponto atual), e o adiciona na lista de saída e depois atribui ao ponto atual o pai dele. No fim desse processo se tem o caminho de trás para frente, bastando apenas revertê-lo para se obter o caminho no sentido correto.

```python
saida = []

if encontrou:

   # Adicione o pai do ponto no trajeto final até que um ponto sem pai seja encontrado;
   while (pt_atual.pt_pai):
      saida.append(pt_atual.pt_pai)
      pt_atual = pt_atual.pt_pai

   # Remova o ponto inicial do trajeto; Por fim inverta o trajeto;
   saida.remove(pt_inicial)
   saida.reverse()
   saida.append(pt_final)

return saida
```

## 2. Exemplo de chamada
```python

x@pc IA_trab1_A_Star/src $ python3 main.py

Digite ou cole o path do arquivo contendo o plano:
plano.txt

Entre com o valor x, y do ponto INICIAL (Ex.: '2 3'):
0 0

Entre com o valor x, y do ponto FINAL (Ex.: '2 3'):
5 -4
```

```
  x	0	1	2	3	4	5
 y _	_	_	_	_	_	_
 0|	-	■	-	-	-	B
-1|	A	■	■	-	-	^
-2|	v	■	-	-	■	^
-3|	v	■	-	>	>	>
-4|	v	>	>	>	■	-
```
- - - - - - - - - - - - - - - - - - - -
PONTOS percorridos (X, Y): [(0, -2), (0, -3), (0, -4), (1, -4), (2, -4), (3, -4), (3, -3), (4, -3), (5, -3), (5, -2), (5, -1), (5, 0)]
```
- - - - - - - - - - - - - - - - - - - -
Distância: 12

A - PONTO INICIAL
B - PONTO FINAL
- - PONTO COMUM
■ - OBSTÁCULOS
^ - TRAJETO FINAL
```
<br>

## 3. FERRAMENTAS UTILIZADAS
* Python 3.6
* Colorama: Lib para Python para colorir textos no CMD
<br>

## 4. REFERÊNCIAS E OUTROS MATERIAIS BASE
[1] “Demonstrando algoritmo A* (Pathfinding)”: https://www.youtube.com/watch?v=s29WpBi2exw<br>
[2] “Explicação do Algoritmo A* (A Star)”: https://www.youtube.com/watch?v=o5_mqZKhTvw<br>
[3] “A * Pathfinding para Iniciantes”: https://ava.cefor.ifes.edu.br/pluginfile.php/273364/mod_resource/content/1/A%20%20%20Pathfinding%20para%20Iniciantes.pdf


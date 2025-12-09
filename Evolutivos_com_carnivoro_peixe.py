pip install numpy matplotlib

import numpy as np
import matplotlib.pyplot as plt
import random
import csv


mapa_largura = 100
mapa_altura = 100
SIZE = 100
N_MOVES = 50

peixe = [5,10,0,0,0,0,0]
mamifero_come_peixe = [15,15,0,0,0,0,0]
mamifero_come_herbivoro = [15,15,0,0,0,0,0]
mamifero_herbivoro = [12,15,0,0,0,0,0]
mosquito = [1,10,0,0,0,0,0]

def gerar_coordenadas(largura, altura):
    x = random.randint(0, largura - 1)
    y = random.randint(0, altura - 1)
    return x, y
peixe[4], peixe[3] = gerar_coordenadas(mapa_largura, mapa_altura)
mamifero_come_peixe[4], mamifero_come_peixe[3] = gerar_coordenadas(mapa_largura, mapa_altura)
mamifero_come_herbivoro[4], mamifero_come_herbivoro[3] = gerar_coordenadas(mapa_largura, mapa_altura)
mamifero_herbivoro[4], mamifero_herbivoro[3] = gerar_coordenadas(mapa_largura, mapa_altura)
mosquito[4], mosquito[3] = gerar_coordenadas(mapa_largura, mapa_altura)


SIZE = 100

# 0 = água
# 1 = terra
# 2 = floresta (árvores)
# 3 = peixe
#4 = mamifero 1
#5 = mamifero 2
#6 = mamifero herb
#7 = mosquito

grid = np.ones((SIZE, SIZE), dtype=int)  

# -----------------------------------------------------------
# 1) RIO SINUOSO HORIZONTAL (fixo)
# -----------------------------------------------------------

def draw_sine_river(grid, amplitude=8, y_offset=50, width=3, frequency=0.12):
    for x in range(SIZE):
        
        y_center = int(amplitude * np.sin(frequency * x) + y_offset)

        for w in range(-width, width + 1):
            y = y_center + w
            if 0 <= y < SIZE:
                grid[y, x] = 0  

draw_sine_river(grid)

# -----------------------------------------------------------
# 2) RIO VERTICAL (cruzando o outro rio)
# -----------------------------------------------------------

def draw_vertical_sine_river(grid, amplitude=8, x_offset=60, width=2, frequency=0.12):
    for y in range(SIZE):
        x_center = int(amplitude * np.sin(frequency * y) + x_offset)

        for w in range(-width, width + 1):
            x = x_center + w
            if 0 <= x < SIZE:
                grid[y, x] = 0

draw_vertical_sine_river(grid)

# -----------------------------------------------------------
# 3) LAGOAS FIXAS
# -----------------------------------------------------------

def draw_lake(grid, cx, cy, radius):
    for x in range(SIZE):
        for y in range(SIZE):
            if (x - cx)**2 + (y - cy)**2 <= radius**2:
                grid[y, x] = 0

draw_lake(grid, 25, 25, 5)
draw_lake(grid, 70, 20, 7)
draw_lake(grid, 40, 80, 6)

# -----------------------------------------------------------
# 4) ILHAS DE TERRA DENTRO DE LAGOAS E RIOS
# -----------------------------------------------------------

islands = [(25, 25), (40, 80), (70, 20), (50, 50), (60, 60)]

for ix, iy in islands:
    if 0 <= ix < SIZE and 0 <= iy < SIZE:
        grid[iy, ix] = 1  # botão de terra no meio da água

# -----------------------------------------------------------
# 5) FLORESTA ESPAÇADA FIXA (padrão pontilhado)
# -----------------------------------------------------------

for x in range(0, 100, 3):      # espaçamento horizontal
    for y in range(0, 50, 3):  # espaçamento vertical
        if grid[y, x] == 1:      # só coloca árvore em terra
            grid[y, x] = 2


original_terrain_layout = grid.copy()


WATER = 0 
water_positions = np.argwhere(original_terrain_layout == WATER)

# -----------------------------------------------------------
# Adiciona os animais
# -----------------------------------------------------------
grid[peixe[4], peixe[3]] = 3
grid[mamifero_come_peixe[4], mamifero_come_peixe[3]] = 4
grid[mamifero_come_herbivoro[4], mamifero_come_herbivoro[3]] = 5
grid[mamifero_herbivoro[4], mamifero_herbivoro[3]] = 6
grid[mosquito[4], mosquito[3]] = 7




# -----------------------------------------------------------
# Visualização
# -----------------------------------------------------------

plt.figure(figsize=(6, 6))
im = plt.imshow(grid, origin='lower')
cbar = plt.colorbar(im, ticks=[0, 1, 2, 3, 4, 5, 6, 7])
cbar.ax.set_yticklabels([
    'Água (0)', 'Terra (1)', 'Floresta (2)',
    'Peixe (3)', 'Mamífero-Peixe (4)', 'Mamífero-Herbivoro (5)',
    'Herbívoro (6)', 'Mosquito (7)'
])
plt.title("Mapa Natural Fixo 100×100 — com animais")
plt.xticks([]); plt.yticks([])
plt.show()


from matplotlib.colors import ListedColormap


cmap = ListedColormap([
    "#6baed6",  # 0 - água (azul)
    "#c2b280",  # 1 - terra (bege)
    "#228b22",  # 2 - floresta (verde escuro)
    "#1f78b4",  # 3 - peixe (azul forte)
    "#ff7f00",  # 4 - mamífero que come peixe (laranja)
    "#e31a1c",  # 5 - mamífero que come herbívoro (vermelho)
    "#ffc0cb",  # 6 - herbívoro (verde claro)
    "#6a3d9a",   # 7 - mosquito (roxo)
    "#7f7f7f"  # 8 cadaver (gray)
])

plt.figure(figsize=(6, 6))
im = plt.imshow(grid, origin='lower', cmap=cmap)


cbar = plt.colorbar(im, ticks=range(9))
cbar.ax.set_yticklabels([
    'Água (0)', 'Terra (1)', 'Floresta (2)',
    'Peixe (3)', 'Mamífero-Peixe (4)',
    'Mamífero-Herbívoro (5)', 'Herbívoro (6)', 'Mosquito (7)','Cadaver (8)'
])

plt.title("Mapa com Animais Coloridos")
plt.xticks([]); plt.yticks([])
plt.show()

movimentos_possiveis = [
    (0, 1),   # cima
    (0, -1),  # baixo
    (1, 0),   # direita
    (-1, 0),  # esquerda
    (0, 0)    # fica parado
]

def gerar_movimentos(qtd=50):
    return [random.choice(movimentos_possiveis) for _ in range(qtd)]
def gerar_peixes():
    
    if len(water_positions) == 0:
        x, y = random.randint(0, SIZE - 1), random.randint(0, SIZE - 1)
    else:
        idx = random.randint(0, len(water_positions) - 1)
        y, x = water_positions[idx] 

    t = gerar_movimentos(N_MOVES)
    return [5, 10, 0, x, y, t.copy(), 0, t.copy()]

def gerar_mamiferos_come_peixe():
    x = random.randint(0, 99)
    y = random.randint(0, 99)
    t = gerar_movimentos(N_MOVES)
    return [15, 15, 0, x, y, t.copy(), 0, t.copy()]

def gerar_mamiferos_come_herbivoro():
    x = random.randint(0, 99)
    y = random.randint(0, 99)
    t = gerar_movimentos(N_MOVES)
    return [15, 15, 0, x, y, t.copy(), 0, t.copy()]

def gerar_herbivoros():
    x = random.randint(0, 99)
    y = random.randint(0, 99)
    t = gerar_movimentos(N_MOVES)
    return [12, 15, 0, x, y, t.copy(), 0, t.copy()]

def gerar_mosquitos():
    x = random.randint(0, 99)
    y = random.randint(0, 99)
    t = gerar_movimentos(N_MOVES)
    return [1, 10, 0, x, y, t.copy(), 0, t.copy()]

qtd_peixes = 400
qtd_mam_peixe = 240
qtd_mam_herb = 240
qtd_herb = 400
qtd_mosquitos = 500

peixes =  [gerar_peixes() for _ in range(qtd_peixes)]
mam_peixes = [gerar_mamiferos_come_peixe() for _ in range(qtd_mam_peixe)]
mam_herb =  [gerar_mamiferos_come_herbivoro() for _ in range(qtd_mam_herb)]
herbivoros = [gerar_herbivoros() for _ in range(qtd_herb)]
mosquitos = [gerar_mosquitos() for _ in range(qtd_mosquitos)]




for a in peixes:
    grid[a[4], a[3]] = 3

for a in mam_peixes:
    grid[a[4], a[3]] = 4

for a in mam_herb:
    grid[a[4], a[3]] = 5

for a in herbivoros:
    grid[a[4], a[3]] = 6

for a in mosquitos:
    grid[a[4], a[3]] = 7
plt.imshow(grid, origin="lower", cmap=cmap)
plt.show()

def criar_individuo(especie):
    # constantes de cada espécie
    if especie == "peixe":
        c1, c2, c3 = 5, 10, 0
       
        if len(water_positions) == 0:
            varA, varB = random.randint(0, SIZE - 1), random.randint(0, SIZE - 1)
        else:
            idx = random.randint(0, len(water_positions) - 1)
            varB, varA = water_positions[idx] 
    elif especie == "herbivoro":
        c1, c2, c3 = 12, 15, 0
        varA = random.randint(0, SIZE - 1)
        varB = random.randint(0, SIZE - 1)
    elif especie == "carnivoro_peixes":
        c1, c2, c3 = 15, 15, 0
        varA = random.randint(0, SIZE - 1)
        varB = random.randint(0, SIZE - 1)
    elif especie == "carnivoro_herb":
        c1, c2, c3 = 15, 15, 0
        varA = random.randint(0, SIZE - 1)
        varB = random.randint(0, SIZE - 1)
    elif especie == "mosquito":
        c1, c2, c3 = 1, 10, 0
        varA = random.randint(0, SIZE - 1)
        varB = random.randint(0, SIZE - 1)
    else:
        raise ValueError("Espécie inválida")

    # Gerar N_MOVES para novos indivíduos e garantir cópias independentes
    initial_moves = gerar_movimentos(N_MOVES)

    return [c1, c2, c3, varA, varB, initial_moves.copy(), 0, initial_moves.copy()]


def mutacao(ind):
    
    val = random.randint(3, 4)  
    var = random.uniform(-5, 5)
    ind[val] = int(max(0, min(SIZE - 1, ind[val] + var))) 

    
    mutation_rate_movements = 0.05 
    for i in range(len(ind[7])):
        if random.random() < mutation_rate_movements:
            ind[7][i] = random.choice(movimentos_possiveis)

    
    ind[5] = ind[7].copy()

def evolucao(pai1, pai2,especie):
    movimentos_filho = []

   
    parent1_orig_moves = pai1[7] if len(pai1) > 7 else []
    parent2_orig_moves = pai2[7] if len(pai2) > 7 else []

    for i in range(N_MOVES): 
        move1 = parent1_orig_moves[i] if i < len(parent1_orig_moves) else random.choice(movimentos_possiveis)
        move2 = parent2_orig_moves[i] if i < len(parent2_orig_moves) else random.choice(movimentos_possiveis)

        if random.random() < 0.5:
            movimentos_filho.append(move1)
        else:
            movimentos_filho.append(move2)
    if especie == "peixe":
        c1, c2, c3 = 5, 10, 0
    elif especie == "herbivoro":
        c1, c2, c3 = 12, 15, 0
    elif especie == "carnivoro_peixes":
        c1, c2, c3 = 15, 15, 0
    elif especie == "carnivoro_herb":
        c1, c2, c3 = 15, 15, 0
    elif especie == "mosquito":
        c1, c2, c3 = 1, 10, 0

    filho = [
        c1 ,
        c2,
        c3,
        int((pai1[3] + pai2[3]) / 2), 
        int((pai1[4] + pai2[4]) / 2), 
        movimentos_filho.copy(), 
        0,
        movimentos_filho.copy()
    ]

    mutacao(filho)
    return filho
def pior_todos(lista):
    pior = 0
    for i in range(len(lista)):
        if lista[i][6] < lista[pior][6]:
            pior = i
    return pior
def melhor_todos(lista):
    melhor = 0
    for i in range(len(lista)):
        if lista[i][6] > lista[melhor][6]:
            melhor = i
    return melhor
def predacao_randomica(lista, indice,especie):
    lista[indice] = criar_individuo(especie)
    return lista

def genocidio(lista, melhor_idx,especie):
    nova = [lista[melhor_idx]] 
    for _ in range(len(lista)-1):
        nova.append(criar_individuo(especie))
    return nova


def select_parent_tournament(lista, tournament_size=3):
    """Selects a parent using tournament selection."""
    if len(lista) == 0:
        return None 
    if len(lista) < tournament_size:
        
        return random.choice(lista)

    tournament_candidates = random.sample(lista, tournament_size)
    best_candidate = tournament_candidates[0]
    for i in range(1, tournament_size):
        if tournament_candidates[i][6] > best_candidate[6]:
            best_candidate = tournament_candidates[i]
    return best_candidate

def darwin(lista, especie):
    melhor_idx = melhor_todos(lista)
    pior_idx = pior_todos(lista)

    
    predacao_randomica(lista, pior_idx, especie)

    
    elite = lista[melhor_idx]
    nova_lista = [elite]

    
    for _ in range(len(lista) - 1):
        parent1 = select_parent_tournament(lista)
        parent2 = select_parent_tournament(lista)
        
        if parent1 is not None and parent2 is not None:
            nova_lista.append(evolucao(parent1, parent2, especie))
        else:
            
            nova_lista.append(criar_individuo(especie))

    return nova_lista

valores_finais = []
def clamp_pos(x, y):
    x = int(max(0, min(SIZE-1, x)))
    y = int(max(0, min(SIZE-1, y))) 
    return x, y
random.seed(42)
np.random.seed(42)

SIZE = 100
N_MOVES = 50

# grid codes
WATER = 0
LAND = 1
TREE = 2
CADAVER = 8
def processar_animal(a, tipo, grid, outros_animais):
    vida, energia, fome, x, y, movs, avalia,movs_or = a

    # Dano por ambiente
    if tipo != "peixe" and tipo != "mosquito" and grid[y, x] == WATER:
        vida -= 2
    elif tipo == "peixe" and grid[y, x] != WATER:
        vida -= 5

    # NÃO POPAR movimentos aqui — já foram consumidos em mover_animais
    # 2) COMIDA
    comeu = False

    if tipo == "peixe":
        pass  # peixes não comem
        comeu = True

    elif tipo == "herbivoro":
        if grid[y, x] == TREE:
           
            fome = 0
            energia += 2
            comeu = True

    elif tipo == "carnivoro_herb":
        # procura herbívoros na mesma posição
        for prey in outros_animais.get("herbivoros", []):
            if prey[3] == x and prey[4] == y and prey[0] > 0:
                prey[0] = 0
                grid[y, x] = CADAVER
                fome = 0
                energia += 5
                comeu = True
                break

    elif tipo == "carnivoro_peixes":
        for prey in outros_animais.get("peixes", []):
            if prey[3] == x and prey[4] == y and prey[0] > 0:
                prey[0] = 0
                grid[y, x] = CADAVER
                fome = 0
                energia += 5
                comeu = True
                break

    elif tipo == "mosquito":
        if grid[y, x] == CADAVER:
            grid[y, x] = LAND
            fome = 0
            energia += 2
            comeu = True

    # 3) fome
    if not comeu:
        fome += 1

    # 4) dano por fome
    if fome >= 20:
        vida -= 1
    avalia +=1
    # atualizar lista do animal
    a[0], a[1], a[2], a[3], a[4], a[6] = vida, energia, fome, x, y, avalia

    
    if vida <= 0:
        grid[y, x] = CADAVER


# mover_animais agora também atualiza energia (mover gasta 1, ficar parado +1)
def mover_animais(lista_animais):
    for a in lista_animais:
        if a[0] <= 0:  # morto
            continue
        movimentos = a[5]
        if len(movimentos) == 0:
            continue
        dx, dy = movimentos.pop(0)
        # energia
        if dx == 0 and dy == 0:
            a[1] += 1
        else:
            a[1] -= 1
        nx, ny = clamp_pos(a[3] + dx, a[4] + dy)
        a[3], a[4] = nx, ny

# função para simular 1 rodada: mover tudo e depois processar comida
def rodada():
    # mover todos (simultâneo no sentido de que movemos primeiro todos)
    mover_animais(peixes)
    mover_animais(herbivoros)
    mover_animais(mam_peixes)
    mover_animais(mam_herb)
    mover_animais(mosquitos)

    # montar dict com listas de presas (passar referências)
    outros = {
        "peixes": peixes,
        "herbivoros": herbivoros
    }

    # processar alimentação para cada grupo
    for a in peixes:
        if a[0] > 0:
            processar_animal(a, "peixe", grid, outros)
    for a in herbivoros:
        if a[0] > 0:
            processar_animal(a, "herbivoro", grid, outros)
    for a in mam_peixes:
        if a[0] > 0:
            processar_animal(a, "carnivoro_peixes", grid, outros)
    for a in mam_herb:
        if a[0] > 0:
            processar_animal(a, "carnivoro_herb", grid, outros)
    for a in mosquitos:
        if a[0] > 0:
            processar_animal(a, "mosquito", grid, outros)


def contar_vivos(lista):
    return sum(1 for a in lista if a[0] > 0)

# --- simular e desenhar a cada rodada ---
last_generation_plots = [] 

for p in range(50):
  for r in range(N_MOVES):
      rodada()

      # preparar plot_grid com sobreposição dos animais vivos
      plot_grid = original_terrain_layout.copy() 


      cadaver_y, cadaver_x = np.where(grid == CADAVER)
      plot_grid[cadaver_y, cadaver_x] = CADAVER

      for a in peixes:
          if a[0] > 0:
              plot_grid[int(a[4]), int(a[3])] = 3
      for a in mam_peixes:
          if a[0] > 0:
              plot_grid[int(a[4]), int(a[3])] = 4
      for a in mam_herb:
          if a[0] > 0:
              plot_grid[int(a[4]), int(a[3])] = 5
      for a in herbivoros:
          if a[0] > 0:
              plot_grid[int(a[4]), int(a[3])] = 6
      for a in mosquitos:
          if a[0] > 0:
              plot_grid[int(a[4]), int(a[3])] = 7


      if p == 49:
          title_text = (f"Rodada {r+1} — vivos: P={contar_vivos(peixes)} H={contar_vivos(herbivoros)} "
                        f"MP={contar_vivos(mam_peixes)} MH={contar_vivos(mam_herb)} X={contar_vivos(mosquitos)}")
          last_generation_plots.append((plot_grid.copy(), title_text)) 

 
  peixes = darwin(peixes,"peixe")
  herbivoros = darwin(herbivoros,"herbivoro")
  mam_peixes = darwin(mam_peixes,"carnivoro_peixes")
  mam_herb = darwin(mam_herb,"carnivoro_herb")
  mosquitos = darwin(mosquitos,"mosquito")
  if p % 50 == 20:
    peixes = genocidio(peixes,melhor_todos(peixes),"peixe")
  if p % 50 == 30:
    herbivoros = genocidio(herbivoros,melhor_todos(herbivoros),"herbivoro")
    mam_peixes = genocidio(mam_peixes,melhor_todos(mam_peixes),"carnivoro_peixes")
  if p % 50 == 40:
    mam_herb =genocidio(mam_herb,melhor_todos(mam_herb),"carnivoro_herb")
    mosquitos =genocidio(mosquitos,melhor_todos(mosquitos),"mosquito")

 
  cadaver_y, cadaver_x = np.where(grid == CADAVER)
  for cy, cx in zip(cadaver_y, cadaver_x):
      grid[cy, cx] = original_terrain_layout[cy, cx]


  valores = [peixes[melhor_todos(peixes)][6], herbivoros[melhor_todos(herbivoros)][6], mam_peixes[melhor_todos(mam_peixes)][6], mam_herb[melhor_todos(mam_herb)][6], mosquitos[melhor_todos(mosquitos)][6]]
  valores_finais.append(valores)

print(valores_finais)

plt.ion() 
fig = plt.figure(figsize=(6,6))
for plot_grid_frame, title_text in last_generation_plots:
    plt.clf() 
    plt.imshow(plot_grid_frame, origin="lower", cmap=cmap, vmin=0, vmax=8)
    plt.title(title_text)
    plt.xticks([]); plt.yticks([])
    plt.pause(0.4) 

plt.ioff()
plt.show()

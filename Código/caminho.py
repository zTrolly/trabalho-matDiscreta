"""
Aluno: Breno Lopes do Carmo
"""


import random
import sys
import heapq

def dijkstra(graph, inicio):
    distancias = {no: [sys.maxsize, None] for no in graph}  # Inicializa todas as distâncias como infinito
    distancias[inicio][0] = 0  # Define a distância do nó de início como 0
    visitados = set()

    heap = [(0, inicio)]  # Cria uma fila de prioridade com a distância atual e o nó de início

    while heap:
        distancia_atual, no_atual = heapq.heappop(heap)  # Remove o nó com menor distância atual da fila de prioridade

        if no_atual in visitados:  # Se o nó já foi visitado, passa para o próximo
            continue

        visitados.add(no_atual)  # Marca o nó como visitado

        for vizinho, peso in graph[no_atual].items():  # Percorre todos os vizinhos do nó atual
            distancia = distancia_atual + peso  # Calcula a distância até o vizinho

            if distancia < distancias[vizinho][0]:  # Se a nova distância for menor que a distância atual
                distancias[vizinho][0] = distancia  # Atualiza a distância do vizinho
                distancias[vizinho][1] = no_atual  # Define o nó atual como o nó anterior no caminho
                heapq.heappush(heap, (distancia, vizinho))  # Insere o vizinho na fila de prioridade com a nova distância

    return distancias  # Retorna as distâncias mínimas a partir do nó de início para todos os outros nós


def ler_grafo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            dados = arquivo.readlines()

            n, inicio, fim = map(int, dados[0].split())  # Obtém o número de cidades, nó de início e nó de destino
            grafo = {no: {} for no in range(1, n + 1)}  # Cria um dicionário vazio para representar o grafo

            for linha in dados[1:-1]:  # Lê as linhas com informações sobre as arestas do grafo
                cidade1, cidade2, distancia = map(int, linha.split())  # Obtém a cidade1, cidade2 e a distância
                grafo[cidade1][cidade2] = distancia  # Adiciona uma aresta entre cidade1 e cidade2 com a distância
                grafo[cidade2][cidade1] = distancia  # Adiciona uma aresta entre cidade2 e cidade1 com a distância

            return grafo, inicio, fim  # Retorna o grafo, nó de início e nó de destino

    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado.")
        sys.exit(1)

    except (ValueError, IndexError):
        print("Formato inválido no arquivo.")
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Utilização: caminho <nome>")
        print("<nome>: nome do arquivo contendo as informações do grafo")
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    grafo, inicio, fim = ler_grafo(nome_arquivo)
    distancias = dijkstra(grafo, inicio)
    

    if distancias[fim][0] == sys.maxsize:
        print(f"Não existe caminho de {inicio} para {fim}.")
    else:
        caminho = []
        no_atual = fim
        while no_atual != inicio:  # Constrói o caminho a partir do nó de destino até o nó de início
            caminho.append(no_atual)
            no_atual = distancias[no_atual][1]  # Obtém o nó anterior no caminho
        caminho.append(inicio)
        caminho.reverse()
        caminho_str = ' '.join(f"{no}({distancias[no][0]})" for no in caminho)
        print(f"Caminho de {inicio} para {fim}: {caminho_str}")


#METODO DE DEBUG PARA CRIAR UM GRAFO ALEATORIO E TESTAR O ALGORITMO
def criar_grafo_aleatorio(num_nodos, origem, destino, distancia_maxima):
    # Cria um grafo vazio
    grafo = {no: {} for no in range(1, num_nodos + 1)}

    # Adiciona arestas aleatórias ao grafo
    for nodo1 in range(1, num_nodos + 1):
        for nodo2 in range(nodo1 + 1, num_nodos + 1):
            distancia = random.randint(1, distancia_maxima)
            grafo[nodo1][nodo2] = distancia
            grafo[nodo2][nodo1] = distancia

    # Abre o arquivo "debug.txt" para escrever as informações do grafo
    with open("debug.txt", "w") as arquivo:
        # Escreve a primeira linha com o número de cidades, origem e destino
        arquivo.write(f"{num_nodos} {origem} {destino}\n")

        # Escreve as linhas de conteúdo com as informações das arestas
        for nodo1 in range(1, num_nodos + 1):
            for nodo2, distancia in grafo[nodo1].items():
                arquivo.write(f"{nodo1} {nodo2} {distancia}\n")

        # Escreve a linha final indicando o término das informações
        arquivo.write("-1 -1 -1\n")

    print("Grafo aleatório criado e salvo em 'debug.txt'.")

if __name__ == "__main__":
    main()

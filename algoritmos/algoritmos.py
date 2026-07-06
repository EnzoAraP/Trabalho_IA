import numpy as np
import sys
import heapq
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modelos.No import No
from modelos.Labirinto import Labirinto


matrizLabirinto = np.zeros((10,10))

class Algoritmos:
    def __init__(self, labirinto, ao_visitar):
        self.labirinto = labirinto
        self.ao_visitar = ao_visitar
        self.listaExplorados = []
        self.listaVistos = []
        self.listaFinal = []
    def backtracking(self):
        print("Entrou no backtracking")
        atual= self.labirinto.inicio
        estadoInicial = atual.valor
        estadoFinal = self.labirinto.fim.valor
        
        sequenciamento= ("d","b","e","c")
        self.listaExplorados.append(atual)
        fracasso = False
        sucesso = False
        proximo = None
        print(atual.valor)
        while((not fracasso and not sucesso)):
            print()
            if(atual.regra.get("d")==0 or atual.regra.get("b")==0 or atual.regra.get("e")==0  or atual.regra.get("c")==0 ):
                for direcao,valor in atual.regra.items():
                    if valor==0:
                        atual.regra[direcao] = 1
                        atual=self.movimentacao(atual,direcao,self.listaExplorados)#será igual a ele mesmo se ja o prox ja estiver presente ( não tem o por que reexplora-lo) ou o novo se for um nó novo
                        break
                if(atual.valor == estadoFinal):
                    print("Resultado encontrado!\n")
                    sucesso=True
                    self.pintarFinal()
                    break
            else:
                if atual.valor == estadoInicial:
                    print("Retnou pro pai inicial,erro")
                    fracasso = True
                else:
                    self.listaFinal.remove(atual)
                    atual = atual.pai             
        return 0
    def pintarFinal(self):
        for no in self.listaFinal:
            no.caminhofinal=True
            self.ao_visitar(no.valor[0],no.valor[1])
            
    def movimentacao(self,Noatual,direcao,listaExplorados):#se estiver correto, só será mudado para o novo nó se ele não estiver adicionado na lista, se não retorna o atual.
        print("Entrou no Movimentacao")
        Noatual.regra[direcao]=1
        novovalor=None
        match direcao:
            case "d":
                novovalor = self.verificapossibilidade(Noatual.valor[0],Noatual.valor[1]+1)
            case "b":
                novovalor = self.verificapossibilidade(Noatual.valor[0]+1,Noatual.valor[1])
            case "e":
                novovalor = self.verificapossibilidade(Noatual.valor[0],Noatual.valor[1]-1)
            case "c":
                novovalor = self.verificapossibilidade(Noatual.valor[0]-1,Noatual.valor[1])
        print(f"valor novovalor:{novovalor}")
        presentenalista = any(no.valor ==(novovalor) for no in listaExplorados)#verifica se o nó com valores novos já está presente na lista de nós
        print(f"estado atual da lista de explorados:{listaExplorados}")
    
        if (presentenalista): #caso já esteja na lista de presentes, apenas poe que tal nó é um dos filhos do nó atual
            filho = next((no for no in listaExplorados if no.valor== novovalor))
            Noatual.filhos.append(filho)
        if not presentenalista and novovalor!=None: #caso o nó não esteja presente na lista, ele é criado com o atual sendo o pai e aidiconado na lista de vistos
            Novono = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
            Novono.pai =Noatual
            Novono.visto=True
            self.ao_visitar(novovalor[0],novovalor[1])
            self.listaFinal.append(Novono)
            listaExplorados.append(Novono)
            return Novono
        return Noatual
    
    
        return 0

    def verificapossibilidade(self,valor1,valor2):#novo valor será None se for um valor que não pode ser incluso na lista (out of bounds ou em barreira), e valor1 valor2 se for possível adicionar
        print("Entrou no verificacao")
        if(self.labirinto.eh_posicao_validamover(valor1,valor2)):
            return(valor1,valor2)
        else:
            return(None)
    
    def busca_profundidade_limitada(self, limite):
        print("Entrou na Busca em Profundidade Limitada")
        
        pilha = []

        self.listaExplorados = [] 
        self.listaVistos = []
        self.listaFinal = []
        
        inicio = self.labirinto.inicio
        fim = self.labirinto.fim
        
        inicio.pai = None

        pilha.append((inicio, 0, None)) 
        
        sucesso = False
        
        while pilha:
            atual, profundidade, pai_do_atual = pilha.pop() 
            
            if atual in self.listaExplorados:
                continue
            if pai_do_atual is not None:
                atual.pai = pai_do_atual
            
            atual.explorado = True
            atual.visto = True
            self.listaExplorados.append(atual)
            self.listaVistos.append(atual)
            
            
            if atual != inicio:
                self.ao_visitar(atual.valor[0], atual.valor[1])
            
            if atual.valor == fim.valor:
                print("Resultado encontrado pelo DFS Limitado!\n")
                sucesso = True
                self.reconstruir_caminho(atual)
                self.pintarFinal()
                break
            
            if profundidade < limite:
                movimentos = [
                    (atual.valor[0], atual.valor[1]+1), # Direita
                    (atual.valor[0]+1, atual.valor[1]), # Baixo
                    (atual.valor[0], atual.valor[1]-1), # Esquerda
                    (atual.valor[0]-1, atual.valor[1])  # Cima
                ]
                # Reverte para manter a prioridade de exploração após o append na pilha
                movimentos.reverse() 
                
                for (l, c) in movimentos:
                    if self.labirinto.eh_posicao_validamover(l, c):
                        vizinho = self.labirinto.pegar_celula(l, c)
                        
                        # Só adicionamos aos ABERTOS (pilha) se ele ainda não foi FECHADO
                        if vizinho not in self.listaExplorados:
                            vizinho.pai = atual 
                            # Adiciona em ABERTOS (Pilha), mas NÃO marca como explorado ainda!
                            pilha.append((vizinho, profundidade + 1, atual))
                        
        if not sucesso:
            print("Fracasso: Caminho não encontrado pelo DFS Limitado.")
        return 0
    
    def reconstruir_caminho(self, no_fim):
        atual = no_fim
        while atual is not None:
            self.listaFinal.append(atual)
            atual = atual.pai
        self.listaFinal.reverse()

    def busca_ordenada(self):
        print("Entrou na Busca Ordenada (Custo Uniforme)")
        
        # ABERTOS: Fila de prioridade. 
        # Formato dos itens: (custo_acumulado, contador_desempate, nó, pai_do_nó)
        abertos = []
        contador = 0 # Usado apenas para desempatar se dois nós tiverem o mesmo custo
        
        self.listaExplorados = [] 
        self.listaVistos = []
        self.listaFinal = [] 
        
        inicio = self.labirinto.inicio
        fim = self.labirinto.fim
        
        inicio.pai = None 
        
        # Insere a raiz. Custo inicial é 0.
        heapq.heappush(abertos, (0, contador, inicio, None))
        
        sucesso = False
        
        # enquanto não fracasso (lista de abertos não vazia)
        while abertos:
            # Retira sempre o nó com o MENOR custo acumulado
            custo_atual, _, atual, pai_do_atual = heapq.heappop(abertos) 
            
            # Se já fechamos esse nó por um caminho mais barato ou igual, ignoramos
            if atual in self.listaExplorados:
                continue
            
            # Registramos o pai vencedor (o que proporcionou o menor custo)
            if pai_do_atual is not None:
                atual.pai = pai_do_atual
            
            # Nó se torna FECHADO
            atual.explorado = True
            atual.visto = True
            self.listaExplorados.append(atual)
            self.listaVistos.append(atual)
            
            if atual != inicio:
                self.ao_visitar(atual.valor[0], atual.valor[1])
            
            # Teste de objetivo
            if atual.valor == fim.valor:
                print("Resultado encontrado pela Busca Ordenada!\n")
                sucesso = True
                self.reconstruir_caminho(atual)
                self.pintarFinal()
                break
            
            # Gerar filhos
            movimentos = [
                (atual.valor[0], atual.valor[1]+1), # Direita
                (atual.valor[0]+1, atual.valor[1]), # Baixo
                (atual.valor[0], atual.valor[1]-1), # Esquerda
                (atual.valor[0]-1, atual.valor[1])  # Cima
            ]
            
            for (l, c) in movimentos:
                if self.labirinto.eh_posicao_validamover(l, c):
                    vizinho = self.labirinto.pegar_celula(l, c)
                    
                    if vizinho not in self.listaExplorados:
                        # O custo do passo para uma casa normal é 1
                        custo_do_passo = 1 
                        novo_custo = custo_atual + custo_do_passo
                        
                        # Incrementa o contador para evitar erro de comparação do Python
                        contador += 1 
                        
                        # Insere o vizinho na fila de prioridade
                        heapq.heappush(abertos, (novo_custo, contador, vizinho, atual))
                        
        if not sucesso:
            print("Fracasso: Caminho não encontrado pela Busca Ordenada.")
        return 0
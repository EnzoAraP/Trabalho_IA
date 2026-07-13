import numpy as np
import sys
import heapq
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modelos.No import No
from modelos.Labirinto import Labirinto



matrizLabirinto = np.zeros((10,10))

class Algoritmos:
    def __init__(self, labirinto, pintar):
        self.labirinto = labirinto
        self.pintar = pintar
        self.listaVisto = []
        self.listaExplorados = []
        self.listaFinal = []
        self.listaExplorados = []
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
            if(atual.regra.get("d")==0 or atual.regra.get("b")==0 or atual.regra.get("e")==0  or atual.regra.get("c")==0 ):
                for direcao,valor in atual.regra.items():
                    if valor==0:
                        atual.regra[direcao] = 1
                        atual=self.movimentacao(atual,direcao)#será igual a ele mesmo se ja o prox ja estiver presente ( não tem o por que reexplora-lo) ou o novo se for um nó novo
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
                    break
                else:
                    self.listaFinal.remove(atual)
                    atual = atual.pai
        dados ={
            "Nós Expandidos":len(self.listaExplorados),
            "Nós Visitados":len(self.listaExplorados),
            "Nós na lista final": len(self.listaFinal),
            "fator de Ramificação":self.labirinto.quantidadeFilhos()/len(self.listaExplorados),
           
        }
        
        return dados   
    
    def pintarFinal(self):
        for no in self.listaFinal:
            no.caminhofinal=True
            self.pintar(no.valor[0],no.valor[1])
            
    def movimentacao(self,Noatual,direcao):#se estiver correto, só será mudado para o novo nó se ele não estiver adicionado na lista, se não retorna o atual.
        print("Entrou no Movimentacao")
        Noatual.regra[direcao]=1
        novovalor=None
        match direcao:
            case "d":# = direita
                novovalor = self.verificapossibilidade(Noatual.valor[0],Noatual.valor[1]+1)
            case "b":#  = baixo
                novovalor = self.verificapossibilidade(Noatual.valor[0]+1,Noatual.valor[1])
            case "e":# = esquerda
                novovalor = self.verificapossibilidade(Noatual.valor[0],Noatual.valor[1]-1)
            case "c":# = cima
                novovalor = self.verificapossibilidade(Noatual.valor[0]-1,Noatual.valor[1])
        print(f"valor novovalor:{novovalor}")
        presentenalista = any(no.valor ==(novovalor) for no in self.listaExplorados)#verifica se o nó com valores novos já está presente na lista de nós
        print(f"estado atual da lista de explorados:{self.listaExplorados}")
    
        if (presentenalista): #caso já esteja na lista de presentes, apenas poe que tal nó é um dos filhos do nó atual
            filho = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
            Noatual.filhos.append(filho)
            print("manterifvivo")
            
        if not presentenalista and novovalor!=None: #caso o nó não esteja presente na lista, ele é criado com o atual sendo o pai e aidiconado na lista de vistos
            filho = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
            Noatual.filhos.append(filho)
            Novono = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
            Novono.pai =Noatual
            Novono.explorado=True
            self.pintar(novovalor[0],novovalor[1])
            self.listaFinal.append(Novono)
            self.listaExplorados.append(Novono)
            return Novono
        return Noatual
    
    
    def movimentacao2(self,Noatual,direcao,listaExplorados):#se estiver correto, só será mudado para o novo nó se ele não estiver adicionado na lista, se não retorna o atual.
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
            self.pintar(novovalor[0],novovalor[1])
            self.listaFinal.append(Novono)
            listaExplorados.append(Novono)
            return Novono
        return Noatual
    def verificapossibilidade(self,valor1,valor2):#novo valor será None se for um valor que não pode ser incluso na lista (out of bounds ou em barreira), e valor1 valor2 se for possível adicionar
        
        if(self.labirinto.eh_posicao_validamover(valor1,valor2)):
            return(valor1,valor2)
        else:
            return(None)
    def manhatan(self,x,y):
         return abs(x -self.labirinto.fim.valor[0]) + abs(y - self.labirinto.fim.valor[1])
    def VerificacaoVistos(self,Noatual,usarlistavizinhos=False):
        for direcao,valor in Noatual.regra.items():
            match direcao:
                case "d":# = direita
                    novovalor = self.verificapossibilidade(Noatual.valor[0],Noatual.valor[1]+1)
                    
                    if(novovalor):
                        heuristica =self.manhatan(novovalor[0],novovalor[1])
                        presentenalistaVistos= any(no.valor ==(novovalor) for no in self.listaVisto)
                        if (presentenalistaVistos): #caso já esteja na lista de presentes, apenas poe que tal nó é um dos filhos do nó atual
                            print("ja presente")
                            filho = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                            Noatual.filhos.append(filho)
                            if(usarlistavizinhos==True):
                                Novono = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                                self.listavizinhosatuais.append(Novono)
                        if not presentenalistaVistos and novovalor!=None: #caso o nó não esteja presente na lista, ele é criado com o atual sendo o pai e aidiconado na lista de vistos
                            
                            Novono = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                            Noatual.filhos.append(Novono)
                            Novono.pai =Noatual
                            Novono.visto=True
                            Novono.heuristica = heuristica
                            self.pintar(novovalor[0],novovalor[1])
                            self.listaVisto.append(Novono)
                            if(usarlistavizinhos==True):
                                self.listavizinhosatuais.append(Novono)
                            print("adicionado na lsitavisto")
                case "b":#  = baixo
                    novovalor = self.verificapossibilidade(Noatual.valor[0]+1,Noatual.valor[1])
                    
                    if(novovalor):
                        heuristica =self.manhatan(novovalor[0],novovalor[1])
                        presentenalistaVistos= any(no.valor ==(novovalor) for no in self.listaVisto)
                        if (presentenalistaVistos): #caso já esteja na lista de presentes, apenas poe que tal nó é um dos filhos do nó atual
                            print("ja presente")
                            filho = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                            Noatual.filhos.append(filho)
                            if(usarlistavizinhos==True):
                                Novono = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                                self.listavizinhosatuais.append(Novono)
                        if not presentenalistaVistos and novovalor!=None: #caso o nó não esteja presente na lista, ele é criado com o atual sendo o pai e aidiconado na lista de vistos
                            
                            Novono = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                            Noatual.filhos.append(Novono)
                            Novono.pai =Noatual
                            Novono.visto=True
                            Novono.heuristica = heuristica
                            
                            self.pintar(novovalor[0],novovalor[1])
                            self.listaVisto.append(Novono)
                            if(usarlistavizinhos==True):
                                self.listavizinhosatuais.append(Novono)
                case "e":# = esquerda
                    novovalor = self.verificapossibilidade(Noatual.valor[0],Noatual.valor[1]-1)
                    
                    if(novovalor):
                        heuristica =self.manhatan(novovalor[0],novovalor[1])
                        presentenalistaVistos= any(no.valor ==(novovalor) for no in self.listaVisto)
                        if (presentenalistaVistos): #caso já esteja na lista de presentes, apenas poe que tal nó é um dos filhos do nó atual
                            print("ja presente")
                            filho = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                            Noatual.filhos.append(filho)
                            if(usarlistavizinhos==True):
                                Novono = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                                self.listavizinhosatuais.append(Novono)
                        if not presentenalistaVistos and novovalor!=None: #caso o nó não esteja presente na lista, ele é criado com o atual sendo o pai e aidiconado na lista de vistos
                            
                            Novono = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                            Noatual.filhos.append(Novono)
                            Novono.pai =Noatual
                            Novono.visto=True
                            Novono.heuristica = heuristica
                            self.pintar(novovalor[0],novovalor[1])
                            self.listaVisto.append(Novono)
                            if(usarlistavizinhos==True):
                                self.listavizinhosatuais.append(Novono)
                case "c":# = cima
                    novovalor = self.verificapossibilidade(Noatual.valor[0]-1,Noatual.valor[1])
                    
                    if(novovalor):
                        heuristica =self.manhatan(novovalor[0],novovalor[1])
                        presentenalistaVistos= any(no.valor ==(novovalor) for no in self.listaVisto)
                        if (presentenalistaVistos): #caso já esteja na lista de presentes, apenas poe que tal nó é um dos filhos do nó atual
                            print("ja presente")
                            filho = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                            Noatual.filhos.append(filho)
                            if(usarlistavizinhos==True):
                                Novono = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                                self.listavizinhosatuais.append(Novono)
                        if not presentenalistaVistos and novovalor!=None: #caso o nó não esteja presente na lista, ele é criado com o atual sendo o pai e aidiconado na lista de vistos
                            
                            Novono = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                            Noatual.filhos.append(Novono)
                            Novono.pai =Noatual
                            Novono.visto=True
                            Novono.heuristica = heuristica
                            print(f"se o valor de novovisitado é true:{Novono.visto}")
                            self.pintar(Novono.valor[0],Novono.valor[1])
                            self.listaVisto.append(Novono)
                            if(usarlistavizinhos==True):
                                self.listavizinhosatuais.append(Novono)
                    
        
    def CaminhoFinal(self):
        tamanhocaminhofinal =0
        noatual= self.labirinto.fim
        while noatual != self.labirinto.inicio:
            noatual.caminhofinal=True
            self.pintar(noatual.valor[0],noatual.valor[1])
            tamanhocaminhofinal=tamanhocaminhofinal+1
            noatual=noatual.pai
        return tamanhocaminhofinal
    def buscagulosa(self):
        print("Entrou na buscagulosa")
        atual= self.labirinto.inicio
        estadoInicial = atual.valor
        estadoFinal = self.labirinto.fim.valor
        listavizinhos = None
        atual.heuristica = self.manhatan(atual.valor[0],atual.valor[1])
        sequenciamento= ("d","b","e","c")
        self.listaVisto.append(atual)
        self.listaExplorados.append(atual)
        fracasso = False
        sucesso = False
        proximo = None
        discarte = None
        tamanhoFinal=None
        print(atual.valor)
        while((not fracasso and not sucesso)):
            self.VerificacaoVistos(atual)
           
            menor = min(
            (no for no in self.listaVisto if no not in self.listaExplorados),
            key=lambda no: no.heuristica,
            default=None
            )
            
            if menor!=None:
                if menor.valor==estadoFinal:
                    sucesso=True
                    print("sucesso")
                    tamanhoFinal=self.CaminhoFinal()
                    break
                menor.explorado=True
                self.pintar(menor.valor[0],menor.valor[1])
                atual=menor
                self.listaExplorados.append(atual)
            else:
                fracasso=True
                print("fracasso")
                break
        dados ={
            "Nós Expandidos":len(self.listaExplorados),
            "Nós Visitados":len(self.listaVisto),
            "Nós na lista final": tamanhoFinal,
            "fator de Ramificação":self.labirinto.quantidadeFilhos()/len(self.listaExplorados),
            
        }
        return dados
    def buscagulosaMateria(self):
        print("Entrou na buscagulosaMateria")
        atual= self.labirinto.inicio
        estadoInicial = atual.valor
        estadoFinal = self.labirinto.fim.valor
        self.listavizinhosatuais = []
        atual.heuristica = self.manhatan(atual.valor[0],atual.valor[1])
        sequenciamento= ("d","b","e","c")
        self.listaVisto.append(atual)
        self.listaExplorados.append(atual)
        fracasso = False
        sucesso = False
        proximo = None
        discarte = None
        
        print(atual.valor)
        while((not fracasso and not sucesso)):
            self.VerificacaoVistos(atual,True)
           
            menor = min(
            (no for no in self.listavizinhosatuais if no not in self.listaExplorados),
            key=lambda no: no.heuristica,
            default=None
            )
            
            if menor!=None:
                if menor.valor==estadoFinal:
                    sucesso=True
                    print("sucesso")
                    self.CaminhoFinal()
                    break
                menor.explorado=True
                self.pintar(menor.valor[0],menor.valor[1])
                atual=menor
                self.listaExplorados.append(atual)
                self.listavizinhosatuais.clear()
            else:
                if atual.valor == estadoInicial:
                    print("Retnou pro pai inicial,erro")
                    fracasso = True
                    break
                else:
                    atual = atual.pai
                    self.listavizinhosatuais.clear()
                    self.VerificacaoVistos(atual, True)
    def buscaLargura(self):
        print("Entrou no backtracking")
        atual= self.labirinto.inicio
        estadoInicial = atual.valor
        estadoFinal = self.labirinto.fim.valor
        self.listaVisto = []
        self.listaExplorados =[]
        sequenciamento= ("d","b","e","c")
        self.listaVisto.append(atual)
        fracasso = False
        sucesso = False
        proximo = None
        tamanhoFinal = None
        print(atual.valor)
        while((not fracasso and not sucesso)):
            if not self.listaVisto:
                print("Fracasso")
                fracasso=True
            else: 
                atual=self.listaVisto.pop(0)
                if atual.valor==estadoFinal:
                    print("Sucesso")
                    sucesso=True
                    tamanhoFinal=self.CaminhoFinal()
                else:
                    if(atual.regra.get("d")==0 or atual.regra.get("b")==0 or atual.regra.get("e")==0  or atual.regra.get("c")==0 ):
                        for direcao,valor in atual.regra.items():
                            if valor==0:
                                atual.regra[direcao] = 1
                                
                                match direcao:
                                    case "d":# = direita
                                        novovalor = self.verificapossibilidade(atual.valor[0],atual.valor[1]+1)
                                    case "b":#  = baixo
                                        novovalor = self.verificapossibilidade(atual.valor[0]+1,atual.valor[1])
                                    case "e":# = esquerda
                                        novovalor = self.verificapossibilidade(atual.valor[0],atual.valor[1]-1)
                                    case "c":# = cima
                                        novovalor = self.verificapossibilidade(atual.valor[0]-1,atual.valor[1])
                                if(novovalor):
                                    novoNo = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                                    if(not novoNo.visto):
                                        novoNo.visto=True
                                        novoNo.pai=atual
                                        atual.filhos.append(novoNo)
                                        self.pintar(novovalor[0],novovalor[1])
                                        self.listaVisto.append(novoNo)
                                    
                    self.listaExplorados.append(atual)
                    atual.explorado=True
                    self.pintar(atual.valor[0],atual.valor[1])
        dados ={
            "Nós Expandidos":len(self.listaExplorados),
            "Nós Visitados":len(self.listaVisto)+len(self.listaExplorados),
            "Nós na lista final": tamanhoFinal,
            "fator de Ramificação":self.labirinto.quantidadeFilhos()/len(self.listaExplorados),
            
        }
        return dados
            
           


    
    def busca_profundidade_limitada(self, limite):
        print("Entrou na Busca em Profundidade Limitada")
        
        pilha = []

        self.listaExplorados = [] 
        self.listaVistos = []
        self.listaFinal = []

        profundidades_visitadas = {}
        
        inicio = self.labirinto.inicio
        fim = self.labirinto.fim
        
        inicio.pai = None

        pilha.append((inicio, 0, None))

        self.listaVistos.append(inicio)
        
        sucesso = False
        
        while pilha:
            atual, profundidade, pai_do_atual = pilha.pop() 
            
            if atual in profundidades_visitadas and profundidades_visitadas[atual] <= profundidade:
                continue

            profundidades_visitadas[atual] = profundidade

            if pai_do_atual is not None:
                atual.pai = pai_do_atual
            
            atual.explorado = True
            self.listaExplorados.append(atual)

            if atual.valor != inicio.valor and atual.valor != fim.valor:
                self.pintar(atual.valor[0], atual.valor[1])
            
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

                        if vizinho not in atual.filhos:
                            atual.filhos.append(vizinho)
                            
                        if vizinho not in self.listaVistos:
                            self.listaVistos.append(vizinho)

                        # Só adicionamos aos ABERTOS (pilha) se ele ainda não foi FECHADO
                        if vizinho not in self.listaExplorados:
                            vizinho.visto = True
                            if vizinho.valor != inicio.valor and vizinho.valor != fim.valor:
                                self.pintar(vizinho.valor[0], vizinho.valor[1])
                                
                            pilha.append((vizinho, profundidade + 1, atual))
                        
        if not sucesso:
            print("Fracasso: Caminho não encontrado pelo DFS Limitado.")
        
        dados = {
            "Nós Expandidos": len(self.listaExplorados),
            "Nós Visitados": len(self.listaVistos),
            "Nós na lista final": len(self.listaFinal),
            "fator de Ramificação": self.labirinto.quantidadeFilhos() / len(self.listaExplorados) if len(self.listaExplorados) > 0 else 0,
        }
        return dados
    
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
        
        self.listaVistos.append(inicio)

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
            self.listaExplorados.append(atual)
            
            if atual.valor != inicio.valor and atual.valor != fim.valor:
                self.pintar(atual.valor[0], atual.valor[1])
            
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

                    if vizinho not in atual.filhos:
                        atual.filhos.append(vizinho)
                        
                    # 2. Correção dos nós visitados
                    if vizinho not in self.listaVistos:
                        self.listaVistos.append(vizinho)
                    
                    if vizinho not in self.listaExplorados:
                        vizinho.visto = True
                        if vizinho.valor != inicio.valor and vizinho.valor != fim.valor:
                            self.pintar(vizinho.valor[0], vizinho.valor[1])
                        # O custo do passo para uma casa normal é 1
                        custo_do_passo = 1 
                        novo_custo = custo_atual + custo_do_passo
                        
                        # Incrementa o contador para evitar erro de comparação do Python
                        contador += 1 
                        
                        # Insere o vizinho na fila de prioridade
                        heapq.heappush(abertos, (novo_custo, contador, vizinho, atual))
                        
        if not sucesso:
            print("Fracasso: Caminho não encontrado pela Busca Ordenada.")
        
        dados = {
            "Nós Expandidos": len(self.listaExplorados),
            "Nós Visitados": len(self.listaVistos),
            "Nós na lista final": len(self.listaFinal),
            "fator de Ramificação": self.labirinto.quantidadeFilhos() / len(self.listaExplorados) if len(self.listaExplorados) > 0 else 0,
        }
        return dados
    
    def busca_a_estrela(self):
        print("Entrou na Busca A* (A-Star)")
        
        import heapq
        
        # ABERTOS: Fila de prioridade. 
        # Formato: (f_score, contador_desempate, g_score, nó, pai_do_nó)
        # Sendo f_score = g_score (custo real) + h_score (heurística)
        abertos = []
        contador = 0
        
        self.listaExplorados = [] 
        self.listaVistos = []
        self.listaFinal = [] 
        
        inicio = self.labirinto.inicio
        fim = self.labirinto.fim
        
        inicio.pai = None 
        
        # O custo inicial (g) é 0. O f_score inicial é 0 + heuristica(inicio)
        g_inicial = 0
        h_inicial = self.manhatan(inicio.valor[0], inicio.valor[1])
        f_inicial = g_inicial + h_inicial
        
        # Insere a raiz na fila
        heapq.heappush(abertos, (f_inicial, contador, g_inicial, inicio, None))
        
        self.listaVistos.append(inicio)

        sucesso = False
        
        while abertos:
            # Retira sempre o nó com o MENOR f_score total
            f_atual, _, g_atual, atual, pai_do_atual = heapq.heappop(abertos)

            h_atual = f_atual - g_atual
            print(f"-> Explorando Nó {atual.valor}: g(n)={g_atual}, h(n)={h_atual}, f(n)={f_atual}")
            
            
            if atual in self.listaExplorados:
                continue
            
            if pai_do_atual is not None:
                atual.pai = pai_do_atual
            
            atual.explorado = True
            self.listaExplorados.append(atual)

            if atual.valor != inicio.valor and atual.valor != fim.valor:
                self.pintar(atual.valor[0], atual.valor[1])
            
            if atual.valor == fim.valor:
                print("Resultado encontrado pela Busca A*!\n")
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

                    if vizinho not in atual.filhos:
                        atual.filhos.append(vizinho)
                        
                    # 2. Correção dos nós visitados
                    if vizinho not in self.listaVistos:
                        self.listaVistos.append(vizinho)
                        
                    
                    if vizinho not in self.listaExplorados:

                        vizinho.visto = True
                        if vizinho.valor != inicio.valor and vizinho.valor != fim.valor:
                            self.pintar(vizinho.valor[0], vizinho.valor[1])
                        # O custo do passo (g) aumenta em 1 em relação ao pai
                        novo_g = g_atual + 1 
                        
                        # Calcula a heurística (h) para o vizinho usando Manhattan
                        h_vizinho = self.manhatan(vizinho.valor[0], vizinho.valor[1])
                        
                        # O novo custo total estimado (f) é a soma dos dois
                        novo_f = novo_g + h_vizinho
                        
                        print(f"   Avaliando Vizinho {vizinho.valor}: g(n)={novo_g}, h(n)={h_vizinho}, f(n)={novo_f}")

                        contador += 1 
                        
                        # Insere o vizinho com a nova prioridade (novo_f)
                        heapq.heappush(abertos, (novo_f, contador, novo_g, vizinho, atual))
                        
        if not sucesso:
            print("Fracasso: Caminho não encontrado pela Busca A*.")
        
        dados = {
            "Nós Expandidos": len(self.listaExplorados),
            "Nós Visitados": len(self.listaVistos),
            "Nós na lista final": len(self.listaFinal),
            "fator de Ramificação": self.labirinto.quantidadeFilhos() / len(self.listaExplorados) if len(self.listaExplorados) > 0 else 0,
        }
        return dados
    
    def busca_ida_estrela(self ,):
        print("Entrou na Busca IDA* (Iterative Deepening A*)")
        
        inicio = self.labirinto.inicio
        fim = self.labirinto.fim
        
        inicio.pai = None

        verdadeiro_inicio = self.labirinto.pegar_celula(inicio.valor[0], inicio.valor[1])
        verdadeiro_inicio.pai = None

        self.listaFinal = []
        total_explorados = 0
        total_visitados = 0

        # O limite inicial é apenas a estimativa (heurística) do início até ao fim
        limite_f = self.manhatan(inicio.valor[0], inicio.valor[1])
        
        while True:
            print(f"\n--- Iniciando iteração IDA* com limite f(n) = {limite_f} ---")
            
            # Limpamos as listas visuais para esta iteração específica
            self.listaExplorados = []
            self.listaVistos = []

            self.listaVistos.append(verdadeiro_inicio)
            
            # Usamos um Set (conjunto) para rastrear o caminho atual e evitar ciclos (loops infinitos)
            caminho_atual = set([verdadeiro_inicio]) 
            
            # Inicia a pesquisa em profundidade recursiva
            sucesso, resultado = self._ida_pesquisa(verdadeiro_inicio, 0, limite_f, caminho_atual, fim)
            
            # Acumula os nós de cada iteração
            total_explorados += len(self.listaExplorados)
            total_visitados += len(self.listaVistos)
            
            if sucesso:
                print("\nResultado encontrado pela Busca IDA*!")
                self.reconstruir_caminho(resultado)
                self.pintarFinal()
                
                dados = {
                    "Nós Expandidos": total_explorados,
                    "Nós Visitados": total_visitados,
                    "Nós na lista final": len(self.listaFinal),
                    "fator de Ramificação": self.labirinto.quantidadeFilhos() / total_explorados if total_explorados > 0 else 0,
                    "Tempo de execução": None
                }
                return dados
            elif resultado == float('inf'):
                print("\nFracasso: Caminho não encontrado pela Busca IDA* (espaço esgotado).")
                
                dados = {
                    "Nós Expandidos": total_explorados,
                    "Nós Visitados": total_visitados,
                    "Nós na lista final": len(self.listaFinal),
                    "fator de Ramificação": self.labirinto.quantidadeFilhos() / total_explorados if total_explorados > 0 else 0,
                }
                return dados
            else:
                # Se não encontrou, o novo limite passa a ser o menor f(n) que ultrapassou o limite anterior
                limite_f = resultado 

    def _ida_pesquisa(self, atual, g_atual, limite_f, caminho_atual, fim):
        # Calcula o f(n) do nó atual
        h_atual = self.manhatan(atual.valor[0], atual.valor[1])
        f_atual = g_atual + h_atual
        
        # Para visualização na interface gráfica
        if atual not in self.listaExplorados:
            atual.explorado = True
            self.listaExplorados.append(atual)

            if atual.valor != self.labirinto.inicio.valor and atual.valor != self.labirinto.fim.valor:
                self.pintar(atual.valor[0], atual.valor[1])
                
        print(f"-> Explorando Nó {atual.valor}: g(n)={g_atual}, h(n)={h_atual}, f(n)={f_atual} (Limite: {limite_f})")
        
        # CORTE: Se o f(n) deste nó exceder o limite atual, paramos de explorar este ramo
        if f_atual > limite_f:
            return (False, f_atual)
            
        if atual.valor == fim.valor:
            return (True, atual)  # Retorna o nó final encontrado
            
        # Variável para rastrear o menor f(n) que excedeu o limite nos filhos
        min_limite_excedido = float('inf')
        
        movimentos = [
            (atual.valor[0], atual.valor[1]+1), # Direita
            (atual.valor[0]+1, atual.valor[1]), # Baixo
            (atual.valor[0], atual.valor[1]-1), # Esquerda
            (atual.valor[0]-1, atual.valor[1])  # Cima
        ]
        
        for (l, c) in movimentos:
            if self.labirinto.eh_posicao_validamover(l, c):
                vizinho = self.labirinto.pegar_celula(l, c)
                
                if vizinho not in atual.filhos:
                    atual.filhos.append(vizinho)
                
                if vizinho not in self.listaVistos:
                    self.listaVistos.append(vizinho)

                # Só exploramos se o vizinho não estiver no caminho atual (evita vai e vem)
                if vizinho not in caminho_atual:
                    vizinho.visto = True
                    if vizinho.valor != self.labirinto.inicio.valor and vizinho.valor != self.labirinto.fim.valor:
                            self.pintar(vizinho.valor[0], vizinho.valor[1])
                    vizinho.pai = atual  # Define o pai do vizinho como o nó atual
                    caminho_atual.add(vizinho)
                    
                    # Chamada recursiva descendo um nível em profundidade (g_atual + 1)
                    sucesso, resultado = self._ida_pesquisa(vizinho, g_atual + 1, limite_f, caminho_atual, fim)
                    
                    if sucesso:
                        return (True, resultado)
                        
                    # Atualizamos o menor limite excedido
                    if resultado < min_limite_excedido:
                        min_limite_excedido = resultado
                        
                    # Backtracking: remove do caminho atual ao retroceder
                    caminho_atual.remove(vizinho)
                    
        return (False, min_limite_excedido)
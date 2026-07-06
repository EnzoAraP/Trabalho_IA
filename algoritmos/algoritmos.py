import numpy as np
import sys
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
            filho = next((no for no in self.listaExplorados if no.valor== novovalor))
            Noatual.filhos.append(filho)
        if not presentenalista and novovalor!=None: #caso o nó não esteja presente na lista, ele é criado com o atual sendo o pai e aidiconado na lista de vistos
            filho = next((no for no in self.listaExplorados if no.valor== novovalor))
            Noatual.filhos.append(filho)
            Novono = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
            Novono.pai =Noatual
            Novono.explorado=True
            self.pintar(novovalor[0],novovalor[1])
            self.listaFinal.append(Novono)
            self.listaExplorados.append(Novono)
            return Novono
        return Noatual
    
    

    def verificapossibilidade(self,valor1,valor2):#novo valor será None se for um valor que não pode ser incluso na lista (out of bounds ou em barreira), e valor1 valor2 se for possível adicionar
        
        if(self.labirinto.eh_posicao_validamover(valor1,valor2)):
            return(valor1,valor2)
        else:
            return(None)
    def manhatan(self,x,y):
         return abs(x -self.labirinto.fim.valor[0]) + abs(y - self.labirinto.fim.valor[1])
    def VerificacaoVistos(self,Noatual):
        for direcao,valor in Noatual.regra.items():
            match direcao:
                case "d":# = direita
                    novovalor = self.verificapossibilidade(Noatual.valor[0],Noatual.valor[1]+1)
                    
                    if(novovalor):
                        heuristica =self.manhatan(novovalor[0],novovalor[1])
                        presentenalistaVistos= any(no.valor ==(novovalor) for no in self.listaVisto)
                        if (presentenalistaVistos): #caso já esteja na lista de presentes, apenas poe que tal nó é um dos filhos do nó atual
                            print("ja presente")
                            #filho = next((no for no in self.listaVisto if no.valor== novovalor))
                            #Noatual.filhos.append(filho)
                        if not presentenalistaVistos and novovalor!=None: #caso o nó não esteja presente na lista, ele é criado com o atual sendo o pai e aidiconado na lista de vistos
                            #filho = next((no for no in self.listaVisto if no.valor== novovalor))
                            #Noatual.filhos.append(filho)
                            Novono = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                            Novono.pai =Noatual
                            Novono.visto=True
                            Novono.heuristica = heuristica
                            self.pintar(novovalor[0],novovalor[1])
                            self.listaVisto.append(Novono)
                            print("adicionado na lsitavisto")
                case "b":#  = baixo
                    novovalor = self.verificapossibilidade(Noatual.valor[0]+1,Noatual.valor[1])
                    
                    if(novovalor):
                        heuristica =self.manhatan(novovalor[0],novovalor[1])
                        presentenalistaVistos= any(no.valor ==(novovalor) for no in self.listaVisto)
                        if (presentenalistaVistos): #caso já esteja na lista de presentes, apenas poe que tal nó é um dos filhos do nó atual
                            print("ja presente")
                            #filho = next((no for no in self.listaVisto if no.valor== novovalor))
                            #Noatual.filhos.append(filho)
                        if not presentenalistaVistos and novovalor!=None: #caso o nó não esteja presente na lista, ele é criado com o atual sendo o pai e aidiconado na lista de vistos
                            #filho = next((no for no in self.listaVisto if no.valor== novovalor))
                            #Noatual.filhos.append(filho)
                            Novono = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                            Novono.pai =Noatual
                            Novono.visto=True
                            Novono.heuristica = heuristica
                            self.pintar(novovalor[0],novovalor[1])
                            self.listaVisto.append(Novono)
                case "e":# = esquerda
                    novovalor = self.verificapossibilidade(Noatual.valor[0],Noatual.valor[1]-1)
                    
                    if(novovalor):
                        heuristica =self.manhatan(novovalor[0],novovalor[1])
                        presentenalistaVistos= any(no.valor ==(novovalor) for no in self.listaVisto)
                        if (presentenalistaVistos): #caso já esteja na lista de presentes, apenas poe que tal nó é um dos filhos do nó atual
                            print("ja presente")
                            #filho = next((no for no in self.listaVisto if no.valor== novovalor))
                            #Noatual.filhos.append(filho)
                        if not presentenalistaVistos and novovalor!=None: #caso o nó não esteja presente na lista, ele é criado com o atual sendo o pai e aidiconado na lista de vistos
                            #filho = next((no for no in self.listaVisto if no.valor== novovalor))
                            #Noatual.filhos.append(filho)
                            Novono = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                            Novono.pai =Noatual
                            Novono.visto=True
                            Novono.heuristica = heuristica
                            self.pintar(novovalor[0],novovalor[1])
                            self.listaVisto.append(Novono)
                case "c":# = cima
                    novovalor = self.verificapossibilidade(Noatual.valor[0]-1,Noatual.valor[1])
                    
                    if(novovalor):
                        heuristica =self.manhatan(novovalor[0],novovalor[1])
                        presentenalistaVistos= any(no.valor ==(novovalor) for no in self.listaVisto)
                        if (presentenalistaVistos): #caso já esteja na lista de presentes, apenas poe que tal nó é um dos filhos do nó atual
                            print("ja presente")
                            #filho = next((no for no in self.listaVisto if no.valor== novovalor))
                            #Noatual.filhos.append(filho)
                        if not presentenalistaVistos and novovalor!=None: #caso o nó não esteja presente na lista, ele é criado com o atual sendo o pai e aidiconado na lista de vistos
                            #filho = next((no for no in self.listaVisto if no.valor== novovalor))
                            #Noatual.filhos.append(filho)
                            Novono = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
                            Novono.pai =Noatual
                            Novono.visto=True
                            Novono.heuristica = heuristica
                            print(f"se o valor de novovisitado é true:{Novono.visto}")
                            self.pintar(Novono.valor[0],Novono.valor[1])
                            self.listaVisto.append(Novono)
                    
        
    def CaminhoFinal(self):
        noatual= self.labirinto.fim
        while noatual != self.labirinto.inicio:
            noatual.caminhofinal=True
            self.pintar(noatual.valor[0],noatual.valor[1])
            noatual=noatual.pai
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
                    self.CaminhoFinal()
                    break
                menor.explorado=True
                self.pintar(menor.valor[0],menor.valor[1])
                atual=menor
                self.listaExplorados.append(atual)
            else:
                fracasso=True
                print("fracasso")
                break
        


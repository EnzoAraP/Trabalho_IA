import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modelos.No import No
from modelos.Labirinto import Labirinto


matrizLabirinto = np.zeros((10,10))

class Algoritmos:
    def __init__(self, labirinto, ao_visitar):
        self.labirinto = labirinto
        self.ao_visitar = ao_visitar
    def backtracking(self):
        print("Entrou no backtracking")
        atual= self.labirinto.inicio
        estadoInicial = atual.valor
        estadoFinal = self.labirinto.fim.valor
        listaVisto = []
        self.listaFinal = []
        sequenciamento= ("d","b","e","c")
        listaVisto.append(atual)
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
                        atual=self.movimentacao(atual,direcao,listaVisto)#será igual a ele mesmo se ja o prox ja estiver presente ( não tem o por que reexplora-lo) ou o novo se for um nó novo
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
            
    def movimentacao(self,Noatual,direcao,listaVisto):#se estiver correto, só será mudado para o novo nó se ele não estiver adicionado na lista, se não retorna o atual.
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
        presentenalista = any(no.valor ==(novovalor) for no in listaVisto)#verifica se o nó com valores novos já está presente na lista de nós
        print(f"estado atual da lista de vistos:{listaVisto}")
    
        if (presentenalista): #caso já esteja na lista de presentes, apenas poe que tal nó é um dos filhos do nó atual
            filho = next((no for no in listaVisto if no.valor== novovalor))
            Noatual.filhos.append(filho)
        if not presentenalista and novovalor!=None: #caso o nó não esteja presente na lista, ele é criado com o atual sendo o pai e aidiconado na lista de vistos
            Novono = self.labirinto.pegar_celula(novovalor[0],novovalor[1])
            Novono.pai =Noatual
            Novono.visto=True
            self.ao_visitar(novovalor[0],novovalor[1])
            self.listaFinal.append(Novono)
            listaVisto.append(Novono)
            return Novono
        return Noatual
    
    
        return 0

    def verificapossibilidade(self,valor1,valor2):#novo valor será None se for um valor que não pode ser incluso na lista (out of bounds ou em barreira), e valor1 valor2 se for possível adicionar
        print("Entrou no verificacao")
        if(self.labirinto.eh_posicao_validamover(valor1,valor2)):
            return(valor1,valor2)
        else:
            return(None)
    


import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modelos.No import No
from modelos.Labirinto import Labirinto

matrizLabirinto = np.zeros((10,10))


def backtracking(labirinto):
    
    atual= labirinto.inicio
    estadoInicial = atual.valor
    estadoFinal = labirinto.final.valor
    listaVisto = [] 
    sequenciamento= ("d","b","e","c")
    listaVisto.append(atual)
    fracasso = False
    sucesso = False
    proximo = None
    while((fracasso or sucesso)):
        if(atual.regra.get("d")==0 or atual.regra.get("b")==0 or atual.regra.get("e")==0  or atual.regra.get("c")==0 ):
            for direcao,valor in atual.regra:
                if valor==0:
                    atual.regra[direcao] = 1
                    atual=movimentacao(labirinto,atual,direcao,listaVisto)#será igual a ele mesmo se ja o prox ja estiver presente ( não tem o por que reexplora-lo) ou o novo se for um nó novo
                    break
            if(atual.valor == estadoFinal):
                print("Resultado encontrado!\n")
                sucesso=True
                break
        else:
            if atual.valor == estadoInicial:
                fracasso = True
            else:
                atual = atual.pai             
    return 0
def movimentacao(labirinto,Noatual,direcao,listaVisto,modo):#se estiver correto, só será mudado para o novo nó se ele não estiver adicionado na lista, se não retorna o atual.
    Noatual.regra[direcao]=1
    novovalor=None
    match direcao:
        case "d":
            novovalor = verificapossibilidade(labirinto,Noatual.valor[0],Noatual.valor[1]+1)
        case "b":
            novovalor = verificapossibilidade(labirinto,Noatual.valor[0]+1,Noatual.valor[1])
        case "e":
            novovalor = verificapossibilidade(labirinto,Noatual.valor[0],Noatual.valor[1]-1)
        case "c":
            novovalor = verificapossibilidade(labirinto,Noatual.valor[0],Noatual.valor[1]-1)
    
    presentenalista = any(no.valor ==(novovalor) for no in listaVisto)#verifica se o nó com valores novos já está presente na lista de nós
    
    if (presentenalista): #caso já esteja na lista de presentes, apenas poe que tal nó é um dos filhos do nó atual
        filho = next((no for no in listaVisto if no.valor== novovalor))
        Noatual.filhos.append(filho)
    if not presentenalista and novovalor!=None: #caso o nó não esteja presente na lista, ele é criado com o atual sendo o pai e aidiconado na lista de vistos
        Novono = labirinto.pegar_celula(novovalor[0],novovalor[1])
        Novono.pai =Noatual
        listaVisto.append(Novono)
        return Novono
    return Noatual
    
    
    return 0

def verificapossibilidade(labirinto,valor1,valor2):#novo valor será None se for um valor que não pode ser incluso na lista (out of bounds ou em barreira), e valor1 valor2 se for possível adicionar
    
    if(labirinto.eh_posicao_validamover(valor1,valor2)):
        return(None)
    else:
        return(valor1,valor2)
    


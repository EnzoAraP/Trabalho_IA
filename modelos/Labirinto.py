from modelos.No import No
class Labirinto:
    def __init__(self,linha,coluna):
        self.linhas=linha
        self.colunas=coluna
        self.inicio = None
        self.fim = None
        self.matriz = [
            [No((i,j),None) for j in range(self.colunas)]
            for i in range(self.linhas)
        ]
    def pegar_celula(self,linha,coluna):
        return self.matriz[linha][coluna]
    
    
    def mudar_tipo(self,linha,coluna,tipo):
        celula = self.pegar_celula(linha, coluna)
        if tipo == "inicio":
            if self.inicio:
                self.inicio.estado = "vazio"

            self.inicio = celula

        elif tipo == "fim":
            if self.fim:
                self.fim.estado = "vazio"
            if (self.inicio==celula):
                self.inicio =None
                
            self.fim = celula

        celula.estado = tipo
    
    def eh_posicao_validamover(self,linha,coluna):
        print(f"valor linha {linha},valor coluna {coluna}")
        print(0<= linha <self.linhas and 0 <= coluna  < self.colunas )
        if(not(0<= linha <self.linhas and 0 <= coluna  < self.colunas) ):
            return False
        print(self.eh_parede(linha,coluna))
        if(self.eh_parede(linha,coluna)):
            return False
        return True
    def quantidadeFilhos(self):
        quantidadetotal=0
        for i in range (self.linhas):
            for j in range (self.colunas):
                no = self.matriz[i][j]
                quantidade =len(no.filhos)
                quantidadetotal =quantidadetotal + quantidade
        return quantidadetotal
    def eh_posicao_validaparede(self,linha,coluna):
        return 0<= linha <self.linhas and 0 <= coluna <=coluna < self.colunas
    def eh_parede(self,linha,coluna):
        return self.matriz[linha][coluna].estado == "parede"
    def limpar_labirinto(self,limpartudo):
        self.inicio =None
        self.fim=None
        for i in range(self.linhas):
            for j in range(self.colunas):
                no = self.matriz[i][j]
                no.pai = None
                no.visto =False
                no.explorado = False
                no.caminhofinal=False
                no.filhos.clear()
                no.heuristica= None
                if(limpartudo):
                    no.estado = "vazio"
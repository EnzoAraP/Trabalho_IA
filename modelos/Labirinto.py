from modelos.No import No
class Labirinto:
    def __init__(self):
        self.linhas=10
        self.colunas=10
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
        if(self.eh_parede(linha,coluna)=="parede"):
            return False
        return 0<= linha <self.linhas and 0 <= coluna <=coluna < self.colunas
    def eh_posicao_validaparede(self,linha,coluna):
        return 0<= linha <self.linhas and 0 <= coluna <=coluna < self.colunas
    def eh_parede(self,linha,coluna):
        return self.matriz[linha][coluna].estado == "parede"
    
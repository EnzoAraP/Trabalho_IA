class No:
    def __init__(self,tupla,pai):
        self.estado = "vazio" #vazio,parede,inicio,fim
        self.valor =tupla
        self.pai = pai
        self.regra={"d":0,
                     "b":0,
                     "e":0,
                     "c":0}
        self.heuristica=None
        self.visto= False
        self.explorado =False
        self.caminhofinal = False
        self.filhos = []
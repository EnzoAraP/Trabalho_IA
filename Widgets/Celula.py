from PyQt6.QtWidgets import QFrame
class Celula(QFrame):
    def __init__(self):
        super().__init__()
        self.cor = "white"
        self.border = "black"
        self.setFixedSize(45, 45)
        self.atualizar()
    def atualizar(self):
        self.setStyleSheet(f"""
            background-color: {self.cor};
            border: 1px solid {self.border};
        """)
    def setCor(self,cor):
        self.cor=cor
        self.atualizar()
    def setBorder(self,border):
        self.border=border
        self.atualizar()   
    
        
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton,QMenu, QLabel,QLineEdit,QVBoxLayout,QGridLayout,QHBoxLayout
from PyQt6.QtGui import QIcon,QFont,QPixmap,QPainter
from PyQt6.QtCore import QSize,Qt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modelos.No import No
from modelos.Labirinto import Labirinto
class Janela(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trabalho de Ia")
        
        self.setGeometry(500,500,800,600)
        self.labirinto =Labirinto()
        linha_botoes  = []
     
        
        tabwidget = QWidget()
        tab = QHBoxLayout(tabwidget)
        button = QPushButton("Algoritmo atual")
        button.setFixedHeight(50)
        button.setFont(QFont("arial",14))
        button.setIconSize(QSize(130,130))
        #popup menu
        menu =QMenu()
        menu.addAction("Backtracking")
        menu.addAction("Busca em Largura")
        menu.addAction("Busca em Profundidade (Limitada)")
        menu.addAction("Busca Ordenada")
        menu.addAction("Busca Gulosa;")
        menu.addAction("Busca A*")
        menu.addAction("Busca IDA*")
        button.setMenu(menu)
        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        Iniciar = QPushButton("Iniciar")
        Iniciar.setFixedHeight(50)
        Iniciar.setFixedWidth(70)
        tab.addWidget(button)
        tab.addWidget(Iniciar)
        self.botoes = []

        for linha in range(10):
            linha_botoes = []

            for coluna in range(10):
                botao = QPushButton("")
                botao.setFixedSize(45, 45)

                botao.clicked.connect(
                    lambda _, l=linha, c=coluna: self.clicar_celula(l, c)
                )

                grid.addWidget(botao, linha, coluna)
                linha_botoes.append(botao)

            self.botoes.append(linha_botoes)
        layout_principal = QVBoxLayout()
        layout_principal.addWidget(tabwidget)      # botão em cima
        layout_principal.addWidget(grid_widget) # grid embaixo
        self.setLayout(layout_principal)
        
        
        
        
        
    def clicar_celula(self, linha, coluna):
        match self.labirinto.pegar_celula(linha,coluna).estado:
            case "vazio":
                self.labirinto.pegar_celula(linha,coluna).estado = "parede"
            case "parede":
                self.labirinto.pegar_celula(linha,coluna).estado = "inicio"
            case "inicio":
                self.labirinto.pegar_celula(linha,coluna).estado = "fim"
            case "fim":
                self.labirinto.pegar_celula(linha,coluna).estado = "vazio"
                
        self.atualizar_botao(linha, coluna)
    def atualizar_botao(self, linha, coluna):
        celula = self.labirinto.pegar_celula(linha, coluna)
        botao = self.botoes[linha][coluna]

        cores = {
            "vazio": "white",
            "parede": "gray",
            "inicio": "green",
            "fim": "red",
            "visitado": "lightblue",
            "caminho": "yellow",
        }

        botao.setStyleSheet(
            f"background-color: {cores[celula.estado]}; border: 1px solid black;"
        )
        
        
app = QApplication(sys.argv)
janela = Janela()
janela.show()
sys.exit(app.exec())
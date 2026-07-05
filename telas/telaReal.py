from PyQt6.QtWidgets import QApplication, QWidget, QPushButton,QMenu, QLabel,QLineEdit,QVBoxLayout,QGridLayout,QHBoxLayout,QStackedWidget,QFrame
from PyQt6.QtGui import QIcon,QFont,QPixmap,QPainter
from PyQt6.QtCore import QSize,Qt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modelos.No import No
from modelos.Labirinto import Labirinto
from Widgets.Celula import Celula
class Janela(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trabalho de Ia")
        self.algoritmo = None
        self.setGeometry(500,500,800,600)
        self.labirinto =Labirinto()
        self.stack =QStackedWidget()
        
        
        #pagina1
        pagina1=QWidget()
        layout1 = QVBoxLayout(pagina1)
        linha_botoes  = []
        tabwidget_inicio = QWidget()
        tab = QHBoxLayout(tabwidget_inicio)
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
        grid_botoes = QWidget()
        grid = QGridLayout(grid_botoes)
        Iniciar = QPushButton("Iniciar")
        Iniciar.setFixedHeight(50)
        Iniciar.setFixedWidth(70)
        Iniciar.clicked.connect(
                    lambda _,:self.clicar_iniciar()
                )
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
        layout1.addWidget(tabwidget_inicio)
        layout1.addWidget(grid_botoes)
        #pagina2
        self.pagina2=QWidget()
        layout2 = QVBoxLayout(self.pagina2)
        layout2.setSpacing(0)
        layout2.setContentsMargins(0, 0, 0, 0)
        tabwidget_fim = QWidget()
        tabnovo = QHBoxLayout(tabwidget_fim)
        frame=QFrame()
        frame.setStyleSheet("background-color: white; border: 1px solid black;")
        frame.setFixedHeight(50)
        Calcular = QPushButton("Calcular")
        Calcular.setFixedHeight(50)
        Calcular.setFixedWidth(70)
        tabnovo.addWidget(frame)
        tabnovo.addWidget(Calcular)
        self.quadrados =[]
        grid_quadrados = QWidget()
        grid_quadrados.setFixedSize(450, 450)
        print(grid_quadrados.size())
        grid2 = QGridLayout(grid_quadrados)
        grid2.setSpacing(0)
        grid2.setContentsMargins(0, 0, 0, 0)
        for linha1 in range(10):
            linha_quadrados = []

            for coluna1 in range(10):
                celula = Celula()
                celula.atualizar()
                grid2.addWidget(celula, linha1, coluna1)
                linha_quadrados.append(celula)
        
        layout2.addWidget(tabwidget_fim)
        layout2.addWidget(
    grid_quadrados,
    alignment=Qt.AlignmentFlag.AlignCenter
)
        
        self.stack.addWidget(pagina1)
        self.stack.addWidget(self.pagina2)
        self.layout_principal = QVBoxLayout()
        self.layout_principal.addWidget(self.stack)
        self.setLayout(self.layout_principal)
        
        
        
        
        
    def clicar_celula(self, linha, coluna):
        estadosalvo = None
        match self.labirinto.pegar_celula(linha,coluna).estado:
            
            case "vazio":
                self.labirinto.mudar_tipo(linha,coluna,"parede")
            case "parede":
                if(self.labirinto.inicio):
                    estadosalvo = self.labirinto.inicio
                self.labirinto.mudar_tipo(linha,coluna,"inicio")
                
            case "inicio":
                if(self.labirinto.fim):
                    estadosalvo = self.labirinto.fim
                self.labirinto.mudar_tipo(linha,coluna,"fim")
                
            case "fim":
                self.labirinto.mudar_tipo(linha,coluna,"vazio")
                
        self.atualizar_botao(linha, coluna,estadosalvo)
 
        
        
        
    def atualizar_botao(self, linha, coluna,estadosalvo):
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
        if(estadosalvo):
            x =estadosalvo.valor[0]
            y = estadosalvo.valor[1]
            botaoatt= self.botoes[x][y]
            botaoatt.setStyleSheet(
            f"background-color: {cores[estadosalvo.estado]}; border: 1px solid black;"
        )
       
       
    def clicar_iniciar(self):
        if(self.labirinto.inicio and self.labirinto.fim):
            self.stack.setCurrentWidget(self.pagina2)
        
app = QApplication(sys.argv)
janela = Janela()
janela.show()
sys.exit(app.exec())
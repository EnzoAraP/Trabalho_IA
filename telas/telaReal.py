from PyQt6.QtWidgets import QApplication, QWidget, QPushButton,QMenu, QLabel,QLineEdit,QVBoxLayout,QGridLayout,QHBoxLayout,QStackedWidget,QFrame
from PyQt6.QtGui import QIcon,QFont,QPixmap,QPainter
from PyQt6.QtCore import QSize,Qt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modelos.No import No
from modelos.Labirinto import Labirinto
from Widgets.Celula import Celula
from algoritmos.algoritmos import Algoritmos
class Janela(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trabalho de Ia")
        
        self.setGeometry(500,500,800,600)
        self.labirinto =Labirinto()
        self.stack =QStackedWidget()
        self.liberado=False
        self.algoritmo = Algoritmos(self.labirinto,self.atualizar_quadrado)
        #pagina1
        pagina1=QWidget()
        layout1 = QVBoxLayout(pagina1)
        linha_botoes  = []
        tabwidget_inicio = QWidget()
        tab = QHBoxLayout(tabwidget_inicio)
        self.button = QPushButton("Algoritmo atual")
        self.button.setFixedHeight(50)
        self.button.setFont(QFont("arial",14))
        self.button.setIconSize(QSize(130,130))
        #popup menu
        menu =QMenu()
        backtracking = menu.addAction("Backtracking")
        buscaLarg = menu.addAction("Busca em Largura")
        Profindidade = menu.addAction("Busca em Profundidade (Limitada)")
        ordenada = menu.addAction("Busca Ordenada")
        gulosa =menu.addAction("Busca Gulosa;")
        a =menu.addAction("Busca A*")
        ida =menu.addAction("Busca IDA*")
        gulosamateria=menu.addAction("Busca Gulosa por vizinhos")
        backtracking.triggered.connect(lambda: self.menu("backtracking"))
        buscaLarg.triggered.connect(lambda: self.menu("buscaLarg"))
        Profindidade.triggered.connect(lambda: self.menu("Profindidade"))
        ordenada.triggered.connect(lambda: self.menu("ordenada"))
        gulosa.triggered.connect(lambda: self.menu("gulosa"))
        a.triggered.connect(lambda: self.menu("a"))
        ida.triggered.connect(lambda: self.menu("ida"))
        gulosamateria.triggered.connect(lambda: self.menu("gulosaMateria"))
        self.button.setMenu(menu)
        grid_botoes = QWidget()
        grid = QGridLayout(grid_botoes)
        Iniciar = QPushButton("Iniciar")
        Iniciar.setFixedHeight(50)
        Iniciar.setFixedWidth(70)
        Iniciar.clicked.connect(
                    lambda _,:self.clicar_iniciar()
                )
        tab.addWidget(self.button)
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
        layoutFrame = QVBoxLayout(frame)
        self.labelFrame = QLabel("Erro")
        self.labelFrame .setAlignment(Qt.AlignmentFlag.AlignCenter)
        Calcular = QPushButton("Calcular")
        Calcular.clicked.connect(
                    lambda _,:self.clicar_calcular()
                )
        layoutFrame.addWidget(self.labelFrame)
        Calcular.setFixedHeight(50)
        Calcular.setFixedWidth(70)
        
        tabnovo.addWidget(frame)
        tabnovo.addWidget(Calcular)
        self.quadrados =[]
        grid_quadrados = QWidget()
        grid_quadrados.setFixedSize(450, 450)
       
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
            self.quadrados.append(linha_quadrados)
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
    def atualizar_quadrado(self,linha,coluna):
        print("entrouaqui")
        celula = self.labirinto.pegar_celula(linha, coluna)
        quadrado = self.quadrados[linha][coluna]
        if(celula.visto==True):
            print(f"visto true do {linha},{coluna}")
            quadrado.setStyleSheet("background-color: lightblue; border: 1px solid black;")
        if(celula.explorado ==True):
            quadrado.setStyleSheet("background-color: DarkGreen; border: 1px solid black;")
        if(celula.caminhofinal==True):
            quadrado.setStyleSheet("background-color: yellow; border: 1px solid black;")
        
        
    def menu(self,escolha):
        
        match escolha:
            case "backtracking":
                self.button.setText("Backtracking")
                self.labelFrame.setText("Backtracking")
                self.liberado=True
            case "buscaLarg":
                self.button.setText("Busca em Largura")
                self.labelFrame.setText("Busca em Largura")
                self.liberado=True
            case "Profindidade":
                self.button.setText("Busca em Profundidade (Limitada)")
                self.labelFrame.setText("Busca em Profundidade (Limitada)")
                self.liberado=True
            case "ordenada":
                self.button.setText("Busca Ordenada")
                self.labelFrame.setText("Busca Ordenada")
                self.liberado=True
            case "gulosa":
                self.button.setText("Busca Gulosa")
                self.labelFrame.setText("Busca Gulosa")
                self.liberado=True
            case "a":
                self.button.setText("Busca A*")
                self.labelFrame.setText("Busca A*")
                self.liberado=True
            case "ida":
                self.button.setText("Busca IDA")
                self.labelFrame.setText("Busca IDA")
                self.liberado=True
            case "gulosaMateria":
                a = self.labirinto.pegar_celula(6, 9)
                b = self.labirinto.pegar_celula(6, 9)

                print(a is b)
                self.button.setText("Busca Gulosa por vizinhos")
                self.labelFrame.setText("Busca Gulosa por vizinhos")
                self.liberado=True
                
    def clicar_iniciar(self):
        cores = {
            "vazio": "white",
            "parede": "gray",
            "inicio": "green",
            "fim": "red",
            "visitado": "lightblue",
            "caminho": "yellow",
        }
        if(self.labirinto.inicio and self.labirinto.fim and self.liberado):
            for i in range (0,10):
                for j in range (0,10):
                    match self.labirinto.pegar_celula(i,j).estado:
                        case("parede"):
                            self.quadrados[i][j].setStyleSheet("background-color: gray; border: 1px solid black;")
                        case("inicio"):
                            self.quadrados[i][j].setStyleSheet("background-color: green; border: 1px solid black;")
                        case("fim"):
                            self.quadrados[i][j].setStyleSheet("background-color: red; border: 1px solid black;")
            self.stack.setCurrentWidget(self.pagina2)      
    def clicar_calcular(self):
        match self.labelFrame.text():
            case "Backtracking":
                self.algoritmo.backtracking()
            case "Busca em Largura":
                self.algoritmo.buscaLargura()
            case "Busca em Profundidade (Limitada)":
                nada= None
            case "Busca Ordenada":
                nada= None
            case "Busca Gulosa":
                self.algoritmo.buscagulosa()
            case "Busca A*":
                nada= None
            case "Busca IDA":
                nada= None
            case "Busca Gulosa por vizinhos":
                self.algoritmo.buscagulosaMateria()
                
                            
        
app = QApplication(sys.argv)
janela = Janela()
janela.show()
sys.exit(app.exec())
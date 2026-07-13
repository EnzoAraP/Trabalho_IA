from PyQt6.QtWidgets import QApplication, QWidget, QPushButton,QMenu, QLabel,QLineEdit,QVBoxLayout,QGridLayout,QHBoxLayout,QStackedWidget,QFrame,QMessageBox
from PyQt6.QtGui import QIcon,QFont,QPixmap,QPainter
from PyQt6.QtCore import QSize,Qt
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modelos.No import No
from modelos.Labirinto import Labirinto
from Widgets.Celula import Celula
from algoritmos.algoritmos import Algoritmos
class Janela(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trabalho de Ia")
        self.dicionarioResposta= None
        self.setGeometry(500,500,800,600)
        self.linhas=None
        self.colunas=None
        self.stack =QStackedWidget()
        self.interacoes=None
        self.liberado=False
        #pagina 0,seleção do tamanho do labirinto e quantidade de interações.
        pagina0 =QWidget()
        layoutInicio=QVBoxLayout(pagina0)
        frameInicio=QFrame()
        frameInicio.setStyleSheet("background-color: white; border: 1px solid black;")
        frameInicio.setFixedHeight(50)
        layoutFrame = QVBoxLayout(frameInicio)
        labelFrameInicio = QLabel("Escolha o tamanho do labirinto(linhas, colunas) e quantas interações deseja realizar")
        labelFrameInicio .setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutFrame.addWidget(labelFrameInicio)
        
        self.botaoLC = QPushButton("Tamanho do Labirinto:")
        menuLC = QMenu()
        dezXdez = menuLC.addAction("10x10")
        vinteXvinte = menuLC.addAction("20x20")
        vintecincoXvintecinco = menuLC.addAction("25x25")
        
        dezXdez.triggered.connect(lambda: self.menuInicial(10))
        vinteXvinte.triggered.connect(lambda: self.menuInicial(20))
        vintecincoXvintecinco.triggered.connect(lambda: self.menuInicial(25))
        self.botaoLC.setMenu(menuLC)
        
        self.botaoInteracoes = QPushButton("Quantidade de interações")
        menuInteracoes = QMenu()
        unica = menuInteracoes.addAction("Única - Visualizando")
        dezInt = menuInteracoes.addAction("Dez iterações sem visualização")
        unica.triggered.connect(lambda: self.menuInicial(1))
        dezInt.triggered.connect(lambda: self.menuInicial(100))
        self.botaoInteracoes.setMenu(menuInteracoes )
        
        botaoIniciar = QPushButton("Iniciar")
        botaoIniciar
        botaoIniciar.clicked.connect(
                    lambda _,:self.clicar_Formacao()
                )
        layoutInicio.addWidget(frameInicio)
        layoutInicio.addWidget(self.botaoLC)
        layoutInicio.addWidget(self.botaoInteracoes)
        layoutInicio.addWidget(botaoIniciar)
        
        
        
        #inicialização labirinto e algoritmo
        
        
        #pagina1
       
        #pagina2
        
        self.stack.addWidget(pagina0)
        
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
 
        
    def criar_labirinto(self):
        self.labirinto =Labirinto(self.linhas,self.colunas)
        self.algoritmo = Algoritmos(self.labirinto,self.atualizar_quadrado)
        
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
        
        celula = self.labirinto.pegar_celula(linha, coluna)
        quadrado = self.quadrados[linha][coluna]
        if(celula.visto==True):
            print(f"visto true do {linha},{coluna}")
            quadrado.setStyleSheet("background-color: lightblue; border: 1px solid black;")
        if(celula.explorado ==True):
            quadrado.setStyleSheet("background-color: DarkGreen; border: 1px solid black;")
        if(celula.caminhofinal==True):
            quadrado.setStyleSheet("background-color: yellow; border: 1px solid black;")
    def criar_pagina1(self):
        self.pagina1=QWidget()
        layout1 = QVBoxLayout(self.pagina1)
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
        print(f"vai gerar com valor de {self.linhas}")
        for linha in range(self.linhas):
            linha_botoes = []

            for coluna in range(self.colunas):
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
    def telaVisualizacao(self):
        teste=False
    def criar_pagina2(self):
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
        grid_quadrados.setFixedSize(self.linhas*45,self.colunas*45)
       
        grid2 = QGridLayout(grid_quadrados)
        grid2.setSpacing(0)
        grid2.setContentsMargins(0, 0, 0, 0)
        for linha1 in range(self.linhas):
            linha_quadrados = []

            for coluna1 in range(self.colunas):
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
    def menuInicial (self,escolha):
        match escolha:
            case 1:
                self.botaoInteracoes.setText("Iteração Única - Visualizando")
                self.interacoes=1
            case 10:
                self.botaoLC.setText("Labirinto 10x10")
                self.linhas=10
                self.colunas=10
            case 20:
                self.botaoLC.setText("Labirinto 20x20")
                self.linhas=20
                self.colunas=20
            case 25:
                self.botaoLC.setText("Labirinto 25x25")
                self.linhas=25
                self.colunas=25
            case 100:
                self.botaoInteracoes.setText("Dez interações sem visualização")
                self.interacoes=10
    def clicar_Formacao(self):
        if(self.linhas and self.colunas and self.interacoes):
            self.criar_labirinto()
            self.criar_pagina1()
            self.criar_pagina2()
            self.stack.addWidget(self.pagina1)
            self.stack.addWidget(self.pagina2)
            self.stack.setCurrentWidget(self.pagina1)
    

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
            for i in range (0,self.linhas):
                for j in range (0,self.colunas):
                    match self.labirinto.pegar_celula(i,j).estado:
                        case("parede"):
                            self.quadrados[i][j].setStyleSheet("background-color: gray; border: 1px solid black;")
                        case("inicio"):
                            self.quadrados[i][j].setStyleSheet("background-color: green; border: 1px solid black;")
                        case("fim"):
                            self.quadrados[i][j].setStyleSheet("background-color: red; border: 1px solid black;")
            self.stack.setCurrentWidget(self.pagina2)      
    def clicar_calcular(self):
        if(self.interacoes==1):
            inicio = time.perf_counter()
            self.executar()
            fim = time.perf_counter()
            tempo = fim - inicio
            self.mostrar_tempo(tempo)     
        else:
            self.dezInteracoes()
    def executar(self):
        match self.labelFrame.text():
                case "Backtracking":
                    nada=self.algoritmo.backtracking()
                    return nada
                case "Busca em Largura":
                    nada=self.algoritmo.buscaLargura()
                    return nada
                case "Busca em Profundidade (Limitada)":
                    dados = self.algoritmo.busca_profundidade_limitada(5)
                    return dados
                case "Busca Ordenada":
                    dados = self.algoritmo.busca_ordenada()
                    return dados
                case "Busca Gulosa":
                    nada=self.algoritmo.buscagulosa()
                    return nada
                case "Busca A*":
                    dados = self.algoritmo.busca_a_estrela()
                    return dados
                case "Busca IDA":
                    dados = self.algoritmo.busca_ida_estrela()
                    return dados
                    
    def dezInteracoes(self):
        tempos =[]
        ListatamanhoVistos=[]
        ListatamanhoExplorados=[]
        listatamanhoFinais=[]
        listaRamificacao=[]
        
        for i in range(10):
            self.labirinto.limpar_labirinto(False)
            self.algoritmo = Algoritmos(self.labirinto,self.atualizar_quadrado)
            inicio = time.perf_counter()
            dado=self.executar()
            ListatamanhoVistos.append(dado["Nós Visitados"])
            ListatamanhoExplorados.append(dado["Nós Expandidos"])
            listatamanhoFinais.append(dado["Nós na lista final"])
            listaRamificacao.append(dado["fator de Ramificação"])
            fim = time.perf_counter()
            tempo = fim - inicio
            tempos.append(tempo)
            tempototal = sum(tempos)
            
            print("Tempos:",tempos)
        mediatempo = sum(tempos)/len(tempos)
        mediaVistos= sum(ListatamanhoVistos)/len(ListatamanhoVistos)
        mediaExplorados= sum(ListatamanhoExplorados)/len(ListatamanhoExplorados)
        mediaFinais= sum(listatamanhoFinais)/len(listatamanhoFinais)
        mediaRamificacao= sum(listaRamificacao)/len(listaRamificacao)
        dados={
            "Tempo de execução":mediatempo,
            "Nós Visitados":mediaVistos,
            "Nós Expandidos":mediaExplorados,
            "Nós na lista final":mediaFinais,
            "fator de Ramificação":mediaRamificacao
        }
        self.mostrar_dados(dados)
        
            
            
        
    def mostrar_dados(self,dados):
        msg = QMessageBox(self)
        msg.setWindowTitle("Resultado")
        msg.setText(f"As 10 iterações duraram em média {dados["Tempo de execução"]:.4f} segundos, foram visitados em média {dados["Nós Visitados"]} nós,foram explorados em média {dados["Nós Expandidos"]} nós, em média tiveram {dados["Nós na lista final"]} nós na lista final, e uma média de ramificação de {dados["fator de Ramificação"]:.4f}.")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()           
    def mostrar_tempo(self, tempo):
        msg = QMessageBox(self)
        msg.setWindowTitle("Resultado")
        msg.setText(f"O algoritmo levou {tempo:.4f} segundos.")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()           
    
          
    
app = QApplication(sys.argv)
janela = Janela()
janela.show()
sys.exit(app.exec())
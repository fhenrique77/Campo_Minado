import pygame
from piece import Piece
from board import Board
import os
from solver import Solver
from time import sleep


class Game:
    def __init__(self, size, prob):  # Inicializa o tabuleiro e configura o ambiente do Pygame
        # Cria um novo tabuleiro com o tamanho e probabilidade fornecidos
        self.board = Board(size, prob)
        pygame.init()  # Inicializa o Pygame
        self.sizeScreen = 800, 800  # Define o tamanho da tela
        # Cria uma tela com o tamanho especificado
        self.screen = pygame.display.set_mode(self.sizeScreen)
        self.pieceSize = (
            self.sizeScreen[0] / size[1], self.sizeScreen[1] / size[0])  # Calcula o tamanho de cada peça
        self.loadPictures()  # Carrega as imagens dos blocos do jogo
        # Cria um solucionador para o tabuleiro
        self.solver = Solver(self.board)
        self.start_time = None  # Temporizador de início do jogo
        self.font = pygame.font.Font(None, 36)  # Fonte para exibir o tempo

    def loadPictures(self):   # Carrega todas as imagens dos blocos do tabuleiro
        self.images = {}
        imagesDirectory = "images"  # Diretório onde as imagens estão armazenadas
        for fileName in os.listdir(imagesDirectory):
            if not fileName.endswith(".png"):
                continue  # Ignora arquivos que não são imagens PNG
            # Caminho completo para o arquivo da imagem
            path = imagesDirectory + r"/" + fileName
            img = pygame.image.load(path)  # Carrega a imagem
            img = img.convert()  # Converte a imagem para o formato adequado
            img = pygame.transform.scale(
                img, (int(self.pieceSize[0]), int(self.pieceSize[1])))  # Redimensiona a imagem para o tamanho da peça
            # Adiciona a imagem ao dicionário
            self.images[fileName.split(".")[0]] = img

    def run(self):   # Inicia o loop principal do jogo
        self.start_time = pygame.time.get_ticks()  # Registra o tempo inicial
        running = True  # Flag para controlar o loop do jogo
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Sai do loop se o usuário fechar a janela
                if event.type == pygame.MOUSEBUTTONDOWN and not (self.board.getWon() or self.board.getLost()):
                    # Verifica se o botão direito foi clicado
                    rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
                    # Trata o clique do mouse
                    self.handleClick(pygame.mouse.get_pos(), rightClick)
                if event.type == pygame.KEYDOWN:
                    self.solver.move()  # Faz um movimento automático se uma tecla for pressionada
            self.screen.fill((0, 0, 0))  # Limpa a tela com a cor preta
            self.draw()  # Desenha o estado atual do tabuleiro
            self.show_timer()  # Exibe o tempo decorrido
            pygame.display.flip()  # Atualiza a tela com as novas renderizações
            if self.board.getWon():  # Verifica se o jogador venceu ou perdeu
                self.vitoria()  # Toca o som de vitória e exibe uma mensagem de vitória
                running = False  # Sai do loop
            if self.board.getLost():
                self.derrota()  # Toca o som de derrota e exibe uma mensagem de derrota
                running = False  # Sai do loop
        pygame.quit()  # Encerra o Pygame

    def draw(self):  # Desenha o tabuleiro na tela
        topLeft = (0, 0)  # Posição inicial para desenhar as peças
        for row in self.board.getBoard():
            for piece in row:
                # Define a área onde a peça será desenhada
                rect = pygame.Rect(topLeft, self.pieceSize)
                # Obtém a imagem correspondente à peça
                image = self.images[self.getImageString(piece)]
                self.screen.blit(image, topLeft)  # Desenha a peça na tela
                # Move a posição para a próxima peça
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
            # Move a posição para a próxima linha
            topLeft = (0, topLeft[1] + self.pieceSize[1])

    def getImageString(self, piece):  # Obtém o nome da imagem com base no estado da peça
        if piece.getClicked():
            return str(piece.getNumAround()) if not piece.getHasBomb() else 'bomb-at-clicked-block'
        if self.board.getLost():
            if piece.getHasBomb():
                return 'unclicked-bomb'
            return 'wrong-flag' if piece.getFlagged() else 'empty-block'
        return 'flag' if piece.getFlagged() else 'empty-block'

    # Converte a posição do clique em índices de peça e processa o clique
    def handleClick(self, position, flag):
        index = tuple(int(pos // size)
                      for pos, size in zip(position, self.pieceSize))[::-1]
        self.board.handleClick(self.board.getPiece(
            index), flag)  # Processa o clique na peça

    def show_timer(self):  # Exibir o tempo decorrido na tela
        # Calcula o tempo decorrido em segundos
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        # Formata o texto do temporizador
        timer_text = f"Tempo: {elapsed_time} s"
        # Renderiza o texto do temporizador
        text_surface = self.font.render(timer_text, True, (255, 255, 255))
        # Exibe o tempo no canto superior esquerdo
        self.screen.blit(text_surface, (10, 10))

    def vitoria(self):
        sound = pygame.mixer.Sound('vitoria.wav')  # Som da vitória
        sound.play()
        sleep(3)  # Pausa para tocar o som de vitória

    def derrota(self):
        sound = pygame.mixer.Sound('derrota.mp3')  # Som da derrota
        sound.play()
        sleep(3)  # Pausa para tocar o som de derrota

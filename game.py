import os
from time import sleep

import pygame

from board import Board
from solver import Solver


class Game:
    def __init__(self, size, prob):
        self.board = Board(size, prob)
        pygame.init()
        pygame.display.set_caption("Campo Minado")
        
        self.header_height = 50
        self.sizeScreen = 800, 800 + self.header_height
        self.screen = pygame.display.set_mode(self.sizeScreen)
        self.pieceSize = (
            800 / size[1],
            800 / size[0],
        )
        self.loadPictures()
        self.solver = Solver(self.board)
        self.start_time = None
        self.font = pygame.font.SysFont("Segoe UI", 32, bold=True)
        self.clock = pygame.time.Clock()

    def loadPictures(self):
        self.images = {}
        imagesDirectory = "images"
        for fileName in os.listdir(imagesDirectory):
            if not fileName.endswith(".png"):
                continue

            path = imagesDirectory + r"/" + fileName
            img = pygame.image.load(path)
            img = img.convert()
            img = pygame.transform.scale(
                img, (int(self.pieceSize[0]), int(self.pieceSize[1]))
            )
            self.images[fileName.split(".")[0]] = img

    def run(self):
        self.start_time = pygame.time.get_ticks()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not (
                    self.board.getWon() or self.board.getLost()
                ):
                    rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
                    # Ajustar a posição Y devido ao cabeçalho (header_height)
                    pos = list(pygame.mouse.get_pos())
                    pos[1] -= self.header_height
                    if pos[1] >= 0:
                        self.handleClick(pos, rightClick)
                if event.type == pygame.KEYDOWN:
                    self.solver.move()

            self.screen.fill((40, 40, 40)) # Cor de fundo mais moderna
            self.draw()
            self.show_header()
            pygame.display.flip()
            self.clock.tick(60)

            if self.board.getWon():
                self.vitoria()
                running = False
            if self.board.getLost():
                self.derrota()
                running = False

        pygame.display.quit()

    def draw(self):
        topLeft = (0, self.header_height)
        for row in self.board.getBoard():
            for piece in row:
                image = self.images[self.getImageString(piece)]
                self.screen.blit(image, topLeft)
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
            topLeft = (0, topLeft[1] + self.pieceSize[1])

    def getImageString(self, piece):
        if piece.getClicked():
            if piece.getHasBomb():
                return "bomb-at-clicked-block"
            return str(piece.getNumAround())
        if self.board.getLost():
            if piece.getHasBomb():
                return "unclicked-bomb"
            return "wrong-flag" if piece.getFlagged() else "empty-block"
        return "flag" if piece.getFlagged() else "empty-block"

    def handleClick(self, position, flag):
        index = tuple(
            int(pos // size) for pos, size in zip(position, self.pieceSize)
        )[::-1]
        
        # Previne cliques fora da área do tabuleiro válidas
        if index[0] >= 0 and index[0] < self.board.size[0] and index[1] >= 0 and index[1] < self.board.size[1]:
            self.board.handleClick(self.board.getPiece(index), flag)

    def show_header(self):
        # Fundo do Header
        pygame.draw.rect(self.screen, (50, 50, 50), (0, 0, 800, self.header_height))
        # Linha inferior do Header
        pygame.draw.line(self.screen, (30, 30, 30), (0, self.header_height - 1), (800, self.header_height - 1), 2)
        
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        mins = elapsed_time // 60
        secs = elapsed_time % 60
        timer_text = f"Tempo: {mins:02}:{secs:02}"
        
        # Quantidade de bombas e flags
        bombs_total = sum(piece.getHasBomb() for row in self.board.getBoard() for piece in row)
        flags_used = sum(piece.getFlagged() for row in self.board.getBoard() for piece in row)
        bombs_text = f"Bandeiras: {flags_used} / {bombs_total}"

        # Renderização do texto
        time_surface = self.font.render(timer_text, True, (240, 240, 240))
        bombs_surface = self.font.render(bombs_text, True, (240, 240, 240))

        self.screen.blit(time_surface, (20, 10))
        self.screen.blit(bombs_surface, (800 - bombs_surface.get_width() - 20, 10))

    def vitoria(self):
        sound = pygame.mixer.Sound("vitoria.wav")
        sound.play()
        sleep(3)

    def derrota(self):
        sound = pygame.mixer.Sound("derrota.mp3")
        sound.play()
        sleep(3)

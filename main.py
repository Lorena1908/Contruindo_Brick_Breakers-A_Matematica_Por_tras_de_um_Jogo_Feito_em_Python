
import pygame
import random
pygame.font.init()

largura, altura = 780, 500
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Brick Breakers')
fonte = pygame.font.SysFont('comicsans', 42)
vidas = 5
pontos = 0

class Tijolo:
    def __init__(self, cor, x, y):
        self.cor = cor
        self.x = x
        self.y = y
        self.largura = 100
        self.altura = 25
    
    def desenhar(self):
        pygame.draw.rect(janela, self.cor, (self.x, self.y, self.largura, self.altura))

class Pa:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cor = (255, 26, 26)
        self.largura = 100
        self.altura = 15
    
    def desenhar(self):
        pygame.draw.rect(janela, self.cor, (self.x, self.y, self.largura, self.altura))

class Bola:
    def __init__(self, pa):
        self.x = 0
        self.y = 0
        self.raio = 15
        self.cor = (26, 26, 255)
        self.xvels = [-0.3, 0.3]
        self.xvel = random.choice(self.xvels)
        self.yvel = -0.3
        self.parada = True
        self.pa = pa
        self.sem_vidas = False
        self.ganhou = False
        self.escala_aceleracao = 1.1

    def desenhar(self):
        if self.parada:
            self.reiniciar()

        pygame.draw.circle(janela, self.cor, (self.x, self.y), self.raio)
    
    def reiniciar(self): # colocar a bola de volta na posição inicial (ficar na pázinha)
        self.parada = True
        self.x = self.pa.x + self.pa.largura/2
        self.y = self.pa.y - self.raio

        self.xvel = random.choice(self.xvels)
        self.yvel = -0.3

    def movimentar(self):
        global vidas, pontos
        if not self.parada:
            self.x += self.xvel
            self.y += self.yvel
        
        if self.x >= largura or self.x <= 0: 
            self.xvel *= -1
        
        if self.y <= 0: 
            self.yvel *= -1
        
        if self.y >= altura: 
            self.reiniciar()
            vidas -= 1

            if vidas <= 0:
                self.sem_vidas = True

        if self.pa.x <= self.x <= self.pa.x + self.pa.largura and self.pa.y <= self.y <= self.pa.y + self.pa.altura:
            self.y = self.pa.y
            self.yvel *= -1

        for i, tijolo in enumerate(tijolos):
            if tijolo.x <= self.x <= tijolo.x + tijolo.largura and tijolo.y <= self.y <= tijolo.y + tijolo.altura:
                self.y = tijolo.y + tijolo.altura
                tijolos.pop(i)
                pontos += 1
                self.yvel *= -1
            
        if len(tijolos) == 0:
            self.ganhou = True


def desenhar_janela(bola, pa):
    # Objetos
    bola.desenhar()
    pa.desenhar()

    for tijolo in tijolos:
        tijolo.desenhar()

    # Texto
    fonte1 = pygame.font.SysFont('comicsans', 30)
    texto_vidas = fonte1.render('Vidas: {}'.format(vidas), 1, (0, 219, 0))
    pontos_texto = fonte1.render('Pontos: {}'.format(pontos), 1, (0, 219, 0))
    janela.blit(pontos_texto, (200,460))
    janela.blit(texto_vidas, (400,460))
    pygame.display.update()


def reinicia_jogo():
    global pontos, vidas
    pontos = 0
    vidas = 5


def main():
    global tijolos
    run = True
    pa = Pa(largura/2 - 50, 430)
    bola = Bola(pa)
    # tijolos_cores = [(255, 0, 102), (102, 255, 51), (255, 102, 0), (252,235,2)]
    # tijolos = [Tijolo(tijolos_cores[i], 10 + j * 110,25 + i * 35) for i in range(4) for j in range(7)]
    
    tijolos = [
        Tijolo((255, 0, 102), 10,25),
        Tijolo((255, 0, 102), 120,25),
        Tijolo((255, 0, 102), 230,25),
        Tijolo((255, 0, 102), 340,25),
        Tijolo((255, 0, 102), 450,25),
        Tijolo((255, 0, 102), 560,25),
        Tijolo((255, 0, 102), 670,25),
        Tijolo((102, 255, 51), 10,60),
        Tijolo((102, 255, 51), 120,60),
        Tijolo((102, 255, 51), 230,60),
        Tijolo((102, 255, 51), 340,60),
        Tijolo((102, 255, 51), 450,60),
        Tijolo((102, 255, 51), 560,60),
        Tijolo((102, 255, 51), 670,60),
        Tijolo((255, 102, 0), 10,95),
        Tijolo((255, 102, 0), 120,95),
        Tijolo((255, 102, 0), 230,95),
        Tijolo((255, 102, 0), 340,95),
        Tijolo((255, 102, 0), 450,95),
        Tijolo((255, 102, 0), 560,95),
        Tijolo((255, 102, 0), 670,95),
        Tijolo((252,235,2), 10,130),
        Tijolo((252,235,2), 120,130),
        Tijolo((252,235,2), 230,130),
        Tijolo((252,235,2), 340,130),
        Tijolo((252,235,2), 450,130),
        Tijolo((252,235,2), 560,130),
        Tijolo((252,235,2), 670,130),
    ]
    segundos = 0
    relogio = pygame.time.Clock()
    tempo = 0
    tempo_necessario = 1000 # 1 second

    # MAIN LOOP
    while run:
        relogio.tick()
        tempo += relogio.get_rawtime()
        janela.fill((0,0,0))
        bola.movimentar()
        desenhar_janela(bola, pa)

        if tempo >= tempo_necessario and not bola.parada:
            tempo = 0
            segundos += 1

            if segundos >= 5:
                segundos = 0
                bola.xvel *= bola.escala_aceleracao
                bola.yvel *= bola.escala_aceleracao

        if bola.sem_vidas:
            texto = fonte.render('Você Perdeu!', 1, (255, 26, 26))
            janela.blit(texto, (largura/2 - texto.get_width()/2, altura/2 - texto.get_height()/2))
            pygame.display.update()
            run = False
            pygame.time.wait(2000)
        
        if bola.ganhou:
            texto = fonte.render('Você Ganhou!', 1, (255,215,0))
            janela.blit(texto, (largura/2 - texto.get_width()/2, altura/2 - texto.get_height()/2))
            pygame.display.update()
            run = False
            pygame.time.wait(2000)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            
            pygame.key.set_repeat(100) 
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    pa.x += 30
                
                if evento.key == pygame.K_LEFT:
                    pa.x -= 30
                
                if evento.key == pygame.K_UP:
                    bola.parada = False

def menu_screen():
    run = True

    while run:
        janela.fill((0,0,0))
        texto = fonte.render('Pressione Qualquer Tecla para Jogar', 1, (255,255,255))
        janela.blit(texto, (largura/2 - texto.get_width()/2, altura/2 - texto.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                reinicia_jogo()
                main()
        

menu_screen()
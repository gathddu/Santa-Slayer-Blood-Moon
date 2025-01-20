import pygame
import sys
from setting import *

pygame.init()

# Configurações de tela
largura, altura = 640, 480
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Configurações")

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)

# Fonte 8-bit
fonte_8bit = pygame.font.Font(UI_FONT, 30)

# Configurações de volume
volume_jogo = 50  # Volume para efeitos ou mecânicas do jogo
volume_musica = 50  # Volume da música

opcoes = ["Volume do Jogo", "Volume da Música"]  # Ajuste as opções
indice_selecionado = 0

background = pygame.image.load("./graphics/background/background.png").convert()
background = pygame.transform.scale(background, (largura, altura))  # Correct scaling

background_alpha = pygame.Surface((largura, altura), pygame.SRCALPHA)
background_alpha.blit(background, (0, 0))
background_alpha.set_alpha(150)



def mostrar_configuracoes():
    global volume_jogo, volume_musica, indice_selecionado
    rodando = True
    while rodando:
        tela.blit(background_alpha, (0, 0))


        # Título
        titulo_texto = fonte_8bit.render("CONFIGURACOES", True, preto)
        tela.blit(titulo_texto, (largura // 2 - titulo_texto.get_width() // 2, 50))

        # Opções
        for i, opcao in enumerate(opcoes):
            cor = vermelho if i == indice_selecionado else preto

            if opcao == "Volume do Jogo":
                texto_opcao = f"{opcao}: {volume_jogo}"
            elif opcao == "Volume da Música":
                texto_opcao = f"{opcao}: {volume_musica}"
            else:
                texto_opcao = opcao

            opcao_texto = fonte_8bit.render(texto_opcao, True, cor)
            tela.blit(opcao_texto, (largura // 2 - opcao_texto.get_width() // 2, 200 + i * 50))

        # Instruções
        instrucoes = fonte_8bit.render("Pressione ESC para voltar", True, preto)
        tela.blit(instrucoes, (largura // 2 - instrucoes.get_width() // 2, altura - 80))

        # Atualizar tela
        pygame.display.flip()

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif evento.key == pygame.K_UP:
                    indice_selecionado = (indice_selecionado - 1) % len(opcoes)
                elif evento.key == pygame.K_DOWN:
                    indice_selecionado = (indice_selecionado + 1) % len(opcoes)
                elif evento.key == pygame.K_RIGHT:
                    if opcoes[indice_selecionado] == "Volume do Jogo":
                        volume_jogo = min(100, volume_jogo + 5)
                    elif opcoes[indice_selecionado] == "Volume da Música":
                        volume_musica = min(100, volume_musica + 5)
                        pygame.mixer.music.set_volume(volume_musica / 100)  # Ajusta o volume da música
                elif evento.key == pygame.K_LEFT:
                    if opcoes[indice_selecionado] == "Volume do Jogo":
                        volume_jogo = max(0, volume_jogo - 5)
                    elif opcoes[indice_selecionado] == "Volume da Música":
                        volume_musica = max(0, volume_musica - 5)
                        pygame.mixer.music.set_volume(volume_musica / 100)  # Ajusta o volume da música

if __name__ == "__main__":
    mostrar_configuracoes()
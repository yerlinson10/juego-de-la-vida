import pygame
import numpy as np
import time

pygame.init()
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))

bg = 255, 255, 255

# Pintando el fondo de negro
screen.fill(bg)

# Numero de celdas
nxC, nyC = 75, 75

# Dimensiones de las celdas 
dimCW = width / nxC
dimCH = height / nyC

# Estado de celdas. Vivas = 1; Muertas = 0;
gameState = np.zeros((nxC, nyC))

# Contadores
generation_count = 0
population_count = 0

# Fuente para texto
font = pygame.font.SysFont("Arial", 28)

# Estados iniciales

# Automata palo
# gameState[5, 3] = 1
# gameState[5, 4] = 1
# gameState[5, 5] = 1

# gameState[21, 21] = 1
# gameState[22, 22] = 1
# gameState[22, 23] = 1
# gameState[21, 23] = 1
# gameState[20, 23] = 1

# Variable para pausar el juego
pauseExect = False

# Bucle de ejecución
while True:
    newGameState = np.copy(gameState)
    
    screen.fill(bg)
    # time.sleep(0)
    
    # Registrar eventos del teclado y mouse
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Detección de la barra espaciadora para pausar/reanudar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pauseExect = not pauseExect

        # Detección de clic del mouse
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            pauseExect = True
            posX, posY = pygame.mouse.get_pos()
            x, y = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[x, y] = not gameState[x, y]  # Cambiar el estado de la celda

    # Solo actualizar el estado del juego si no está pausado
    if not pauseExect:
        generation_count += 1  # Incrementar el contador de generaciones
        population_count = 0   # Resetear el contador de población

        for y in range(0, nxC):
            for x in range(0, nyC):
                # Calculamos el número de vecinos cercanos
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                          gameState[(x-1) % nxC, (y) % nyC] + \
                          gameState[(x-1) % nxC, (y+1) % nyC] + \
                          gameState[(x) % nxC, (y-1) % nyC] + \
                          gameState[(x) % nxC, (y+1) % nyC] + \
                          gameState[(x+1) % nxC, (y-1) % nyC] + \
                          gameState[(x+1) % nxC, (y) % nyC] + \
                          gameState[(x+1) % nxC, (y+1) % nyC]
                
                # Regla #1: Una celda muerta con exactamente 3 vecinas vivas, "revive"
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                
                # Regla #2: Una celda con menos de 2 o más de 3 vecinas vivas, "muere"
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

                # Contar las células vivas
                population_count += newGameState[x, y]

    # Dibujar la cuadrícula y las células
    for y in range(0, nxC):
        for x in range(0, nyC):
            poly = [((x) * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x) * dimCW, (y+1) * dimCH)]
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (25, 25, 25), poly, 0)
    
    # Actualizamos el estado del juego
    gameState = np.copy(newGameState)
    
    # Mostrar contadores de generaciones y población
    gen_text = font.render(f"Generations: {generation_count}", True, (25, 25, 25))
    pop_text = font.render(f"Population: {int(population_count)}", True, (25, 25, 25))
    
    screen.blit(gen_text, (10, 10))
    screen.blit(pop_text, (10, 40))
    
    # Actualizamos la pantalla
    pygame.display.flip()

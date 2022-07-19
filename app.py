#importamos la libreria para los graficos 2d 
import pygame
# Importamos la libreria para los calculos matematicos
import math
# Iniciamos la aplicaión..
pygame.init()

# Definimos el tamaño de la ventana que contendra la simulación
WIDTH, HEIGHT = 800, 800
# Se dibuja el area donde se realizara la simulacion
# En donde se dibujaran los planetas.
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Ponemos el nombre de la ventana.
pygame.display.set_caption("Simulación del Sistema Solar")

# La simulación del sistema solar se realiza en un bucle infinito.
# El único evento que se ejecutara será el movimiento de los planetas.
def main():
    run = True
    
    while run:
        for event in pygame.event.get():
            # El unico evento que nos interesa registrar es cuando se
            # pulse en la esquina superior derecha la "x" para salir del programa.
            if event.type == pygame.QUIT:
                run = False
    
    pygame.quit()
    
if __name__=="__main__":
    main()

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
# El objeto WIN nos servirá para dibujar objetos en la pantalla.
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Ponemos el nombre de la ventana.
pygame.display.set_caption("Simulación del Sistema Solar")

# Color de relleno del fondo de la pantalla
WHITE = (255, 255, 255)

# La simulación del sistema solar se realiza en un bucle infinito.
# El único evento que se ejecutara será el movimiento de los planetas.
def main():
    run = True
    # Para determinar el frame rate del programa y que no vaya ni muy deprisa
    # ni muy despacio establecemos la variable clock
    clock = pygame.time.Clock()
    
    while run:
        # número máximo de veces que se actualizará la pantalla por segundo (frame rate maximo)
        # Lo hacemos para asegurarnos de que el programa no vaya demasiado rapido.
        clock.tick(60)
        # Rellena el fondo de la pantalla con el color que le pasemos como argumento
        # No se mostrara mientras no se actualice la pantalla.
        WIN.fill(WHITE)
        # Actualiza la pantalla. Los objetos que hayamos puesto se mostrarán en la misma.
        pygame.display.update()
        
        for event in pygame.event.get():
            # El unico evento que nos interesa registrar es cuando se
            # pulse en la esquina superior derecha la "x" para salir del programa.
            if event.type == pygame.QUIT:
                run = False
    
    pygame.quit()
    
if __name__=="__main__":
    main()

''' Simulador del sistema solar.

Simulador lo más exacto posible usando pygame como biblioteca
de partida. '''

#importamos la libreria para los graficos 2d 
import pygame
# Importamos la libreria para los calculos matematicos
import math
# Iniciamos la aplicación..
pygame.init()

# Definimos el tamaño de la ventana que contendra la simulación
WIDTH, HEIGHT = 800, 800
# Se dibuja el area donde se realizara la simulacion
# En donde se dibujaran los planetas.
# El objeto WIN nos servirá para dibujar objetos en la pantalla.
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Ponemos el nombre de la ventana.
pygame.display.set_caption("Simulación del Sistema Solar")

# COLORES.
# Color de relleno del fondo de la pantalla
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# RADIOS de los planetas en KILOMETROS
RADIO_SOL = 695_700
RADIO_MERCURIO = 2_439.7
RADIO_VENUS = 6_051.8
RADIO_TIERRA = 6_371
RADIO_MARTE = 3_389.5
RADIO_JUPITER = 69_911
RADIO_SATURNO = 58_232
RADIO_URANO = 25_362
RADIO_NEPTUNO = 24_622
RADIO_PLUTON = 1_188.3
# Se aumenta o disminuye el valor cambiando el valor del numerador en R_ESCALA
R_ESCALA = 50 / 695_700

# MASAS de los planetas en KILOGRAMOS
M_SOL = 1.989e30


# Para construir los planetas vamos a utilizar la clase Planet()
class Planet:
    ''' Definicion de los Planetas.

    Argumentos:
    
    x, y - Posición de los planetas en la pantalla.
    radius - radio del planeta.
    color - color del planeta.
    mass - masa del planeta.'''
    
    # Constantes planetarias para realizar los calculos UNIDADES ASTRONOMICAS
    # UNIDAD ASTRONOMICA - Distancia media entre la tierra y el sol en METROS.
    AU = 149_597_870_700
    # CONSTANTE GRAVITACIONAL - Para calcular la fuerza de atración de los planetas. (N*m2)/Kg2
    G = 6.67428e-11
    # La escala sirve para ajustar las unidades astronomicas a nuestro grafico. No podemos dibujar
    # las distancias espaciales en nuestra pantalla. Por ello utilizamos la escala en la que aproximadamente
    # 100 pixeles equivale a una UNIDAD ASTRONOMICA.
    SCALE = 250 / AU
    # Cada vez que actualice los frames o la pantalla, cuanto tiempo ha pasado en la realidad
    # Vamos a establecerlo en un dia terrestre pero en en SEGUNDOS.
    TIMESTEP = 3600 * 24 
    
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        
        # Lista vacia para realizar un seguimiento de todos los puntos que sigue el planeta
        # para poder dibujar su orbita.
        self.orbit = [] 
        # Nos dice si el planeta es el sol o no.
        # El sol va a ser estatico y no se le aplicaran los calculos de las orbitas.
        self.sun = False
        # Distancia hasta el sol.
        self.distance_to_sun = 0
        
        # Velocidad en los ejes x e y
        self.x_vel = 0
        self.y_vel = 0
        
    def draw(self, win):
        ''' Funcion para dibujar los planetas en la pantalla '''
        # Las coordenadas espaciales hay que pasarlas a una escala para dibujarlas
        # en la pantalla.
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        # El punto (0,0) en pygame esta en la parte superior izquierda de la pantalla.
        # Por esto tenemos que calcular el centro de la pantalla para desde ahi centrar los graficos.
        # Por eso usamos + WIDTH/2 -> x e HEIGHT/2 -> y
        pygame.draw.circle(win, self.color, (x, y), self.radius)
        


# La simulación del sistema solar se realiza en un bucle infinito.
# El único evento que se ejecutara será el movimiento de los planetas.
def main():
    run = True
    # Para determinar el frame rate del programa y que no vaya ni muy deprisa
    # ni muy despacio establecemos la variable clock
    clock = pygame.time.Clock()
    
    # Lista de los planetas.
    
    # La masa de los planetas esta en KILOGRAMOS.
    sun = Planet(0, 0, RADIO_SOL * R_ESCALA, YELLOW, M_SOL)
    sun.sun = True
    
    planets = [sun]
    
    while run:
        # número máximo de veces que se actualizará la pantalla por segundo (frame rate maximo)
        # Lo hacemos para asegurarnos de que el programa no vaya demasiado rapido.
        clock.tick(60)
        # Rellena el fondo de la pantalla con el color que le pasemos como argumento
        # No se mostrara mientras no se actualice la pantalla.
        WIN.fill(WHITE)
        # Actualiza la pantalla. Los objetos que hayamos puesto se mostrarán en la misma.
                
        for event in pygame.event.get():
            # El unico evento que nos interesa registrar es cuando se
            # pulse en la esquina superior derecha la "x" para salir del programa.
            if event.type == pygame.QUIT:
                run = False
                
        for planet in planets:
            planet.draw(WIN)
            
        pygame.display.update()
    
    pygame.quit()
    
if __name__=="__main__":
    main()

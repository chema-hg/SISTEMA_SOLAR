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
WIDTH, HEIGHT = 1200, 800 # 800 x 800
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
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
BROWN = (80, 40, 0)

# RADIOS de los planetas en KILOMETROS
RADIO_SOL = 696_340
RADIO_MERCURIO = 2_439.7
RADIO_VENUS = 6_051.8
RADIO_TIERRA = 6_371
RADIO_MARTE = 3_389.5
RADIO_JUPITER = 69_911
RADIO_SATURNO = 58_232
RADIO_URANO = 25_362
RADIO_NEPTUNO = 24_622
RADIO_PLUTON = 1_188.3


# MASAS de los planetas en KILOGRAMOS
M_SOL = 1.989e30
M_MERCURIO = 3.285e23
M_VENUS = 4.867e24
M_TIERRA = 5.972e24
M_MARTE = 6.39e23
M_JUPITER = 1.898e27
M_SATURNO = 5.683e26
M_URANO = 8.681e25
M_NEPTUNO = 1.024e26
M_PLUTON = 1e22

# Para hacer los planetas más grandes o pequeños en relación a la tierra establecemos
# la variable tamano que es tamaño representado de la tierra.
TAMANO = 7 # 16


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
    SCALE = 90 / AU # 250 / AU
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
        
    def attraction(self, other):
        '''Calcula la fuerza de atracción del planeta con respecto a todos
        los demas planetas que no son el mismo. '''
        # Pasamos las coordenadas del otro planeta
        other_x, other_y = other.x, other.y
        # Calculamos la fuerza de atracción.
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        if other.sun:
            self.distance_to_sun = distance
        
        # Calculamos la fuerza de atración una vez que sabemos las distancias.
        # F = (G * M1 * M2) / distancia ** 2
        # Es la fuerza de atracción directa, en linea recta
        force = (self.G * self.mass * other.mass) / distance ** 2
        # Ahora que tenemos la fuerza total hay que descomponerla en la fuerza x
        # y la fuerza en el eje y.
        # Angulo theta  = Formado por la hipotenusa (fuerza total) y el cateto adyacente (fuerza x)
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            # Si el planeta es el mismo, no tiene sentido calcular la fuerza consigo mismo.
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
            
        # Una vez que conocemos todas las fuerzas que actuan sobre el planeta
        # tenemos que calcular la velocidad del mismo 2ª Ley de Newton
        # Partimos de que Fuerza = masa * aceleracion; Fuerza = masa * (Iv / It)
        # Fuerza = masa * (v - vº) / (t - tº) y como vº = tº = 0
        # Fuerza = masa * (v / t) y despejando la velocidad
        # v = (f * t) / m        
        self.x_vel += (total_fx * self.TIMESTEP) / self.mass
        self.y_vel += (total_fy * self.TIMESTEP) / self.mass
        # El desplazamiento es la velocidad por el tiempo
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


# La simulación del sistema solar se realiza en un bucle infinito.
# El único evento que se ejecutara será el movimiento de los planetas.
def main():
    run = True
    # Para determinar el frame rate del programa y que no vaya ni muy deprisa
    # ni muy despacio establecemos la variable clock
    clock = pygame.time.Clock()
    
    # Lista de los planetas.
    
    # La masa de los planetas esta en KILOGRAMOS.
    # El tamaño del sol no es real porque sino se nos saldria del grafico
    # y no se verian los otros planetas.
    # Es necesario establecer una velocidad inicial al eje_y en m*s ya que si no
    # los planetas caerian hacia el sol directamente y no girarian.
    sun = Planet(0, 0, TAMANO * 2, YELLOW, M_SOL)
    sun.sun = True
    
    mercury = Planet(-0.387 * Planet.AU, 0, TAMANO * 0.4, DARK_GREY, M_MERCURIO)
    mercury.y_vel = 47.4e3
    
    venus = Planet(-0.723 * Planet.AU, 0, TAMANO * 0.9, WHITE, M_VENUS)
    venus.y_vel = 35.012e3
    
    earth = Planet(-1 * Planet.AU, 0, TAMANO, BLUE, M_TIERRA)
    earth.y_vel = 29.783e3
    
    mars = Planet(-1.524 * Planet.AU, 0, TAMANO * 0.5, RED, M_MARTE)
    mars.y_vel = 24.1e3
    
    jupiter = Planet(-5.20 * Planet.AU, 0, TAMANO * 11.20, BROWN, M_JUPITER)
    jupiter.y_vel = 13.10e3
    
    # Los siguientes planetas afectan a los calculos pero no se ven.
    
    saturn = Planet(-9.54 * Planet.AU, 0, TAMANO * 9.5, BLUE, M_SATURNO)
    saturn.y_vel = 9.7e3
    
    uranus = Planet(-19.19 * Planet.AU, 0, TAMANO * 4, BLUE, M_URANO)
    uranus.y_vel = 6.8e3
    
    neptune = Planet(-30.07 * Planet.AU, 0, TAMANO * 3.9, BLUE, M_NEPTUNO)
    neptune.y_vel = 5.4e3
    
    pluto = Planet(-39.48 * Planet.AU, 0, TAMANO * 0.186, BLUE, M_PLUTON)
    pluto.y_vel = 4.74e3
    
    
    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto]
    
    while run:
        # número máximo de veces que se actualizará la pantalla por segundo (frame rate maximo)
        # Lo hacemos para asegurarnos de que el programa no vaya demasiado rapido.
        clock.tick(60)
        # Rellena el fondo de la pantalla con el color que le pasemos como argumento
        # No se mostrara mientras no se actualice la pantalla.
        # Necesitamos refrescar la pantalla en cada actualización cada vez que
        # se muevan los planetas volviendo a dibujar el fondo, si no lo hacemos
        # se vería una estela.
        WIN.fill((0, 0, 0))
        # Actualiza la pantalla. Los objetos que hayamos puesto se mostrarán en la misma.
                
        for event in pygame.event.get():
            # El unico evento que nos interesa registrar es cuando se
            # pulse en la esquina superior derecha la "x" para salir del programa.
            if event.type == pygame.QUIT:
                run = False
                
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
            
        pygame.display.update()
    
    pygame.quit()
    
if __name__=="__main__":
    main()

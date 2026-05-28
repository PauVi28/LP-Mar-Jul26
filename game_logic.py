import pygame
import random

ANCHO, ALTO = 900, 600

class Particula:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(1, 3)
        self.vida = random.randint(15, 30)
        self.radio = random.randint(2, 4)

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vida -= 1
        if self.radio > 0.1:
            self.radio -= 0.05

    def dibujar(self, superficie):
        if self.vida > 0 and self.radio > 0:
            pygame.draw.circle(superficie, self.color, (int(self.x), int(self.y)), int(self.radio))

class Obstaculo:
    def __init__(self, carril):
        self.carril = carril
        if carril == 1:
            self.x = random.randint(183, 396)
        else:
            self.x = random.randint(458, 679)
        self.y = -90
        self.w, self.h = 44, 80
        self.color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))

    def mover(self, velocidad):
        self.y += velocidad

    def dibujar(self, superficie):
        # Llantas antes del cuerpo para que queden por debajo visualmente
        tire_color = (25, 25, 25)
        tw, th = 8, 16
        pygame.draw.rect(superficie, tire_color, (int(self.x) - 5, int(self.y) + 4, tw, th), border_radius=2)
        pygame.draw.rect(superficie, tire_color, (int(self.x) + self.w - 3, int(self.y) + 4, tw, th), border_radius=2)
        pygame.draw.rect(superficie, tire_color, (int(self.x) - 5, int(self.y) + self.h - 20, tw, th), border_radius=2)
        pygame.draw.rect(superficie, tire_color, (int(self.x) + self.w - 3, int(self.y) + self.h - 20, tw, th), border_radius=2)
        # Cuerpo
        pygame.draw.rect(superficie, self.color, (int(self.x), int(self.y), self.w, self.h), border_radius=6)
        pygame.draw.rect(superficie, (200, 230, 255), (int(self.x)+4, int(self.y)+15, self.w-8, 12))

    def fuera(self):
        return self.y > ALTO

    def rect_col(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

class Nitro:
    def __init__(self):
        self.x = random.randint(185, 670)
        self.y = -50
        self.w, self.h = 25, 40

    def mover(self, velocidad):
        self.y += velocidad

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, (100, 200, 255), (int(self.x), int(self.y), self.w, self.h), border_radius=4)
        pygame.draw.circle(superficie, (255, 220, 0), (int(self.x) + self.w//2, int(self.y) + self.h//2), 6)

    def fuera(self):
        return self.y > ALTO

    def rect_col(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

class Carro:
    def __init__(self, x, y, color, color_osc, limite_izq, limite_der):
        self.x = x
        self.y = y
        self.w, self.h = 46, 84
        self.color = color
        self.color_osc = color_osc
        self.limite_izq = limite_izq
        self.limite_der = limite_der
        self.vel = 5
        self.vivo = True
        self.particulas = []

    def mover(self, direccion):
        self.x += direccion * self.vel
        if self.x < self.limite_izq:
            self.x = self.limite_izq
        if self.x + self.w > self.limite_der:
            self.x = self.limite_der - self.w

    def explotar(self):
        for _ in range(30):
            self.particulas.append(Particula(self.x + self.w//2, self.y + self.h//2, (255, random.randint(50, 150), 0)))

    def actualizar_particulas(self):
        for p in self.particulas[:]:
            p.actualizar()
            if p.vida <= 0:
                self.particulas.remove(p)

    def dibujar(self, superficie):
        if self.vivo:
            # LLANTAS primero: quedan por debajo del cuerpo
            tire_color = (25, 25, 25)
            tw, th = 9, 18
            # Delanteras
            pygame.draw.rect(superficie, tire_color, (int(self.x) - 5, int(self.y) + 5, tw, th), border_radius=2)
            pygame.draw.rect(superficie, tire_color, (int(self.x) + self.w - 4, int(self.y) + 5, tw, th), border_radius=2)
            # Traseras
            pygame.draw.rect(superficie, tire_color, (int(self.x) - 5, int(self.y) + self.h - 23, tw, th), border_radius=2)
            pygame.draw.rect(superficie, tire_color, (int(self.x) + self.w - 4, int(self.y) + self.h - 23, tw, th), border_radius=2)
            # Cuerpo principal encima de las llantas
            pygame.draw.rect(superficie, self.color, (int(self.x), int(self.y), self.w, self.h), border_radius=8)
            # Techo
            pygame.draw.rect(superficie, self.color_osc, (int(self.x)+4, int(self.y)+25, self.w-8, 30), border_radius=4)
            # Parabrisas y luneta trasera
            pygame.draw.rect(superficie, (200, 235, 255), (int(self.x)+6, int(self.y)+18, self.w-12, 6))
            pygame.draw.rect(superficie, (200, 235, 255), (int(self.x)+6, int(self.y)+58, self.w-12, 4))
        else:
            for p in self.particulas:
                p.dibujar(superficie)

    def rect_col(self):
        if not self.vivo:
            return pygame.Rect(-1000, -1000, 0, 0)
        return pygame.Rect(self.x, self.y, self.w, self.h)
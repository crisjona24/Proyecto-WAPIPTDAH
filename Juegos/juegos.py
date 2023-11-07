import pygame
import random
import math
import sys
import os

# Obtener la ruta de recursos assets
def resource_path(relative_path):
    # Construye la ruta relativa desde el directorio actual del script
    asset_path = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), relative_path)
    return os.path.abspath(asset_path)


# Cambiar el directorio de trabajo al directorio "PRUEBAEMAIL"
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.running = True

        self.init_assets()
        self.init_game_objects()
        self.run_game_loop()

    def init_assets(self):
        # Cargar todos los recursos aquí
        imagen = resource_path("assets/images/background.png")
        self.background = pygame.image.load(imagen)
        # Otros recursos...

    def init_game_objects(self):
        # Inicializar objetos del juego
        self.player = Player()
        self.enemies = [Enemy() for _ in range(10)]
        self.bullet = Bullet()
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()
                elif event.key == pygame.K_SPACE:
                    self.bullet.shoot(self.player.rect.centerx,
                                      self.player.rect.top)

    def update_game_objects(self):
        # Actualizar objetos del juego
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
            if self.bullet.collides_with(enemy):
                self.score += 1
                enemy.reset_position()
        self.bullet.update()

    def draw_game_objects(self):
        # Dibujar objetos del juego
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.bullet.draw(self.screen)

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        pygame.display.update()

    def run_game_loop(self):
        while self.running:
            self.handle_events()
            self.update_game_objects()
            self.draw_game_objects()
            self.clock.tick(60)


class Player:
    def __init__(self):
        # Inicializa el jugador
        self.image = pygame.image.load(
            resource_path("assets/images/space-invaders.png"))
        self.rect = self.image.get_rect()
        self.rect.centerx = 370
        self.rect.centery = 480
        self.speed = 5

    def move_left(self):
        # Mover a la izquierda
        self.rect.x -= self.speed

    def move_right(self):
        # Mover a la derecha
        self.rect.x += self.speed

    def update(self):
        # Actualizar lógica del jugador
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800

    def draw(self, screen):
        # Dibujar al jugador en la pantalla
        screen.blit(self.image, self.rect)


class Enemy:
    # Clase para representar a los enemigos
    def __init__(self):
        # Inicializar un enemigo
        self.image = pygame.image.load(
            resource_path("assets/images/enemy1.png"))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 736)
        self.rect.y = random.randint(50, 150)

    def update(self):
        # Actualizar lógica de los enemigos
        self.rect.x += random.randint(-1, 1)
        self.rect.y += random.randint(1, 3)

    def draw(self, screen):
        # Dibujar al enemigo en la pantalla
        screen.blit(self.image, self.rect)

    def reset_position(self):
        # Resetear la posición del enemigo
        self.rect.x = random.randint(0, 736)
        self.rect.y = random.randint(50, 150)


class Bullet:
    def __init__(self):
        # Inicializar la bala
        self.image = pygame.image.load(
            resource_path("assets/images/bullet.png"))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 480
        self.speed = 10
        self.state = "ready"

    def shoot(self, x, y):
        # Disparar la bala
        if self.state == "ready":
            self.rect.centerx = x
            self.rect.top = y
            self.state = "fire"

    def update(self):
        # Actualizar la bala
        if self.state == "fire":
            self.rect.y -= self.speed
        if self.rect.y < 0:
            self.state = "ready"

    def draw(self, screen):
        # Dibujar la bala en la pantalla
        if self.state == "fire":
            screen.blit(self.image, self.rect)

    def collides_with(self, enemy):
        # Verificar si la bala colisiona con un enemigo
        return self.rect.colliderect(enemy.rect)

if __name__ == "__main__":
    game = Game()

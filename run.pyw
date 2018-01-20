import pygame, random

pygame.init()
window = pygame.display.set_mode((600,400))
clock = pygame.time.Clock()


class Player:

    def __init__(self):
        self.size = 50

        self.y = (400 - self.size) / 2

    def update(self, window):
        self.move()
        self.show(window)

    def show(self, window):
        pygame.draw.rect(window, (50, 255, 50), (50, self.y, self.size, self.size))

    def move(self):
        key = pygame.key.get_pressed()

        speed = 10
        if key[pygame.K_UP]: self.y -= speed
        if key[pygame.K_DOWN]: self.y += speed

        self.y = max(min(self.y, 400 - self.size), 0)


    def touching_block(self, blocks):

        for block in blocks:

            # touching?
            if block.rect[0] <= 50 + self.size:
                if block.rect[0] + block.rect[2] >= 50:
                    if block.rect[1] <= self.y + self.size:
                        if block.rect[1] + block.rect[3] >= self.y:

                            return True
        return False
            


class Block_Handler:
    def __init__(self):
        self.blocks = []
        self.block_size = 50

    def manage(self, window):

        updated = []
        for block in self.blocks:
            block.update(window)

            if block.on_screen():
                updated.append(block)

        self.blocks = updated

    spawn_tick = 0
    def spawn(self):
        if self.spawn_tick >= 30 - score / 2:
            self.blocks.append(Block((600, random.randint(0, 400 - self.block_size), self.block_size, self.block_size)))
            self.spawn_tick = 0
        self.spawn_tick += 1

    def update(self, window):
        self.spawn()
        self.manage(window)
        

class Block:
    def __init__(self, rect):
        self.rect = list(rect)

    def move(self):
        self.rect[0] -= score / 5 + 5

    def show(self, window):
        pygame.draw.rect(window, (255, 100, 100), self.rect)

    def update(self, window):
        self.move()
        self.show(window)

    def on_screen(self):
        if self.rect[0] == self.rect[2] <= 0:
            return False
        return True

def message(window, text, pos, color):
    mes = font.render(text, 0, color)
    window.blit(mes, pos)

player = Player()
block_handler = Block_Handler()

score = 0
high_score = 0

font = pygame.font.SysFont(0, 30)

# Game loop
while True:

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()


    if player.touching_block(block_handler.blocks):
        # reset game
        player = Player()
        block_handler = Block_Handler()
        score = 0

    score += 1 / 30
    high_score = max(high_score, score)

    clock.tick(30)

    window.fill((255, 255, 255))

    block_handler.update(window)
    player.update(window)

    message(window, 'Score: ' + str(int(score)), (10, 10), (100, 100, 100))
    message(window, 'High: ' + str(int(high_score)), (10, 50), (200, 200, 200))

    pygame.display.update()
    pygame.display.set_caption('Score: ' + str(int(score)))

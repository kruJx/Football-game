import pygame, numpy, random, os, time

WIDTH = 1920
HEIGHT = 1080

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)#, pygame.FULLSCREEN
pygame.display.set_caption("Football with AI")

vec = pygame.math.Vector2

gamestate=0
score1=0
score2=0

my_font = pygame.font.SysFont('Comic Sans MS', 30)


class Button(pygame.sprite.Sprite):
    def __init__(self,text,posx,posy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((300,100))
        self.image.fill((200,200,255))
        self.text = my_font.render(text, 1, (255,255,255))
        self.image.blit(self.text, (100, 25))
        self.rect = self.image.get_rect()
        self.rect.center = (posx, posy)
    def update(self):
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(mouse):
                    return True
                     

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60,60))
        pygame.draw.circle(self.image, (0, 255, 0),(30,30),30)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/4, HEIGHT/2)
        self.pos = vec((WIDTH/4, HEIGHT/2))
        self.vel = vec(0,0)
        self.direction = vec(0,0)
        self.speed = 0
        self.radius = 30

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if self.speed < 8:
                self.speed+=1
            self.direction.y = -1
        elif keys[pygame.K_s]: 
            if self.speed < 8:
                self.speed+=1
            self.direction.y = 1
        else: 
            self.direction.y = 0
        if keys[pygame.K_a]: 
            if self.speed < 8:
                self.speed+=1
            self.direction.x = -1
        elif keys[pygame.K_d]: 
            if self.speed < 8:
                self.speed+=1
            self.direction.x = 1
        else: 
            self.direction.x = 0

    def update(self,dt):
        self.old_rect = self.rect.copy()

        self.move()

        if self.speed > 0 and self.direction.y == 0 and self.direction.x == 0:
            self.speed -= 1

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.vel = self.direction * self.speed * 60

        self.pos.x += int(self.vel.x) * dt
        self.pos.y += int(self.vel.y) * dt
        
        self.rect.center = self.pos

        self.collide_window()

    def collide_window(self):
        if self.rect.top < 0:
            self.rect.top = 0
            self.pos.y = self.rect.centery
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.pos.y = self.rect.centery
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.centerx
        if self.rect.right > WIDTH/2:
            self.rect.right = WIDTH/2
            self.pos.x = self.rect.centerx

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        pygame.draw.circle(self.image, (0, 0, 255),(15,15),15)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec((WIDTH/2, HEIGHT/2))
        self.vel = vec(0,0)
        self.direction = vec(0,0)
        self.speed = 0
        self.radius = 15

    def update(self,dt):
        self.old_rect = self.rect.copy()

        self.pos.x += int(self.vel.x) * dt
        self.pos.y += int(self.vel.y) * dt
        
        self.rect.center = self.pos

        self.collide_player()
        self.collide_window()
        self.collide_goal()

    def collide_goal(self):
        global score1, score2
        if pygame.sprite.collide_rect(self,goal1):
            score1+=1
            balls.remove(self)
            self.kill()
            ball=Ball()
            balls.add(ball)
        if pygame.sprite.collide_rect(goal2,self):
            score2+=1
            balls.remove(self)
            self.kill()
            ball=Ball()
            balls.add(ball)

    def collide_window(self):
        if self.rect.top < 0:
            self.rect.top = 0
            self.pos.y = self.rect.centery
            self.vel.y *= -1
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.pos.y = self.rect.centery
            self.vel.y *= -1
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.centerx
            self.vel.x *= -1
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.pos.x = self.rect.centerx
            self.vel.x *= -1

    def collide_player(self):
        if (self.pos.x - player.pos.x)**2 + (self.pos.y - player.pos.y)**2 < 45**2:
            self.direction.x = self.pos.x - player.pos.x
            self.direction.y = self.pos.y - player.pos.y
            self.direction = self.direction.normalize()
            self.vel.x = ((player.vel.x**2+player.vel.y**2)**(1/2))*self.direction.x*2
            self.vel.y = ((player.vel.x**2+player.vel.y**2)**(1/2))*self.direction.y*2

        if (self.pos.x - enemy.pos.x)**2 + (self.pos.y - enemy.pos.y)**2 < 45**2:
            self.direction.x = self.pos.x - enemy.pos.x
            self.direction.y = self.pos.y - enemy.pos.y
            self.direction = self.direction.normalize()
            self.vel.x = ((enemy.vel.x**2+enemy.vel.y**2)**(1/2))*self.direction.x*2
            self.vel.y = ((enemy.vel.x**2+enemy.vel.y**2)**(1/2))*self.direction.y*2

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60,60))
        pygame.draw.circle(self.image, (255, 0, 0),(30,30),30)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (3*WIDTH/4, HEIGHT/2)
        self.pos = vec((3*WIDTH/4, HEIGHT/2))
        self.vel = vec(0,0)
        self.direction = vec(0,0)
        self.speed = 8
        self.radius = 30

    def update(self,dt):
        for sprite in balls:
            sprite1=sprite
        self.old_rect = self.rect.copy()
        self.direction.x = -(self.pos.x - sprite1.pos.x)
        self.direction.y = -(self.pos.y - sprite1.pos.y)*2
        if sprite1.pos.x>WIDTH-50 and sprite1.pos.y > HEIGHT-50 or sprite1.pos.y < 50 and sprite1.pos.x>WIDTH-50:
            self.direction.x = -1
            self.direction.y = HEIGHT/2-self.pos.y
        if sprite.pos.y - 10 < self.pos.y < sprite.pos.y + 10 and sprite.pos.x > WIDTH-50:
            self.direction.y = HEIGHT/2-self.pos.y
        if sprite.pos.x - 10 < self.pos.x < sprite.pos.x + 10 and sprite.pos.y > HEIGHT-50:
            self.direction.x = WIDTH-self.pos.x
        if sprite.pos.x - 10 < self.pos.x < sprite.pos.x + 10 and sprite.pos.y < 50:
            self.direction.x = WIDTH-self.pos.x

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.vel = self.direction * self.speed * 60

        self.pos.x += int(self.vel.x) * dt
        self.pos.y += int(self.vel.y) * dt
        
        self.rect.center = self.pos

        self.collide_window()

    def collide_window(self):
        if self.rect.top < 0:
            self.rect.top = 0
            self.pos.y = self.rect.centery
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.pos.y = self.rect.centery
        if self.rect.left < WIDTH/2:
            self.rect.left = WIDTH/2
            self.pos.x = self.rect.centerx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.pos.x = self.rect.centerx

class Goal(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,150))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (pos, HEIGHT/2)
        self.pos = vec((pos, HEIGHT/2))

def menu():
    global gamestate
    start_button=Button("Play",WIDTH/4,HEIGHT/2)
    quit_button=Button("Quit",3*WIDTH/4,HEIGHT/2)
    if start_button.update():
        gamestate=1
        start_button.kill()
        quit_button.kill()
    screen.blit(start_button.image,(start_button.rect.x,start_button.rect.y))
    screen.blit(quit_button.image,(quit_button.rect.x,quit_button.rect.y))
    if quit_button.update():
        global running
        running = False
        
def gamestart():
    global player,enemy,ball,goal1,goal2,score1,score2,gamestate,players,balls,enemies,goals
    if score1 !=0 or score2 !=0:
        enemy.kill()
        player.kill()
        ball.kill()
        goal1.kill()
        goal2.kill()
        score1=0
        score2=0

    players = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    goals = pygame.sprite.Group()

    player=Player()
    players.add(player)

    ball=Ball()
    balls.add(ball)

    enemy=Enemy()
    enemies.add(enemy)

    goal1=Goal(5)
    goal2=Goal(WIDTH-5)
    goals.add(goal1)
    goals.add(goal2)

    gamestate = 2

def game():
    global gamestate
    players.update(dt)
    balls.update(dt)
    enemies.update(dt)
    
    screen.fill((30,30,30))
    players.draw(screen)
    balls.draw(screen)
    goals.draw(screen)
    enemies.draw(screen)

    score1_text = my_font.render("Your score: {0}".format(score2), 1, (255,255,255))
    screen.blit(score1_text, (15, 10))
    score2_text = my_font.render("Enemy score: {0}".format(score1), 1, (255,255,255))
    screen.blit(score2_text, (WIDTH-256, 10))

    if score1 == 20:
        gamestate = 3
    if score2 == 20:
        gamestate = 3

def gameend():
    if score2 == 20:
        gameend_text = my_font.render("You win! Would you like to play again?", 1, (255,255,255))
        screen.blit(gameend_text, (400, HEIGHT/2-105))
    if score1 == 20:
        gameend_text = my_font.render("Oh you lost :( But you can try again", 1, (255,255,255))
        screen.blit(gameend_text, (400, HEIGHT/2-105))

        global gamestate
    start_button=Button("Play",WIDTH/4,HEIGHT/2)
    quit_button=Button("Quit",3*WIDTH/4,HEIGHT/2)
    if start_button.update():
        gamestate=1
        start_button.kill()
        quit_button.kill()
    screen.blit(start_button.image,(start_button.rect.x,start_button.rect.y))
    screen.blit(quit_button.image,(quit_button.rect.x,quit_button.rect.y))
    if quit_button.update():
        global running
        running = False

last_time = time.time()
running = True

while running == True:
    dt = time.time() - last_time
    last_time = time.time()
    
    for event in pygame.event.get(eventtype=pygame.QUIT):
        if event:
           running = False

    if gamestate == 0:
        menu()
           
    if gamestate == 1:
        gamestart()

    if gamestate == 2:
        game()

    if gamestate == 3:
        gameend()
    
    pygame.display.update()


pygame.quit()

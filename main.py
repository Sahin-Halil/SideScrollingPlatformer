#Dinosaur player images by Arks
#https://arks.itch.io/dino-characters
#Twitter: @ScissorMarks

import pygame, random  #imports the pygame library

game_map =[['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],                      
           ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
           ['0','0','0','0','2','0','0','0','0','0','0','0','0','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','2','2','2','0','0','0','0','0','0','2'],
           ['0','0','0','0','1','2','2','2','2','2','2','2','2','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','1','1','1','0','0','0','0','0','0','0'],
           ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','0','0','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
           ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','0','0','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
           ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','0','0','1','1','0','0','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
           ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','0','0','1','1','0','0','0','0','0','0','0','0','0','0','2','0','0','0'],
           ['0','0','2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','2','2','0','0','0','0','0','0','1','1','0','0','1','1','2','2','2','2','2','2','2','2','2','2','1','0','0','2'],
           ['0','0','1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1','1','1','0','0','0','0','0','0','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
           ['0','0','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','0','0','0','0','0','0','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
           ['0','0','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','0','0','2','2','0','0','0','0','0','0','2','0','0','0','0','0','0','2','0','0','0','0','0','2','2','0'],
           ['0','0','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','0','0','1','1','0','0','0','0','0','0','1','2','2','2','2','2','2','1','0','0','0','0','0','1','1','0']]

#variables for player
moveright = False  #declared a variable to store boolean value for if player is moving right
moveleft = False  #declared a variable to store boolean value for if player is moving left
fire = False #declared a variable to store boolean value for if character attacks

#constant variables
dirt_image = pygame.image.load("dirt.png")
grass_image = pygame.image.load("grass.png")
brick_size = dirt_image.get_width()
width = 600 #declared a variable to store width of game screen
height = 400 #declared a variable to store height of game screen
size_of_screen = (width, height)  #declared a variable to store the height and width of the screen
bg_colour = (222, 203, 104)  #declared a variable to store the bg colour of screen
pf_colour = (0, 0, 0) #
FPS = 60  #declared variable to store the speed at which game runs
gravity = 0.5 #declared variable to store the rate at which player falls down
list_of_heals = [20,40,50,10,-5,-10,-20,30]
list_of_powerups = [1, 0.01, 0.5, 0, -0.5, -1]
damage_coefficient = 0
scroll_limit = 200
scroll_screen = 0

#init
pygame.init()  #all imported python modules are initialised
screen = pygame.display.set_mode(size_of_screen)  #a game window is initialised
pygame.display.set_caption("Platform Game")  #game windows caption is set
system_clock = pygame.time.Clock()  #declared variable to control speed of game
health_brick = pygame.image.load('health brick.png').convert_alpha()
powerup_brick = pygame.image.load("powerup.png").convert_alpha()
bricks = {
  'heal' : health_brick,
  'powerup' : powerup_brick
}
font = pygame.font.SysFont("", 30)
display = pygame.Surface((300,200))

def draw_writings(writings, font, colour, x, y):
  image = font.render(writings, True, colour)
  image = pygame.transform.scale(image, (80, 10))
  display.blit(image, (x,y))

class Characters(pygame.sprite.Sprite):  #base class is created and inherits from sprite class
    def __init__(self, char, x, y, scale, speed, health):  #values are put in the constructor method
        pygame.sprite.Sprite.__init__(self)  #constructor from sprite class is called
        self.vision = pygame.Rect(0, 0, 75, 20)
        self.idle = False
        self.idle_counter = 0
        self.counter = 0
        self.health = health #attribute initialised to store health of character
        self.max_health = self.health #attribute initialised to store max_health of character
        self.attack_cooldown = 0 #attribute initialised to store cooldown of each character attack
        self.direction = 1 #attribute initialised to store direction characters face when they move left/right
        self.air = True #attribute init
        self.char = char
        self.life = True  #attribute initialised to store state of characters life
        self.jump = False
        self.vv = 0
        self.speed = speed  #attribute for character is initialised to store speed of character
        self.spin = False  #attribute initialised to store direction character is moving
        self.animation_list = []  #attribute initialised to store all sequence of animations for sprites within 2D list
        self.index = 0  #attribute initialised to locate index of sequences within specific animation
        self.activity = 0  #attribute initialised to locate index of animation sequences within animation list
        self.time = pygame.time.get_ticks()  #attribute declared to store current time game has been running
        types_of_animation = ['idle', 'moving', 'jump', "death"]
        for ani in types_of_animation:
            templist = []  #declared a variable which will be used to store a temporary list
            for x1 in range(10):  #loops through numbers 0-10
                try:
                    img = pygame.image.load(f'{self.char}/{self.char}.{ani}.sprite_{x1}.png').convert_alpha() #loads an image from your file
                    img = pygame.transform.scale(img, (int(scale), int(scale)))  #resizes your image
                    templist.append(img)  #resized image is added to temporary list
                except:
                    break
            self.animation_list.append(templist)  #adds all images passed into temporary list to main one
        self.img = self.animation_list[self.activity][self.index]  #attribute initialised to store intial image of sprite
        self.rect = self.img.get_rect()  #a rectangle is formed around sprite
        self.rect.center = (x, y)  #centre of rectangle varies with the position of sprite
        self.rect = self.rect.inflate(-5,-5)
      
    def movecharacter(self, moveleft, moveright, tiles):  #new method defined to move character
        global scroll_screen 
       #change in movement variables
        #scroll_screen = 0
        dy = 0  #declared a variable to store the change in distance travelled in the vertical direction
        dx = 0  #declared a variable to store the change in distance travelled in the horizontal direction

        #movement variables are updated if there are movements left or right
        if moveleft:  #checks to see if user has inputted "a" key
            dx -= self.speed  #character has moved backwards
            self.direction = -1
            self.spin = True  #character changed direction(faces left)
           
        if moveright:  #checks to see if the user has inputted "d" key
            dx += self.speed  #character has moved forward
            self.spin = False  #character changed direction(faces right)
            self.direction = 1
           
        #these variables are for jumping
        if self.jump and not self.air:  #checks to see if user has inputted "w" key and is in mid-air
            self.vv = -8  #determines how high the character can jump
            self.jump = False  #this variable is set to false so character doesn't fly of the screen
            self.air = True  #this variable is set to true so character can't infinitely jump while in mid-dair

        if self.vv > 0 and self.air == 0:
          self.vv = 4
        
        #gravity is applied here
        self.vv += gravity  #vertical velocity is incremented until character starts to move in opposite direction
        if self.vv > 9:  #checks to see if character's vertical velocity has passed 9
            self.vv = 9  #vertical velocity is capped to 9
        dy += self.vv  #change in distance travelled in vertical direction is increased
        
        #rectangle position is updated
        self.rect.x += dx  #position of rectangle has changed in horizontal direction
        hitlist = self.collision_test(tiles)
        for tile in hitlist:
             if dx > 0:
               self.rect.right = tile.left
             elif dx < 0:
               self.rect.left = tile.right
        self.rect.y += dy  #position of rectangle has changed in vertical direction 
        hitlist = self.collision_test(tiles)
        for tile in hitlist:
          if dy > 0:
            self.rect.bottom = tile.top
            self.air = False
          elif dy < 0:
            self.rect.top = tile.bottom
            self.air = True

        if self.char == 'player':
          if self.rect.right > 0.5*(width - scroll_limit) or self.rect.left < (scroll_limit*0.4):
            self.rect.x -=dx
            for enemy in enemies_group:
              enemy.rect.x -=dx
            for cube in item_cube_group:
              cube.rect.x -=dx
            scroll_screen -= dx
        return scroll_screen
      
    def alive_check(self):
      if self.health <=0:
        self.life = False
        self.speed = 0
        self.health = 0
        self.update_activity(3)
  
    def attack(self):  
      if not self.attack_cooldown:
        self.attack_cooldown = 50
        ball = Fireball(self.rect.centerx + self.rect.size[0] * self.direction, self.rect.centery, self.direction, self.spin)
        fireball_group.add(ball)

    def collision_checker(self):
      if pygame.sprite.spritecollide(player, fireball_group, False):
        if player.life:
          player.health -=2
          fireball_group.remove()
  
      for enemy in enemies_group:
        if pygame.sprite.spritecollide(enemy, fireball_group, False):
          if enemy.life: 
            enemy.health -=3 + damage_coefficient
      
    def cooldown(self):
     if self.attack_cooldown > 0:
       self.attack_cooldown -=1

    def collision_test(self, tiles):
      hitlist = []
      for tile in tiles:
        if self.rect.colliderect(tile):
          hitlist.append(tile)
      return hitlist
  
    def animation(self):  #new method defined to change characters animation
        animation_timer = 100  #declared variable to store time for how long character is in each animation
        self.img = self.animation_list[self.activity][self.index]  #characters animation is updated
        if pygame.time.get_ticks() - self.time > animation_timer:  #checks to see if it is time to update sprites
            self.time = pygame.time.get_ticks()  #time game has been running for is redefined
            self.index += 1  #index for current animation sequence is increased so next animation can be outputted
        if self.index >= len(self.animation_list[self.activity]):  #checks to see if index value has passed the highest index of animation sequence list
          if self.activity == 3:
            self.index = len(self.animation_list[self.activity]) -1
          else:
           self.index = 0  #index is reset back to initial value

    def update_activity(self, updated_activity):  #new method defined to update which animation sequence character is in
        if updated_activity != self.activity:  #checks if current activity is equal to new activity
            self.activity = updated_activity  #value for activity is updated
            self.index = 0  #index is reset to initial value
            self.time = pygame.time.get_ticks()  #time game has been running is updated

    def enemy_ai(self, tiles):
      if self.life and player.life:
       if random.randint(1, 300) == 1 and self.idle_counter <= 0:
         self.idle = True
         self.idle_counter = 100
         self.update_activity(0)
         
         
       if self.vision.colliderect(player.rect):
         self.update_activity(0)
         self.attack()
       else:
         if self.idle == False:
              if self.direction == 1:
                  moving_rightai = True
              else:
                 moving_rightai = False
              moving_leftai = not moving_rightai
              self.movecharacter(moving_leftai, moving_rightai, tiles)
              self.update_activity(1)
              self.counter += 1
              self.vision.center = (self.rect.centerx +  32.5 * self.direction, self.rect.centery)
              #pygame.draw.rect(display, 'red', self.vision)

              if self.counter > brick_size:
                self.direction *= -1
                self.counter *= -1 
         else:
          self.idle_counter -= 1
          if self.idle_counter <= 0:
           self.idle = False
            
    def draw(self):  #new method defined to draw images to screen
        display.blit(pygame.transform.flip(self.img, self.spin, False), (self.rect.x, self.rect.y))  #draws image to screen
        #pygame.draw.rect(display, "red", self.rect, 1)

class Health_bar():
  def __init__(self, x, y, health, maxhealth):
    self.x = x
    self.y = y
    self.maxhealth = maxhealth
    self.health = health

  def draw(self, health):
    self.health = health
    hratio = self.health/self.maxhealth
    pygame.draw.rect(display, 'black', (self.x-2, self.y-2, 54, 14))
    pygame.draw.rect(display, 'red', (self.x, self.y, 50, 10))
    pygame.draw.rect(display, 'green', (self.x, self.y, 50*hratio, 10))
    
class Cubes(pygame.sprite.Sprite):
  def __init__(self, item, x, y):
         pygame.sprite.Sprite.__init__(self)
         self.item = item
         self.x = x
         self.y = y
         self.image = bricks[self.item]
         self.image = pygame.transform.scale(self.image, (20,20))
         self.rect = self.image.get_rect()
         self.rect.center = (x, y)

  def update(self):
    global damage_coefficient  
    if pygame.sprite.collide_rect(self, player):
        if self.item == "heal":
          player.health += list_of_heals[random.randint(0,7)]
          if player.health > player.max_health:
            player.health = player.max_health
        if self.item =="powerup":
          damage_coefficient += list_of_powerups[random.randint(0,5)]
          if damage_coefficient > 2.5:
            damage_coefficient = 2.4
          elif damage_coefficient > 1.1:
            damage_coefficient = 1.1
        self.kill()
    
class Fireball(pygame.sprite.Sprite):
  def __init__(self, x, y, direction, spin):
        pygame.sprite.Sprite.__init__(self)
        self.spin = spin    
        self.direction = direction
        self.speed = 5
        self.images = []
        self.index = 0
        for x1 in range(1, 9):
           img = pygame.image.load(f'fireball images/fireball_{x1}.png').convert_alpha()
           img = pygame.transform.flip(img, self.spin, False)
           img = pygame.transform.scale(img, (20,20))
           self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0

  def update(self, tiles):
    for tile in tiles:
      if tile.colliderect(self.rect):
        self.kill()
    
    if self.counter >= self.speed and self.index < len(self.images) - 1:
              self.counter = 0
              self.index += 1
              self.image = self.images[self.index]
    if self.index >= len(self.images) - 1 and self.counter >= self.speed:
              self.kill()
    self.rect.x += (self.direction * self.speed)
    if self.rect.right < 0 or self.rect.left > width:
      self.kill()
    self.counter+=1

fireball_group = pygame.sprite.Group() 
enemies_group = pygame.sprite.Group()
item_cube_group = pygame.sprite.Group()

item_cube = Cubes("heal", 450, 155)
item_cube_group.add(item_cube)
item_cube2 = Cubes("heal", 700, 155)
item_cube_group.add(item_cube2)
item_cube3 = Cubes("powerup", 60, 15)
item_cube_group.add(item_cube3)
      
player = Characters("player", 40, 100, 25, 3, 100)
health_cube = Health_bar(10, 10, player.health, player.max_health)
enemy = Characters("enemy0", 150, 30, 25, 2, 100)
enemy2 = Characters("enemy0", 150, 100, 25, 2, 100)
enemies_group.add(enemy)
enemies_group.add(enemy2)
enemy3 = Characters("enemy1", 600, 100, 25, 2, 100)
enemy4 = Characters("enemy1", 600, 180, 25, 2, 100)
enemies_group.add(enemy3)
enemies_group.add(enemy4)

run = True  #declared a variable to store a boolean value to determine state of game
while run:  #game loop-infinite loop which runs game until game is finished
    #draw
    display.fill(bg_colour)  #displays the specified bg colour
    pygame.draw.line(screen, pf_colour, (0, 400), (width, 400))
    draw_writings(f'DAMAGE_BOOST: {damage_coefficient}', font, "white", 10, 25)
    health_cube.draw(player.health)
    item_cube_group.update()
    item_cube_group.draw(display) 
    player.draw() #calls draw method from base class so player is drawn on screen
    tile_rect = [] #list declared to store any tiles for collision
    y = 0 #variable declared and set to 0 so tiles are drawn in the correct positions
    for row in game_map:
      x = 0 #variable declared and set to 0 so tiles are drawn in the correct positions
      for tile in row:
        if tile == '2':
          display.blit(grass_image, (x*brick_size + scroll_screen, y*brick_size))
        if tile == '1':
          display.blit(dirt_image, (x*brick_size + scroll_screen, y*brick_size))
        if tile != "0":
          tile_rect.append(pygame.Rect(x*brick_size+scroll_screen, y*brick_size, brick_size, brick_size))
        x += 1  #variable is incremented by one
      y += 1 #variable is icremented by one
    for enemy in enemies_group:
      enemy.collision_checker() #calls collision_checker method from base class to check if characters have been hit
      enemy.alive_check() #calls alive_check method from base class to check if enemy is alive 
      enemy.animation() #calls animation method from base class so enemies animation is updated
      enemy.draw() #calls draw method from base class so enemy is drawn on screen
      enemy.enemy_ai(tile_rect) #calls enemy_ai method from base class to update enemies movement
      enemy.cooldown() #calls cooldown method from base class to check if attack is on cooldown
    fireball_group.update(tile_rect) #calls update method from Fireball class to check if fireball goes through walls or update the fireball animation
    fireball_group.draw(display) #calls draw method from Fireball class to draw fireball on to screen
    surf = pygame.transform.scale(display, size_of_screen) #variable declared to 
    screen.blit(surf, (0,0)) #
    pygame.display.flip() #the contents of entire display are updated
    system_clock.tick(FPS) #function declared to limit the speed game runs at
    player.alive_check() #calls alive_check method from base class to check if player is alive
    player.animation()  #calls animation method from base class so players animation is updated
    player.cooldown() #calls cooldown method from base class to check if attack is on cooldown
    if player.life:  #checks to see if player is alive 
        if fire:
          player.attack() 
        if player.air:  #checks to see if player is in air
            player.update_activity(2) #updates the value of activity attribute within base class
        elif moveleft or moveright: #checks if player is moving
            player.update_activity(1) #updates the value of activity attribute within base class
        else:
            player.update_activity(0) #current value of acitivity remains 0
        scroll_screen = player.movecharacter(moveleft, moveright, tile_rect)  #calls movecharacter method from base class so character can move
    #input
    for event in pygame.event.get():  #loops through all the events registered by user
        #quit game
        if event.type == pygame.QUIT:  #checks to see if user has selected the exit button
            run = False  #state of game is set to false to signal game window has been closed
        #keyboard inputs
        if event.type == pygame.KEYDOWN:  #checks to see if user has inputted a key
            if event.key == pygame.K_a:  #checks to see if user has inputted "a" key
               moveleft = True  #variable is set to true so character moves left
            if event.key == pygame.K_d:  #checks to see if user has inputted "d" key
               moveright = True  #variable is set to true so character moves right
            if event.key == pygame.K_w and player.life:  #checks to see if the user has inputted "w" key
                player.jump = True  #variable is set to true so character jumps
            if event.key == pygame.K_SPACE: #checks to see if the user has inputted the "space" key
              fire = True #variable is set to true so character stops jumping
        #keyboard input released
        if event.type == pygame.KEYUP:  #checks to see if user released a key
            if event.key == pygame.K_a:  #checks to see if user has inputted "a" key
                moveleft = False  #variable is set to false so character stops moving left
            if event.key == pygame.K_d:  #checks to see if user has inputted the "d" key
                moveright = False  #variable is set to false so character stops moving right
            if event.key == pygame.K_SPACE: #checks to see if the user has inputted the "space" key
              fire = False #variable is set to false so character stops jumping

#quit
pygame.quit()  #all pygame modules are uninitialised

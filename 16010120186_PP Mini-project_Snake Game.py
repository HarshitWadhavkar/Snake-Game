import pygame,sys,random
pygame.init()

class position:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __add__(self,other):
        return position((self.x+other.x),(self.y+other.y))
    def __sub__(self,other):
        return position((self.x-other.x),(self.y-other.y))
    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

class cursor:
    def __init__(self,x,y): 
        self.x = x
        self.y = y
        self.position = position(self.x,self.y)
        self.menu1 = True
    def up(self):
        if self.position == position(4,6):
            self.position = position(4,9)
        elif self.position != position(14,7.5):
            self.position += position(0,-1)
    def down(self):
        if self.position == position(4,9):
            self.position = position(4,6)
        elif self.position != position(14,7.5):
            self.position += position(0,1)
    def left(self):
        if self.menu1 == False:
            self.position = position(4,6)
            self.menu1 =  True
    def right(self):
        if self.menu1:
            self.position = position(14,7.5)
            self.menu1 = False
    def drawcursor(self):
        cursor_rect = pygame.Rect((self.position.x)*cs,(self.position.y)*cs,cs,cs)
        pygame.draw.ellipse(screen,(255,0,0),cursor_rect)
    def cursorpos(self):
        return self.position.y

class snake:
    def __init__(self):
        self.body = [position(10,10),position(9,10),position(8,10)]
        self.direction = position(0,0)
        self.new_block = False
        self.drawsnake()
    def drawsnake(self):
        for block in self.body:
            xpos = (block.x)*cs
            ypos = (block.y)*cs
            block_rect = pygame.Rect(xpos,ypos,cs,cs)
            pygame.draw.rect(screen,(0,0,255),block_rect)
    def movesnake(self):
        if self.direction != position(0,0):
            if self.new_block:
                newbody = self.body[:]
                newbody.insert(0,newbody[0]+self.direction)
                self.body = newbody[:]
                self.new_block = False
            else:
                newbody = self.body[:-1]
                newbody.insert(0,newbody[0]+self.direction)
                self.body = newbody[:]
            if self.body[0].x > cn-1:
                self.body[0].x = -1
                self.body[0] += position(1,0)
            if self.body[0].x < 0:
                self.body[0].x = cn+1
                self.body[0] += position(-1,0)
            if self.body[0].y > cn-1:
                self.body[0].y = -1
                self.body[0] += position(0,1)
            if self.body[0].y < 0:
                self.body[0].y = cn+1
                self.body[0] += position(0,-1)
    def addblock(self):
        self.new_block = True                

class fruit:
    def __init__(self):
        self.randomize()
        self.drawfruit()
    def randomize(self):
        self.x = (random.randint(0,cn-1))
        self.y = (random.randint(0,cn-1))
        self.fruitposition = position(self.x,self.y)        
    def drawfruit(self):
        fruit_rect = pygame.Rect((self.x)*cs,(self.y)*cs,cs,cs)
        pygame.draw.rect(screen,(255,0,0),fruit_rect)

class obstacles:
    def __init__(self,x):
        self.mapblocks = []
        if x == 2:
            for j in range(0,cn+1):
                for i in range(0,cn,cn-1):
                    self.mapblocks.append(position(i,j))
                self.mapblocks.append(position(j,0))
                self.mapblocks.append(position(j,cn-1))
        if x == 3:
            for j in range(0,int(cn/3)):
                self.mapblocks.append(position(j,cn-7))
                self.mapblocks.append(position(j,6))
                self.mapblocks.append(position(j+int(2*cn/3),cn-7))
                self.mapblocks.append(position(j+int(2*cn/3),6))
                self.mapblocks.append(position(cn-7,j+int(cn/3)))
                self.mapblocks.append(position(6,j))
                self.mapblocks.append(position(6,j+int(2*cn/3)))
        if x == 4:
            for j in range(0,cn+1):
                self.mapblocks.append(position(int(cn/3)-1,j))
                self.mapblocks.append(position(int(2*cn/3),j))
                self.mapblocks.append(position(j,int(cn/3)-1))
                self.mapblocks.append(position(j,int(2*cn/3)))
            for i in range(int(cn/3)-3,int(2*cn/3)+3):
                for j in range(int(cn/3)-1,int(2*cn/3)+1):
                    if position(i,j) in self.mapblocks:
                        self.mapblocks.remove(position(i,j))                 
            for j in range(0,7):
                self.mapblocks.append(position(7+j,14))
    def drawobstacle(self):
        for block in self.mapblocks:
            xpos = (block.x)*cs
            ypos = (block.y)*cs
            block_rect = pygame.Rect(xpos,ypos,cs,cs)
            pygame.draw.rect(screen,(75,185,75),block_rect)
                          
class game(snake,fruit,obstacles):
    def __init__(self,x):
        self.running = True
        fruit.__init__(self)
        snake.__init__(self)
        obstacles.__init__(self,x)
        self.level = x
    def draw(self):
        self.drawfruit()
        self.drawsnake()
        self.drawobstacle()
        self.drawscore(self.level,len(self.body))
    def eat(self):
        if self.fruitposition == self.body[0] :   
            self.addblock()
    def checksnake(self):
        if self.body[0] in self.mapblocks:
            self.running = False
        for block in self.body[1:]:
            if self.body[0] == block:
                self.running = False
    def checkfruit(self):
        if self.fruitposition in self.mapblocks:
            self.randomize()
        for block in self.body:
            if self.fruitposition == block:
                self.randomize()
    def update(self):
        self.checksnake()
        self.eat()
        self.checkfruit()
        self.movesnake()
    def drawscore(self,x,y):
        Score = font.render('Level '+(str(x))+' '*35+'Score: '+str(y-3), True, (255,0,0))
        Score_rect = Score.get_rect()
        Score_rect.topleft = (1*cs,0)
        screen.blit(Score,Score_rect)
    
def menu():
    while True:
        screen.fill((0,0,0))
        menutext  = font.render('MENU', True,(255,0,0))
        menu_rect = menutext.get_rect()
        menu_rect.topleft = (9*cs,2*cs)
        screen.blit(menutext,menu_rect)
        for lvl in range(1,5):
            text = font.render(('Level '+str(lvl)), True, (255,0,0))
            lvl_rect = text.get_rect()
            lvl_rect.midleft = (6*cs,(5.5+lvl)*cs)
            screen.blit(text,lvl_rect)
        quit_button  = font.render('Quit', True,(255,0,0))
        quit_rect = quit_button.get_rect()
        quit_rect.midleft = (16*cs,8*cs)
        screen.blit(quit_button,quit_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:    
                    cursor.up()             
                if event.key == pygame.K_DOWN:
                    cursor.down()
                if event.key == pygame.K_LEFT:
                    cursor.left()
                if event.key == pygame.K_RIGHT:
                    cursor.right()
                if event.key == pygame.K_RETURN:
                    if cursor.position == position(14,7.5):
                        pygame.quit()
                        sys.exit()
                    else:
                        lvl_select = cursor.position.y - 5
                        gamestart(game,lvl_select)
        cursor.drawcursor()       
        pygame.display.update()
        clock.tick(60)
        
def gamestart(game,x):
    game = game(x)   
    while game.running:
                screen.fill(pygame.Color('light green'))
                game.draw() 
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == UPDATE:
                        game.update()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            if game.direction != position(0,1):
                                game.direction = position(0,-1)
                        if event.key == pygame.K_DOWN:
                            if game.direction != position(0,-1):
                                game.direction = position(0,1)
                        if event.key == pygame.K_LEFT:
                            if game.direction != position(0,0) and game.direction != position(1,0):
                                game.direction = position(-1,0)
                        if event.key == pygame.K_RIGHT:
                            if game.direction != position(-1,0):
                                game.direction = position(1,0)                
                pygame.display.update()
                clock.tick(60)     

cs = 30
cn  = 21
screen = pygame.display.set_mode((cs*cn,cs*cn))
clock  = pygame.time.Clock()
cursor = cursor(4,6)
font = pygame.font.SysFont('ariel',50)
UPDATE = pygame.USEREVENT
pygame.time.set_timer(UPDATE,150)
menu()






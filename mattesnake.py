#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      VEGABR
#
# Created:     19.12.2022
# Copyright:   (c) VEGABR 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame
import random

pygame.init()
screenw = 800
screenh = 600
screen = pygame.display.set_mode((screenw,screenh))


font = pygame.font.SysFont(None, 36)
oppgavefont = pygame.font.SysFont(None,45)
loss = font.render("YOU LOSE", True, (64,150,200))
#img = font.render('hello', True, BLUE)
#screen.blit(img, (20, 20))

class Snake():
    def __init__(self,mode):
        self.mode = mode
        self.width = 20
        self.height = 20
        self.rect = pygame.rect.Rect(screenw/2,screenh/2,self.width,self.height)
        self.body = []
        self.retning = "up"
        self.speed = 200
        self.bunnstart = 1
        self.toppstart = 10
        self.bunn = self.bunnstart
        self.topp = self.toppstart

    def draw(self):
        pygame.draw.rect(screen,(64,64,64),self.rect)
        pygame.draw.rect(screen,(0,0,0),self.rect,1)
        if len(self.body) > 0:
            for piece in self.body:
                pygame.draw.rect(screen,(0,0,0),piece)

    def move(self):
        if len(self.body) > 0:
            i = len(self.body)-1
            while i > 0:
                self.body[i].x = self.body[i-1].x
                self.body[i].y = self.body[i-1].y
                i-=1
            self.body[0].x = self.rect.x
            self.body[0].y = self.rect.y
        if self.retning == "up":
            self.rect.y = self.rect.y - self.height
            self.canturny = False
            self.canturnx = True
        elif self.retning == "down":
            self.rect.y = self.rect.y + self.height
            self.canturny = False
            self.canturnx = True
        elif self.retning == "right":
            self.rect.x = self.rect.x + self.width
            self.canturnx = False
            self.canturny = True
        elif self.retning == "left":
            self.rect.x = self.rect.x - self.width
            self.canturnx = False
            self.canturny = True
        if self.rect.x > screenw-self.width:
            self.rect.x = 0
        if self.rect.x < 0:
            self.rect.x = screenw-self.width
        if self.rect.y < 0:
            self.rect.y = screenh-self.height
        if self.rect.y > screenh-self.height:
            self.rect.y = 0

    def grow(self):
        if len(self.body) == 0:
            self.body.append(pygame.rect.Rect(self.rect.x,self.rect.y,self.width,self.height))
        else:
            self.body.append(pygame.rect.Rect(self.body[len(self.body)-1].x,self.body[len(self.body)-1].y,self.width,self.height))
        if self.speed > 80:
            self.speed -= 10
        if self.mode == "pluss":
            if len(self.body)%3 == 0:
                self.bunn += 1
            else:
                self.topp += 1
            print("bunn ",self.bunn,"    topp ",self.topp)

    def hit(self):
        global apple
        global oppgave

        for obj in oppgave.feilrects:
            if self.rect.colliderect(obj):
                self.body = []
                oppgave = Pluss(snake.bunn,snake.topp,snake.mode)
                self.speed = 200
                self.bunn = self.bunnstart
                self.topp = self.toppstart
        i = 0
        for piece in self.body:
            if self.rect.colliderect(piece):
               self.body = []
               self.speed = 200
               self.bunn = self.bunnstart
               self.topp = self.toppstart
               print(i)
               i += 1
        if self.rect.colliderect(apple.rect):
            self.grow()
            apple = Apple()
        if self.rect.colliderect(oppgave.svarrect):
            self.grow()
            oppgave = Pluss(snake.bunn,snake.topp,snake.mode)


class Apple():
    def __init__(self):
        self.rect = pygame.rect.Rect(random.randint(0,screenh/20-1)*20,random.randint(0,screenh/20-1)*20,20,20)
        self.color = (255,0,0)

    def draw(self):
        pygame.draw.rect(screen,self.color,self.rect)
class Pluss():
    def __init__(self,bunn,topp,mode):
        self.mode = mode
        if self.mode == "pluss":
            self.ledd1 = random.randint(bunn,topp)
            self.ledd2 = random.randint(bunn,topp)
            self.svar = self.ledd1+self.ledd2
            self.tasktxt = oppgavefont.render(str(self.ledd1)+" + "+str(self.ledd2)+" = ??",True,(0,0,0))
        elif self.mode == "gange":
            self.ledd1 = random.randint(1,10)
            self.ledd2 = random.randint(1,10)
            self.svar = self.ledd1*self.ledd2
            self.tasktxt = oppgavefont.render(str(self.ledd1)+" x "+str(self.ledd2)+" = ??",True,(0,0,0))
        while True:
            self.feilesvar = [random.randint(int(self.svar-self.svar/2),int(self.svar+self.svar/2)) for i in range(3)]
            if self.svar not in self.feilesvar:
                break
        self.taskpos = (screenw/2-self.tasktxt.get_width()/2,1)
        self.taskrect = pygame.rect.Rect(self.taskpos[0],self.taskpos[1],self.tasktxt.get_width(),self.tasktxt.get_height())
        self.svartxt = font.render(str(self.svar),True,(0,0,0))
        self.svarpos = (random.randint(0,screenw-30),random.randint(0,screenh-30))
        self.feilesvartxt = [font.render(str(num),True,(0,0,0)) for num in self.feilesvar]
        self.feilpos = [(random.randint(0,screenw-30),random.randint(0,screenh-30)) for txt in self.feilesvartxt]
        self.svarrect = pygame.rect.Rect(self.svarpos[0], self.svarpos[1], self.svartxt.get_width(), self.svartxt.get_height())
        self.feilrects = [pygame.rect.Rect(self.feilpos[i][0],self.feilpos[i][1],self.feilesvartxt[i].get_width(),self.feilesvartxt[i].get_height()) for i in range(0,len(self.feilesvartxt))]
        self.allrects = []
        #self.allrects.extend(self.feilrects)
        #self.allrects.append(self.svarrect)
        self.allrects.append(self.taskrect)
        while self.svarrect.collidelistall(self.allrects):
            self.svarrect.x = random.randint(0,screenw-30)
            self.svarrect.y = random.randint(0,screenh-30)
        self.allrects.append(self.svarrect)
        for o in self.feilrects:
            while o.collidelistall(self.allrects):
                o.x = random.randint(0,screenw-30)
                o.y = random.randint(0,screenh-30)
            self.allrects.append(o)

    def draw(self):
        screen.blit(self.tasktxt,(self.taskrect.x,self.taskrect.y))
        screen.blit(self.svartxt,(self.svarrect.x,self.svarrect.y))
        i = len(self.feilesvartxt)-1
        while i >=0:
            screen.blit(self.feilesvartxt[i],(self.feilrects[i].x,self.feilrects[i].y))
            i -= 1
        pygame.draw.rect(screen,(0,0,0),self.taskrect,1)

def getInput():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                quit()
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                if snake.canturny:
                    snake.retning = "up"
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                if snake.canturnx:
                    snake.retning = "left"
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                if snake.canturnx:
                    snake.retning = "right"
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if snake.canturny:
                    snake.retning = "down"
            if event.key == pygame.K_SPACE:
                #oppgave = Pluss()
                pass

def oppgavemode():
    snake.move()
    oppgave.draw()
    snake.draw()
    snake.hit()
def applemode():
    snake.move()
    apple.draw()
    snake.draw()
    snake.hit()

def hover(rect):
    if rect.x < pygame.mouse.get_pos()[0] < rect.x+rect.width and rect.y < pygame.mouse.get_pos()[1] < rect.y+rect.height:
        return True
    return False

class Button():
    def __init__(self,pos=(0,0),text="Text here"):
        self.pos = pos
        self.text = text
        self.text = oppgavefont.render(self.text,True,(0,0,0))
        self.rect = pygame.rect.Rect(self.pos[0],self.pos[1],self.text.get_width(),self.text.get_height())
    def draw(self):
        if hover(self.rect):
            pygame.draw.rect(screen,(100,120,0),self.rect)
        else:
            pygame.draw.rect(screen,(0,120,200),self.rect)
        screen.blit(self.text,(self.rect.x,self.rect.y))

snake = Snake("gange")
oppgave = Pluss(snake.bunn,snake.topp,snake.mode)
apple = Apple()
state = "menu1"
def mainMenu():
    buttons = []
    buttons.append(Button((screenw/3,screenh/2),"Gange"))
    buttons.append(Button((screenw/3*2,screenh/2),"Pluss"))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hover(buttons[0]):
                    gangeMenu()
                if hover(buttons[1]):
                    gangeMenu()
        screen.fill((255,255,255))
        for button in buttons:
            button.draw()
        pygame.display.flip()

def gangeMenu():
    buttons = []
    buttons.append(Button((screenw/10*1,screenh/3),"2"))
    buttons.append(Button((screenw/10*2,screenh/3),"3"))
    buttons.append(Button((screenw/10*3,screenh/3),"4"))
    buttons.append(Button((screenw/10*4,screenh/3),"5"))
    buttons.append(Button((screenw/10*5,screenh/3),"6"))
    buttons.append(Button((screenw/10*6,screenh/3),"7"))
    buttons.append(Button((screenw/10*7,screenh/3),"8"))
    buttons.append(Button((screenw/10*8,screenh/3),"9"))
    buttons.append(Button((screenw/10*9,screenh/3),"10"))
    buttons.append(Button((screenw/10*10,screenh/3),"1-10"))



    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hover(buttons[0]):
                    snake.topp = 2
                if hover(buttons[1]):
                    snake.topp = 3
                if hover(buttons[2]):
                    snake.topp = 4
                if hover(buttons[3]):
                    snake.topp = 5
                if hover(buttons[4]):
                    snake.topp = 6
                if hover(buttons[5]):
                    snake.topp = 7
                if hover(buttons[6]):
                    snake.topp = 8
                if hover(buttons[7]):
                    snake.topp = 9
                if hover(buttons[8]):
                    snake.topp = 10
                return
        screen.fill((255,255,255))
        for button in buttons:
            button.draw()
        pygame.display.flip()

def main():
    global playing
    global retning
    global canturny
    global canturnx
    global oppgave
    global state

    #gangeMenu()


    for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

    while True:
        pygame.time.wait(snake.speed)

        getInput()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        screen.fill((255,255,255))


        #applemode()
        oppgavemode()

        pygame.display.flip()

if __name__ == '__main__':
    main()

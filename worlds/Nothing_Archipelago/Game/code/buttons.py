from settings import * 


class Button:
    def __init__(self,font,text,x,y,color,bonus):       
        self.font = font
        self.value = bonus
        self.text = self.font.render(str(text),False,color)
        self.rect = self.text.get_frect(center = (x,y))
        self.clicked = False
        self.clickable = True

    def draw(self,surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos) and self.clickable:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.text, (self.rect.x, self.rect.y))
        
        return action
    
    def updatetr(self,text,x,y,color,bonus):
        self.value = bonus
        self.text = self.font.render(str(text),False,color)
        self.rect = self.text.get_frect(topright = (x,y))
        self.clicked = False

    def updatec(self,text,x,y,color,bonus):
        self.value = bonus
        self.text = self.font.render(str(text),False,color)
        self.rect = self.text.get_frect(center = (x,y))
        self.clicked = False


    def updatetl(self,text,x,y,color,bonus):
        self.value = bonus
        self.text = self.font.render(str(text),False,color)
        self.rect = self.text.get_frect(topleft = (x,y))
        self.clicked = False

    def finishedtr(self,text,x,y,color,bonus):
        self.value = bonus
        self.text = self.font.render(str(text),False,color)
        self.rect = self.text.get_frect(topright = (x,y))
        self.clicked = False
        self.clickable = False
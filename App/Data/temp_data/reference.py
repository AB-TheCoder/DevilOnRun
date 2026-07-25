# Space Craft shooting game 
#by-Aarav Bhatt

#--------------------------------------------------------------------------------------------------------
import pygame 
pygame.init()
# import pygame_widgets
# from  pygame_widgets.button import Button 



import sys 
from pathlib import Path


class game_info: # simple display setup helper
    def __init__(self,dimensions,caption):
        
        
        self.dimension_screen=dimensions# set the screen dimensions 
        self.caption=caption# set the caption

    def set_caption(self):
        return pygame.display.set_caption(self.caption)
    @property
    def screen(self):# create the screen surface
        return pygame.display.set_mode(self.dimension_screen)# create the screen surface 
            
        # use to give a title to the display screen



#------------------buttons-------------------------------------------
class button:# button helper class
    def __init__(self,pos,image,dimension):
        self.image=pygame.image.load(image).convert_alpha()# load the button image
        self.dimension=pygame.Vector2(dimension)
        self.pos=pygame.Vector2(pos)# set the position
        self.image_rect=self.image.get_rect(topleft=(int(self.pos.x), int(self.pos.y)))
        self._on_press=None
        
    def when_pressed(self,when_pressed):
        self._on_press=when_pressed
    def transform(self,dimension):# scale the button image
        self.dimension=pygame.Vector2(dimension)
        self.image=pygame.transform.scale(self.image,self.dimension)
        self.image_rect=self.image.get_rect(topleft=(int(self.pos.x), int(self.pos.y)))
    def pressed(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if self.image_rect.collidepoint(event.pos):
                if self._on_press is not None:
                    self._on_press()
        
    def draw(self,surface):
        return surface.blit(self.image,self.pos)
    def hover(self,animation,event):
        if event.type == pygame.MOUSEMOTION:
            if  self.image_rect.collidepoint(event.pos):
                animation()



        

#--------------------------------------------------------------------
#------------images----------------------------------------------------
class image:
    def __init__(self,image,dimension=(1000,700),pos=(0,0)):
        self.image=pygame.image.load(image).convert_alpha()
        self.dimensions=pygame.Vector2(dimension)# dimensions of the image
        self.pos=pygame.Vector2(pos)# set the position
        self.image_rect=self.image.get_rect()
    def transform(self):# scale the button image
        self.image=pygame.transform.scale(self.image,self.dimensions)

#----------------------------------------------------------------------
#------------------------------sound------------------------------------
class audio:
    def __init__(self,audio_file):
        self.music=pygame.mixer.Sound(audio_file)

    def play(self,loops=0):
        self.music.play(loops=loops)
    def stop(self):
    
        self.music.stop()
    def set_volume(self,volume):
        self.music.set_volume(volume)
    



#-----------------------------------------------------------------------------
# -------------------------------------font--------------------------------------------
class text:
    def __init__(self,font,text,pos,size,color,bold,italic):
        self.fontt=font
        self.text=text
        self.pos=pygame.Vector2(pos)
        self.size=size
        self.color=color
        self.bold=bold
        self.italic=italic

    def create_font(self):
        self.font= pygame.font.SysFont(self.fontt,self.size,self.bold,self.italic)
    
    def render_text(self,surface):
        self.create_font()
        self.image=self.font.render(self.text,False,self.color)
        return surface.blit(self.image,self.pos)


# basic functions and screens ------------------------------------------------------------------

score=0
HIGHSCORE_PATH=Path(__file__).with_name('HIGHSCORE')

def read_highscore():
    try:
        data=HIGHSCORE_PATH.read_text(encoding='utf-8').strip()
        return int(data) if data else 0
    except FileNotFoundError:
        HIGHSCORE_PATH.write_text('0',encoding='utf-8')
        return 0
    except ValueError:
        HIGHSCORE_PATH.write_text('0',encoding='utf-8')
        return 0

def write_highscore(value):
    HIGHSCORE_PATH.write_text(str(int(value)),encoding='utf-8')

def shutdown():
    pygame.quit()
    sys.exit()

def gameover():
    highscore=read_highscore()
    background_audio.stop()

    dimension=(500,459)
    pos=(270,-50)
    game_over_image=image(r'secondary Data\game_over.png',dimension,pos)
    game_over_image.transform()

    retry_text=text('sys','Press ENTER To Play Again',(330,400),40,'white',True,False)
    score_text=text('sys',f'SCORE: {score}',(230,300),40,'white',True,False)
    if score>highscore:
        highscore=score
        write_highscore(highscore)
    hscore_text=text('sys',f'HIGH SCORE: {highscore}',(630,300),40,'white',True,False)

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:shutdown()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    return 'retry'

        Screen.blit(background.image,background.pos)
        Screen.blit(game_over_image.image,game_over_image.pos)
        retry_text.render_text(Screen)
        score_text.render_text(Screen)
        hscore_text.render_text(Screen)
        pygame.display.update()
        clock.tick(40)


def screen_2():
    global score,speed_ships
    speed_ships=1
    score=0
    game_over_state={'pending':False}

    global shooting_audio
    shooting_audio=audio(r'secondary Data\bullet shoot sound1.mp3')
    shotdown_audio=audio(r'secondary Data\shotdown.wav')
    nextlevel_audio=audio(r'secondary Data\next_level.mp3')

    def pause_screen():
        pygame.mixer.pause()
        overlay=pygame.Surface(Screen.get_size(),pygame.SRCALPHA)
        overlay.fill((0,0,0,180))

        paused_title=text('sys','PAUSED',(360,190),70,'white',True,False)
        resume_text=text('sys','Press ESC to Resume',(300,280),40,'white',True,False)
        quit_text=text('sys','Press Q to Quit',(340,330),30,'white',True,False)

        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    shutdown()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        pygame.mixer.unpause()
                        return
                    if event.key==pygame.K_q:
                        pygame.mixer.unpause()
                        shutdown()

            Screen.blit(background.image,background.pos)
            bullet_group.draw(Screen)
            shooter_group.draw(Screen)
            ship_group.draw(Screen)
            display_score()

            Screen.blit(overlay,(0,0))
            paused_title.render_text(Screen)
            resume_text.render_text(Screen)
            quit_text.render_text(Screen)
            pygame.display.update()
            clock.tick(40)
    class bullets(pygame.sprite.Sprite):
        def __init__(self,pos,color='yellow',dimension=(15,25),speed=10):
            super().__init__()
            self.image=pygame.Surface(dimension)
            self.image.fill(color)
            self.rect = self.image.get_rect(center=pos)
            self.speed=speed
        def update(self):
            self.rect.y-=self.speed
            if self.rect.bottom<0:
                self.kill()


    class shooter(pygame.sprite.Sprite):
        def __init__(self,shooter,dimension,pos):
            super().__init__()
            self.image=pygame.image.load(shooter).convert_alpha()
            self.image=pygame.transform.scale(self.image,dimension)
            self.pos=pygame.Vector2(pos)
            self.rect=self.image.get_rect()
            self.rect.center =[self.pos.x,self.pos.y]
        def right(self):
            if self.pos.x<930:self.pos.x+=10
            self.rect.center =[self.pos.x,self.pos.y]
        def left(self):
            if self.pos.x>70:self.pos.x-=10
            self.rect.center =[self.pos.x,self.pos.y]

        def pos_update(self,new_x,new_y):
            self.pos.x=new_x
            self.pos.y=new_y
            self.rect.center=[self.pos.x,self.pos.y]

    class ships(pygame.sprite.Sprite):
        def __init__(self,dimension=(100,100),pos_x=100,pos_y=0,speed=1):
            super().__init__()
            self.image=pygame.image.load(r'secondary Data\alien_ship2.png').convert_alpha()
            self.image=pygame.transform.rotate(self.image,180)
            self.image=pygame.transform.scale(self.image,dimension)
            self.pos=pygame.Vector2(pos_x,pos_y)
            self.rect=self.image.get_rect()
            self.rect.center =[self.pos.x,self.pos.y]
            self.speed=speed
        def update(self):
            self.rect.y+=self.speed
            if self.rect.top>490:
                if not game_over_state['pending']:
                    shotdown_audio.play()
                    game_over_state['pending']=True
                self.kill()
            

    shooter_sprite=shooter(r'secondary Data\shooter1.png',(150,150),(500,485))
    shooter_group=pygame.sprite.Group()
    shooter_group.add(shooter_sprite) 
    bullet_group=pygame.sprite.Group()
    ship_group=pygame.sprite.Group() 
 
    def draw_ships():
        if len(ship_group)==0:
            x=40
            while x<950:
                ship_group.add(ships(pos_x=x,pos_y=0,speed=speed_ships))
                ship_group.add(ships(pos_x=x,pos_y=-50,speed=speed_ships))
                ship_group.add(ships(pos_x=x,pos_y=-100,speed=speed_ships))
                x+=100
    def shotdown():
        global score
        colision=pygame.sprite.groupcollide(bullet_group,ship_group,True,True)
        if colision:
            score+=len(colision)

    def warrior_down():
        colision=pygame.sprite.groupcollide(shooter_group,ship_group,True,True)
        if colision and not game_over_state['pending']:
            shotdown_audio.play()
            game_over_state['pending']=True
    score_text=text('sys','0',(30,470),70,'white',True,False)
    def display_score():
        score_text.text=str(score)
        score_text.render_text(Screen)

    background_audio.set_volume(0.3)
    background_audio.play(loops=-1)
    def next_level():
        global speed_ships
        if len(ship_group)==0:
            speed_ships+=0.3
            nextlevel_audio.play()


    draw_ships()

    while True:
        
        Screen.blit(background.image,background.pos)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:shutdown()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pause_screen()
                if event.key==pygame.K_SPACE:
                    
                    shooting_audio.play()
                    bullet_sprite=bullets(shooter_sprite.rect.center)
                    bullet_group.add(bullet_sprite)
                    # random_ships() 
        key=pygame.key.get_pressed()

        if key[pygame.K_RIGHT]:
            shooter_sprite.right()
            
            
        if key[pygame.K_LEFT]:
            shooter_sprite.left()

        bullet_group.update()
        ship_group.update()

        shotdown()
        warrior_down()

        if game_over_state['pending']:
            return gameover()

        next_level()
        draw_ships()
        display_score()

        bullet_group.draw(Screen)

        shooter_group.update()
        shooter_group.draw(Screen)
        ship_group.draw(Screen)
        pygame.display.update()
        clock.tick(40)
        







#-------------------------------------------------------------------------------------
def set_display():
    global Screen
    dimension=1000,550
    caption="SpaceShoot"
    shooter_Game=game_info(dimension,caption)
    shooter_Game.set_caption()
    Screen=shooter_Game.screen
    

def set_time():
    global clock
    clock=pygame.time.Clock()


def set_background_image():
    global background
    pos=0,0
    background=image(r'secondary Data\Background.jpg',(Screen.get_width(),Screen.get_height()))
    background.transform()

def set_main_logo():
    global main_logo
    pos=(230,-70)
    main_logo=image(r'secondary Data\main logo.png',(500,455),pos)
    main_logo.transform()

def set_background_audio():
    global background_audio
    background_audio=audio(r'secondary Data\background.mp3')
def button_audio():
    global Button_sound
    Button_sound=audio(r'secondary Data\beep.mp3')
def set_start_button():
    global start_button
    dimension=150,150
    pos=(580,370)
    start_button=button(image=r'secondary Data\startButton2.png',pos=pos,dimension=dimension)
    start_button.transform(dimension)
    start_button.when_pressed(start_pressed)

def set_Quit_button():
    global Quit_Button
    dimension=[150,150]
    pos=[200,370]
    Quit_Button=button(image=r'secondary Data\QUIT.png',pos=pos,dimension=dimension)
    Quit_Button.transform(dimension)
    Quit_Button.when_pressed(button_shutdown)

    

def button_shutdown():
    background_audio.stop()
    button_animation(Quit_Button)
    Button_sound.play()
    shutdown()
def start_pressed():
    background_audio.stop()
    button_animation(start_button)
    Button_sound.play()
    while True:
        action=screen_2()
        if action!='retry':
            break


def button_animation(Button):
    Button.transform((Button.dimension.x+3,Button.dimension.y+3))
    Screen.blit(background.image,background.pos)
    Screen.blit(main_logo.image,main_logo.pos)
    start_button.draw(Screen)

    Quit_Button.draw(Screen)
    pygame.display.update()

set_display()
set_time()
set_background_image()
set_main_logo()
set_background_audio()
button_audio()
set_start_button()
set_Quit_button()


#game_loop----------------------------------------------------------------------------------
def screen_1():
    
    
    while True:
        

        #user_interaction----------------------------------------------------------------------
        key=pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:shutdown()





        for event in pygame.event.get():
            if event.type == pygame.QUIT:shutdown()
            start_button.pressed(event)
            Quit_Button.pressed(event)

            




 



        #basics and execution-------------------------------------------------
        
        Screen.blit(background.image,background.pos)
        Screen.blit(main_logo.image,main_logo.pos)
        start_button.draw(Screen)

        Quit_Button.draw(Screen)
        
        pygame.display.update()
        clock.tick(40)
screen_1()

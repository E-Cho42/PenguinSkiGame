#imports -->
import pygame as pg
import random as rd
import time  

def main():
    
    # setting up pygame window -->
    pg.init() 
    canvas = pg.display.set_mode((800, 800)) 
    pg.display.set_caption("SKI GAME") 
    pg.font.init() 
    my_font = pg.font.SysFont('Comic Sans MS', 30)
    my_font_two = pg.font.SysFont('Comic Sans MS', 60)
    clock = pg.time.Clock()


    # setting up penguin/player class -->
    class penguin():
        def __init__(self, pos,direction,passes, image_left, image_right, speed, number_of_passes):
            self.pos = pos
            #True = left  Flase= right 
            self.direction = direction
            self.passes = passes
            self.image = image_left
            self.image_right = image_right
            self.speed = speed
            self.number_of_passes = number_of_passes
        # crash function -->
        def crash(self, sec, minu, hou):
            print(f"time crashed: {hou}:{minu}:{sec}")
            # clear sceeen and fill with read -->
            pg.draw.rect(canvas,(255,0,0), pg.Rect(0, 0, 800, 800))
            canvas.fill((240,0,0))
            tree_list.clear()
            ski_pass_list.clear()
            
            # high score display and calculate -->
            scores = []
            with open("scores.txt" , 'r') as f:
                for line in f:
                    scores.append(line.strip())
                if self.number_of_passes > int(scores[0]):
                    scores[0] = self.number_of_passes
                print(scores)
            with open('scores.txt', "r+") as f:
                f.truncate(0)
            with open("scores.txt" , 'w') as f:
                for i in scores:
                    f.write(str(i)+'\n') 
            
            # final stuff -->  
            gameOverText =  my_font_two.render(f'Game Over', False, (0, 0, 0))
            self.number_of_passes = 0  
            score_text = my_font.render(f'High Score: {scores[0]}', False, (0, 0, 0)) 
            canvas.blit(gameOverText, (255, 310))  
            canvas.blit(score_text,(310,400))
            pg.display.update()
            time.sleep(2)
            

    penguin_left = pg.image.load('penguin_fliped.png')
    penguin_right = pg.image.load('penguin.png')
    player = penguin([400,400], False, 0, 'penguin_fliped.png', 'penguin.png', .1, 0 )
    # Setting up trees -->
    number_of_trees = 10
    tree_list = []

    class tree():
        def __init__(self, pos):
            self.pos = pos 
        
            
    tree_sprite = pg.image.load("tree.png")
    tree_timer = 0
    tree_frequancy = 1000 # lower = faster
    tree_speed = .1

    # setting up ski passes -->
    class ski_pass():
        def __init__(self,pos):
            self.pos = pos 
        def collected():
            pass

    ski_pass_sprite = pg.image.load("ski_pass.png")
    ski_pass_list = []
    pass_frequancy = 2

    # timer stuff:
    seconds = 0
    minuts = 0
    hours = 0

    # main game loop -->
    exit = False
    while not exit: 
        
        # timer:
        seconds += (1/30)
        if seconds >= 60:
            minuts += 1
            seconds = 0
        if minuts >= 60:
            hours += 1
        
        # drawing stuff:
        canvas.fill((255,250,250))
        score = my_font.render(f'Number of Passes Collected: {str(player.number_of_passes)}', False, (0, 0, 0))
        times = my_font.render(f'{hours}:{minuts}:{seconds:.2f}', False, (0, 0, 0))

        # Events -->
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                exit = True
        
        # movement_logic --> 
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            player.direction = False
        if keys[pg.K_d]:
            player.direction = True
        if keys[pg.K_w]:
            pass
        if keys[pg.K_s]:
            pass
        if player.direction:
            player.pos[0] += player.speed 
        else:
            player.pos[0] -= player.speed
                
        # tree logic -->
        if tree_timer == tree_frequancy:
            tree_timer = 0
            for i in range(number_of_trees):
                tree_list.append(tree([rd.randint(0,799), 800]))
            for i in range(pass_frequancy):
                ski_pass_list.append(ski_pass([rd.randint(0,799), 800]))
        else:
            tree_timer += 1
        for i in tree_list:
            i.pos[1] -= tree_speed
        for i in ski_pass_list:
            i.pos[1] -= tree_speed
        # drawing player-->
        if player.direction:
            canvas.blit(penguin_right, player.pos)
        else:
            canvas.blit(penguin_left, player.pos)
        # drawing trees-->
        for i in tree_list:
            
            #player death --> 
            canvas.blit(tree_sprite, i.pos)
            if player.pos[0] > i.pos[0] and player.pos[0] < i.pos[0] + 30 and player.pos[1]+10 > i.pos[1] and player.pos[1]+10 < i.pos[1] + 60:
                player.crash(seconds ,minuts, hours )
                pass
            
        # ski passes logic and colletion -->
        for i in ski_pass_list:
            canvas.blit(ski_pass_sprite, i.pos)
            if player.pos[0] > i.pos[0] and player.pos[0]-16 < i.pos[0] + 16 and player.pos[1] + 32 > i.pos[1] and player.pos[1] < i.pos[1] + 32:
                player.number_of_passes += 1
                ski_pass_list.remove(i)

        # scores drawing -->
        canvas.blit(score, (0,0))
        canvas.blit(times,(0,30 ))
        
        # update screen -->
        pg.display.update()
        

if __name__ == "__main__":
    main()
 
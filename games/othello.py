import pygame as py,numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
import subprocess
from datetime import date
from  game import BoardGame 



clock=py.time.Clock()

class Othello(BoardGame):
    #colour for player1,player2
    colour={1:"white",2:"black"}

    #dictionary for storing number of valid moves
    no_of_valid={1:2,2:2}

    #------------width and height of one box----------------
    x=BoardGame.BOARD_W/8
    y=BoardGame.BOARD_H/8
    score=np.array([60,2,2])


    def update_score(self):
        s1=0
        s2=0
        for x in zip(*np.where(self.board==1)):
            s1+=1
        for x in zip(*np.where(self.board==2)):
            s2+=1
        self.score[1]=s1
        self.score[2]=s2
        self.score[0]=64-s1-s2

    def scoreboard(self,screen:py.Surface):
       s1=self.score[1]
       s2=self.score[2]
       p1_l=(s1/(s1+s2))*self.W
       p2_l=(s2/(s1+s2))*self.W
       py.draw.rect(screen,"white",(0,self.TOP_BAR_H,p1_l,10))
       py.draw.rect(screen,"black",(p1_l,self.TOP_BAR_H,p2_l,10))


    def draw_top_bar(self, surf):
        py.draw.rect(surf,'#074B4F', (0, 0,self.W,self.TOP_BAR_H))
        game_text = self.get_font(30, True).render(self.__class__.__name__, True, "gold")
        surf.blit(game_text, (20,20))

        if( self.winner is None):
            p1_text = self.get_font(30).render(self.player_names[1], True, 'white')
            p2_text = self.get_font(30).render(self.player_names[2], True, (28, 28, 28))
            vs_text = self.get_font(30).render(" v/s ", True, "yellow")
            p1s_text=self.get_font(30).render(str(self.score[1]),True, 'white')
            p2s_text=self.get_font(30).render(str(self.score[2]),True,(28, 28, 28))
            

            x = self.W / 2 - (p1_text.get_width() + p2_text.get_width() + vs_text.get_width()) / 2

            surf.blit(p1_text, (x, 20)); surf.blit(p1s_text,(x-30,20));x += p1_text.get_width()
            surf.blit(vs_text, (x, 20)); x += vs_text.get_width()
            surf.blit(p2_text,(x,20))
            surf.blit(p2s_text,(x+p2_text.get_width()+5,20))

            turn_color = 'white' if self.current_player == 1 else (28, 28, 28)
            turn_text = self.get_font(30).render(f"{self.current_player_name()}'s Turn", True, turn_color)
            surf.blit(turn_text, (self.W - turn_text.get_width() - 10, 20))

        elif self.winner == 0:
                draw_text = self.get_font(40).render("It's a Draw", True, "white")
                x = self.W / 2 - draw_text.get_width() / 2
                surf.blit(draw_text, (x, 20))

        else :
                winner_text = self.get_font(40).render(f"{self.player_names[self.winner]} Wins", True, "white")
                x = self.W / 2 - winner_text.get_width() / 2
                surf.blit(winner_text, (x, 20))
   

        py.draw.line (surf, ( 45,  45,  75), (0,self.TOP_BAR_H), (self.W,self.TOP_BAR_H))


    def draw_board(self,screen:py.Surface):
        
        x=self.BOARD_W/8
        y=self.BOARD_H/8
        BS=py.Surface((self.BOARD_W,self.BOARD_H))
        BS.fill('#32a832')
        screen.blit(BS,(self.BOARD_X,self.BOARD_Y))
        for i in range(0,9):
            py.draw.line(screen,'black',(self.BOARD_X+i*x,self.BOARD_Y),(self.BOARD_X+i*x,self.BOARD_Y+self.BOARD_H),2)
        for i in range(0,9):
            py.draw.line(screen,'black',(self.BOARD_X,self.BOARD_Y+i*y),(self.BOARD_X+self.BOARD_W,self.BOARD_Y+i*y),2)
        
    def reset(self):
        self.board=np.zeros((8,8))
        self.current_player=1
        self.winner=None
        self.move_count=0
        self.score=[60,2,2]
        self.board[3,3]=1
        self.board[3,4]=2
        self.board[4,3]=2
        self.board[4,4]=1

    #----------box(screen,i,j) returns you the  transparent surface,rectangle of the box at (i,j) location------------------------------------
    def box(self,screen:py.Surface,i:int,j:int) -> tuple[py.Surface,py.Rect]:
        box_s=py.Surface((self.x,self.y),py.SRCALPHA) #py.SRCALPHA allow transparency
        box_r=box_s.get_rect()
        box_r.topleft=(self.BOARD_X+j*self.x,self.BOARD_Y+i*self.y)
        screen.blit(box_s,box_r)
        
        return box_s,box_r
    
    #this functions fills the screen with circles
    def fill_board(self,screen:py.Surface):
        centre=(self.x//2,self.y//2)
        for i,j in zip(*np.where(self.board==1)):
            bs,br=self.box(screen,i,j)
            py.draw.circle(bs,self.colour[1],centre,(self.x -4)//2,0)
            screen.blit(bs,br)
            
        for i,j in zip(*np.where(self.board==2)):
            bs,br=self.box(screen,i,j)
            py.draw.circle(bs,self.colour[2],centre,(self.x-4)//2,0)
            screen.blit(bs,br)

    #mx=mouse x_pos,my=mouse y_pos 
    #k is a variable which is set to be false for any point fi the point is along diagonal or horizontal or vertical to the mouse point then k is set to true and if in betwen the point and mouse point if there is some random 
    def is_validmove(self,i:int,j:int):
        if(0<=i and i<8 and 0<=j and j<8):
            for a,b in zip(*np.where(self.board==self.current_player)):
                if(self.board[i,j]==0):
                    k=False  
                    if(b-a == j-i):
                        arr=np.diag(self.board[min(a,i)+1:max(a,i),min(b,j)+1:max(b,j)])
                        k=True
                        if(np.any(arr != self.opponent_player()) or arr.size==0):
                            k=False
                         
                    if(b+a==j+i):
                        arr=np.diag(np.fliplr(self.board[min(a,i)+1:max(a,i),min(b,j)+1:max(b,j)])) 
                        k=True  
                        if(np.any(arr!=self.opponent_player()) or arr.size==0):
                            k=False
                        
                    if(a==i):
                        arr=self.board[i,min(b,j)+1:max(j,b)]
                        k=True
                        if(np.any(arr!=self.opponent_player()) or arr.size==0):
                            k=False
                     
                    if(b==j):
                        arr=self.board[min(a,i)+1:max(a,i),j]
                        k=True
                        if(np.any(arr!=self.opponent_player())  or arr.size==0):
                            k=False

                    if(k):
                        return True     
            return False
    

    #--------it highlights the box if it is valid to place there and it shows all valid moves also and returns number of valid moves of current player---------
    def show_valid(self,screen:py.Surface) -> int:
        a=0
        for i,j in zip(*np.where(self.board==0)):
            bs,br=self.box(screen,i,j)
            if(self.is_validmove(i,j)):
                py.draw.circle(screen,self.colour[self.current_player],br.center,br.width/2,5)
                a+=1
        mx,my=py.mouse.get_pos()
        i=int((my-self.BOARD_Y)/(self.y))
        j=int((mx-self.BOARD_X)/(self.x))
        if(0<=i and i<8 and 0<=j and j<8):
            bs,br=self.box(screen,i,j)
            if(self.is_validmove(i,j)):
                py.draw.rect(screen,'yellow',br,5)

        return a

    #---------modifies board value on click and changes the turn-----------
    def update_board(self):
        mx,my=py.mouse.get_pos()
        i=int((my-self.BOARD_Y)/(self.y))
        j=int((mx-self.BOARD_X)/(self.x))
        n=0
        if(self.is_validmove(i,j)):
            for a,b in zip(*np.where(self.board==self.current_player)):
                k=False  
                if(b-a == j-i):
                    arr=np.diag(self.board[min(a,i)+1:max(a,i),min(b,j)+1:max(b,j)])
                    k=True
                    if(np.any(arr != self.opponent_player()) or arr.size==0):
                        k=False
                         
                elif(b+a==j+i):
                    arr=np.diag(np.fliplr(self.board[min(a,i)+1:max(a,i),min(b,j)+1:max(b,j)])) 
                    k=True  
                    if(np.any(arr!=self.opponent_player()) or arr.size==0):
                         k=False
                        
                elif(a==i):
                    arr=self.board[i,min(b,j)+1:max(j,b)]
                    k=True
                    if(np.any(arr!=self.opponent_player()) or arr.size==0):
                        k=False
                     
                elif(b==j):
                    arr=self.board[min(a,i)+1:max(a,i),j]
                    k=True
                    if(np.any(arr!=self.opponent_player())  or arr.size==0):
                        k=False



                if(k and a!=i):
                    m=int((b-j)/(a-i))
                    for x in range(0,(a-i),int(abs(a-i)//(a-i))):
                        self.board[i+x,j+m*x]=self.current_player
                elif(k and a==i):
                    for y in range(0,(b-j),int(abs(b-j)//(b-j))):
                        self.board[i,j+y]=self.current_player    
            self.switch_turn()

    #----check win status and returns true or false ----------
    def gameover(self):
        if(self.score[0]==0 or (self.no_of_valid[1]==0 and self.no_of_valid[2]==0)):
            if(self.score[1]>self.score[2]):
                self.winner=int(1)
            elif(self.score[1]<self.score[2]):
                self.winner=int(2)
            else:
                self.winner=0
            
            return True
        else:
            return False
        
   

    
    #----run_game runs the gameloop and returns winner and loser in a tuple and exits the loop 
    def run_game(self,screen:py.Surface):
        running=True


        while(running):
            for e in py.event.get():
                if(e.type==py.QUIT):
                    py.quit()
                    sys.exit()
                if(e.type==py.MOUSEBUTTONDOWN):
                    self.update_board()
                    self.update_score()
            
            screen.fill("gold")
            self.draw_board(screen)
            self.scoreboard(screen)
            self.draw_top_bar(screen)    
            self.fill_board(screen)
            k=self.show_valid(screen)
            self.no_of_valid[self.current_player]=k
            py.display.update()
            if(k==0):
                self.switch_turn()
            if(self.gameover()):
                running=False
                if(self.winner==1 or self.winner==2):
                    a=(self.player_names[self.winner],self.player_names[3-self.winner])
                elif(self.winner==0):
                    a=(None,None)
            clock.tick(60)    
        
        return a

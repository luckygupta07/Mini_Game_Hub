import pygame as py,numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
import subprocess
from datetime import date
from  game import BoardGame 

py.init()

clock=py.time.Clock()

class othello(BoardGame):
    #colour for player1,player2
    colour={1:"red",2:"green"}

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
        p1_t=self.get_font(40)
        p1_s=p1_t.render(self.player_names[1],True,self.colour[1])
        p1_r=p1_s.get_rect()
        vs_t=self.get_font(40)
        vs_s=vs_t.render('VS',True,'black')
        vs_r=vs_s.get_rect()
        p2_t=self.get_font(40)
        p2_s=p2_t.render(self.player_names[2],True,self.colour[2])
        p2_r=p2_s.get_rect()
        vs_r.center=(self.W/2,30)
        l=vs_r.width
        p1_r.topright=((self.W-l-20)/2,0)
        p2_r.topleft=((self.W+l+20)/2,0)
        p1s_t=self.get_font(30)
        p1s_s=p1s_t.render(str(self.score[1]),True,self.colour[1])
        p1s_r=p1s_s.get_rect(center=(p1_r.centerx,p1_r.centery+40))
        
        p2s_t=self.get_font(30)
        p2s_s=p2s_t.render(str(self.score[2]),True,self.colour[2])
        p2s_r=p2s_s.get_rect(center=(p2_r.centerx,p2_r.centery+40))
        
        c=max(p1_r.width,p2_r.width)
        a=20+c+10+vs_r.width+10+c+20
        b=90
        bg_s=py.Surface((a,b))
        bg_r=bg_s.get_rect(center=(self.W/2,47))
        
        
        py.draw.rect(screen,'white',bg_r,0,10,10,10,10,10)
        py.draw.rect(screen,'black',(p1s_r.topleft[0],p1s_r.topleft[1],30,40),0,4)
        py.draw.rect(screen,'black',(p2s_r.topleft[0],p2s_r.topleft[1],30,40),0,4)
        
        screen.blit(p1_s,p1_r)
        screen.blit(vs_s,vs_r)
        screen.blit(p2_s,p2_r)
        screen.blit(p1s_s,p1s_r)
        screen.blit(p2s_s,p2s_r)




    def draw_board(self,screen:py.Surface):
        
        x=self.BOARD_W/8
        y=self.BOARD_H/8
        BS=py.Surface((self.BOARD_W,self.BOARD_H))
        screen.blit(BS,(self.BOARD_X,self.BOARD_Y))
        for i in range(0,9):
            py.draw.line(screen,'white',(self.BOARD_X+i*x,self.BOARD_Y),(self.BOARD_X+i*x,self.BOARD_Y+self.BOARD_H),2)
        for i in range(0,9):
            py.draw.line(screen,'white',(self.BOARD_X,self.BOARD_Y+i*y),(self.BOARD_X+self.BOARD_W,self.BOARD_Y+i*y),2)
        
    def reset(self):
        self.board=np.zeros((8,8))
        self.current_player=1
        self.winner=None
        self.move_count=0
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
            
            screen.fill(self.colour[self.current_player])
            self.draw_board(screen)
            self.scoreboard(screen)    
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

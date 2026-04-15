import pygame as py,numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
import subprocess
from datetime import date
from  game import BoardGame 





class othello(BoardGame):
    #colour for player1,player2
    colour={1:"red",2:"green"}

    #------------width and height of one box----------------
    x=BoardGame.BOARD_W/8
    y=BoardGame.BOARD_H/8

    def draw_board(self,screen:py.Surface):
        
        x=self.BOARD_W/8
        y=self.BOARD_H/8
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
    def is_validmove(self):
        mx,my=py.mouse.get_pos()
        i=int((my-self.BOARD_Y)/(self.y))
        j=int((mx-self.BOARD_X)/(self.x))
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
    

    #--------it highlights the box if it is valid to place there---------
    def show_valid(self,screen:py.Surface):
        mx,my=py.mouse.get_pos()
        i=int((my-self.BOARD_Y)/(self.y))
        j=int((mx-self.BOARD_X)/(self.x))
        if(0<=i and i<8 and 0<=j and j<8):
            bs,br=self.box(screen,i,j)
            if(self.is_validmove()):
                py.draw.rect(screen,'yellow',br,5)

    #---------modifies board value on click and changes the turn-----------
    def game_play(self):
        mx,my=py.mouse.get_pos()
        i=int((my-self.BOARD_Y)/(self.y))
        j=int((mx-self.BOARD_X)/(self.x))
        if(self.is_validmove()):
            self.board[i,j]=self.current_player
            self.switch_turn()

    def run_game(self,screen:py.Surface):
        for e in py.event.get():
            if(e.type==py.QUIT):
                py.quit()
                sys.exit()
            if(e.type==py.MOUSEBUTTONDOWN):
                self.game_play()
        
        screen.fill('black')
        self.draw_board(screen)    
        self.fill_board(screen)
        self.show_valid(screen)
        py.display.update()

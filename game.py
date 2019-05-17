from tkinter import *
import time
import random

tk= Tk()
tk.title('Bounce!')
tk.resizable(0,0)
canvas=Canvas(tk,height='500', width='500')
canvas.pack()
tk.update()
start_time = time.time()
class Ball:

    def __init__(self,canvas, paddle):

        self.paddle=paddle
        self.x=random.choice([-6,6])
        self.y=-7
        self.canvas=canvas
        self.id=canvas.create_oval(10,10,25,25, fill='grey')
        self.canvas.move(self.id, 250, 100)
        self.score=0

    def hity(self,pos):
        paddle_pos=self.canvas.coords(self.paddle.id)
        if pos[2]<=paddle_pos[2] and pos[0]>=paddle_pos[0]:
            if pos[3]>=paddle_pos[1] and pos[3]<=paddle_pos[3]:
            
                return True
            else:
                return False
        else:
            return False        

    def DrawBall(self):
        
        pos=self.canvas.coords(self.id)
        
        if pos[1]<=0:
            self.y=-self.y
            self.score+=1
        if pos[3]>=500:
            self.y=-self.y
            
        if pos[0]<=0:
            self.x=-self.x
            
        if pos[2]>=500:
            self.x=-self.x
        if self.hity(pos)==True:
            self.y=-self.y
        self.canvas.move(self.id,self.x,self.y)
    
class Paddle:

    def __init__(self,canvas):
        self.canvas=canvas
        self.id=canvas.create_rectangle(10,10,130,25)
        self.x=0
        self.canvas.move(self.id, 250,250)
        self.canvas.bind_all('<KeyPress-Left>', self.left)
        self.canvas.bind_all('<KeyPress-Right>', self.right)

    def DrawPaddle(self):
        self.canvas.move(self.id, self.x,0)
        
        self.posp=self.canvas.coords(self.id)
        if self.posp[0]<=0 or self.posp[2]>=500 :
            self.x=0
        
    def left(self,event):
        self.x=-5

    def right(self,event):
        self.x=5
        
    def draw(self):
        self.canvas.move(self.id,self.x,0)


    
paddle=Paddle(canvas)                
ball=Ball(canvas,paddle)

while True:
    ball.DrawBall()
    paddle.DrawPaddle()
    time.sleep(0.01)
    canvas.update()
    canvas.update_idletasks()
    if time.time() - start_time >=60:
        print('GAME OVER!\nYour score is: ' + str(ball.score))
        time.sleep(100)
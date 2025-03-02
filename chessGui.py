
import chess.pgn
import chess.pgn
import chess.engine
from tkinter import *
from matplotlib.figure import Figure
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
#from tensorflow import keras
from alphabeta import *
from dialog import ChoicePopup
from pieces import Pieces
from move import Board
from pvb import Bot
class Game():
    def __init__(self):
        self.board=Board()
        self.count=0
        self.pieces=[]
        self.clicked=None
        self.white_bot=None
        self.black_bot=None
        self.promCount=0
        self.y=[]
        self.image_refs=[]

        self.game()
    
    def translate(self,matrix,chess_dict):
        rows = []
        for row in matrix:
            terms = []
            for term in row:
                terms.append(chess_dict[term])
            rows.append(terms)
        return rows
    def change_photo(self,index):
        img=self.get_images()[index]
        self.canvas.imgref=img
        self.image_refs.append(img)
        return img
    

    def promotion(self,move,pos1,pos2,prom):
        obj=self.pieces[self.clicked]
        color=not obj.color()
        print(color)
        if type(obj)==Pieces:
            name="w"
        else:
            name="b"
        match prom:
            case "q":
                photo=8+color
                name+="quenn"
            case "r":
                photo=2+color
                name+="rook"
            case "n":
                photo=4+color
                name+="knight"
            case "b":
                photo=6+color
                name+="bishop"
        img=self.change_photo(photo)
        self.promCount+=1
        self.canvas.itemconfig( obj.obj,image=img)
        self.pieces[self.clicked].name=name+str(self.promCount)
        self.control(move,pos1,pos2,prom)

 
    def casting(self,move):
        t= self.pieces[self.clicked].color()
        board=self.board.get_board()
        moveOn=[[-112,188],[128,-112]]
        pos=1 if t else 8
        color="w" if t else "b"
        if board.is_kingside_castling(move):
            kpos=Board.move_to_cor('e',pos)
            rpos=Board.move_to_cor('h',pos)
            for i in self.pieces:
                if i.name==color+"king":
                    # print("Finnd king casteling")
                    piece="rook2"
                    for j in self.pieces:
                        if  j.name==color+piece:
                            self.canvas.moveto(i.obj,kpos[0]+moveOn[t][0],kpos[1]+8)
                            self.canvas.moveto(j.obj,rpos[0]+moveOn[t][1],rpos[1]+8)

        elif board.is_queenside_castling(move):
            kpos=Board.move_to_cor('e',pos)
            rpos=Board.move_to_cor('a',pos)
            piece="rook1" 
            for i in self.pieces:
                if i.name==color+"king":
                    for j in self.pieces:
                        if  j.name==color+piece:
                            self.canvas.moveto(i.obj,kpos[0]+moveOn[-t][0],kpos[1]+8)
                            self.canvas.moveto(j.obj,rpos[0]+moveOn[-t][1],rpos[1]+8)
    
        print(self.board.get_board())

    def passant(self,fpos,ppos):
        print(f"{ppos=}")
 
        addX=30 
        addY=30 
        l=[ppos[0]+addX,ppos[1]+addY]
        print (l)
        print("l:"+str(l))
        for i in  enumerate(self.pieces):
            coords=self.canvas.coords(i[1].obj)
            if coords[0]==l[0] and coords[1]==l[1]:
            # print("White")
                self.canvas.delete(i[1].obj)
                self.pieces.remove(i[1])
                self.correction(i[0])
                print(f"Delete {i[0]}")
                break
                
        
    def control(self,move,pos1,pos2=None,prom=None):
        note=f"{pos1}{pos2}{prom}" if prom else f"{pos1}{pos2}"
        print(f"{note=}")
        self.add_one(chess.Move.from_uci(note))
        board=self.board.get_board()

        if board.is_kingside_castling(move) or  board.is_queenside_castling(move) :
           # print(list(board.legal_moves))
            print(board.legal_moves)
            self.casting(move)
            board.push(chess.Move.from_uci(f"{pos1}{pos2}"))
            self.board.set_board(board)
            info = self.engine.analyse(self.board.get_board(), chess.engine.Limit(time=0.1))
            return True
        l=Board.move_to_cor(pos2[0],pos2[1])
        print(f"Before {self.clicked=}")

        if board.is_en_passant(move):
            ppos=Board.move_to_cor(pos2[0],pos1[1])
            fpos=Board.one_move_to_cor(pos1[0])
            self.passant(fpos, ppos)
        else:
            for i in enumerate(self.pieces) :
                if self.canvas.coords(i[1].obj)[0]-30==l[0] and self.canvas.coords(i[1].obj)[1]-30==l[1]:
                    if not self.pieces[self.clicked] == i[1].obj:
                        self.canvas.delete(i[1].obj)
                        self.pieces.remove(i[1])
                        print(f"Delete ind: {i[0]}")
                        self.correction(i[0])
        print(f"After {self.clicked=}")
        self.canvas.moveto(self.pieces[self.clicked].obj,l[0]+8,l[1]+8)
        if prom:
             print(f"{self.pieces[self.clicked].name=},{self.pieces[self.clicked].obj=}")
             board.push(chess.Move.from_uci(f"{pos1}{pos2}{prom}"))
        else:
            board.push(chess.Move.from_uci(f"{pos1}{pos2}"))
       # print (self.canvas.coords(self.pieces[self.clicked].obj))
       # print(self.board.get_board())

        self.board.set_board(board)
        info = self.engine.analyse(self.board.get_board(), chess.engine.Limit(time=0.1))
       # self.draw(info)
    def select(self,event):
        if self.count ==0:
          #  print("there")
            canv=self.canvas.find_closest(event.x,event.y)
            for i in range(len(self.pieces)):
                if self.pieces[i].obj ==canv[0]:
                    print(i)
                    self.clicked=i
                    self.count+=1
                    break
            else:
                self.count=0
           # print("end click 1")
        else:
           # print(f"{self.board.get_board().turn= }")
         #   print("second click")
            self.count=0
            if  self.clicked==None:
                return False
        #    print (event.x,event.y)
            board=self.board.get_board()
            x=self.canvas.coords(self.pieces[self.clicked].obj)[0]
            y=self.canvas.coords(self.pieces[self.clicked].obj)[1]
            pos1=Board.cor_to_move(Pieces,x,y)
            pos2=Board.cor_to_move(Pieces,event.x,event.y)
            if pos1==None or pos2==None or pos1==pos2:
                print(f"same:{pos1}{pos2}")
                return False
            if (pos1=="e1" and (pos2=="a1" or pos2=="h1")) or pos1=="e8" and (pos2=="a8"or pos2=="h8"):
                if pos2[0]=='h':
                    pos2="g"+pos2[1:]
                else:
                    pos2=='c'+pos2[1:]
            move=chess.Move.from_uci(f"{pos1}{pos2}")
        #    print(move, list(board.legal_moves))  
            if chess.Move.from_uci(f"{pos1}{pos2}q") in board.legal_moves:
                self.add_one(f"{pos1}{pos2}q")
                print("promotion")
                prom=ChoicePopup.get_choice(self.root)
                print(prom)
                
                self.promotion(move,pos1,pos2,prom)
                try:
                    self.m.tk_popup(event.x_root, event.y_root)
                finally:
                    self.m.grab_release()
                    return True
            if  move in board.legal_moves:
                
            #    print("legal")
                self.control(move,pos1,pos2)
    def add_one(self,move):
        s = self.display_text.get()
        if self.board.get_board().turn==1:

            s = f"{str(self.board.get_board().fullmove_number)}. {move} " 
        else:
            s = f"{move} "
        self.display_text.set(s) 
        self.Output.insert(END,s)
        #self.canvas.itemconfigure(self.moves,text=s)

        
    def cheek_boot(self,turn=None,type=None):
        if type=="random":
            if turn=="White":
             #   print("Start White")
                self.white_bot="random"
            if turn=="Black":
          #      print("Start Black")
                self.black_bot="random"
        if type=="keras":
            if turn=="White":
            #    print("Start White")
                self.white_bot="keras"
            if turn=="Black":
            #    print("Start Black")
                self.black_bot="keras"
        if type=="pesto":
            if turn=="White":
           #     print("Start White")
                self.white_bot="pesto"
            if turn=="Black":
             #   print("Start Black")
                self.black_bot="pesto"
        elif not type:
            if turn =="White":
                self.white_bot=None
            if turn =="Black":
                self.black_bot=None
            if not turn:
                self.white_bot=None
                self.black_bot=None
   
    def correction(self,i):
        if i<self.clicked:
            self.clicked-=1
        
    def random_bot(self):
        res=Bot.random_bot(self.board.get_board(),self.board.get_turn())
        pos=Board.move_to_cor(res[1][0],res[1][1])
        closet=self.canvas.find_closest(pos[0]+8,pos[1]+8)
        for i in range(len(self.pieces)):
            if self.pieces[i].obj ==closet[0]:
                self.clicked=i
        self.control(res[0],res[1],res[2])

    def run_bot(self,root):
        root.after_cancel(self.run)
        if self.white_bot=="random":
            self.random_bot("White")
        elif self.white_bot =="keras":
            self.keras_bot("White")
        elif self.white_bot == "pesto":
             self.pesto_bot("White")
        if self.black_bot=="random":
            self.random_bot("Black")
        elif self.black_bot == "keras":
            self.keras_bot("Black")
        elif self.black_bot =="pesto":
            self.pesto_bot("Black")



        self.run=root.after(3000,lambda:self.run_bot(root))

    def get_images(self):
        wpawn= PhotoImage(file="D:/chess/chess-pack/chess-pawn.png")
        bpawn= PhotoImage(file="D:/chess/chess-pack/chess-pawn (1).png")
        wrook=PhotoImage(file="D:/chess/chess-pack/chess-rook.png")
        brook=PhotoImage(file="D:/chess/chess-pack/chess-rook (1).png")
        wbishop= PhotoImage(file="D:/chess/chess-pack/chess-bishop.png")
        bbishop=PhotoImage(file="D:/chess/chess-pack/chess-bishop (1).png")
        wknight= PhotoImage(file="D:/chess/chess-pack/chess-knight.png")
        bknight= PhotoImage(file="D:/chess/chess-pack/chess-knight (1).png")
        wqueen = PhotoImage(file="D:/chess/chess-pack/chess-queen.png")
        bqueen= PhotoImage(file="D:/chess/chess-pack/chess-queen (1).png")
        wking=PhotoImage(file="D:/chess/chess-pack/chess-king.png")
        bking=PhotoImage(file="D:/chess/chess-pack/chess-king (1).png")
        return wpawn,bpawn,wrook,brook,wknight,bknight,wbishop,bbishop,wqueen,bqueen,wking,bking
    def donothing():
       x = 0
    def draw(self,info):
        try: 
            self.pcanvas.get_tk_widget().destroy()
        except:
            pass
        fig=Figure(figsize = (5, 5),dpi = 100)
        check= type(info["score"].relative)
        print(f"if Mate{check}")
        if check==chess.engine.Mate:
            self.y.append(info["score"].relative.score(mate_score=100000))
        else:
            self.y.append(info["score"].relative.score())
        if  self.board.get_board().turn==False:
            self.y[-1]=-self.y[-1]
        print(f"{self.y=}")
        plot1 = fig.add_subplot()
        y=np.array(self.y)
        plot1.plot(self.y ,marker="o",mfc='k')
        self.pcanvas = FigureCanvasTkAgg(fig,master = self.frame2)  
       # self.pcanvas.draw()
  
        self.pcanvas.get_tk_widget().pack()
  
        # creating the Matplotlib toolbar
  
        # placing the toolbar on the Tkinter window
        self.pcanvas.get_tk_widget().pack()
    def game(self,delet=False):
        self.board.set_board(chess.Board())
        if delet:
            self.root.destroy

        self.root = Tk()
        self.root.title('Chess')
        #root.geometry('640x480')
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=1)
        filemenu.add_command(label="PVP", command=lambda:self.game(True))
        filemenu.add_command(label="Open", command=self.donothing)
        filemenu.add_command(label="Save", command=self.donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="random white", command=lambda:self.cheek_boot("White","random"))
        helpmenu.add_command(label="random black", command=lambda:self.cheek_boot("Black","random"))
        
        helpmenu.add_command(label="keras white", command=lambda:self.cheek_boot("White","keras"))
        helpmenu.add_command(label="keras black", command=lambda:self.cheek_boot("Black","keras"))
        helpmenu.add_command(label="pesto white", command=lambda:self.cheek_boot("White","pesto"))
        helpmenu.add_command(label="pesto black", command=lambda:self.cheek_boot("Black","pesto"))
        helpmenu.add_command(label="disable white.", command=lambda:self.cheek_boot("White"))
        helpmenu.add_command(label="disablwe black", command=lambda:self.cheek_boot("Black"))
        menubar.add_cascade(label="Bot", menu=helpmenu)

        self.root.config(menu=menubar)
        self.m = Menu(self.root, tearoff = 1)
        #self.keras_model = keras.models.load_model("D:\chess\chess-pack\weights.hdf5")
        bg = PhotoImage(file ='D:/chess/chess-pack/board.png')
        frame1=Frame(self.root)
        frame1.pack(side="left")
        self.frame2=Frame(self.root)
        self.frame2.pack(side="right")
        self.canvas = Canvas(frame1, bg="black", bd=0, highlightthickness=0, width=480, height=480)
        #canvas_move = Canvas(frame2, bg="white", bd=0, highlightthickness=0, width=100, height=240)
        #Wself.canvas_stack = Canvas(root, bg="black", bd=0, highlightthickness=0, width=50, height=240)
        self.canvas.pack()
        #canvas_move.pack()
       # self.canvas_stack.pack()
        self.Output = Text(self.frame2, height = 15,width = 40,bg = "light cyan")
        self.Output.pack(side="top")
        self.canvas.create_image(0,0,anchor=NW,image=bg)
        images= self.get_images()
        for i in range(8):
            self.pieces.append(Pieces(f"wpawn{i}",self.canvas.create_image(30+60*i,390,image=images[0])))
            self.pieces.append(Pieces(f"bpawn{i}",self.canvas.create_image(30+60*i,90,image=images[1])))
        self.pieces.append(Pieces("wrook1",self.canvas.create_image(30,450,image=images[2])))
        self.pieces.append(Pieces("brook1",self.canvas.create_image(30,30,image=images[3])))
        self.pieces.append(Pieces("wrook2",self.canvas.create_image(450,450,image=images[2])))
        self.pieces.append(Pieces("brook2",self.canvas.create_image(450,30,image=images[3])))
        self.pieces.append(Pieces("wknight1",self.canvas.create_image(90,450,image=images[4])))
        self.pieces.append(Pieces("bknight1",self.canvas.create_image(90,30,image=images[5])))
        self.pieces.append(Pieces("bknight1",self.canvas.create_image(390,450,image=images[4])))
        self.pieces.append(Pieces("bknight2",self.canvas.create_image(390,30,image=images[5])))
        self.pieces.append(Pieces("wbishop1",self.canvas.create_image(150,450,image=images[6])))
        self.pieces.append(Pieces("bbishop1",self.canvas.create_image(150,30,image=images[7])))
        self.pieces.append(Pieces("wbishop2",self.canvas.create_image(330,450,image=images[6])))
        self.pieces.append(Pieces("bbishop2",self.canvas.create_image(330,30,image=images[7])))
        self.pieces.append(Pieces("wqueen",self.canvas.create_image(210,450,image=images[8])))
        self.pieces.append(Pieces("bqueen",self.canvas.create_image(210,30,image=images[9])))
        self.pieces.append(Pieces("wking",self.canvas.create_image(270,450,image=images[10])))
        self.pieces.append(Pieces("bking",self.canvas.create_image(270,30,image=images[11])))
        self.display_text = StringVar()
       # self.moves=canvas_move.create_text(540, 0, text=self.display_text, fill="black", font=('Helvetica 10 bold'))
        #self.display = Label(self.canvas, textvariable=self.display_text)
        #self.display.place(height = 240, width = 60,anchor ="e")
        #self.display.pack() 
        #self.canvas.create_window(540, 10, window=self.display) 
        
        self.engine= chess.engine.SimpleEngine.popen_uci("D:/chess/chess-pack/stockfish_15_win_x64_popcnt/stockfish_15_x64_popcnt.exe")
        while not self.board.is_game_over():
            #print("not over")
            self.run=self.root.after(3000,lambda:self.run_bot(self.root))            
            self.canvas.bind('<Button-1>', self.select)
            self.Output.bind('<Key>',lambda e:"break")
            self.root.attributes('-fullscreen', False)
            self.root.mainloop()
Game()

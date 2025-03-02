import chess
from dictionary import alpha_dict,number_dict
 
class Board():
    def init(self,board=chess.Board()):
        self.board=board

    def attacked_squares(self,board, color):
        attacked = chess.SquareSet()
        for attacker in chess.SquareSet(board.occupied_co[color]):
            attacked |= board.attacks(attacker)
        attacked=str(attacked)
        res=[]
        for i in attacked:
            if i==' ':
                continue
            elif i== '.':
                res.append(0)
            elif i=='1':
                res.append(1)
        return [res[x:x+8] for x in range(0, len(res), 8)]

    def convert_to_int(self,board):
        
        l = [0] * 64
        #l[sq] = board.piece_type_at(sq)
        for sq in chess.scan_reversed(board.occupied_co[chess.BLACK]):  # Check if white
            l[sq] = board.piece_type_at(sq)
        for sq in chess.scan_reversed(board.occupied_co[chess.WHITE]):  # Check if black
            l[sq] = -board.piece_type_at(sq) 
        res=[]
        for i in range(1,7):
            t=[]

            for obj in l:
                t.append(1)if obj==i else t.append(0)
            res.append([t[x:x+8] for x in range(0, len(t), 8)])
        for i in range(-1,-7,-1):
            t=[]
            for obj in l:
                t.append(-1)if obj==i else t.append(0)
            res.append([t[x:x+8] for x in range(0, len(t), 8)])
        res.append(self.attacked_squares(board.turn))
        res.append(self.attacked_squares(not board.turn))

        return  res
    def cor_to_move(self,x:int,y:int):
        a  = self.read_dict(alpha_dict,self.tran_cor(x))
        b = self.read_dict(number_dict,self.tran_cor(y))
        return a+str(b)
    def move_to_cor(x:str,y:int):
        a=alpha_dict[x]
        b=number_dict[int(y)]
        return int(a), int(b)
    def one_move_to_cor(x:str):
        a=alpha_dict[x]
        return int(a)
    def get_board(self):
        return self.board
    def set_board(self,board):
        self.board=board
    def get_turn(self):
        return self.board.turn
    def  is_game_over(self):
        self.board.is_game_over()

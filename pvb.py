import random
import chess
class Bot():

    def random_bot(self,board,turn,canvas):

        if (turn =="White" and board.turn ) or (turn=="Black" and not board.turn ) :
            
            if board.legal_moves.count()>0:
                index=random.randint(0,board.legal_moves.count()-1)
                tmove=str(list(board.legal_moves)[index])
                print(f"{tmove=}")
                pos1=tmove[:2]
                pos2=tmove[2:]
                move=chess.Move.from_uci(f"{pos1}{pos2}")
               #s pos=Board.move_to_cor(pos1[0],pos1[1])
                return move,pos1,pos2

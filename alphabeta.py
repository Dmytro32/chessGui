from evolve import eval
def bestmove(board,a,b,maxPlayer,maxdepth):
    res=[]
    best_move=None
    def alphabeta(board,a,b,maxPlayer,depth):
        nonlocal  best_move
        if depth ==0 or board.is_game_over(): 
            return eval(board)
        if maxPlayer:
            v=float('-inf')
            for move in board.legal_moves:
                board1=board.copy()
                board1.push(move)
                score=alphabeta(board1,a,b,False,depth-1)
                if score >v or best_move==None:
                    v=score
                    if depth==maxdepth:
                        print(["max",move,score])
                        best_move=move
                a=max(a,v)
                if b<=a:
                    break
            return v
        else:
            v=float('inf')
            for move in  board.legal_moves:
                board1=board.copy()
                board1.push(move)
                score=alphabeta(board1,a,b,True,depth-1)
                #v = min(v,score)
                if v>score or best_move==None:
                    v=score
                    if depth==maxdepth:
                        print(["min",move,score])
                        best_move=move
                b=min(b,v)
                if b<=a:
                    break
            return v
    alphabeta(board,a,b,maxPlayer,maxdepth)
    return best_move

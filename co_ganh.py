
# ======================== Class Player =======================================
import random
class Player:
    # student do not allow to change two first functions

    Initial_Board = [
                  ['b', 'b', 'b', 'b', 'b'], \
                  ['b', '.', '.', '.', 'b'], \
                  ['b', '.', '.', '.', 'r'], \
                  ['r', '.', '.', '.', 'r'], \
                  ['r', 'r', 'r', 'r', 'r'], \
                ]
    def __init__(self, str_name):
        self.str = str_name

        self.opp = 'r' if str_name == 'b' else 'b'

        self.previous_state = [
                  ['b', 'b', 'b', 'b', 'b'], \
                  ['b', '.', '.', '.', 'b'], \
                  ['b', '.', '.', '.', 'r'], \
                  ['r', '.', '.', '.', 'r'], \
                  ['r', 'r', 'r', 'r', 'r'], \
                ]

        self.neighborPosDict = {}
        self.neighborPosDictFull = {}
        
        state_len = 5
        
        for r in range(state_len):
            for c in range(state_len):
                neighborPos = []
                temp1 = []
                temp2 = []

                # horizontal and vertical
                temp1.append((r,c-1))
                temp1.append((r,c+1))
                temp1.append((r-1,c))
                temp1.append((r+1,c))

                # diagonal      
                temp2.append((r-1,c-1))
                temp2.append((r+1,c+1))
                temp2.append((r-1,c+1))
                temp2.append((r+1,c-1))
                
                temp1 = list(filter(lambda x : (x[0] >= 0 and x[0] <= 4) and (x[1] >= 0 and x[1] <= 4),temp1))
                temp2 = list(filter(lambda x : (x[0] >= 0 and x[0] <= 4) and (x[1] >= 0 and x[1] <= 4),temp2))
                
                # Full adj
                self.neighborPosDictFull[str(r*state_len+c)] = temp1 + temp2
                
                # Valid move adj
                neighborPos = temp1
                if not((r % 2 == 0 and c % 2 != 0) or (r % 2 != 0 and c % 2 == 0)):
                    neighborPos += temp2            
                
                self.neighborPosDict[str(r*state_len+c)] = neighborPos


    

    def __str__(self):
        return self.str
    
    def flatten(self, lst):
        return [item for sublist in lst for item in sublist]

    def getBoard(self , move, state):
        new_state = self.board_copy(state)
    
        # Next move
        row,col = move[1]
        max_row = max_col = 4
        
        if move[0] == move[1]:
            return new_state
        
        oldrow,oldcol = move[0]
        if new_state[oldrow][oldcol] != '.':
            new_state[row][col] = new_state[oldrow][oldcol]
            new_state[oldrow][oldcol] = '.'

        # Check GH,dont check corner
        corner = [(0,0),(0,4),(4,0),(4,4)]
        GHpiece = []
        if (row,col) not in corner:
                # left,right,down up
            if row == 0 or row == max_row:
                if new_state[row][col-1] == new_state[row][col+1] and new_state[row][col-1] != new_state[row][col]:
                    GHpiece.append((row,col-1))
                    GHpiece.append((row,col+1))
            elif col == 0 or col == max_col:
                if new_state[row-1][col] == new_state[row+1][col] and new_state[row-1][col] != new_state[row][col]:
                    GHpiece.append((row-1,col))
                    GHpiece.append((row+1,col))
            # Diagonal
            else:
                if new_state[row][col-1] == new_state[row][col+1] and new_state[row][col-1] != new_state[row][col]:
                        GHpiece.append((row,col-1))
                        GHpiece.append((row,col+1))
                if new_state[row-1][col] == new_state[row+1][col] and new_state[row-1][col] != new_state[row][col]:
                        GHpiece.append((row-1,col))
                        GHpiece.append((row+1,col))
                if not((row % 2 == 0 and col % 2 != 0) or (row % 2 != 0 and col % 2 == 0)):
                    if new_state[row-1][col-1] == new_state[row+1][col+1] and new_state[row-1][col-1] != new_state[row][col]:
                            GHpiece.append((row-1,col-1))
                            GHpiece.append((row+1,col+1))
                    if new_state[row+1][col-1] == new_state[row-1][col+1] and new_state[row+1][col-1] != new_state[row][col]:
                            GHpiece.append((row-1,col+1))
                            GHpiece.append((row+1,col-1))
        
        if GHpiece:
            for r,c in GHpiece:
                if new_state[r][c] != '.':
                    new_state[r][c] = self.changePiece(new_state[r][c])
   
        # Check CH,check for each piece
        neighborPos = self.neighborPosDict[str(row*len(new_state)+col)]
        
        # Get neighbor of "new move" piece
        queue = []
        for r,c in neighborPos:
            if new_state[r][c] != new_state[row][col] and new_state[r][c] != '.':
                queue.append((r,c))
        
        # For each neighbor (it might "outside" or "inside" neighbor)
        for e in queue:

            adjPiece = [e]
            chFlag = True
            temp_state = self.board_copy(new_state)
            
            # Like BFS 
            while adjPiece and chFlag:
                #Get b to visit and mark it as visited,then pop it out from CHpiece
                temp = adjPiece.pop(0)
                #Get it neighbor
                neighborPos = self.neighborPosDict[str(temp[0]*len(new_state)+temp[1])]
                res = []
                for r,c in neighborPos:
                    if temp_state[r][c] == '.':
                        res = []
                        chFlag = False
                        break
                    elif temp_state[r][c] != temp_state[row][col]:
                        res.append((r,c))

                if chFlag:
                    temp_state[temp[0]][temp[1]] = self.changePiece(temp_state[temp[0]][temp[1]])
                    adjPiece += res
            
            if chFlag:
                new_state = temp_state
                break
        return new_state

    def changePiece(self,piece):
        if piece == 'r':
            return 'b'
        elif piece == 'b':
            return 'r'

    def board_copy(self,board):
        new_board = [[]]*5
        for i in range(5):
            new_board[i] = [] + board[i]
        return new_board
    
    # Check if pos can make a GH
    def isGH(self, player, pos, state):
        opp = 'b'
        if player == 'b':
            opp = 'r'
            
        row = pos[0]
        col = pos[1]
        max_row = max_col = 4
        # Check GH,dont check corner
        corner = [(0,0),(0,4),(4,0),(4,4)]

        if (row,col) not in corner:
            if row == 0 or row == max_row:
                if state[row][col-1] == state[row][col+1] and state[row][col-1] == opp:
                    return True
            elif col == 0 or col == max_col:
                if state[row-1][col] == state[row+1][col] and state[row-1][col] == opp:
                    return True
            # Diagonal
            else:
                if state[row][col-1] == state[row][col+1] and state[row][col-1] == opp:
                    return True
                if state[row-1][col] == state[row+1][col] and state[row-1][col] == opp:
                    return True

                if not (row % 2 == 0 and col % 2 != 0) or (row % 2 != 0 and col % 2 == 0):
                    if state[row][col-1] == state[row][col+1] and state[row][col-1] == opp:
                            return True
                    if state[row-1][col] == state[row+1][col] and state[row-1][col] == opp:
                            return True
                    if state[row-1][col-1] == state[row+1][col+1] and state[row-1][col-1] == opp:
                            return True
                    if state[row+1][col-1] == state[row-1][col+1] and state[row+1][col-1] == opp:
                            return True
        return False

    def getTrapMove(self,player, state):
        temp1 = self.flatten(self.previous_state)
        temp2 = self.flatten(state)
        
        print(temp1)
        print(temp2)
        # If not GH or CH
        if temp1.count('r') != temp2.count('r'):
            print("aaaaa")
            return []

        cmp_state = list(zip(temp1,temp2))

        diff_state = [cmp_state.index((i,j)) for i,j in cmp_state if i != j]
        
        curr_move = list(filter(lambda pos: temp2[pos] != '.',diff_state)).pop()

        # Get all valid move nieghbor,check for each piece
        neighborPos = self.neighborPosDict[str(curr_move)]
    
        # Get all pos can make trap
        adjPiece = list(filter(lambda x : state[x[0]][x[1]] == '.',neighborPos))
        
        trapMove = []
        
        # print(str(curr_move))
        # print(neighborPos)
        # print(adjPiece)
     
        for r,c in adjPiece:
            neighborPos = self.neighborPosDict[str(r*len(state)+c)]
            pos = (r,c)
            
            trapEnemy = list(filter(lambda x: state[x[0]][x[1]] == player,neighborPos))
            if trapEnemy and self.isGH(player,pos,state):
                trapMove += list(map(lambda x : [x,pos],trapEnemy))
        
        return trapMove
    
    def generateMove(self,player,state):
        moveLst = []
        # If not trap
        for r in range(len(state)):
            for c in range(len(state)):
                if state[r][c] == player:
                    neighborPos = self.neighborPosDict[str(r*len(state)+c)]
                    for pos in neighborPos:
                        if state[pos[0]][pos[1]] == '.':
                            moveLst.append([(r,c),pos])
        
        return moveLst
    
    def evaluateBoard(self,player,state):
        temp = self.flatten(state)
        
        opp = 'b'
        if player == 'b':
            opp = 'r'

        return temp.count(player) - temp.count(opp)

    def minimaxRoot(self,player, depth, state, isMaximisingPlayer = True):
        
        trapMove = []
        if state != self.previous_state:
            trapMove = self.getTrapMove(player,state)

        if trapMove:
            print("trap")
            print("trap")
            print("trap" + str(trapMove))
            return trapMove[random.randint(0,len(trapMove) - 1)]
        
        moveLst = self.generateMove(self.str,state)
        
        if moveLst:
            return moveLst[random.randint(0,len(moveLst) - 1)]
        else:
            return []
    

    # Student MUST implement this function
    # The return value should be a move that is denoted by a list of tuples:
    # [(row1, col1), (row2, col2)] with:
        # (row1, col1): current position of selected piece
        # (row2, col2): new position of selected piece
    def next_move(self, state):            
        result = self.minimaxRoot(self.str,3,state)
        
        if result:
            self.previous_state = self.getBoard(result,state)
        return result

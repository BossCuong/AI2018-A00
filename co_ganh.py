
# ======================== Class Player =======================================
import random
class Player:
    # student do not allow to change two first functions
    def __init__(self, str_name):
        self.str = str_name

        self.opp = 'r' if str_name == 'b' else 'b'

        self.previous_state = []

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
                
                temp1 = list(filter(lambda x : (x[0] >= 0 and x[0] <= 4) and (x[1] >= 0 and x[1] <=4),temp1))
                temp2 = list(filter(lambda x : (x[0] >= 0 and x[0] <= 4) and (x[1] >= 0 and x[1] <=4),temp2))
                
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
    
    # Check if pos can make a GH
    def isGH(self, pos, state):

        row = pos[0]
        col = pos[1]
        max_row = max_col = 4
        # Check GH,dont check corner
        corner = [(0,0),(0,4),(4,0),(4,4)]

        if (row,col) not in corner:
            if row == 0 or row == max_row:
                if state[row][col-1] == state[row][col+1] and state[row][col-1] == self.opp:
                    return True
            elif col == 0 or col == max_col:
                if state[row-1][col] == state[row+1][col] and state[row-1][col] == self.opp:
                    return True
            # Diagonal
            else:
                if state[row][col-1] == state[row][col+1] and state[row][col-1] == self.opp:
                    return True
                if state[row-1][col] == state[row+1][col] and state[row-1][col] == self.opp:
                    return True

                if not (row % 2 == 0 and col % 2 != 0) or (row % 2 != 0 and col % 2 == 0):
                    if state[row][col-1] == state[row][col+1] and state[row][col-1] == self.opp:
                            return True
                    if state[row-1][col] == state[row+1][col] and state[row-1][col] == self.opp:
                            return True
                    if state[row-1][col-1] == state[row+1][col+1] and state[row-1][col-1] == self.opp:
                            return True
                    if state[row+1][col-1] == state[row-1][col+1] and state[row+1][col-1] == self.opp:
                            return True
        return False

    def getTrapPos(self, state):
        temp1 = self.flatten(self.previous_state)
        temp2 = self.flatten(state)

        if temp1.count('r') == temp2.count('r'):
            return []

        cmp_state = list(zip(temp1,temp2))

        diff_state = [cmp_state.index((i,j)) for i,j in cmp_state if i != j]
        
        curr_move = list(filter(lambda pos: temp2[pos] != '.',diff_state)).pop()

        # Get all valid move nieghbor,check for each piece
        neighborPos = self.neighborPosDict[str(curr_move)]
    
        # Get all pos can make trap
        adjPiece = list(filter(lambda x : state[x[0]][x[1]] == '.',neighborPos))
        
        trapPos = []

        for r,c in adjPiece:
            neighborPos = self.neighborPosDict[str(r*len(state)+c)]
            pos = (r,c)

            if (list(filter(lambda x: state[x[0]][x[1]] == self.opp,neighborPos)) 
                and self.isGH(pos,state)):
                trapPos.append((r,c))
        
        return trapPos

    def generateMove(self, player ,state):
        moveLst = []
        
        for r in range(len(state)):
            for c in range(len(state)):
                if state[r][c] == player:
                    neighborPos = self.neighborPosDict[str(r*len(state)+c)]
                    for pos in neighborPos:
                        if state[pos[0]][pos[1]] == '.':
                            moveLst.append([(r,c),pos])
        if not moveLst:
            return []
        return moveLst[random.randint(0,len(moveLst) - 1)]
    # Student MUST implement this function
    # The return value should be a move that is denoted by a list of tuples:
    # [(row1, col1), (row2, col2)] with:
        # (row1, col1): current position of selected piece
        # (row2, col2): new position of selected piece
    def next_move(self, state):
        if state == self.previous_state:
            return []
        result = self.generateMove(self.str,state)
        print(result)
        self.previous_state = state
        return result
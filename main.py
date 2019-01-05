
import imp
import time
#======================================================================


def board_print(board, move=[], num=0):

    print("====== The current board(", num, ")is (after move): ======")
    if move:
        print("move = ", move)
    for i in [4, 3, 2, 1, 0]:
        print(i, ":", end=" ")
        for j in range(5):
            print(board[i][j], end=" ")
        print()
    print("   ", 0, 1, 2, 3, 4)
    print("")


def board_copy(board):
    new_board = [[]]*5
    for i in range(5):
        new_board[i] = [] + board[i]
    return new_board

#======================================================================

# Student SHOULD implement this function to change current state to new state properly
def changePiece(piece):
    if piece == 'r':
        return 'b'
    elif piece == 'b':
        return 'r'

def doit(move, state):
    new_state = board_copy(state)
    
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
                new_state[r][c] = changePiece(new_state[r][c])

    neighborPosDict = {}
    neighborPos = []
    for r in range(len(new_state)):
        for c in range(len(new_state)):
            neighborPos.append((r,c-1))
            neighborPos.append((r,c+1))
            neighborPos.append((r-1,c))
            neighborPos.append((r+1,c))
            #if not((row % 2 == 0 and col % 2 != 0) or (row % 2 != 0 and col % 2 == 0)):
            neighborPos.append((r-1,c-1))
            neighborPos.append((r+1,c+1))
            neighborPos.append((r-1,c+1))
            neighborPos.append((r+1,c-1))

            neighborPos = list(filter(lambda x : (x[0] >= 0 and x[0] <= 4) and (x[1] >= 0 and x[1] <=4),neighborPos))
            
            neighborPosDict[str(r*len(new_state)+c)] = neighborPos

            neighborPos = []
    
    # Check CH,check for each piece
    neighborPos = neighborPosDict[str(row*len(new_state)+col)]
    
    # Get neighbor of "new move" piece
    queue = []
    for r,c in neighborPos:
        if new_state[r][c] != new_state[row][col] and new_state[r][c] != '.':
            queue.append((r,c))
    
    # For each neighbor (it might "outside" or "inside" neighbor)
    for e in queue:

        adjPiece = [e]
        chFlag = True
        temp_state = board_copy(new_state)
        
        # Like BFS 
        while adjPiece and chFlag:
            #Get b to visit and mark it as visited,then pop it out from CHpiece
            temp = adjPiece[0]
            adjPiece.pop(0)
        
            #Get it neighbor
            neighborPos = neighborPosDict[str(temp[0]*len(new_state)+temp[1])]
            res = []
            for r,c in neighborPos:
                if temp_state[r][c] == '.':
                    res = []
                    chFlag = False
                    break
                if temp_state[r][c] != temp_state[row][col]:
                    res.append((r,c))
            
            temp_state[temp[0]][temp[1]] = changePiece(temp_state[temp[0]][temp[1]])
            adjPiece += res
        
        if chFlag:
            new_state = temp_state
            break
    return new_state

#======================================================================
Initial_Board = [
                  ['b', 'b', 'b', 'b', 'b'], \
                  ['b', '.', '.', '.', 'b'], \
                  ['b', '.', '.', '.', 'r'], \
                  ['r', '.', '.', '.', 'r'], \
                  ['r', 'r', 'r', 'r', 'r'], \
                ]

# 4 : r r r r r
# 3 : r . . . r
# 2 : b . . . r
# 1 : b . . . b
# 0 : b b b b b
#     0 1 2 3 4
#======================================================================


def play(student_a, student_b, start_state=Initial_Board):
    player_a = imp.load_source(student_a, student_a + ".py")
    player_b = imp.load_source(student_b, student_b + ".py")

    a = player_a.Player('b')
    b = player_b.Player('r')
    
    curr_player = a
    state = start_state    

    board_num = 0
        
    board_print(state)
    
    while True:
        print("It is ", curr_player, "'s turn")

        start = time.time()
        move = curr_player.next_move(state)
        elapse = time.time() - start

        # print(move)

        if not move:
            break

        print("The move is : ", move, end=" ")
        print(" (in %.2f ms)" % (elapse*1000), end=" ")
        if elapse > 3.0:
            print(" ** took more than three second!!", end=" ")
            break
        print()
        # check_move
        state = doit(move, state)

        board_num += 1
        board_print(state, num=board_num)

        if curr_player == a:
            curr_player = b
        else:
            curr_player = a

    print("Game Over")
    if curr_player == a:
        print("The Winner is:", student_b, 'red')
    else:
        print("The Winner is:", student_a, 'blue')

play("co_ganh", "co_ganh")

import numpy as np
from collections import deque

# reading the inputs as the initial state
filepath = 'input6.txt'
state = np.zeros((6,4))
with open(filepath) as fp:
    lines = fp.readlines()
    i=0
    for line in lines:
        state[i,:]=line.split(" ")
        i+=1
print("the loaded cube state requiers 6 moves to solve")

def is_goal_state(state,goal=None):
    """
    a function to return whether <state> input is a goal state
    if <goal> is given , it will check <state> with the given goal
    otherwise it will be checked automaticaly
    """
    state = np.array(state)
    if(goal is None):
        if(np.sum(state.std(1))==0):
            return True
    else:
        goal = np.array(goal)
        if(np.sum(abs(state-goal))==0):
            return True
    return False

def change_state(state,move):
    """
    changes the <state> according to the given <move>
    
    (depending on the type of moves this method will change to fit the
    needs of the related problem)
    """
    side = (move-1)//2+1 # number between <1,...,6> regarding the side which is about to turn
    rotation = np.mod(move,2) # number between <0,1> indicating whether rotation is clock wise (==1) or not (==0)
#     print(side,rotation)
    # fixing the neighbours whcih are about to change
    u = [0,1] # upper cells
    r = [1,3] # right cells
    d = [2,3] # down cells
    l = [0,2] # left cells
    if(side==1):
        neighbours = [[6,d,1],[4,u,0],[3,u,0],[2,u,0]]
    elif(side==2):
        neighbours = [[1,l,0],[3,l,0],[5,l,0],[6,l,0]]
    elif(side==3):
        neighbours = [[1,d,0],[4,l,0],[5,u,1],[2,r,1]]
    elif(side==4):
        neighbours = [[1,r,0],[6,r,0],[5,r,0],[3,r,0]]
    elif(side==5):
        neighbours = [[3,d,0],[4,d,0],[6,u,1],[2,d,0]]
    elif(side==6):
        neighbours = [[1,u,0],[2,l,1],[5,d,1],[4,r,0]]
    
    if(rotation==1): # clock wise
        # changing the neighbours
        temp = np.copy(state[int(neighbours[3][0]-1)])
        for i in range(3,0,-1):
            dest = neighbours[i]
            src = neighbours[i-1]
            in_order = dest[1]
            out_order = src[1]
            if (src[2]==1):
                out_order = src[1][::-1]
            if (dest[2]==1):
                in_order = dest[1][::-1]
#             print(str(src[0])+str(out_order)+" -->> "+str(dest[0])+str(in_order))
#             print(str(state[src[0]-1,src[1]])+" -->> "+str(state[dest[0]-1,order]))
#             print("___________________")
            state[dest[0]-1,in_order]= state[src[0]-1,out_order]
        dest = neighbours[0]
        in_order = dest[1]
        out_order = neighbours[3][1]
        if (neighbours[3][2]==1):
            out_order = neighbours[3][1][::-1]
        if (dest[2]==1):
            in_order = dest[1][::-1]
#         print(str(neighbours[3][0])+str(out_order)+"-->>"+
#               str(dest[0])+str(in_order))
#         print("___________________")
        state[int(dest[0])-1,in_order]= temp[out_order]
        # rotating the side it self
        state[side-1] = state[side-1,[2,0,3,1]]
        
    else: # unclock wise
        temp = np.copy(state[int(neighbours[0][0]-1)])
        for i in range(0,3):
            dest = neighbours[i]
            src = neighbours[i+1]
            in_order = dest[1]
            out_order = src[1]
            if (src[2]==1):
                out_order = src[1][::-1]
            if (dest[2]==1):
                in_order = dest[1][::-1]
#             print(str(src[0])+str(out_order)+" -->> "+str(dest[0])+str(in_order))
#             print("___________________")
            state[dest[0]-1,in_order]= state[src[0]-1,out_order]
        dest = neighbours[3]
        in_order = dest[1]
        out_order = neighbours[0][1]
        if (neighbours[0][2]==1):
            out_order = neighbours[0][1][::-1]
        if (dest[2]==1):
            in_order = dest[1][::-1]
#         print(str(neighbours[0][0])+str(out_order)+"-->>"+
#               str(dest[0])+str(in_order))
#         print("___________________")
        state[int(dest[0])-1,in_order]= temp[out_order]
        # rotating the side it self
        state[side-1] = state[side-1,[1,3,0,2]]
        
    return state

created_nodes=0
opened_nodes=0
nodes_in_memory=0
max_nodes_in_memory=0

def is_redundant(move1,move2):
    if move1 == 1 :
        if move2==2 : return True
    elif move1 == 2:
        if move2==1 : return True
    elif move1 == 3:
        if move2==4 : return True
    elif move1 == 4:
        if move2==3 : return True
    elif move1 == 5:
        if move2==6 : return True
    elif move1 == 6:
        if move2==5 : return True
    return False

def UCS(state,moves):
    if is_goal_state(state):
        return []
    global created_nodes
    global opened_nodes
    global nodes_in_memory
    global max_nodes_in_memory
    queue = deque()
    queue.append([state,[]])
    while(True):
        item = queue.popleft()
        opened_nodes+=1
        nodes_in_memory=len(queue)
        max_nodes_in_memory=max(max_nodes_in_memory,nodes_in_memory)
        for move in moves:
            n = change_state(np.copy(np.array(item[0])),move)
            m = item[1].copy()
            if is_goal_state(n):
                m.append(move)
                return m
            if len(m)>0 :
                if is_redundant(m[len(m)-1],move): continue
            m.append(move)
            found = False
## the below code is actually a part of the algorithem
## which decreases expanded nodes , yet , due to the
## latancy casued by for loops in python , it reduces
## speed. so it is commented for now

#             print(len(queue),end=' ')
#             for i in range(len(queue)):
#                 if np.sum(abs(queue[i][0]-n))==0 :
#                     found = True
#                     if len(m) < len(queue[i][1]) :
#                         queue[i][1] = m
#                     break
            if not found:
                queue.append([n,m])
                created_nodes+=1
def show_moves(input):
    for move in input:
        side = (move-1)//2+1 # number between <1,...,6> regarding the side which is about to turn
        rotation = np.mod(move,2) # number between <0,1> indicating whether rotation is clock wise (==1) or not (==0)
        print("     side "+str(side),end=" ")
        if rotation==1:
            print("clockwise")
        else:
            print("anti-clockwise")
    print("")
    
#############################################################
print("solving the problem using UCS...")

moves = [1,2,3,4,5,6]
output = UCS(np.copy(state),moves)
print("Answer:",end=" ")
if output is False :
    print("couldn't solve the problem")
else:
    print(output)
    show_moves(output)
print("nodes created : "+str(created_nodes))
print("opened nodes : "+str(opened_nodes))
if(output is not False):
    print("goal depth : "+str(len(output)))
print("max nodes in mem : "+str(max_nodes_in_memory))
created_nodes=0
opened_nodes=0
nodes_in_memory=0
max_nodes_in_memory=0
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

def get_all_goal_states():
    filepath = 'done.txt'
    state = np.zeros((6,4))
    with open(filepath) as fp:
        lines = fp.readlines()
        i=0
        for line in lines:
            state[i,:]=line.split(" ")
            i+=1
    output = []
    for i in range(4):
        change_state(state,5)
        output.append([np.copy(change_state(state,12)),[]])
    return output
def inverse(moves):
    new_moves = []
    for move in moves:
        if(np.mod(move,2)==1):
            new_moves.append(move+1)
        else:
            new_moves.append(move-1)
    return new_moves

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

def bidirectional(initial_state,moves):
    global created_nodes
    global opened_nodes
    global nodes_in_memory
    global max_nodes_in_memory
    forward_queue = []
    forward_queue.append([initial_state.copy(),[]])
    backward_queue  = get_all_goal_states()
    visited = []
    while(len(forward_queue)!=0 and len(backward_queue)!=0):
        item = forward_queue.pop(0)
        opened_nodes+=1
        nodes_in_memory-=1
        if is_goal_state(item[0]):
            return item[1]
        for b in backward_queue:
            if np.sum(abs(b[0]-item[0]))==0:
                return [item[1],inverse(b[1][::-1])]
        for move in moves:
            m = item[1].copy()
            if len(m)>0 :
                if is_redundant(m[len(m)-1],move): continue
            m.append(move)
            n = change_state(np.copy(np.array(item[0])),move)
            found = False
            for x in visited:
                if np.sum(abs(x-n))==0:
                    found=True
                    break
            if not found:
                forward_queue.append([n,m])
            created_nodes+=1
            nodes_in_memory+=1
        visited.append(item[0])
        max_nodes_in_memory=max(max_nodes_in_memory,nodes_in_memory)
        item = backward_queue.pop(0)
        opened_nodes+=1
        nodes_in_memory-=1
        if is_goal_state(item[0],initial_state):
            return item[1][::-1]
        for f in forward_queue:
            if np.sum(abs(f[0]-item[0]))==0:
                return [f[1],inverse(item[1][::-1])]
        for move in moves:
            m = item[1].copy()
            m.append(move)
            n = change_state(np.copy(np.array(item[0])),move)
            found = False
            for x in visited:
                if np.sum(abs(x-n))==0:
                    found=True
                    break
            if not found:
                backward_queue.append([n,m])
            created_nodes+=1
            nodes_in_memory+=1
        max_nodes_in_memory=max(max_nodes_in_memory,nodes_in_memory)
        visited.append(item[0])

def show_moves(input):
    if len(input)>1:
        input = input[0]+input[1]
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
print("solving the problem using Bidirectional approach...")

moves = [1,2,3,4,5,6]
output = bidirectional(np.copy(state),moves)
print("Answer:",end=" ")

if output is False :
    print("couldn't solve the problem")
else:
    print(output)
    show_moves(output)
    if len(output)>1:
        print("goal depth : "+str(len(output[0])+len(output[1])))
    else:
        print("goal depth : "+str(len(output)))
print("nodes created : "+str(created_nodes))
print("opened nodes : "+str(opened_nodes))
print("max nodes in Mem : "+str(max_nodes_in_memory))
created_nodes=0
opened_nodes=0
nodes_in_memory=0
max_nodes_in_memory=0
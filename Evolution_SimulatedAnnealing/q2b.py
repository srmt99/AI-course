import numpy as np
import matplotlib.pyplot as plt
# initilizing colors (can change for new problems)
colors = ["red","blue","yellow","green"]
# initilizing the adjacancy graph (can change)
nodes = [
    ["first_node",["second_node","third_node"]],
    ["second_node",["first_node","third_node","fourth_node"]],
    ["third_node",["first_node","second_node","fourth_node","fifth_node","sixth_node"]],
    ["fourth_node",["second_node","third_node","fifth_node"]],
    ["fifth_node",["third_node","fourth_node","sixth_node"]],
    ["sixth_node",["third_node","fifth_node"]]
]
#####
file = open("iran.txt",'r')
lines = file.readlines()
nodes = []
indx = 0
for line in lines:
    nodes.append([indx,line.replace("\n","").split(" ")])
    indx+=1
#####
# print(nodes[0])

def fitness(chromosome,nodes):
    fitness = 0
    edges = 0
    for member in chromosome:
        for neigbour in member[1]:
            edges+=1
            for i in range(len(chromosome)):
                if chromosome[i][0][0]==neigbour:
                    break
            if member[0][1] != chromosome[i][0][1]:
                fitness+=1
                
    return fitness/edges
def temp(T0,k,type):
    if type=="1":
        alpha = 0.997
        return T0 * (alpha**k)
    elif type=="2":
        alpha = 2
        return T0/(1+alpha*np.log(1+k))
    elif type=="3":
        alpha = 0.03
        return T0/(1+alpha*k)
    elif type=="4":
        alpha = 0.2
        return T0/(1+alpha*(k**2))
    else:
        print("invalid type , should be among <1,2,3,4>")
    return None
def simulated_annealing(nodes,features,colding_type,initial_temperature,time_out):
    # initilize current state
    temp_ = np.copy(nodes)
    for j in range(len(nodes)):
        r = np.random.randint(len(features))
        temp_[j][0] = [nodes[j][0],features[r]]
    current_state = np.copy(temp_)
    time=0
    temp_hist = []
    while(time<time_out):
        time+=1
        T = temp(initial_temperature,time,colding_type)
        temp_hist.append(T)
        if T == 0 : return current_state
        # randomly select next_state
        next_state = np.copy(current_state)
        f_i = np.random.randint(len(features))
        g_i = np.random.randint(len(nodes))
        next_state[g_i][0]=np.copy([next_state[g_i][0][0],features[f_i]])
        delta_E = fitness(next_state,nodes) - fitness(current_state,nodes)
        if delta_E >= 0 :
            current_state = next_state
        else:
            if np.random.rand()<np.exp(delta_E/T):
#                 print(T,np.exp(delta_E/T))
                current_state = next_state
    print("     final fitness = "+str(fitness(current_state,nodes)))
    plt.plot(temp_hist)
    plt.xlabel("iteration(time)")
    plt.ylabel("Temperature")
    plt.title("Temp Func _"+str(colding_type)+"_")
    plt.show()
    return current_state

output = simulated_annealing(np.copy(nodes),colors,colding_type="1",initial_temperature=100,time_out=5000)
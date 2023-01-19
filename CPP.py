from Dijkstra import *

def sum_edges(graph):
    w_sum = 0
    l = len(graph)
    for i in range(l):
        for j in range(i,l):
            w_sum += graph[i][j]
    return w_sum
                                        
def get_odd(graph):
    degrees = [0 for i in range(len(graph))]
    for i in range(len(graph)):
        for j in range(len(graph)):
                if(graph[i][j]!=0):
                    degrees[i]+=1
                
    odds = [i for i in range(len(degrees)) if degrees[i]%2!=0]
    return odds

def gen_pairs(odds):
    pairs = []
    for i in range(len(odds)-1):
        pairs.append([])
        for j in range(i+1,len(odds)):
            pairs[i].append([odds[i],odds[j]])
        
    return pairs


def Chinese_Postman(graph):
    odds = get_odd(graph)
    if(len(odds)==0):
        return  _edges(graph)
    pairs = gen_pairs(odds)
    l = (len(pairs)+1)//2
    
    pairings_sum = []
    
    def get_pairs(pairs, done = [], final = []):
        
        if(pairs[0][0][0] not in done):
            done.append(pairs[0][0][0])
            
            for i in pairs[0]:
                f = final[:]
                val = done[:]
                if(i[1] not in val):
                    f.append(i)
                else:
                    continue
                
                if(len(f)==l):
                    pairings_sum.append(f)
                    return 
                else:
                    val.append(i[1])
                    get_pairs(pairs[1:],val, f)
                    
        else:
            get_pairs(pairs[1:], done, final)
            
    get_pairs(pairs)
    min_sums = []
    
    for i in pairings_sum:
        s = 0
        for j in range(len(i)):
            s += dijktra(graph, i[j][0], i[j][1])
        min_sums.append(s)
    
    added_dis = min(min_sums)
    chinese_dis = added_dis + sum_edges(graph)
    print ('min Sums: ', min_sums)
    return chinese_dis    
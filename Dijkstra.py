def dijktra(graph, source, dest):
    shortest = [1 for i in range(len(graph))]
    selected = [source]
    l = len(graph)
    inf = 10000000
    min_sel = inf
    for i in range(l):
        if(i==source):
            shortest[source] = 0
        else:
            if(graph[source][i]==0):
                shortest[i] = inf
            else:
                shortest[i] = graph[source][i]
                if(shortest[i] < min_sel):
                    min_sel = shortest[i]
                    ind = i
                
    if(source==dest):
        return 0
    selected.append(ind) 
    while(ind!=dest):
        for i in range(l):
            if i not in selected:
                if(graph[ind][i]!=0):
                    if((graph[ind][i] + min_sel) < shortest[i]):
                        shortest[i] = graph[ind][i] + min_sel
        temp_min = 1000000
        print('shortest:',shortest)
        
        for j in range(l):
            if j not in selected:
                if(shortest[j] < temp_min):
                    temp_min = shortest[j]
                    ind = j
        min_sel = temp_min
        selected.append(ind)
    return shortest[dest]
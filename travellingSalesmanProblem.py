# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""TravellingSalesmanProblem.py"""

import numpy as np
import random
import time
import matplotlib.pyplot as plt
from itertools import combinations

#Greedy
def TSP_Greedy(recent,notVisited,weight):
    notVisited.remove(recent)

    if len(notVisited) == 1:
      g = notVisited.pop()
      cost =  weight[recent][g] + weight[g][0]
      return cost
      
    else:
      dis = weight[recent][:]
      while True:
        i = np.argmin(dis) #min index
        if i in notVisited:
          cost = TSP_Greedy(i,notVisited,weight) + weight[recent][i]
          return cost
        else:
          dis[i] = 31 #設成大於1~30區間的數值



#Dynamic Programming
def TSP_DP(num, weight):
  notVisited = set([c for c in range(1,num)])
  D = {}

  for i in range(1,num):
    D[str(i)+"set()"] = weight[i][0]

  for k in range(1,num):
    for A in combinations(notVisited,k):
      for i in notVisited:
        if i not in A:
          every = []
          for j in A:
            s = sorted(set(A))
            s.remove(j)
            key = str(j)+str(set(s))
            every.append(weight[i][j]+D[key])
          key = str(i)+str(set(sorted(set(A))))
          D[key] = min(every)

  every = []
  for j in notVisited:
    v = notVisited.copy()
    v.remove(j)
    key = str(j)+str(v)
    every.append(weight[0][j]+D[key])
  return min(every)



#generate weight graph
def randomGraph(n):
  graph = np.zeros([n,n])
  for i in range(n):
    for j in range(n):
      if i != j and graph[i][j] == 0:
        graph[i][j] = random.randint(1, 30)
        graph[j][i] = graph[i][j]
  return graph




if __name__ == "__main__":

  averageTimeGreedy = []
  averageTimeDP = []
  errorSum = []

  cityNum = 20
  startPoint = 0

  for i in range(4,cityNum):
    print('頂點數：',i)
    runTimeGreedy = []
    runTimeDP = []
    gWeight = 0
    dpWeight = 0
    for times in range(5):
      notVisitedCities = set([k for k in range(i)])
      graph = randomGraph(i)

      start = time.perf_counter()
      dw = TSP_DP(i,graph)
      end = time.perf_counter()
      runTimeDP.append(end-start)
      dpWeight += dw
      print("DP Weight:",dw)

      start = time.perf_counter()
      gw = TSP_Greedy(startPoint,notVisitedCities,graph)
      end = time.perf_counter()
      runTimeGreedy.append(end-start)
      gWeight += gw
      print("Greedy Weight:",gw)

    print()
    averageTimeGreedy.append(np.mean(runTimeGreedy))
    averageTimeDP.append(np.mean(runTimeDP))
    errorSum.append((gWeight-dpWeight)/dpWeight)

  # 圖一
  plt.plot(np.arange(4,cityNum),averageTimeGreedy,label="Greedy")
  plt.plot(np.arange(4,cityNum),averageTimeDP,label="DP")
  plt.title('Average Run Time')
  plt.xlabel('Point Number')
  plt.ylabel('Seconds')
  plt.legend(loc='upper left')
  plt.show()

  #圖二
  plt.plot(np.arange(4,cityNum),errorSum)
  plt.title('Averge Error')
  plt.xlabel('Point Number')
  plt.ylabel('Weight')
  plt.show()
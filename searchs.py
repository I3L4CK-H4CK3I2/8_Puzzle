#!/usr/bin/python
'Created by l3L4CK H4CK3l2'

from queue import PriorityQueue
from time import time
from queue import Queue

class Puzzle:
    goal = [1,2,3,
            8,0,4,
            7,6,5]
    heuristic=None
    needs_hueristic=False
    num_of_instances=0

    def __init__(self,state,parent,action,path_cost,needs_hueristic=False):
        self.parent=parent
        self.state=state
        self.action=action
        if parent:
            self.path_cost = parent.path_cost + path_cost
        else:
            self.path_cost = path_cost
        if needs_hueristic:
            self.needs_hueristic=True
            self.generate_heuristic()
            self.evaluation_function1=self.heuristic + self.path_cost
            self.evaluation_function3=self.heuristic
        Puzzle.num_of_instances+=1

    def generate_heuristic(self):
        self.heuristic=0
        for num in range(0,9):
            if (self.state.index(num) != self.goal.index(num)):
                distance1  =self.state.index(num)
                distance2 = self.goal.index(num)
                i1 = int(distance1 / 3)
                j1 = int(distance1 % 3)
                i2 = int(distance2 / 3)
                j2 = int(distance2 % 3)
                distance=abs((i1+j1)-(i2+j2))
                self.heuristic=self.heuristic+distance

    def goal_test(self):
        if self.state == self.goal:
            return True
        return False

    @staticmethod
    def find_legal_actions(i,j):
        legal_action = ['U', 'D', 'L', 'R']
        if i == 0:
            legal_action.remove('U')
        elif i == 2:
            legal_action.remove('D')
        if j == 0:
            legal_action.remove('L')
        elif j == 2:
            legal_action.remove('R')
        return legal_action

    def generate_child(self):
        children=[]
        x = self.state.index(0)
        i = int(x / 3)
        j = int(x % 3)
        legal_actions=self.find_legal_actions(i,j)

        for action in legal_actions:
            new_state = self.state.copy()
            if action == 'U':
                new_state[x], new_state[x-3] = new_state[x-3], new_state[x]
            elif action == 'D':
                new_state[x], new_state[x+3] = new_state[x+3], new_state[x]
            elif action == 'L':
                new_state[x], new_state[x-1] = new_state[x-1], new_state[x]
            elif action == 'R':
                new_state[x], new_state[x+1] = new_state[x+1], new_state[x]
            children.append(Puzzle(new_state,self,action,1,self.needs_hueristic))
        return children

    def find_solution(self):
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        return solution

def Astar_search(initial_state):
    count=0
    explored=[]
    start_node=Puzzle(initial_state,None,None,0,True)
    q = PriorityQueue()
    q.put((start_node.evaluation_function1,count,start_node))

    while not q.empty():
        node=q.get()
        node=node[2]
        explored.append(node.state)
        if node.goal_test():
            return node.find_solution()

        children=node.generate_child()
        for child in children:
            if child.state not in explored:
                count += 1
                q.put((child.evaluation_function1,count,child))
    return

def Greedy(initial_state):
    count=0
    explored=[]
    start_node=Puzzle(initial_state,None,None,0,True)
    q = PriorityQueue()
    q.put((start_node.evaluation_function3,count,start_node))

    while not q.empty():
        node=q.get()
        node=node[2]
        explored.append(node.state)
        if node.goal_test():
            return node.find_solution()

        children=node.generate_child()
        for child in children:
            if child.state not in explored:
                count += 1
                q.put((child.evaluation_function3,count,child))
    return

def breadth_first_search(initial_state):
    start_node = Puzzle(initial_state, None, None, 0)
    if start_node.goal_test():
        return start_node.find_solution()
    q = Queue()
    q.put(start_node)
    explored=[]
    while not(q.empty()):
        node=q.get()
        explored.append(node.state)
        children=node.generate_child()
        for child in children:
            if child.state not in explored:
                if child.goal_test():
                    return child.find_solution()
                q.put(child)
    return

state = [0, 1, 2,
         3, 4, 5,
         6, 8, 7]

Puzzle.num_of_instances = 0
t0 = time()
astar = Astar_search(state)
t1 = time() - t0
print('A*     :',astar)
print('Space  :', Puzzle.num_of_instances)
print('Time   :', t1 , 'ms')
print('-------------------------------------------------------------------------------------------------------------------------')

Puzzle.num_of_instances = 0
t0 = time()
greedy = Greedy(state)
t1 = time() - t0
print('Greedy :',greedy)
print('Space  :', Puzzle.num_of_instances)
print('Time   :', t1 , 'ms')
print('-------------------------------------------------------------------------------------------------------------------------')

Puzzle.num_of_instances = 0
t0 = time()
bfs = breadth_first_search(state)
t1 = time() - t0
print('BFS    :',bfs)
print('Space  :', Puzzle.num_of_instances)
print('Time   :', t1 , 'ms')
print('-------------------------------------------------------------------------------------------------------------------------')

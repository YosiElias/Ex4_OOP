import json
from heapq import heappush, heappop
from itertools import count
from Digraph import *
from collections import deque
from typing import List


"""
In this task we used pattern MVC (Model-View-Controller), we did it in order to maintain the code order and correct implementation of the problem.
This is the main algorithm file, i.e. the part responsible for the 'Controller'.

This part is the 'Model', here the heavy calculations for the optimal routes for agents take place.
This section receives data from 'Controller' and returns answers to queries, so that eventually new data will be displayed in 'View' part.

Authors: Roee Tal and Yossi Elias

"""



class GraphAlgo():

    def __init__(self):
        self._graph = DiGraph()
        self.INF = float('inf')

    def get_graph(self):
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self._graph



    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        try:
            with open(file_name, 'w') as f:
                dict_to_save = {}
                dict_to_save["Edges"] = self._graph._Edges
                for node in self._graph.getN().values():    # convert 'info' to str for legal json file
                    if node.get_info() == float('inf'):
                        node.set_info(str(node.get_info()))
                dict_to_save["Nodes"] = self._graph.getN()
                json.dump(dict_to_save, indent=2, fp=f, default=lambda a: a.__dict__)
                for node in self._graph.getN().values():  # convert 'info' back to float for the next use of this data
                    node.set_info(float(node.get_info()))
            return True
        except:
            return False


    def shortest_path(self, id1: int, id2: int):
        """
         Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        :param id1: The start node id
        :param id2: The end node id
        :return: The distance of the path, a list of the nodes ids that the path goes through
        """
        curr = self._graph.getNode((id1))
        dest = self._graph.getNode((id2))
        if curr is None or dest is None:
            return float(self.INF), []
        n_list = self._graph.getN()
        GraphAlgo.reset(self, n_list)
        curr.set_info(0)
        push = heappush # Todo: !
        pop = heappop
        c = count()
        heap = []
        push(heap, (0, next(c), curr))
        curr.set_visit(True)

        while heap:
            (dist, _, cur_n) = pop(heap)
            cur_key = cur_n.get_id()
            dic = DiGraph.getNeighboursDict(self._graph, cur_n.get_id())
            cur_n.set_visit(True)
            for neighbour in dic.keys():
                i = neighbour
                node = self._graph.getNode(i)
                if Node is not None and node.get_visit() is False:
                # if Node is not None:
                    edge = self._graph.getEdge(str(cur_key), str(node.get_id()))
                    new_tag = edge.get_weight() + cur_n.get_info()
                    if (new_tag < self.INF and node.get_info() == self.INF) or node.get_info() > new_tag:
                        node.set_tag(cur_key)
                        node.set_info(new_tag)
                        push(heap, (new_tag, next(c), node))

        if dest.get_info() is self.INF:
            return float('inf'), []
        path_list = GraphAlgo.find_path(self, id2, id1)
        return dest.get_info(), path_list


    def find_path(self, dest: int, src: int):
        curr = self._graph.getNode((dest))
        stack = deque()
        while curr.get_id() is not src:
            # i = curr.get_id()
            stack.append(curr.get_id())
            if curr.get_tag is self.INF:
                return []
            if curr is not None:
                curr = self._graph.getNode((curr.get_tag()))
                if curr is None:
                    break
        if curr is not None:
            stack.append(curr.get_id())

        counter = GraphAlgo.index_num(self, stack)
        list = []
        for i in range(counter):
            temp_n = stack.pop()
            list.append(temp_n)
        return list


    def index_num(self, stack: deque):
        cou = 0
        for i in stack:
            cou = cou+1
        return cou

    def reset(self, node_list: dict):
        for id in node_list:
            node: Node = node_list.get((id))
            node.set_tag(-1)
            node.set_info(self.INF)
            node.set_visit(False)

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """
        finalCost = 0
        path = []
        path.append(node_lst[0])
        tempPath = []

        for j in range(len(node_lst)):  # loop on all the cities and search path from the city that my path get to NodeData
            src_id = path[len(path) - 1]  # take the last node in the path
            minCost = float('inf')
            # reset distances from 'src' node:
            if (j == 0 and len(node_lst) >= 2):  # if first loop AND have >= 2 node in cities:
                comparTo_id = node_lst[1]
            else:
                comparTo_id = node_lst[0]
            short_path = self.shortest_path(src_id, comparTo_id)

            for i in range(len(node_lst)):
                dest: Node = self._graph.getNode(node_lst[i])
                if (not dest.get_id() == src_id and not dest.get_id() in path):
                    # not check path from node to itself AND search only for nodes that not in the path yet
                    cost = dest.get_info()
                    if (cost < minCost):
                        minPath = self.shortest_path(src_id, dest.get_id())[
                            1]
                        del minPath[0]
                        minCost = cost
                        tempPath = minPath
            for i in range(len(tempPath)):
                # add the chosen path to cost and to path
                path.append(tempPath[i])
            tempPath = []
            if not minCost == float('inf'):
                finalCost = finalCost + minCost

        return (path, finalCost)

    def centerPoint(self) -> (int, float):
        """
        Finds the node that has the shortest distance to it's farthest node.
        :return: The nodes id, min-maximum distance
        """
        num, l = self.update_maxDist()
        if l == float('inf'):
            return None, float('inf')
        # now find the minimum max dist of all nodes
        n_list = self._graph.getN()
        min_node = None
        max_val = self.INF
        for n in n_list:
            cur_n = self._graph.getNode((n))
            dist = cur_n.get_maxDist()
            if dist < max_val:
                max_val = dist
                min_node = cur_n
        return min_node.get_id(), min_node.get_maxDist()

    def update_maxDist(self):
        n_list = self._graph.getN()
        # update the largest distance to every node - to be distance from every node to the his furthest other node
        for no in n_list:
            # if no == str(len(n_list) - 1):
            if no == str(len(n_list) -1):
                max_dist = -float('inf')
                cur_n = self._graph.getNode((no))
                n = int(no)
                self.shortest_path(n, n - 1)
            else:
                max_dist = -float('inf')
                cur_n = self._graph.getNode((no))
                n = int(no)
                self.shortest_path(n, n + 1)
            for node in n_list:
                if no is not node:
                    temp_n = self._graph.getNode((node))
                    dist = temp_n.get_info()
                    if dist is not self.INF:
                        if dist > max_dist:
                            max_dist = dist
                    else:
                        # if the graph is not connected
                        return None, float('inf')
            cur_n.set_maxDist(max_dist)
        return 1,[]


    def __str__(self):
        return self._graph
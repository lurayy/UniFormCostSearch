import heapq
import time


class PriorityQueue:

    def __init__(self):
        self._queue = []
        self._index = 0

    def insert(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def remove(self):
        return heapq.heappop(self._queue)[-1]

    def is_empty(self):
        return len(self._queue) == 0


class Node:

    def __init__(self, key):
        # key = name of the node , should be unique
        # weight = cost of the node .. must be +ve
        # successors = child node
        # [] = list , {} = dict.
        self.key, self.successors, self.weight_successors = key, [], {}

    def getKey(self):
        return self.key

    def getSuccessors(self):
        # return child of the node
        return self.successors

    def addSuccessor(self, node, weight):
        if node.getKey() not in self.weight_successors:
            # checking key with the keys in the dict. weight_successors
            self.successors.append(node)
            self.weight_successors[node.getKey()] = weight
            # as in dict[key_of_the_item] = item

    def getWeightSuccessors(self):
        # returns the dict of the successors of the node
        return self.weight_successors


# class for the graph , collection of nodes
class Graph:

    def __init__(self):
        self.nodes = {}
        # key: key/name of the node , value = instance of the node

    def addNode(self, node_key):
        if node_key in self.nodes:
            print("Error The given node {} is already had been added".format(node_key))
        else:
            # creating instance of the node
            node = Node(node_key)
            self.nodes[node_key] = node
            print('{} node is added successfully.'.format(node_key))

    def addSuccessor(self, p_key, s_key, weight):
        # p_key = parent key and s_key = successor/child key with with 'weight'
        if p_key in self.nodes and s_key in self.nodes:
            if p_key != s_key:
                if weight > 0:
                    # connect parent with child
                    self.nodes[p_key].addSuccessor(self.nodes[s_key], weight)
                    print("Node '{}' is added as child of node '{}' with weight {}".format(s_key, p_key, weight))
                    time.sleep(1)
                else:
                    print('Error weight cannot be negative. {} node weight is negative.'.format(s_key))
            else:
                print('Error same node cannot be connected.')
        else:
            print('Given nodes does not exists')

    def getWeightline(self, p_key, s_key):
        if p_key in self.nodes and s_key in self.nodes:
            if p_key != s_key:
                weights = self.nodes[p_key].getWeightSuccessors()
                # check if s_key is a successor
                if s_key in weights:
                    return weights[s_key]
                else:
                    print("{} is not the successor of {}".format(s_key, p_key))
            else:
                print("Error same keys")
        else:
            print("Error: One or both of the given key/s does not exists")

    def getSuccessors(self, p_key):
        if p_key in self.nodes:
            nodes = self.nodes[p_key].getSuccessors()
            s_keys = [node.getKey() for node in nodes]
            return s_keys
        else:
            print('Given Parent keys does not exists.')

    def getNodes(self):
        return self.nodes


def SearchUnifromly(graph, start_node_key, goal_node_key, verbose=False, time_sleep=0):
    if start_node_key not in graph.getNodes() or goal_node_key not in graph.getNodes():
        print("One of the given start or goal node does not exists.")
    else:
        # initialize priority queue for saving the nodes according to it's weight
        queue = PriorityQueue()

        # process the initial node

        # get successor/s of initial start node
        keys_s = graph.getSuccessors(start_node_key)

        # add the obtain successors in the queue which will prioritize the list according to it's weight
        for key_s in keys_s:
            weight = graph.getWeightline(start_node_key, key_s)
            queue.insert((key_s, weight), weight)

        goal_status, cumulative_cost = False, -1
        # cumulative increasing

        while not queue.is_empty():
            # remove item of queue for processing
            current_node_key, cost_node = queue.remove()

            if current_node_key == goal_node_key:
                goal_status, cumulative_cost = True, cost_node
                break

            if verbose:
                print("\nProcessing node '{}' with cumulative cost {}".format(current_node_key, cost_node))
                time.sleep(time_sleep)

            # get all successors of the current node
            keys_s = graph.getSuccessors(current_node_key)

            if keys_s:
                for key_s in keys_s:
                    cumulative_cost = graph.getWeightline(current_node_key, key_s) + cost_node
                    queue.insert((key_s, cumulative_cost),cumulative_cost)

        if goal_status:
            print('\nGoal Node {} reached with Cost: {}\n'.format(goal_node_key, cumulative_cost))
        else:
            print("\n Cannot reach goal.")


if __name__ == "__main__":
    # build the graph...
    # adds nodes in the graph
    graph = Graph()
    graph.addNode('S')  # start
    graph.addNode('a')
    graph.addNode('b')
    graph.addNode('c')
    graph.addNode('d')
    graph.addNode('e')
    graph.addNode('f')
    graph.addNode('G')  # goal
    graph.addNode('h')
    graph.addNode('p')
    graph.addNode('q')
    graph.addNode('r')
    # linking the nodes
    print("")
    graph.addSuccessor('S', 'd', 3)
    graph.addSuccessor('S', 'e', 9)
    graph.addSuccessor('S', 'p', 1)
    graph.addSuccessor('b', 'a', 2)
    graph.addSuccessor('c', 'a', 2)
    graph.addSuccessor('d', 'b', 1)
    graph.addSuccessor('d', 'c', 8)
    graph.addSuccessor('d', 'e', 2)
    graph.addSuccessor('e', 'h', 8)
    graph.addSuccessor('e', 'r', 2)
    graph.addSuccessor('f', 'c', 3)
    graph.addSuccessor('f', 'G', 2)
    graph.addSuccessor('h', 'p', 4)
    graph.addSuccessor('h', 'q', 4)
    graph.addSuccessor('p', 'q', 15)
    graph.addSuccessor('r', 'f', 1)

    SearchUnifromly(graph=graph, start_node_key='S', goal_node_key='G', verbose=True, time_sleep=1)
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util, copy, time
from game import Directions

s = Directions.SOUTH
w = Directions.WEST
n = Directions.NORTH
e = Directions.EAST

directions = {
    'North': Directions.NORTH,
    'South': Directions.SOUTH,
    'West': Directions.WEST,
    'East': Directions.EAST
}

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    import time
    import inspect
    print("\n\nStart:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    print("\n\n")

    state = problem.getStartState()
    print('caller name:', inspect.stack()[1][3])
    print("\n\n")
    # print("test: ", type(problem.getSuccessors(state)))
    print("test: ", type(problem))

    print("\n\n")
    time.sleep(5)

    return  [s, s, w, s, w, w, s, n, s, n, s, n, s, n, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    frontier = util.Stack()
    currentPosition = problem.getStartState()

    # nodes on the stack => [position, [pathWeTookToNode]]
        # parentNode will be used to retrieve children nodes and help construct their data (ie path taken)
    parentNode = 0
    alreadyVisited = []

    while not problem.isGoalState(currentPosition):
        # prevent program from getting stuck in infinite cycle by tracking nodes we've already visited
        alreadyVisited.append(currentPosition)

        # pull node from top of stack if possible, otherwise setup/find child nodes based on start state
        if not frontier.isEmpty():
            # pull top node of the frontier off the stack
            parentNode = frontier.pop()
            # get position from parentNode
            currentPosition = parentNode[0]

            # check if we've found the cookie
            if problem.isGoalState(currentPosition):
                break

            # get list of triples that have the data we need to create child nodes [((x, y), 'direction', cost), ... ]
            successorStates = problem.getSuccessors(currentPosition)
        else:
            # if stack is empty, we get currentPosition from start state. It's already set
            successorStates = problem.getSuccessors(currentPosition)

        # setup & push child nodes onto the stack
        for successor in successorStates:
            # make sure successor isn't a node we've already been to
            if successor[0] not in alreadyVisited:
                # check if we actually got parentNode off stack or are at the start state (ie no nodes yet)
                if parentNode != 0:
                    currentPath = copy.deepcopy(parentNode[1])
                else:
                    currentPath = []
                # construct child node, which will be pushed on stack
                node = [None]*2
                # I want to store each successor in the frontier stack as [position, [pathWeTookToNode]]
                    # set child node's postion
                node[0] = successor[0]
                    # set child node's path
                currentPath.append(successor[1])
                node[1] = currentPath
                frontier.push(node)

    # return list of directions needed to get to the cookie
    return parentNode[1]

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    frontier = util.Queue()
    currentPosition = problem.getStartState()

    # nodes on the queue => [position, [pathWeTookToNode]]
        # parentNode will be used to retrieve children nodes and help construct their data (ie path taken)
    parentNode = 0
    alreadyVisited = []

    while not problem.isGoalState(currentPosition):
        # prevent program from getting stuck in infinite cycle by tracking nodes we've already visited
        alreadyVisited.append(currentPosition)

        # pull node from top of queue if possible, otherwise setup/find child nodes based on start state
        if not frontier.isEmpty():
            # pull top node of the frontier off the queue
            parentNode = frontier.pop()
            # get position from parentNode
            currentPosition = parentNode[0]

            # check if we've found the cookie
            if problem.isGoalState(currentPosition):
                break

            # get list of triples that have the data we need to create child nodes [((x, y), 'direction', cost), ... ]
            successorStates = problem.getSuccessors(currentPosition)
        else:
            # if queue is empty, we get currentPosition from start state. It's already set
            successorStates = problem.getSuccessors(currentPosition)

        # setup & push child nodes onto the queue
        for successor in successorStates:
            # make sure successor isn't a node we've already been to
            if successor[0] not in alreadyVisited and successor[0] not in (node[0] for node in frontier.list):
                # check if we actually got parentNode off queue or are at the start state (ie no nodes yet)
                if parentNode != 0:
                    currentPath = copy.deepcopy(parentNode[1])
                else:
                    currentPath = []
                # construct child node, which will be pushed onto the queue
                node = [None]*2
                # I want to store each successor in the frontier queue as [position, [pathWeTookToNode]]
                    # set child node's postion
                node[0] = successor[0]
                    # set child node's path
                currentPath.append(successor[1])
                node[1] = currentPath
                frontier.push(node)
    # return list of directions needed to get to the cookie
    return parentNode[1]

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    frontier = util.PriorityQueue()
    currentPosition = problem.getStartState()

    # nodes on the queue => [position, [pathWeTookToNode], cost]
        # parentNode will be used to retrieve children nodes and help construct their data (ie path taken)
    parentNode = 0
    alreadyVisited = []

    while not problem.isGoalState(currentPosition):
        # prevent program from getting stuck in infinite cycle by tracking nodes we've already visited
        alreadyVisited.append(currentPosition)

        # pull node from top of queue if possible, otherwise setup/find child nodes based on start state
        if not frontier.isEmpty():
            # pull top node of the frontier off the queue
            parentNode = frontier.pop()

            # get position from parentNode
            currentPosition = parentNode[0]

            # check if we've found the cookie
            if problem.isGoalState(currentPosition):
                break

            # get list of triples that have the data we need to create child nodes [((x, y), 'direction', cost), ... ]
            successorStates = problem.getSuccessors(currentPosition)
        else:
            # if queue is empty, we get currentPosition from start state. It's already set
            successorStates = problem.getSuccessors(currentPosition)

        # setup & push child nodes onto the queue
        for successor in successorStates:
            # make sure successor isn't a node we've already been to
            if successor[0] not in alreadyVisited and successor[0] not in (node[2][0] for node in frontier.heap):
                # check if we actually got parentNode off queue or are at the start state (ie no nodes yet)
                if parentNode != 0:
                    currentPath = copy.deepcopy(parentNode[1])
                else:
                    currentPath = []
                # construct child node, which will be pushed onto the queue
                node = [None]*3
                # I want to store each successor in the frontier queue as [position, [pathWeTookToNode], cumulativeBranchCost]
                    # set child node's postion
                node[0] = successor[0]
                    # set child node's path
                currentPath.append(successor[1])
                node[1] = currentPath
                # add previous node's cost (if there was one) to current node, otherwise set cost as current node's cost
                if parentNode != 0:
                    cumulativeBranchCost = parentNode[2] + successor[2]
                    node[2] = cumulativeBranchCost
                else:
                    cumulativeBranchCost = successor[2]
                    node[2] = cumulativeBranchCost
                frontier.push(node, cumulativeBranchCost)
    # return list of directions needed to get to the cookie
    return parentNode[1]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()
    currentPosition = problem.getStartState()

    # nodes on the queue => [position, [pathWeTookToNode], cost]
        # parentNode will be used to retrieve children nodes and help construct their data (ie path taken)
    parentNode = 0
    alreadyVisited = []

    while not problem.isGoalState(currentPosition):
        # prevent program from getting stuck in infinite cycle by tracking nodes we've already visited
        alreadyVisited.append(currentPosition)

        # pull node from top of queue if possible, otherwise setup/find child nodes based on start state
        if not frontier.isEmpty():
            # pull top node of the frontier off the queue
            parentNode = frontier.pop()

            # get position from parentNode
            currentPosition = parentNode[0]

            # check if we've found the cookie
            if problem.isGoalState(currentPosition):
                break

            # get list of triples that have the data we need to create child nodes [((x, y), 'direction', cost), ... ]
            successorStates = problem.getSuccessors(currentPosition)
        else:
            # if queue is empty, we get currentPosition from start state. It's already set
            successorStates = problem.getSuccessors(currentPosition)

        # setup & push child nodes onto the queue
        for successor in successorStates:
            # make sure successor isn't a node we've already been to
            if successor[0] not in alreadyVisited and successor[0] not in (node[2][0] for node in frontier.heap):
                # check if we actually got parentNode off queue or are at the start state (ie no nodes yet)
                if parentNode != 0:
                    currentPath = copy.deepcopy(parentNode[1])
                else:
                    currentPath = []
                # construct child node, which will be pushed onto the queue
                node = [None]*3
                # I want to store each successor in the frontier queue as [position, [pathWeTookToNode], heuristicPlusBranchCostSoFar]
                    # set child node's postion
                node[0] = successor[0]
                    # set child node's path
                currentPath.append(successor[1])
                node[1] = currentPath
                # add previous node's cost (if there was one) to current node, otherwise set cost as current node's cost
                if parentNode != 0:
                    heuristicPlusBranchCostSoFar = parentNode[2] + successor[2] + heuristic(currentPosition, problem)
                    node[2] = heuristicPlusBranchCostSoFar
                else:
                    heuristicPlusBranchCostSoFar = successor[2] + heuristic(currentPosition, problem)
                    node[2] = heuristicPlusBranchCostSoFar
                frontier.push(node, heuristicPlusBranchCostSoFar)
    # return list of directions needed to get to the cookie
    return parentNode[1]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

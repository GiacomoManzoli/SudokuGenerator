
from search import Problem, Node
from util import PriorityQueue

class AStarSearch(object):

    def __memoize(self, fn, slot=None):
        """Memoize fn: make it remember the computed value for any argument list.
        If slot is specified, store result in that slot of first argument.
        If slot is false, store results in a dictionary."""
        if slot:
            def memoized_fn(obj, *args):
                if hasattr(obj, slot):
                    return getattr(obj, slot)
                else:
                    val = fn(obj, *args)
                    setattr(obj, slot, val)
                    return val
        else:
            def memoized_fn(*args):
                if not memoized_fn.cache.has_key(args):
                    memoized_fn.cache[args] = fn(*args)
                return memoized_fn.cache[args]
            memoized_fn.cache = {}
        return memoized_fn

    def __best_first_graph_search(self, problem, f):
        """Search the nodes with the lowest f scores first.
        You specify the function f(node) that you want to minimize; for example,
        if f is a heuristic estimate to the goal, then we have greedy best
        first search; if f is node.depth then we have breadth-first search.
        There is a subtlety: the line "f = memoize(f, 'f')" means that the f
        values will be cached on the nodes as they are computed. So after doing
        a best first search you can examine the f values of the path returned."""
        f = self.__memoize(f, 'f')
        node = Node(problem.initial)

        assert node != None and node.state != None

        if problem.goal_test(node.state):
            return node
        frontier = PriorityQueue(min, f)


        frontier.append(node)
        explored = set()
        step = 0
        while frontier:
            step+=1
            
            node = frontier.pop()
            assert node != None and node.state != None, "Estratto un nodo None"
            print '---- CURRENT NODE ----'
            print node.state
            if problem.goal_test(node.state):
                return node, len(explored)
            explored.add(node.state)
            
            for child in node.expand(problem):
                assert child != None and child.state != None
                if child.state not in explored and child not in frontier:
                    frontier.append(child)
                elif child in frontier:
                    incumbent = frontier[child]
                    if f(child) < f(incumbent):
                        del frontier[incumbent]
                        frontier.append(child)
        return None


    def search(self, problem, h=None):
        """A* search is best-first graph search with f(n) = g(n)+h(n).
        You need to specify the h function when you call astar_search, or
        else in your Problem subclass."""
        h = self.__memoize(h or problem.h, 'h')
        def heuristic(n):
            v = h(n)
            return n.path_cost + v
        return self.__best_first_graph_search(problem, heuristic)

    
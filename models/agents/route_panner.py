

class RoutePlannter:
    """
    Class for planning routes based on agent preference
    and relative prestige of paintings

    The aim here is to find an algorithm that maximises enjoyment of paintings.
    For a linear museum - agents will only skip if the desire to see painting is overwhelmed
    by crowd negative

    Basic approach:
        If only one next painting + is positive enjoyment - will go 100% of time
        If only one next painting + is negative enjoyment - will skip 100% of the time (not scored)

    """

    def __init__(self):
        self.path = [] #path of the paintings

    def dfs(self, node, end_node):
        """
        Generates the path that the agent will take from node.
        Works to maximise the agent's enjoyment - agent will
        choose a path that
        :param node:
        :return:
        """
        visited = [False for i in range(end_node)]
        stack = []

        stack.append(node)

        while(stack):
            s = stack[-1]
            stack.pop()

            if (not visited[s]):
                visited[s] = True

            for node in succesors:
                if (not visited[node]):
                    stack.append(node)



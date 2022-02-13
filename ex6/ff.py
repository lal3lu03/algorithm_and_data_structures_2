# Ford-Fulkerson algorith in Python


class Graph:

    def __init__(self, graph):
        self.graph = graph  # original graph
        self.residual_graph = [[cell for cell in row] for row in graph]  # cloned graph
        self.latest_augmenting_path = [[0 for cell in row] for row in
                                       graph]  # empty graph with same dimension as graph
        self.current_flow = [[0 for cell in row] for row in graph]  # empty graph with same dimension as graph

    def ff_step(self, source, sink):
        """
        Perform a single flow augmenting iteration from source to sink
        Update the latest augmenting path, the residual graph and the current flow by the maximum possible
        amount according to your chosen path.
        The path must be chosen based on BFS.
        @param source the source's vertex id
        @param sink the sink's vertex id
        @return the amount by which the flow has increased.
        """
        self.latest_augmenting_path, (track, move), p_line = [[0 for cell in row] for row in self.graph], \
                                                             self.breadth_first_search(source, sink), 0
        if move <= 0: return 0

        for col in track:

            if col == 0: continue

            self.residual_graph[p_line][col] -= move
            self.latest_augmenting_path[p_line][col] = move

            if self.current_flow[col][p_line] + move > self.graph[p_line][col]:
                self.current_flow[col][p_line] -= move
            else: self.current_flow[p_line][col] += move

            p_line = col

        return move

    def ford_fulkerson(self, source, sink):
        """
        Execute the ford-fulkerson algorithm (i.e., repeated calls of ff_step())
        @param source the source's vertex id
        @param sink the sink's vertex id
        @return the max flow from source to sink
        """
        MaxFlow, move = 0, self.ff_step(source, sink)

        while move > 0:
            MaxFlow += move
            move = self.ff_step(source, sink)

        return MaxFlow

    def breadth_first_search(self, source, sink):
        list_, been = [(source, [source], float('inf'))], set()

        while list_:
            line, way, maxflow = list_.pop(0)
            been.add(line)

            for c, w in enumerate(self.residual_graph[line]):

                if self.current_flow[c][line] > 0:

                    if c not in been:
                        min_ = min(maxflow, self.current_flow[c][line])
                        list_.append((c, way + [c], min_))

                        if c == sink: return way + [c], min_

                elif w != 0:

                    if c not in been:
                        min_ = min(maxflow, w)
                        list_.append((c, way + [c], min_))

                        if c == sink: return way + [c], min_
        return (), 0
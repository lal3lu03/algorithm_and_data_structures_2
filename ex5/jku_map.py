"""Author: Max Hageneder"""

from graph import Graph
from step import Step
from vertex import Vertex
import math


class JKUMap(Graph):

    def __init__(self):
        super().__init__()
        v_spar = self.insert_vertex("Spar")
        v_lit = self.insert_vertex("LIT")
        v_porter = self.insert_vertex('Porter')
        v_open_lab = self.insert_vertex('Open Lab')
        v_bank = self.insert_vertex('Bank')
        v_khg = self.insert_vertex('KHG')
        v_chat = self.insert_vertex('Chat')
        v_library = self.insert_vertex('Library')
        v_lui = self.insert_vertex('LUI')
        v_teichwerk = self.insert_vertex('Teichwerk')
        v_sp1 = self.insert_vertex('SP1')
        v_sp3 = self.insert_vertex('SP3')
        v_parking = self.insert_vertex('Parking')
        v_bella_casa = self.insert_vertex('Bella Casa')
        v_castle = self.insert_vertex('Castle')
        v_papaya = self.insert_vertex('Papaya')
        v_jkh = self.insert_vertex('JKH')

        self.insert_edge(v_spar, v_lit, 50)
        self.insert_edge(v_spar, v_porter, 103)
        self.insert_edge(v_lit, v_porter, 80)
        self.insert_edge(v_porter, v_open_lab, 70)
        self.insert_edge(v_porter, v_bank, 100)
        self.insert_edge(v_spar, v_khg, 165)
        self.insert_edge(v_bank, v_khg, 150)
        self.insert_edge(v_bank, v_chat, 115)
        self.insert_edge(v_chat, v_library, 160)
        self.insert_edge(v_chat, v_lui, 240)
        self.insert_edge(v_library, v_lui, 90)
        self.insert_edge(v_lui, v_teichwerk, 135)
        self.insert_edge(v_lui, v_sp1, 175)
        self.insert_edge(v_sp1, v_sp3, 130)
        self.insert_edge(v_sp1, v_parking, 240)
        self.insert_edge(v_khg, v_parking, 190)
        self.insert_edge(v_parking, v_bella_casa, 145)
        self.insert_edge(v_castle, v_papaya, 85)
        self.insert_edge(v_papaya, v_jkh, 80)

    def get_shortest_path_from_to(self, from_vertex: Vertex, to_vertex: Vertex):
        """
        This method determines the shortest path between two POIs "from_vertex" and "to_vertex".
        It returns the list of intermediate steps of the route that have been found
        using the dijkstra algorithm.

        :param from_vertex: Start vertex
        :param to_vertex:   Destination vertex
        :return:
           The path, with all intermediate steps, returned as an list. This list
           sequentially contains each vertex along the shortest path, together with
           the already covered distance (see example on the assignment sheet).
           Returns None if there is no path between the two given vertices.
        :raises ValueError: If from_vertex or to_vertex is None, or if from_vertex equals to_vertex
        """
        if from_vertex is None: raise ValueError
        if to_vertex is None: raise ValueError
        if from_vertex is to_vertex: raise ValueError

        (d, p), list = self._dijkstra(from_vertex), []
        if p[to_vertex.name] is None:
            return None
        for step in p[to_vertex.name]:
            list.append(Step(self.find_vertex(step), d[step]))
        return list

    def get_steps_for_shortest_paths_from(self, from_vertex: Vertex):
        """
        This method determines the amount of "steps" needed on the shortest paths
        from a given "from" vertex to all other vertices.
        The number of steps (or -1 if no path exists) to each vertex is returned
        as a dictionary, using the vertex name as key and number of steps as value.
        E.g., the "from" vertex has a step count of 0 to itself and 1 to all adjacent vertices.

        :param from_vertex: start vertex
        :return:
          A map containing the number of steps (or -1 if no path exists) on the
          shortest path to each vertex, using the vertex name as key and the number of steps as value.
        :raises ValueError: If from_vertex is None.
        """
        if from_vertex is None: raise ValueError
        d, p = self._dijkstra(from_vertex)
        dict_short = dict()
        for key in p:
            try:
                dict_short[key] = len(p[key]) - 1
            except TypeError: dict_short[key] = -1
        return dict_short

    def get_shortest_distances_from(self, from_vertex: Vertex):
        """
        This method determines the shortest paths from a given "from" vertex to all other vertices.
        The shortest distance (or -1 if no path exists) to each vertex is returned
        as a dictionary, using the vertex name as key and the distance as value.

        :param from_vertex: Start vertex
        :return
           A dictionary containing the shortest distance (or -1 if no path exists) to each vertex,
           using the vertex name as key and the distance as value.
        :raises ValueError: If from_vertex is None.
        """
        if from_vertex is None: raise ValueError
        d, p = self._dijkstra(from_vertex)
        return d

    def helper(self, c: Vertex, visited_list, distances: dict, paths: dict):
        """
        This method is expected to be called with correctly initialized data structures and recursively calls itself.

        :param cur: Current vertex being processed
        :param visited_list: List which stores already visited vertices.
        :param distances: Dict (nVertices entries) which stores the min. distance to each vertex.
        :param paths: Dict (nVertices entries) which stores the shortest path to each vertex.
        """

        visited_list.append(c)
        ver = self.get_adjacent_vertices(c)
        for v in ver:
            if v not in visited_list:
                nwe_dist = distances[c.name] + self.find_edge(c, self.find_vertex(v)).weight
                if nwe_dist < distances[v]:
                    distances[v] = nwe_dist
                    paths[v] = paths[visited_list[-1].name].copy()
                    paths[v].append(v)

        min, not_, next = math.inf, [], None

        for l in distances:
            if l not in [x.name for x in visited_list]:
                not_.append(l)
        try:
            for l in not_:
                if distances[l] < min:
                    min = distances[l]
                    next = l
            c = self.find_vertex(next)
            self.helper(c, visited_list, distances, paths)
        except ValueError:
            for l in distances:
                if distances[l] == math.inf:
                    distances[l] = -1
                    paths[l] = None
        return distances, paths

    def _dijkstra(self, cur: Vertex):
        been_list, d, p = [], dict(), dict()
        for v in self.vertices:
            d[v.name], p[v.name] = math.inf, []
        d[cur.name] = 0
        p[cur.name].append(cur.name)
        return self.helper(cur, been_list, d, p)

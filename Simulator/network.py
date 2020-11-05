from math import inf, pow, floor
import random
import json
import sys

class Topology:

    __DEFAULT_NODES = list(range(6))
    __DEFAULT_EDGES = [(0, 1), (0, 2), (0, 3),
                       (1, 0), (1, 2), (1, 4),
                       (2, 0), (2, 1), (2, 5),
                       (3, 0), (3, 4), (3, 5),
                       (4, 1), (4, 3), (4, 5),
                       (5, 2), (5, 3), (5, 4)]


    def __init__(self, nodes=None, edges=None, capacities=None):
        if nodes is None or edges is None:
            nodes = self.__DEFAULT_NODES
            edges = self.__DEFAULT_EDGES
        self._nodes = nodes
        self._edges = edges
        self._fail_probability = {}
        self._choose_fp()
        self._traffic = {}
        self._flows = {}
        self._link_capacities = capacities
        self._failure_links = {}
        self._packet_loss = {}
        self._usage = {}
        self._ml_data_x = []
        self._ml_data_y = []
        self._ml_data_nf_x = []
        self._ml_data_nf_y = []

    def _choose_fp(self):
        max_bad = floor(len(self._edges)*2.5/100)
        max_good = len(self._edges) - max_bad
        bad = []
        good = []
        for edge in self._edges:
            if bool(random.getrandbits(1)) and max_bad>0:
                bad.append(edge)
                #self._fail_probability[edge] = self._bathtub(0.85)
                max_bad = max_bad -1
            else:
                if max_good > 0:
                    good.append(edge)
                    #self._fail_probability[edge] = self._bathtub(0.3)
                    max_good = max_good -1
                else:
                    bad.append(edge)
                    #self._fail_probability[edge] = self._bathtub(0.85)
                    max_bad = max_bad -1
        lnks = good+bad
        for ndx, edge in enumerate(lnks):
            l = ndx+1
            if edge in good:
                self._fail_probability[edge] = l ** -1.35
            else:
                self._fail_probability[edge] = l ** -0.73

    def __start_traffic(self):
        for e in self._edges:
            self._traffic[e] = 0

    def get_node_count(self):
        return len(self._nodes)
    
    def get_edge_count(self):
        return len(self._edges)
    
    def get_nodes(self):
        return list(map(lambda x: str(x), self._nodes))

    def get_node_name(self, index):
        if index < len(self._nodes):
            return self._nodes[index]
        else:
            return None
    
    def get_edges(self):
        return self._edges

    def get_capacity(self, source, destination):
        link = (source, destination)
        if link in self._link_capacities:
            return self._link_capacities[link]
        else:
            return 0
        
    def get_flows(self, source, destination):
        link = (source, destination)
        if link not in self._edges and source != destination:
            return None
        if link in self._flows:
            return self._flows[link]
        else:
            return []
    
    def get_flow(self, source, destination, i, j):
        link = (i, j)
        if link not in self._edges and source != destination:
            return -1
        if link in self._flows:
            for fl in self._flows[link]:
                if fl[0] == source and fl[1] == destination:
                    return fl[2]
            return 0
        else:
            return 0
            
    def get_traffic(self, source, destination):
        link = (source, destination)
        if link not in self._edges and source != destination:
            return -1
        if link in self._traffic:
            return self._traffic[link]
        else:
            return 0

    def get_adjacent(self, node):
        adj = []
        for e in self._edges:
            if e[0] == node:
                adj.append(e[1])
        return adj

    def shortest_path(self, source, destination):  # Dijkstra
        if source not in self._nodes or destination not in self._nodes:
            raise RuntimeError('Source or destination does not exist')
        else:
            distances = {}
            prevnodes = {}
            for n in self._nodes:
                if n == source:
                    distances[n] = 0
                else:
                    distances[n] = inf
            marked = []
            a = source
            while a != destination:
                adj = self.get_adjacent(a)
                for m in marked:
                    if m in adj:
                        adj.remove(m)
                for ad in adj:
                    dst = distances[a] + 1
                    if dst < distances[ad]:
                        distances[ad] = dst
                        prevnodes[ad] = a
                marked.append(a)
                min_dst = inf
                next_node = -1
                for n in self._nodes:
                    if n not in marked:
                        if distances[n] < min_dst:
                            min_dst = distances[n]
                            next_node = n
                if next_node == -1:
                    raise RuntimeError('Unlinked')
                a = next_node
            path = [destination]
            route_node = destination
            while route_node != source:
                route_node = prevnodes[route_node]
                path.insert(0, route_node)
            return path

    def route_traffic(self, traffic):  # K-shortest path
        original_edges = self._edges.copy()
        total_assignment = self._traffic.copy()
        total_flows = self._flows.copy()
        for link in traffic:  # For each demand...
            path_found = False
            trf = traffic[link]
            while not path_found:  # ...We try to find a path
                assignment = total_assignment.copy()
                flows = total_flows.copy()
                # Initially, we try the shortest
                try:
                    path = self.shortest_path(link[0], link[1])
                except RuntimeError:
                    print('Something is wrong! Could not route traffic from {} to {}'.format(link[0], link[1]))
                    print('Edges left: {}'.format(str(self._edges)))
                    sys.exit(1)
                for i in range(len(path)-1):
                    lnk = (path[i], path[i+1])
                    if lnk in assignment:
                        # If at some point in the path we go over the maximum capacity of a link...
                        if assignment[lnk]+trf > self.get_capacity(lnk[0], lnk[1]):
                            # ...We remove that link...
                            self._edges.remove(lnk)
                            break  # ...And try again
                        else:  # If we don't...
                            # ...We simply assign the traffic
                            assignment[lnk] += trf
                            flow = link+(trf,)
                            if lnk in flows:
                                flows[lnk].append(flow)
                            else:
                                flows[lnk] = [flow]
                            # And if we  reach the destination...
                            if i == len(path)-2:
                                path_found = True  # ...We've found a path
                    else:
                        # If we go over the capacity of a link without traffic...
                        if trf > self.get_capacity(lnk[0], lnk[1]):
                            # ...The traffic cannot be delivered (all links have same capacity)
                            raise RuntimeError('Surpassed static capacity')
                        else:
                            assignment[lnk] = trf
                            flow = link+(trf,)
                            if lnk in flows:
                                flows[lnk].append(flow)
                            else:
                                flows[lnk] = [flow]
                            if i == len(path)-2:
                                path_found = True
            # After each process, we restore the original links of the network
            self._edges = original_edges.copy()
            for x in assignment:
                total_assignment[x] = assignment[x]
            total_flows = flows.copy()
        self._traffic = total_assignment
        self._flows = total_flows

    def show_flows(self):
        print(self._flows)

    def show_traffic(self):
        print(self._traffic)

    def show_nodes(self):
        print(self._nodes)

    def show_links(self):
        print(self._edges)
    
    def _bathtub(self, x):
        return pow((x-0.5), 10)*1000+0.005

    def simulate(self, matrices, alpha, fi, outJson, nfJson):
        for matrix in matrices:
            self._traffic = {}
            self.route_traffic(matrix)
            for edge in self._edges:
                usage = self._traffic.get(edge, 0) / self._link_capacities[edge]
                self._usage[edge] = usage
                if edge not in self._failure_links:
                    fail = random.uniform(0, 1)
                    if fail > self._fail_probability[edge]:
                        self._failure_links[edge] = 0
                    else:
                        self._ml_data_nf_x.append((usage, 0, usage, 0))
                        __, delta = fi(0)
                        self._ml_data_nf_y.append(delta)
                    self._packet_loss[edge] = 0
                if edge in self._failure_links:
                    self._failure_links[edge] += 1
                    if self._packet_loss[edge] < 1:
                        #myploss = fi(delta, self._failure_links[edge])
                        myploss, delta = fi(self._failure_links[edge])
                        if myploss < 1:
                            ploss = (1-alpha)*myploss + alpha*usage
                        else:
                            ploss = 1
                        ml_x = (usage, ploss, self._usage[edge], self._packet_loss[edge])
                        ml_y = delta - self._failure_links[edge]
                        self._ml_data_x.append(ml_x)
                        self._ml_data_y.append(ml_y)
                        self._packet_loss[edge] = ploss
            print('Simulated matrix')
                        
        with open(outJson, 'w') as jsonO:
            json.dump({'ml_x': self._ml_data_x, 'ml_y': self._ml_data_y}, jsonO)
        
        with open(nfJson, 'w') as json1:
            json.dump({'ml_x': self._ml_data_nf_x, 'ml_y': self._ml_data_nf_y}, json1)

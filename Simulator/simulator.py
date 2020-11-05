import argparse
from network import Topology
import os
from XMLNetParser import parse, parseTraffic
from fi import *
import pickle

#ALPHA_VALUES = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
ALPHA_VALUES = [0.5]
#DELTA_VALUES = [24, 48, 72, 144, 288] #2h, 4h, 6h, 12h, 24h
#DELTA_VALUES = [1]
#FUNCTIONS = list(functions())

FUNCTIONS = nonlinear()

def main():
    parser = argparse.ArgumentParser(description="LFP simulator, Python edition")
    parser.add_argument('-i', help='Input network topology in SNDLib XML format, or pre-processed Python format', metavar='input_network', required=True)
    parser.add_argument('-it', help='Input traffic, must be a folder containing traffic matrices in SNDLib XML format or a pre-processed Python file', metavar='input_traffic', required=True)
    parser.add_argument('-ona', help='If set, the network topology and will be saved in this file as a pre-processed Python object', metavar='output_network_accelerate', required=False, default=None)
    parser.add_argument('-ota', help='If set, the traffic will be saved in this file as a pre-processed Python object', metavar='output_traffic_accelerate', required=False, default=None)
    parser.add_argument('-o', help='Output ML file prefix', metavar='output', required=True)

    x = parser.parse_args()
    if x.i.split('.')[-1] != 'pynetwork':
        nodes, links, caps = parse(x.i)
        print('Parsed network')
    else:
        nodes, links, caps = None, None, None
        with open(x.i, 'rb') as in_network:
            (nodes, links, caps) = pickle.load(in_network)
        print('Loaded pre-processed network, {} nodes, {} links'.format(len(nodes), len(links)))
    if os.path.isdir(x.it):
        matrices = os.listdir(x.it)
        matrices.sort()
        matrices = list(map(lambda a: os.path.join(x.it, a), matrices))
        traffic = []
        for matrix in matrices:
            traffic.append(parseTraffic(matrix))
            print('Parsed traffic matrix {}'.format(matrix))
    else:
        with open(x.it, 'rb') as in_traffic:
            traffic = pickle.load(in_traffic)
            print('Loaded {} pre-processed traffic matrices'.format(len(traffic)))
    
    if x.ona is not None:
        dirname = os.path.dirname(x.ona)
        if dirname == '':
            dirname = '.'
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        if x.ona.split('.')[-1] != 'pynetwork':
            x.ona += '.pynetwork'
        with open(x.ona, 'wb') as out_network:
            pickle.dump((nodes, links, caps), out_network)
        print('Saved preprocessed network')
    
    if x.ota is not None:
        dirname = os.path.dirname(x.ota)
        if dirname == '':
            dirname = '.'
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        if x.ota.split('.')[-1] != 'pytraffic':
            x.ona += '.pytraffic'
        with open(x.ota, 'wb') as out_traffic:
            pickle.dump(traffic, out_traffic)
        print('Saved preprocessed traffic')

    main_loop(nodes, links, caps, traffic, x.o)


def main_loop(nodes, links, caps, traffic: list, output: str):
    for alpha in ALPHA_VALUES:
        for ndx, function in enumerate(FUNCTIONS):
            out_filename = output+"A"+str(alpha)+"F"+str(ndx)+".json"
            out_non_fail_filename = output+"A"+str(alpha)+"NonFail"+"F"+str(ndx)+".json"
            topo = Topology(nodes, links, caps)
            topo.simulate(traffic, alpha, function, out_filename, out_non_fail_filename)
            print('Simulated alpha: {}, fi: {}'.format(str(alpha), ndx))

if __name__ == "__main__":
    main()
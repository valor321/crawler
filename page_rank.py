import sys
import os
import time
import argparse
import random

import ranking


def load_graph(filename):

    graphL = {}

    with open(filename, "r") as f:
        # Iterate through the file line by line
        for line in f:
            # And split each line into two URLs
            node = line.strip().split()
            if len(node)  == 2:
                url = node[0].strip()
                target = (node[1].strip())
                #check if the url is already in the dic and assigns another value to it
                if url in graphL:
                    graphL[url].append(target)
                else:
                    #otherwise created a new dic value
                    graphL[url] = [target]

    return graphL


def print_stats(graphL):
        num_nodes = len(graphL)
        num_of_edges = sum(len(targets) for targets in graphL.values())
        print("Number of nodes:", num_nodes)
        print("Number of edges:", num_of_edges)


def stochastic_page_rank(graphP, repeats):

    #how many times a node is visited
    hit_count = {node: 0 for node in graphP}

    current_node = random.choice(list(graphP.keys()))

    hit_count[current_node] += 1

    for _ in range(repeats):
        if not graphP[current_node]:
            #if they dont have edges, choose another node
            current_node = random.choice(list(graphP.keys()))
        else:
            #seeing if they have edges
            current_node = random.choice(graphP[current_node])

        hit_count[current_node] += 1

    return  hit_count



def distribution_page_rank(graphD, steps):
    """Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """
    #prob. of all nodes balanced
    node_prob = {node: 1/len(graphD) for node in graphD}

    for _ in range(steps):
        #all nodes prob. to 0
        next_prob = {node: 0 for node in graphD}
        #update all nodes prob
        for node in graphD:
            p = node_prob[node] / len(graphD) if graphD[node] else 0
            #distrubute probs. of all edges
            for target in graphD[node]:
                next_prob[target] += p

            node_prob[node] = next_prob[node]

    return node_prob

    #raise RuntimeError("This function is not implemented yet.")


parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")


if __name__ == '__main__':

    #graph = load_graph("school_web2024-1.txt")
    #print_stats(graph)



    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph("school_web2024-1.txt")
    print_stats(graph)

    #start = time.time()
    #ranking = algorithm(graph, args)
    #stop = time.time()
    #time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")


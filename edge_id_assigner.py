
from typing import Dict
import networkx as nx

class BitVector:
    width: int
    value: int

    def __init__(self, width: int, value: int):
        if value >> width != 0:
            raise RuntimeError("Invalid bitvector")
        self.width = width
        self.value = value

    def __str__(self):
        return f"{self.width}'d{self.value}"
    
    def concat(self, other: "BitVector") -> "BitVector":
        return BitVector(width = self.width + other.width, value=self.value << other.width + other.value)

G = nx.MultiDiGraph
def print_graph(g: G):
    for (u,v,k,d) in g.edges(keys=True, data=True):
        label = d.get("label", "")
        print(f"{u} ->{label} {k}@{v}")

def graph_from_dict(d: Dict[str, Dict[str, str]]) -> G:
    ret = G()
    for parent, child_edges in d.items():
        for (inst_name, child) in child_edges.items():
            ret.add_edge(parent, child, key=inst_name)
    return ret

def roots(g: G):
    return [n for n in g.nodes() if g.in_degree(n) == 0]

def leaves(g: G):
    return [n for n in g.nodes() if g.out_degree(n) == 0]

def paths(g: G):
    ret = []
    for r in roots(g):
        for l in leaves(g):
            ret.extend(nx.all_simple_edge_paths(g, source=r, target=l))

    return ret


def assign_edge_ids(g : G):
    ctr = {} # separate counter for each design
    for(u,v,d) in g.edges(data=True):
        c = ctr.setdefault(v, 0)
        d["label"] = BitVector(10, c)
        ctr[v] += 1



def main():
    g = graph_from_dict({"r": {"g0": "g", "g1": "g"}, "g": {"d0": "d", "d1": "d"}})
    assign_edge_ids(g)
    print_graph(g)
    print(paths(g))

if __name__ == "__main__":
    main()
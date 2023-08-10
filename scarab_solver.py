import itertools

import sys

if len(sys.argv) != 2:
    raise ValueError("Usage: python3 parks.py scarab_state")

scarab_state = sys.argv[1]

def move_scarab(start_state, move_scarab_from, move_scarab_to):
    earlier, later = min(move_scarab_from, move_scarab_to), max(move_scarab_to, move_scarab_from)
    return (*start_state[:earlier],
            start_state[later],
            *start_state[earlier + 1:later],
            start_state[earlier],
            *start_state[later + 1:])


def edge_exists_in_scarab_state(scarab_from, scarab_to):
    manually_entered_edges = (
        # Ring
        {(i, i + 1) for i in range(1, 7)} | {(6, 1)} |
        # Star
        {(0, i) for i in range(1, 7)}
    )
    return ((scarab_from, scarab_to) in manually_entered_edges or
            (scarab_to, scarab_from) in manually_entered_edges)

def make_path(sink, parents):
    path = [sink]
    while parents[sink] is not None:
        sink = parents[sink]
        path.append(sink)
    return list(reversed(path))


def bfs(vertices, edges, source, sink):
    Q = [source]
    parents = {source: None}
    while Q:
        frontier = Q.pop(0)
        if frontier == sink:
            return make_path(sink, parents)
        for neighbor in edges[frontier]:
            if neighbor not in parents:
                parents[neighbor] = frontier
                Q.append(neighbor)


class ScarabGraph:
    '''
    - A node in the graph is a scarab board state.
      0 is the center hole, while 1 is the goal state
      for "1" scarab etc.  self[i] is the scarab number
      in hole i.
    
    - An undirected edge in the graph (u, v)
      represents that u and v are reachable from each
      other by sliding a single scarab.
    '''
    def __init__(self):
        self.vertices = set()
        self.edges = {}

        for vertex in itertools.permutations(list(range(7))):
            self.vertices.add(vertex)
            # Add edge for each scarab being switched with the 0.
            self.edges[vertex] = set()
            hole = vertex.index(0)
            for i in range(len(vertex)):
                if edge_exists_in_scarab_state(i, hole):
                    self.edges[vertex].add(move_scarab(vertex, i, hole))

    def get_min_path(self, source, sink=tuple(range(7))):
        return bfs(self.vertices, self.edges, source, sink)


# class Switch:
#     def __init__(self, vertex, from_index, to_index):
#         self.vertex = vertex
#         self.from_index = from_index
#         self.to_index = to_index

#     def to_str(self):
#         start_scarab = self.vertex[from_index]
#         if self.from_indx

def get_switch(u, v):
    to_switch = set()
    for i, (ui, vi) in enumerate(zip(u, v)):
        if ui != vi:
            to_switch.add(max(ui, vi))
    if len(to_switch) > 1:
        raise ValueError(f"vertices are not adjacent: {u}, {v}")
    for x in to_switch:
        return x

def get_list_of_switches(min_path):
    switches = []
    for u, v in zip(min_path[:-1], min_path[1:]):
        switches.append(get_switch(u, v))
    return switches

if __name__ == "__main__":
    scarab_state = tuple(int(x) for x in scarab_state)
    if len(scarab_state) != 7 or set(scarab_state) != set(range(7)):
        raise ValueError("Please enter a string of length 7 where 0 is the center hole, while 1 is the goal state for '1' scarab etc., and self[i] is the scarab number in hole i.")
    graph = ScarabGraph()
    min_path = graph.get_min_path(source=scarab_state)
    switches = get_list_of_switches(min_path)
    for vertex, switch in zip(min_path, switches):
        print(vertex)
        print("------------")
        print(f"Slide scarab number {switch} to the hole.")
    print(f"Complete! {len(switches)} steps.")

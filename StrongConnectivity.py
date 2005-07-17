"""StrongConnectivity.py

DFS-based algorithm for computing strongly connected components.

D. Eppstein, July 2005.
"""

import unittest
import DFS

class StronglyConnectedComponents(DFS.Searcher):
    """
    Generate the strongly connected components of G.  G should be
    represented in such a way that "for v in G" loops through the
    vertices, and "G[v]" produces a list of the neighbors of v;
    for instance, G may be a dictionary mapping each vertex to its
    neighbor set.  The result of StronglyConnectedComponents(G) is
    a sequence of lists of vertices of G.
    """

    def __init__(self,G):
        """Search for strongly connected components of graph G."""

        # set up data structures for DFS
        self._components = []
        self._dfsnumber = {}
        self._activelen = {}
        self._active = []
        self._low = {}
        self._biglow = len(G)

        # perform the Depth First Search
        DFS.Searcher.__init__(self,G)

        # clean up now-useless data structures
        del self._dfsnumber, self._activelen, self._active, self._low

    def __iter__(self):
        """Return iterator for sequence of strongly connected components."""
        return iter(self._components)

    def preorder(self,parent,child):
        if parent == child:
            self._active = []
        self._activelen[child] = len(self._active)
        self._active.append(child)
        self._low[child] = self._dfsnumber[child] = len(self._dfsnumber)

    def backedge(self,source,destination):
        self._low[source] = min(self._low[source],self._low[destination])

    def postorder(self,parent,child):
        if self._low[child] == self._dfsnumber[child]:
            self._components.append(self._active[self._activelen[child]:])
            for v in self._components[-1]:
                self._low[v] = self._biglow
            del self._active[self._activelen[child]:]
        else:
            self._low[parent] = min(self._low[parent],self._low[child])

# If run as "python StrongConnectivity.py", run tests on various small graphs
# and check that the correct results are obtained.

class StrongConnectivityTest(unittest.TestCase):
    G1 = { 0:[1], 1:[2,3], 2:[4,5], 3:[4,5], 4:[6], 5:[], 6:[] }
    C1 = [[0],[1],[2],[3],[4],[5],[6]]
    
    G2 = { 0:[1], 1:[2,3,4], 2:[0,3], 3:[4], 4:[3] }
    C2 = [[0,1,2],[3,4]]
    
    knownpairs = [(G1,C1),(G2,C2)]

    def testStronglyConnectedComponents(self):
        """Check known graph/component pairs."""
        for (graph,expectedoutput) in self.knownpairs:
            output = list(StronglyConnectedComponents(graph))
            for component in output:
                component.sort()
            output.sort()
            self.assertEqual(output,expectedoutput)

if __name__ == "__main__":
    unittest.main()   
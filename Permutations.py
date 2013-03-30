"""Permutations.py
Efficient recursive version of the Steinhaus-Johnson-Trotter algorithm
for listing all permutations of a set of items.
D. Eppstein, October 2011.

The algorithm sets up a sequence of recursive simple generators,
each taking constant space, for a total space of O(n), where n is
the number of items being permuted. The number of recursive calls
to generate a swap that moves the item originally in position n
of the input permutation is O(n-i+1), so all but a 1/n fraction of
the swaps take no recursion and the rest always take O(n) time,
for an average time per swap of O(1).
"""

import unittest

def PlainChanges(n):
    """Generate the swaps for the Steinhaus-Johnson-Trotter algorithm."""
    if n < 1:
        return
    up = xrange(n-1)
    down = xrange(n-2,-1,-1)
    recur = PlainChanges(n-1)
    try:
        while True:
            for x in down:
                yield x
            yield recur.next() + 1
            for x in up:
                yield x
            yield recur.next()
    except StopIteration:
        pass

def SteinhausJohnsonTrotter(x):
    """Generate all permutations of x.
    If x is a number rather than an iterable, we generate the permutations
    of range(x)."""

    # set up the permutation and its length
    try:
        perm = list(x)
    except:
        perm = range(x)
    n = len(perm)

    # run through the sequence of swaps
    yield perm
    for x in PlainChanges(n):
        perm[x],perm[x+1] = perm[x+1],perm[x]
        yield perm

def DoublePlainChanges(n):
    """Generate the swaps for double permutations."""
    if n < 1:
        return
    up = xrange(1,2*n-1)
    down = xrange(2*n-2,0,-1)
    recur = DoublePlainChanges(n-1)
    try:
        while True:
            for x in up:
                yield x
            yield recur.next() + 1
            for x in down:
                yield x
            yield recur.next() + 2
    except StopIteration:
        pass

def DoubleSteinhausJohnsonTrotter(n):
    """Generate all double permutations of the range 0 through n-1"""
    perm = []
    for i in range(n):
        perm += [i,i]

    # run through the sequence of swaps
    yield perm
    for x in DoublePlainChanges(n):
        perm[x],perm[x+1] = perm[x+1],perm[x]
        yield perm

def StirlingChanges(n):
    """Variant Steinhaus-Johnson-Trotter for Stirling permutations.
    A Stirling permutation is a double permutation in which each
    pair of values has only larger values between them.
    The algorithm is to sweep the largest pair of values through
    the sequence of smaller values, recursing when it reaches
    the ends of the sequence, exactly as in the standard
    Steinhaus-Johnson-Trotter algorithm. However, it differs
    in swapping items two positions apart instead of adjacent items."""
    if n <= 1:
        return
    up = xrange(2*n-2)
    down = xrange(2*n-3,-1,-1)
    recur = StirlingChanges(n-1)
    try:
        while True:
            for x in down:
                yield x
            yield recur.next() + 2
            for x in up:
                yield x
            yield recur.next()
    except StopIteration:
        pass

def StirlingPermutations(n):
    """Generate all Stirling permutations of order n."""
    perm = []
    for i in range(n):
        perm += [i,i]

    # run through the sequence of swaps
    yield perm
    for x in StirlingChanges(n):
        perm[x],perm[x+2] = perm[x+2],perm[x]
        yield perm

def InvolutionChanges(n):
    """Generate change sequence for involutions on n items.
    Uses a variation of the Steinhaus-Johnson-Trotter idea,
    in which we first recurse for n-1, generating involutions
    in which the last item is fixed, and then we the match
    for the last item back and forth over a recursively
    generated sequence for n-2."""
    if n <= 3:
        for c in [[],[],[0],[0,1,0]][n]:
            yield c
        return
    for c in InvolutionChanges(n-1):
        yield c
    yield n-2
    for i in range(n-4,-1,-1):
        yield i
    ic = InvolutionChanges(n-2)
    try:
        while True:
            yield ic.next() + 1
            for i in range(0,n-2):
                yield i
            yield ic.next()
            for i in range(n-3,-1,-1):
                yield i
    except StopIteration:
        yield n-4

def Involutions(n):
    """Generate involutions on n items.
    The first involution is always the one in which all items
    are mapped to themselves, and the last involution is the one
    in which only the final two items are swapped.
    Each two involutions differ by a change that either adds or
    removes an adjacent pair of swapped items, moves a swap target
    by one, or swaps two adjacent swap targets."""
    p = range(n)
    yield p
    for c in InvolutionChanges(n):
        if p[c] == c:
            if p[c+1] == c+1:
                p[c],p[c+1] = c+1,c     # add new pair
            else:                       # move end of one pair
                i = p[c+1]
                p[c],p[c+1],p[i] = i,c+1,c
        elif p[c+1] == c+1:             # again, move end of one pair
            i = p[c]
            p[c],p[c+1],p[i] = c,i,c+1
        elif p[c] == c+1:
            p[c],p[c+1] = c,c+1         # remove one pair
        else:                           # swap ends of two pairs
            x,y = p[c],p[c+1]
            p[x],p[y] = c+1,c
            p[c],p[c+1] = y,x
        yield p

# If run standalone, perform unit tests
class PermutationTest(unittest.TestCase):    
    def testChanges(self):
        """Do we get the expected sequence of changes for n=3?"""
        self.assertEqual(list(PlainChanges(3)),[1,0,1,0,1])
    
    def testLengths(self):
        """Are the lengths of the generated sequences factorial?"""
        f = 1
        for i in range(2,7):
            f *= i
            self.assertEqual(f,len(list(SteinhausJohnsonTrotter(i))))
    
    def testDistinct(self):
        """Are all permutations in the sequence different from each other?"""
        for i in range(2,7):
            s = set()
            n = 0
            for x in SteinhausJohnsonTrotter(i):
                s.add(tuple(x))
                n += 1
            self.assertEqual(len(s),n)
    
    def testAdjacent(self):
        """Do consecutive permutations in the sequence differ by a swap?"""
        for i in range(2,7):
            last = None
            for p in SteinhausJohnsonTrotter(i):
                if last:
                    diffs = [j for j in range(i) if p[j] != last[j]]
                    self.assertEqual(len(diffs),2)
                    self.assertEqual(p[diffs[0]],last[diffs[1]])
                    self.assertEqual(p[diffs[1]],last[diffs[0]])
                last = list(p)
    
    def testListInput(self):
        """If given a list as input, is it the first output?"""
        for L in ([1,3,5,7], list('zyx'), [], [[]], range(20)):
            self.assertEqual(L,SteinhausJohnsonTrotter(L).next())

    def testInvolutions(self):
        """Are these involutions and do we have the right number of them?"""
        telephone = [1,1,2,4,10,26,76,232,764]
        for n in range(len(telephone)):
            count = 0
            sorted = range(n)
            invs = set()
            for p in Involutions(n):
                self.assertEqual([p[i] for i in p],sorted)
                invs.add(tuple(p))
                count += 1
            self.assertEqual(len(invs),count)
            self.assertEqual(len(invs),telephone[n])

if __name__ == "__main__":
    unittest.main()

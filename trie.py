#!/usr/bin/env python
#
# Copyright (c) 2011 Kyle Gorman
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 
# trie.py
# Python implementation of the 'trie' data structure
# 
# Kyle Gorman <kgorman@ling.upenn.ed>


class Trie(object):
    """ 
    A Python implementation of a prefix tree

    # initialization
    >>> t = Trie()
    >>> corpus = 'apple applesauce application applejack apricot'.split()
    >>> t.update(corpus)

    # check membership
    >>> 'appl' in t
    False
    >>> 'apple' in t
    True
    >>> 'apples' in t
    False
    >>> 'foo' in t
    False

    # autocompletion
    >>> ' '.join(sorted(list(t.autocomplete('appl'))))
    'apple applejack applesauce application'
    >>> ' '.join(sorted(list(t.autocomplete('foobar'))))
    ''
    """

    def __init__(self):
        self.root = {}


    def __repr__(self):
        return 'Trie(%r)' % self.root


    # pickling and unpickling
    def __getstate__(self):
        """
        for pickling
        """
        return self.root


    def __setstate__(self, other):
        """
        for unpickling
        """
        self.root = other


    def __contains__(self, word):
        """ 
        True if "word" is a licit completion 
        """
        curr_node = self.root
        for char in word:
            # try/except is faster than checking for key membership
            try:
                curr_node = curr_node[char]
            except KeyError:
                return False
        if None in curr_node: # just make sure it's a licit completion 
            return True
        else: # an incomplete string
            return False


    def add(self, word):
        """
        add an iterable (probably a string) to the trie
        """
        curr_node = self.root
        for char in word:
            # try/except is faster than checking for key membership
            try: 
                curr_node = curr_node[char]
            except KeyError:
                curr_node[char] = {} # make it
                curr_node = curr_node[char] # then enter it
        curr_node[None] = word # None is then the "terminal" symbol


    def update(self, words):
        """ 
        add all elements in words to the trie
        """
        for word in words:
            self.add(word)


    def _traverse(self, curr_node):
        for char in curr_node:
            if char == None:
                yield curr_node[None]
            else:
                yield self._traverse(curr_node[char])


    def _smash(self, iterable):
        for i in iterable:
            if getattr(i, '__iter__', False):
                for j in self._smash(i):
                    yield j
            else: # base case
                yield i


    def autocomplete(self, prefix):
        """ 
        returns all licit completions of the prefix iterable
        """
        # traverse down to the prefix
        curr_node = self.root
        for char in prefix:
            # try/except is faster than checking for key membership
            try:
                curr_node = curr_node[char]
            except KeyError: 
                return [] # break out
        # recursively follow all the other paths
        return self._smash(self._traverse(curr_node))


if __name__ == '__main__':
    import doctest
    doctest.testmod()

"""
File: linkedbst.py
Author: Ken Lambert
"""
from random import shuffle

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
import time
from math import log
import sys


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def __len__(self):
        return len(list(self.inorder()))

    def is_empty(self):
        return len(self) == 0

    def is_root(self, p):
        return p == list(self.inorder())[0]

    def is_leaf(self, p):
        return not (p.left or p.right)

    def children(self, p):
        return p.left, p.right

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                lyst.append(node.data)
                recurse(node.left)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        """Supports a preorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                recurse(node.right)
                lyst.append(node.data)

        recurse(self._root)
        return iter(lyst)

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return 0
            elif self.is_leaf(top):
                return 0
            else:
                return 1 + max(height1(child) for child in self.children(top))

        p = self._root
        return height1(p)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return True if self.height() < 2 * log(len(self) + 1, 2) - 1 else False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        return list(filter(lambda x: low <= x <= high, self.inorder()))

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''

        def partition(array):
            curr_half = int(len(array) / 2)
            return array[:curr_half], array[curr_half:]

        def recurse(array):
            curr_half = int(len(array) / 2)
            self.add(array.pop(curr_half))
            left, right = partition(array)
            if left:
                recurse(left)
                if right:
                    recurse(right)
            elif right:
                recurse(right)
                if left:
                    recurse(left)
            else:
                return

        tree_data = list(self.inorder()).copy()
        self.clear()

        return recurse(tree_data)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for el in range(item + 1, max(list(self.inorder())) + 1):
            if self.find(el):
                return el
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for el in range(item - 1, min(list(self.inorder())) - 1,  -1):
            if self.find(el):
                return el
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        sys.setrecursionlimit(2000)

        def get_words(_path):
            with open(f'{_path}', 'r') as file:
                return [x.strip() for idx, x in enumerate(file.readlines()) if idx % 150 == 0]

        def get_words_bst(bst, _path, ordered):
            with open(f'{_path}', 'r') as file:
                data = [x.strip() for x in file.readlines()]

                if ordered:
                    for idx, el in enumerate(data):
                        if idx % 150 == 0:
                            bst.add(el)

                    return bst
                else:
                    shuffle(data)
                    for idx, el in enumerate(data):
                        if idx % 150 == 0:
                            bst.add(el)
                    return bst

        def _time_list_search(words: list, words_to_find: list):
            first_time = time.time()
            for idx in range(len(words_to_find)):
                words.index(words_to_find[idx])
            return time.time() - first_time

        def _time_bst_search(bst, words_to_find):
            first_time = time.time()
            for word in words_to_find:
                bst.find(word)
            return time.time() - first_time

        all_words = get_words(path)

        random_words = all_words.copy()
        shuffle(random_words)
        random_words = random_words[:10000]
        print('Search random words in array: ', _time_list_search(all_words, random_words), ' seconds')
        all_words_bst_ordered = get_words_bst(self, path, ordered=True)
        print('Search random words in ordered bst: ', _time_bst_search(all_words_bst_ordered, random_words), ' seconds')
        all_words_bst_unordered = get_words_bst(self, path, ordered=False)
        print('Search random words in unordered bst: ', _time_bst_search(all_words_bst_unordered, random_words),
              ' seconds')
        all_words_bst_ordered.rebalance()
        print('Search random words in balanced bst: ', _time_bst_search(all_words_bst_ordered, random_words),
              ' seconds')


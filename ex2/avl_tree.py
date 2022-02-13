from avl_node import AVLNode


class AVLTree:

    def __init__(self):
        """Default constructor. Initializes the AVL tree.
        """
        self.root = None

    def get_tree_root(self):
        """
        Method to get the root node of the AVLTree
        :return AVLNode -- the root node of the AVL tree
        """
        return self.root

    def get_tree_height(self):
        """Retrieves tree height.
        :return -1 in case of empty tree, current tree height otherwise.
        """
        return -1 if self.root is None else self.root.height

    def get_tree_size(self):
        """Yields number of key/value pairs in the tree.
        :return Number of key/value pairs.
        """
        return len(self.to_array())

    def to_array(self):
        """Yields an array representation of the tree's values (pre-order).
        :return Array representation of the tree values.
        """
        node = self.root
        array = []
        for node in self.nodes_preorder(node):
            array.append(int(node.value))
        return array

    def find_by_key(self, key):
        """Returns value of node with given key.
        :param key: Key to search.
        :return Corresponding value if key was found, None otherwise.
        :raises ValueError if the key is None
        """
        if key is None:
            return ValueError('Key for finding is None')

        for node in self.to_array_nodes():
            if node.key == key: return node.value
        return None

    def insert(self, key, value):
        """Inserts a new node into AVL tree.
        :param key: Key of the new node.
        :param value: Data of the new node. May be None. Nodes with the same key
        are not allowed. In this case False is returned. None-Keys and None-Values are
        not allowed. In this case an error is raised.
        :return True if the insert was successful, False otherwise.
        :raises ValueError if the key or value is None.
        """
        if self.find_node(key) is not None: return False
        if key is None or value is None: raise ValueError('Key or Value is None')

        new = AVLNode(key, value)

        if self.root is None:
            self.root = new
            return True

        node = self.root

        while True:
            if new.key < node.key and node.left is None:
                new.parent = node
                node.left = new
                if node.right is None:
                    self.height_REFRASHER(new)
                self.if_same_height(new)
                return True

            if new.key > node.key and node.right is None:
                new.parent = node
                node.right = new
                if node.left is None:
                    self.height_REFRASHER(new)
                self.if_same_height(new)
                return True

            node = node.left if new.key < node.key else node.right

    def remove_by_key(self, key):
        """Removes node with given key.
        :param key: Key of node to remove.
        :return True If node was found and deleted, False otherwise.
        @raises ValueError if the key is None.
        """
        if key is None:
            return ValueError('Key is None in remove_by_key')

        if not isinstance(key, int):
            raise ValueError

        node = self.find_node(key)

        if node is None:
            return False

        p = node.parent
        r_kid = node.right
        l_kid = node.left

        if node != self.root:

            if l_kid is None and r_kid is None:
                if node.key < p.key:
                    p.left = None
                    c = p
                    while c.right is not None:
                        c = c.right
                    self.if_same_height(c)
                else:
                    p.right = None
                    c = p
                    while c.left is not None:
                        c = c.left
                    self.if_same_height(c)
                self.refrash_all()
                return True

            if l_kid is not None and r_kid is not None:

                if r_kid.left is None:
                    r_kid.parent = None
                    r_kid.left = l_kid
                    l_kid.parent = r_kid
                    self.if_same_height(p)
                    return True
                if l_kid.right is None:
                    l_kid.parent = p
                    l_kid.right = r_kid
                    r_kid.parent = l_kid
                    p.left = l_kid if node.key <= p.key else p.right
                    self.if_same_height(p)
                    return True

                l_r_child = r_kid
                while l_r_child.left is not None:
                    l_r_child = l_r_child.left
                change_node = l_r_child
                change_node.parent.left = change_node.right
                change_node.parent = p
                change_node.left = node.left
                change_node.right = node.right
                node.left.parent = change_node
                node.right.parent = change_node

                if node.key <= p.key:
                    p.left = change_node
                else:
                    p.right = change_node
                self.if_same_height(p)
                return True

            if l_kid is not None:
                l_kid.parent = p
                if p.key >= node.key:
                    p.left = l_kid
                else:
                    p.right = l_kid
                self.if_same_height(p)
                self.refrash_all()
                return True

            if r_kid is not None:
                r_kid.parent = p
                if p.key >= node.key:
                    p.left = r_kid
                else:
                    p.right = r_kid
                self.if_same_height(self.root)
                return True
        else:

            if l_kid is None and r_kid is None:
                self.root = None
                self.if_same_height(self.root)
                return True

            if l_kid is not None and r_kid is not None:

                if r_kid.left is None:
                    b_control = r_kid.parent
                    r_kid.parent = None
                    r_kid.left = l_kid
                    l_kid.parent = r_kid
                    self.root = r_kid
                    self.if_same_height(b_control)
                    return True
                if l_kid.right is None:
                    b_control = r_kid.parent
                    l_kid.parent = None
                    l_kid.right = r_kid
                    r_kid.parent = l_kid
                    self.root = l_kid
                    self.if_same_height(b_control)
                    return True

                l_r_child = r_kid
                while l_r_child.left is not None:
                    l_r_child = l_r_child.left
                change_node = l_r_child
                change_node.parent.left = change_node.right
                b_control = change_node.parent
                change_node.parent = None
                change_node.left = node.left
                change_node.right = node.right
                l_kid.parent = change_node
                r_kid.parent = change_node
                self.root = change_node
                self.if_same_height(b_control)
                return True

            if r_kid is not None:
                self.root = r_kid
                self.if_same_height(r_kid.parent)
                r_kid.parent = None
                return True
            if l_kid is not None:
                self.root = l_kid
                self.if_same_height(l_kid.parent)
                l_kid.parent = None
                return True

    def to_array_nodes(self):
        n = self.root
        a = []
        for n in self.nodes_preorder(n):
            a.append(n)
        return a

    def refrash_all(self):
        for n in self.to_array_nodes():
            n.height = 0
        for n in self.to_array_nodes():
            current = n
            while current.parent is not None:
                p_left = current.parent.left
                p_right = current.parent.right
                p_left = -1 if p_left is None else p_left.height
                p_right = -1 if p_right is None else p_right.height
                current.parent.height = max(p_left, p_right) + 1
                current = current.parent

    def height_REFRASHER(self, node):
        now = node
        while now.parent is not None:
            now.parent.height = now.height + 1
            now = now.parent
        self.root = now

    def if_same_height(self, curr):
        while curr is not None:
            try:
                gparent = curr.parent.parent
                if gparent is None:
                    p_subtree = None
                    gparent = curr.parent
                    left_height = -1 if gparent.left is None else gparent.left.height
                    right_height = -1 if gparent.right is None else gparent.right.height

                    if abs(left_height - right_height) > 1:
                        self.restructure(curr, curr.parent, gparent, p_subtree, left)
                else:
                    p_subtree = gparent.parent
                if p_subtree is not None:
                    left = True if p_subtree.left is gparent else False
                left_height = -1 if gparent.left is None else gparent.left.height
                right_height = -1 if gparent.right is None else gparent.right.height
                if abs(left_height - right_height) > 1:
                    self.restructure(curr, curr.parent, gparent, p_subtree, left)
            except:
                pass
            curr = curr.parent

    def find_node(self, key):
        if key is None:
            raise ValueError('Key in find_node is None')
        for node in self.to_array_nodes():
            if node.key is key:
                return node
        return None

    def not_the_same(self, node):
        return True if abs(node.left - node.right) > 1 else False

    def get_key(self, node):
        return node.key

    def nodes_preorder(self, node):
        if not node:
            return iter(())

        yield node
        yield from self.nodes_preorder(node.left)
        yield from self.nodes_preorder(node.right)

    def restructure(self, a, b, c, p_subtree, left):
        first, second, third = sorted([a, b, c], key=self.get_key)
        B = [first.left, first.right, second.left, second.right, third.left, third.right]
        for xy in [first, second, third]:
            try:
                B.remove(xy)
            except ValueError:
                pass

        second.left = first
        first.parent = second
        second.right = third
        third.parent = second
        first.left = B[0]
        first.right = B[1]
        third.left = B[2]
        third.right = B[3]
        if B[0] is not None: B[0].parent = first
        if B[1] is not None: B[1].parent = first
        if B[2] is not None: B[2].parent = third
        if B[2] is not None: B[2].parent = third
        _0_height = -1 if B[0] is None else B[0].height
        _1_height = -1 if B[1] is None else B[1].height
        _2_height = -1 if B[2] is None else B[2].height
        _3_height = -1 if B[3] is None else B[3].height
        first.height = max(_0_height, _1_height) + 1
        third.height = max(_2_height, _3_height) + 1
        second.height = max(first.height, third.height) + 1
        second.parent = p_subtree
        self.height_REFRASHER(second)
        if p_subtree is not None:
            if left:
                p_subtree.left = second
            else:
                p_subtree.right = second
        self.refrash_all()

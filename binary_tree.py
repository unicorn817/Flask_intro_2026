from collections import deque
from typing import Any, Optional


class Node:
    """A node in a binary tree."""

    def __init__(
        self,
        value: Any,
        left: Optional[Node] = None,
        right: Optional[Node] = None,
    ) -> None:
        self.value = value
        self.left = left
        self.right = right


class BinaryTree:
    """A binary tree data structure."""

    def __init__(self, root_value: Any = None) -> None:
        self.root = Node(root_value) if root_value is not None else None

    def insert_left(self, current_node: Optional[Node], value: Any) -> None:
        """Insert a node as the left child of the current node."""
        if current_node is None:
            raise ValueError("Cannot insert a child under an empty node.")

        if current_node.left is None:
            current_node.left = Node(value)
        else:
            new_node = Node(value)
            new_node.left = current_node.left
            current_node.left = new_node

    def insert_right(self, current_node: Optional[Node], value: Any) -> None:
        """Insert a node as the right child of the current node."""
        if current_node is None:
            raise ValueError("Cannot insert a child under an empty node.")

        if current_node.right is None:
            current_node.right = Node(value)
        else:
            new_node = Node(value)
            new_node.right = current_node.right
            current_node.right = new_node

    def preorder_traversal(self, start: Optional[Node], traversal: str) -> str:
        """Traverse the tree in preorder (root, left, right)."""
        if start:
            traversal += (str(start.value) + " ")
            traversal = self.preorder_traversal(start.left, traversal)
            traversal = self.preorder_traversal(start.right, traversal)
        return traversal

    def inorder_traversal(self, start: Optional[Node], traversal: str) -> str:
        """Traverse the tree in inorder (left, root, right)."""
        if start:
            traversal = self.inorder_traversal(start.left, traversal)
            traversal += (str(start.value) + " ")
            traversal = self.inorder_traversal(start.right, traversal)
        return traversal

    def post_traversal(self, start: Optional[Node], traversal: str) -> str:
        """Traverse the tree in postorder (left, right, root)."""
        if start:
            traversal = self.post_traversal(start.left, traversal)
            traversal = self.post_traversal(start.right, traversal)
            traversal += str(start.value) + " "
        return traversal

    def postorder_traversal(self, start: Optional[Node], traversal: str) -> str:
        """Alias for post_traversal."""
        return self.post_traversal(start, traversal)

    def search(self, root: Optional[Node], key: Any) -> Optional[Node]:
        """Return the first matching node in level order, or None."""
        if root is None:
            return None

        pending: deque[Node] = deque([root])
        while pending:
            current = pending.popleft()
            if current.value == key:
                return current
            if current.left is not None:
                pending.append(current.left)
            if current.right is not None:
                pending.append(current.right)
        return None

    def delete_node(self, root: Optional[Node], key: Any) -> Optional[Node]:
        """Remove the first matching node, keeping the tree complete.

        The deepest rightmost node replaces the matching node. Returns the
        updated root; deleting from this tree also updates ``self.root``.
        """
        if root is None:
            return None

        is_tree_root = root is self.root
        pending: deque[tuple[Node, Optional[Node]]] = deque([(root, None)])
        target: Optional[Node] = None
        deepest: Optional[Node] = None
        deepest_parent: Optional[Node] = None

        while pending:
            current, parent = pending.popleft()
            if target is None and current.value == key:
                target = current
            deepest = current
            deepest_parent = parent

            if current.left is not None:
                pending.append((current.left, current))
            if current.right is not None:
                pending.append((current.right, current))

        if target is None or deepest is None:
            return root

        if target is deepest:
            if deepest_parent is None:
                root = None
            elif deepest_parent.right is deepest:
                deepest_parent.right = None
            else:
                deepest_parent.left = None
        else:
            if deepest_parent is None:
                return root
            target.value = deepest.value
            if deepest_parent.right is deepest:
                deepest_parent.right = None
            else:
                deepest_parent.left = None

        if is_tree_root:
            self.root = root
        return root


# Example usage
if __name__ == "__main__":
    tree = BinaryTree("R")
    root = tree.root
    if root is None:
        raise RuntimeError("The example tree needs a root node.")

    # Insert nodes
    tree.insert_left(root, "A")
    tree.insert_right(root, "B")
    left_child = root.left
    right_child = root.right
    if left_child is None or right_child is None:
        raise RuntimeError("The example tree is missing a child node.")
    tree.insert_left(left_child, "C")
    tree.insert_right(left_child, "D")
    tree.insert_left(right_child, "E")
    tree.insert_right(right_child, "F")
    right_grandchild = right_child.right
    if right_grandchild is None:
        raise RuntimeError("The example tree is missing a right grandchild.")
    tree.insert_left(right_grandchild, "G")

    print("Preorder traversal:", tree.preorder_traversal(root, ""))
    print("Inorder traversal:", tree.inorder_traversal(root, ""))
    print("Postorder traversal:", tree.post_traversal(root, ""))
    found_node = tree.search(root, "G")
    if found_node is None:
        raise RuntimeError("The example tree could not find G.")
    print("Search for G:", found_node.value)
    tree.root = tree.delete_node(tree.root, "B")
    print("After deleting B:", tree.preorder_traversal(tree.root, ""))

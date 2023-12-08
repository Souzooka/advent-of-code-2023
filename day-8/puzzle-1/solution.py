from __future__ import annotations

from typing import Dict, Optional, Union


class Node:

    def __init__(self) -> None:
        # Private constructor don't touch >:(
        self.name: Optional[str] = None
        self.left: Optional[Union[str, Node]] = None
        self.right: Optional[Union[str, Node]] = None

    @classmethod
    def createGraph(cls, lines: str) -> Node:
        # Creates a network from the provided lines, then returns the head
        nodes: Dict[str, Node] = {}

        for line in lines:
            node = cls()

            # Going to assume that all names are 3 characters long, and all lines
            # follow XXX = (XXX, XXX) format
            node.name = line[:3]
            node.left = line[7:10]
            node.right = line[12:15]
            nodes[node.name] = node

        # Resolve the pointers to other nodes in the network
        for node in nodes.values():
            assert node.left in nodes
            assert node.right in nodes
            node.left = nodes[node.left]
            node.right = nodes[node.right]

        # Return the head
        assert 'AAA' in nodes
        return nodes['AAA']

    def __repr__(self) -> str:
        # For debugging
        name = "<unnamed>"
        if self.name is not None:
            name = self.name

        left = "None"
        if self.left is not None:
            if isinstance(self.left, str):
                left = self.left
            else:
                left = self.left.name

        right = "None"
        if self.right is not None:
            if isinstance(self.right, str):
                right = self.right
            else:
                right = self.right.name

        return f"Node {name}; Left {left}; Right {right}"

def main() -> None:
    lines = []
    with open("../input.txt", "r") as file:
        lines = [line.strip() for line in file.readlines()]

    # First line is directions through the maze
    directions = lines[0]

    # Then we have the nodes and their paths after an empty line
    head = Node.createGraph(lines[2:])

    # Then we just iterate forever until we find our way out of here...
    steps = 0
    directionIndex = 0
    while head.name != 'ZZZ':
        direction = directions[directionIndex]
        if direction == 'L':
            head = head.left
        else:
            head = head.right

        steps += 1
        directionIndex = (directionIndex + 1) % len(directions)

    print(f"Total steps = {steps}")

main()

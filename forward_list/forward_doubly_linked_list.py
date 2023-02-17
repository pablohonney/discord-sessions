from __future__ import annotations

from typing import Iterable, Any
from dataclasses import dataclass


@dataclass
class Node:
    value: int
    next: Node = None
    double: Node = None


def build_forward_list(array: Iterable[Any]) -> Node:
    array = iter(array)
    head = previous = Node(next(array))

    for next_value in array:
        next_ = Node(next_value)
        previous.next = next_
        previous = next_

    return head


def iterate_nodes(node: Node) -> Iterable[Node]:
    yield node
    while node.next:
        yield node.next
        node = node.next


def forward_list_len(node: Node) -> int:
    return len(list(iterate_nodes(node)))


def add_double_references(head: Node) -> Node:
    if not head.next:
        return head

    reference_limit = forward_list_len(head) / 2
    queue = []

    for i, node in enumerate(iterate_nodes(head.next), start=1):
        if i < reference_limit:
            queue.append(node)

        if i % 2 == 0:
            queue.pop(0).double = node

    return head


def get_node_at_index(node: Node, i: int) -> Node:
    if i == 0:
        return node

    return (
        get_node_at_index(node, i // 2).double
        if i % 2 == 0
        else get_node_at_index(node, i - 1).next
    )


class ForwardList:
    def __init__(self, array: Iterable[Any]):
        self.root = build_forward_list(array)
        add_double_references(self.root)

    def __iter__(self) -> Iterable[Any]:
        for node in iterate_nodes(self.root):
            yield node.value

    def __len__(self) -> int:
        return forward_list_len(self.root)

    def __getitem__(self, index: int) -> Any:
        return get_node_at_index(self.root, index).value

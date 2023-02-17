from ..forward_doubly_linked_list import (
    build_forward_list,
    iterate_nodes,
    forward_list_len,
    add_double_references,
    get_node_at_index,
    ForwardList,
)


def test_build_forward_list():
    fl = build_forward_list(range(10))
    assert [n.value for n in iterate_nodes(fl)] == list(range(10))


def test_forward_list_len():
    fl = build_forward_list(range(10))
    assert forward_list_len(fl) == 10


def test_add_double_references():
    fl = build_forward_list(range(10))
    fl = add_double_references(fl)

    assert fl.double is None  # 0th node has no double

    assert fl.next.double.value == 2
    assert fl.next.next.double.value == 4
    assert fl.next.next.next.double.value == 6
    assert fl.next.next.next.next.double.value == 8

    assert fl.next.double == fl.next.next  # 1 * 2 == 2
    assert fl.next.next.double == fl.next.next.next.next  # 2 * 2 == 4


def test_get_node_at_index():
    fl = build_forward_list(range(10))
    fl = add_double_references(fl)

    for i in range(10):
        assert get_node_at_index(fl, i).value == i


def test_forward_list():
    fl = ForwardList(range(10))

    assert len(fl) == 10
    assert list(fl) == list(range(10))
    for i in range(10):
        assert fl[i] == i

from basic.tensors import *


def test():
    assert is_vector([1, 2, 3])
    assert not is_vector([1, 2, [1]])
    assert not is_vector(1)
    assert is_matrix([[1, 2], [3, 4]])
    assert not is_matrix(1)
    assert not is_matrix([])
    assert not is_matrix([1, 1])
    assert not is_matrix([1, [1, 1]])
    assert not is_matrix([[1, [1, 1]], [1, 1]])
    assert tensor_sum([1, 2, [3, 4]]) == 10
    assert tensor_scalar_prod(1, 2) == 2
    assert tensor_scalar_prod([1, [2, 3]], .5) == [.5, [1., 1.5]]
    assert add_tensor_float([1, 2], .5) == [1.5, 2.5]
    assert tensor_count([1, [1, 1, 2]], equal_to=1) == 3
    assert number_of_elements_in_tensor([1, [1, 2]]) == 3
    assert conditioned_number_of_elements_in_tensor([1, [1, 3, [4]]], condition=lambda x: x >= 3) == 2
    assert zeros([4], v0=2) == [2, 2, 2, 2]
    assert zeros([3, 2], v0=1) == [[1, 1], [1, 1], [1, 1]]
    assert replace_in_tensor([[1, 2, 3], 3], 3, 'doggo') == [[1, 2, 'doggo'], 'doggo']
    assert join_tensor([1, 'a', [2, [3, 'd', 5]]], c=' ') == '1 a 2 3 d 5'
    assert clean_tensor([1, 2, 'ff', [3, 'd']]) == [1, 2, [3]]
    assert tensor_max([1, [2, 0]]) == 2.
    assert tensor_min([1, [2, 0]]) == 0.
    assert negate_tensor([1, [1, -1]]) == [-1, [-1, 1]]
    assert tensor_module([1, [1, 1, 1]]) == 2
    assert normalize_tensor([1, 2, [1, 2, 4]]) == [.1, .2, [.1, .2, .4]]
    assert almost_equal(normalize_tensor([1, 2, [3, 4]]), [.1, .2, [.3, .4]])
    assert remove_from_tensor([1, 2, [1, 2]], 1) == [2, [2]]
    assert conditioned_remove([1, 2, [1, 2]], lambda x: x < 2) == [2, [2]]
    assert conditioned_remove([1], lambda x: x > 0) == []
    assert apply_to_tensor([1, [2, 3]], lambda x: x*2) == [2, [4, 6]]
    assert tensor_to_string([1, 1]) == '1\t1'
    assert tensor_to_string([[1, 1], [1, 1]]) == '1\t1\n1\t1'
    assert tensor_to_string([[[1, 1], [1, 1]], [[1, 1], [1, 1]]]) == '1\t1\n1\t1\n\n1\t1\n1\t1'
    assert round_tensor([1.11, [2.22, 3.333]], 1) == [1.1, [2.2, 3.3]]
    assert split_tensor(['1 2 3', ['1 2', '3 4']]) == [['1', '2', '3'], [['1', '2'], ['3', '4']]]
    assert string_to_matrix('1 2\n3 4', separator=' ') == [['1', '2'], ['3', '4']]


if __name__ == "__main__":
    test()

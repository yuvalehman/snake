import pytest

from snake_game.objects import Snake, Board
from snake_game.tests import setup_game


@pytest.mark.parametrize("snake_head_start_index, move_to_index, should_grow, expected_head, expected_tail, "
                         "expected_length", [
                             ((2, 2), (1, 2), False, (1, 2), (3, 2), 3),
                             ((2, 2), (1, 2), True, (1, 2), (4, 2), 4),
                         ])
def test_get_snake_forward(snake_head_start_index, move_to_index, should_grow, expected_head, expected_tail,
                           expected_length):
    snake = Snake(snake_head_start_index)
    snake.get_snake_forward(move_to_index, should_grow)
    assert snake.head == expected_head
    assert snake.tail == expected_tail
    assert snake.length == expected_length


@pytest.mark.parametrize("snake_head_start_index, foods, n, index, expected", [
                             ((2, 2), [], 5, (0, 0), False),
                             ((2, 2), [], 5, (-1, 0), True),
                             ((2, 2), [], 5, (5, 0), True),
                         ])
def test_is_out_of_board(snake_head_start_index, foods, n, index, expected):
    board = Board(snake_head_start_index, foods, n)
    assert board.is_out_of_board(index) is expected


@pytest.mark.parametrize("snake_head_start_index, foods, n, next_move_index, snake_locations, expected", [
    ((2, 2), [], 5, (0, 0), [(2, 2), (3, 2), (4, 2)], False),
])
def test_is_self_collide(snake_head_start_index, foods, n, next_move_index, snake_locations, expected):
    board = Board(snake_head_start_index, foods, n)
    board.matrix = {}
    for location in snake_locations:
        board.matrix[location] = 's'
    assert board.is_self_collide(next_move_index) is expected


@pytest.mark.parametrize("n, foods, moves, expected_matrix, expected_snake_nodes, expected_game_over", [
    (  # regular move, with and without eating
            5, [(0, 2), (4, 2)], ['', ''],
            {(0, 2): 's', (1, 2): 's', (2, 2): 's', (3, 2): 's', (4, 2): 'f'},
            [(3, 2), (2, 2), (1, 2), (0, 2)], False),

    (  # move out of board
            5, [], ['6', '', ''], {(2, 2): 's', (2, 3): 's', (2, 4): 's'},
            [(2, 2), (2, 3), (2, 4)], True),
    (  # move into itself
            5, [(2, 3)], ['6', '8', '4'], {(2, 2): 's', (2, 3): 's', (3, 3): 's', (3, 2): 's'},
            [(3, 2), (2, 2), (2, 3), (3, 3)], True),
    (  # return food to the matrix
            5, [(2, 3)], ['6', '', '8', '', '4'],
            {(2, 4): 's', (3, 4): 's', (4, 4): 's', (4, 3): 's', (2, 3): 'f'},
            [(2, 4), (3, 4), (4, 4), (4, 3)], False),
])
def test_multiple_movements(n, foods, moves, expected_matrix, expected_snake_nodes, expected_game_over):
    game = setup_game(n, foods)
    for move in moves:
        game.move(move)

    assert game.board.matrix == expected_matrix
    assert game.snake.nodes == expected_snake_nodes
    assert game.game_over is expected_game_over


"""
Sample board:
(0,0)(0,1)(0,2)(0,3)(0,4)
(1,0)(1,1)(1,2)(1,3)(1,4)
(2,0)(2,1)(2,2)(2,3)(2,4)
(3,0)(3,1)(3,2)(3,3)(3,4)
(4,0)(4,1)(4,2)(4,3)(4,4)
"""

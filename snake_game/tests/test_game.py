import pytest

from snake_game.tests import setup_game


@pytest.mark.parametrize("n, foods, game_over, next_move_index, expected, expected_game_over", [
    (5, [(1, 2)], False, (1, 2), (4, (1, 2)), False),  # move with snake growing by eating
    (5, [], False, (1, 2), (3, (1, 2)), False),  # moving without eating anything
    (5, [(1, 2)], True, (1, 2), (3, (2, 2)), True),  # game over already, nothing should happen
    (5, [], False, (5, 5), (3, (2, 2)), True),  # out of board next index, should cause game over
])
def test_move_to_next_index(n, foods, game_over, next_move_index, expected, expected_game_over):
    game = setup_game(n, foods)
    game.game_over = game_over
    assert game.move_to_next_index(next_move_index) == expected
    assert game.game_over == expected_game_over


@pytest.mark.parametrize("n, foods, snake_direction, paused, single_move_input, expected, expected_paused", [
    (5, [], '2', False, '', '2', False),  # empty input
    (5, [], '2', False, '8', '2', False),  # 180 deg turn, stay in the same direction
    (5, [], '2', False, '5', '2', True),  # pause game
    (5, [], '2', True, '5', '2', False),  # unpause game
    (5, [], '2', False, '4', '4', False),  # legal turn
    (5, [], '4', False, '2', '2', False),  # legal turn
    (5, [], '2', False, '10*', '2', False),  # irrelevant input
])
def test_find_move_direction(n, foods, snake_direction, paused, single_move_input, expected, expected_paused):
    game = setup_game(n, foods)
    game.snake.direction = snake_direction
    game.paused = paused
    assert game.find_move_direction(single_move_input) == expected
    assert game.paused == expected_paused


@pytest.mark.parametrize("n, foods, direction, snake_head, expected", [
    (5, [], '2', (2, 2), (1, 2)),
    (5, [], '4', (2, 2), (2, 1)),
    (5, [], '6', (2, 2), (2, 3)),
    (5, [], '8', (2, 2), (3, 2)),
])
def test_calc_next_move_index(n, foods, direction, snake_head, expected):
    game = setup_game(n, foods)
    game.snake.nodes[-1] = snake_head
    assert game.calc_next_move_index(direction) == expected


@pytest.mark.parametrize("n, foods, snake_head, snake_tail, snake_length, single_move_input, expected_head, "
                         "expected_tail, expected_length, is_game_over", [
                             (5, [], (2, 2), (4, 2), 3, '', (1, 2), (3, 2), 3, False),  # no input, moves up
                             (5, [(1, 2)], (2, 2), (4, 2), 3, '', (1, 2), (4, 2), 4, False),  # eats & moves up
                             (5, [], (0, 2), (2, 2), 3, '', (0, 2), (2, 2), 3, True),  # no input, snake out of board
                             (5, [], (2, 0), (4, 0), 3, '4', (2, 0), (4, 0), 3, True),  # turn into snake out of board
                             (5, [(1, 2)], (2, 2), (4, 2), 3, '5', (2, 2), (4, 2), 3, False),  # pause
                         ])
def test_move(n, foods, snake_head, snake_tail, snake_length, single_move_input, expected_head,
              expected_tail, expected_length, is_game_over):
    game = setup_game(n, foods)
    game.snake.nodes[-1] = snake_head
    game.snake.nodes[0] = snake_tail
    game.snake.length = snake_length
    game.move(single_move_input)
    assert game.snake.length == expected_length
    assert game.snake.head == expected_head
    assert game.snake.tail == expected_tail
    assert game.snake.length == expected_length
    assert game.game_over == is_game_over

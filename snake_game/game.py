from objects import Snake, Board


class Game:
    """
    holds all the logic and actual game sequence.
    """
    IRRELEVANT_KEYPRESS = ['1', '3', '7', '9', '0', '*', '#']
    PAUSE_KEY = '5'
    POSSIBLE_MOVEMENTS = {
        '2': {'4', '6'},
        '4': {'2', '8'},
        '8': {'4', '6'},
        '6': {'2', '8'},
    }

    board = None
    snake = None
    paused = False
    game_over = False

    def __init__(self, n, foods):
        if not self.validate_input(n):
            raise Exception('invalid input')
        snake_head_start_index = (n // 2, n // 2)
        self.snake = Snake(snake_head_start_index)
        self.board = Board(snake_head_start_index, foods, n)

    @staticmethod
    def validate_input(n):
        if n < 5:
            print('Board too little, skipping this case')
            return False
        return True

    def is_game_over(self, next_move_index):
        if self.board.is_out_of_board(next_move_index):
            return True
        if self.board.is_self_collide(next_move_index):
            return True
        return False

    def move(self, single_move_input):
        if self.game_over:
            return
        parsed_input = self.parse_input(single_move_input)
        move_direction = self.find_move_direction(parsed_input)
        if self.paused:
            return
        self.snake.update_direction(move_direction)
        next_move_index = self.calc_next_move_index(move_direction)
        self.move_to_next_index(next_move_index)

    def parse_input(self, single_move_input):
        if len(single_move_input) == 0:
            return self.PAUSE_KEY if self.paused else self.snake.direction
        return single_move_input[-1]

    def move_to_next_index(self, next_move_index) -> tuple:
        """
        move the snake to it's next location
        :return: snake length and head location
        """
        if self.game_over or self.is_game_over(next_move_index):
            self.game_over = True
            print('GAME OVER!')
            return self.snake.length, self.snake.head
        # nothing bad happened, moving the snake forward, first get the original matrix content
        next_index_content = self.board.matrix.get(next_move_index)
        self.board.mark_snake(next_move_index)
        should_grow = next_index_content == 'f'
        if not should_grow:
            self.board.unmark_snake(self.snake.tail)
        self.snake.get_snake_forward(next_move_index, should_grow)
        return self.snake.length, self.snake.head

    def find_move_direction(self, parsed_input):
        """
        understanding if and what should be the snake's next movement's direction
        """
        if parsed_input == self.PAUSE_KEY:
            self.paused = not self.paused  # switching the pause state but anyway need to signal the game to hold the move until the next input
            return self.snake.direction

        # validating the next move is a 90 deg turn and not 180 / 0 which will leave us in the same direction
        possible_movements = self.POSSIBLE_MOVEMENTS.get(parsed_input)
        if not possible_movements:
            return self.snake.direction

        # only if the snake is already in one of the 90 deg directions we can accept the turn
        if self.snake.direction in possible_movements:
            return parsed_input

        # any other symbol will lead the snake to remain in the same direction
        return self.snake.direction

    def calc_next_move_index(self, direction):
        """
        finding the next location for the move according to the snake's current location and next move's direction
        """
        head_index = self.snake.head
        if direction == '2':  # Up
            next_index = (head_index[0] - 1, head_index[1])
        elif direction == '8':  # Down
            next_index = (head_index[0] + 1, head_index[1])
        elif direction == '4':  # Left
            next_index = (head_index[0], head_index[1] - 1)
        else:  # '6':  # Right
            next_index = (head_index[0], head_index[1] + 1)
        return next_index

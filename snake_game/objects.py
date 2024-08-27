
class Snake:
    """
    holds the current state of the snake and actions
    """
    length = 3
    direction = '2'
    nodes = None

    def __init__(self, snake_head_start_index):
        head_index = snake_head_start_index
        self.nodes = []
        self.nodes.append((head_index[0] + 2, head_index[1]))
        self.nodes.append((head_index[0] + 1, head_index[1]))
        self.nodes.append(head_index)

    @property
    def tail(self):
        return self.nodes[0]

    @property
    def head(self):
        return self.nodes[-1]

    def get_snake_forward(self, index, should_grow=False):
        self.nodes.append(index)
        if should_grow:
            self.length += 1
        else:
            self.nodes = self.nodes[1:]

    def update_direction(self, new_direction):
        self.direction = new_direction


class Board:
    """
    holds the information about the playing board as it is currently ordered, helps with the keeps an updated state and
    validating possible game actions
    """
    matrix = None
    size = None
    n = None
    foods = None

    def __init__(self, snake_head_start_index, foods, n):
        self.n = n
        self.foods = set(foods)

        self._init_food(foods)  # make sure food is initiated first, snake mark should override food at this point!
        self._init_snake_location(snake_head_start_index)

    def _init_food(self, foods):
        self.matrix = {}
        for food in foods:
            if self.is_out_of_board(food):
                print('Some food inputs are out of index, ignoring {}'.format(food))
                continue
            self.matrix[food] = 'f'

    def _init_snake_location(self, snake_head_start_index):
        start_index = snake_head_start_index
        self.mark_snake(start_index)
        self.mark_snake((start_index[0] + 1, start_index[1]))
        self.mark_snake((start_index[0] + 2, start_index[1]))

    def mark_snake(self, index):
        self.matrix[index] = 's'

    def unmark_snake(self, index):
        # returning the food if the snake moved on
        if index in self.foods:
            self.matrix[index] = 'f'
        else:
            self.matrix.pop(index)

    def is_out_of_board(self, index):
        for i in index:
            if i < 0 or i >= self.n:
                return True
        return False

    def is_self_collide(self, next_move_index):
        if next_move_index in self.matrix and self.matrix[next_move_index] == 's':
            return True
        return False

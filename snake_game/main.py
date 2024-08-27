from ast import literal_eval

from game import Game


def run():
    num_cases = int(input())
    for case in range(1, num_cases + 1):
        n = int(input())
        k = int(input())
        foods = literal_eval(input())

        game = Game(n, foods)

        for _ in range(k):
            single_move_input = input()
            game.move(single_move_input)

        print("Case #{}: {}".format(case, game.snake.length))


if __name__ == '__main__':
    run()

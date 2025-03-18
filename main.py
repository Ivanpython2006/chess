from table import *

transformer_r = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
transformer_c = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}

game = Table()
while True:
    print(game)
    if game.queue % 2 == 0:
        print('Ходят белые. Введите координаты фигуры, которой ходите походить. Если хотите'
              'отменить последний ход, введите R k (k - количество ходов):')
    if game.queue % 2 == 1:
        print('Ходят чёрные. Введите координаты фигуры, которой ходите походить. Если хотите'
              'отменить последний ход, введите R k (k - количество ходов):')
    c, r = input().split(' ')
    if c == 'R':
        r = int(r)
        for i in range(r):
            game.reverse()
    else:
        r = transformer_r[r]
        c = transformer_c[c]
        print('Введите клетку, куда ходите походить. Если хотите увидеть подсказки, введите C C:')
        new_c, new_r = input().split(' ')
        if new_c == 'C' and new_r == 'C':
            print(game.print_pos(r, c))
            new_c, new_r = input().split(' ')
        new_r = transformer_r[new_r]
        new_c = transformer_c[new_c]
        game.move(r, c, new_r, new_c)
        game.change_pawn()
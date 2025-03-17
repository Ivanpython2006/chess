from figure import *

class Checker(Figure):
    def __init__(self, r, c, color):
        super().__init__(r, c, color)
        self.is_king = False  # Является ли шашка дамкой

    def move(self, new_r, new_c, attack=False):
        if self.is_king:
            # Дамка может двигаться на любое количество клеток по диагонали
            if abs(new_r - self.r) == abs(new_c - self.c):
                super().move(new_r, new_c)
                return True
        else:
            # Обычная шашка может двигаться только на одну клетку по диагонали
            if abs(new_r - self.r) == 1 and abs(new_c - self.c) == 1:
                super().move(new_r, new_c)
                return True
        return False

    def promote_to_king(self):
        if (self.color == 'W' and self.r == 0) or (self.color == 'B' and self.r == 7):
            self.is_king = True

    def can_capture(self, table):
        # Проверка, может ли шашка выполнить взятие
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if self.is_king else [(-1, -1), (-1, 1)] if self.color == 'W' else [(1, -1), (1, 1)]
        for dr, dc in directions:
            r = self.r + dr
            c = self.c + dc
            if 0 <= r < 8 and 0 <= c < 8:
                enemy = table.get_figure(r, c)
                if enemy and enemy.color != self.color:
                    r2 = r + dr
                    c2 = c + dc
                    if 0 <= r2 < 8 and 0 <= c2 < 8 and table.get_figure(r2, c2) is None:
                        return True
        return False

    def perform_capture(self, table, new_r, new_c):
        # Выполнение взятия
        dr = new_r - self.r
        dc = new_c - self.c
        step_r = dr // abs(dr)
        step_c = dc // abs(dc)
        r, c = self.r, self.c
        while r != new_r or c != new_c:
            r += step_r
            c += step_c
            enemy = table.get_figure(r, c)
            if enemy:
                table.table.remove(enemy)
                break
        super().move(new_r, new_c)
        return True

class Table:
    def __init__(self):
        self.queue = 0  # Очередь хода (0 - белые, 1 - черные)
        self.table = set()

        # Расстановка шашек
        for r in range(8):
            for c in range(8):
                if (r + c) % 2 == 1:  # Шашки ставятся только на черные клетки
                    if r < 3:
                        self.table.add(Checker(r, c, 'B'))  # Черные шашки
                    elif r > 4:
                        self.table.add(Checker(r, c, 'W'))  # Белые шашки

    def __repr__(self):
        s = '   A B C D E F G H   \n\n'
        for i in range(8):
            s += str(8 - i) + '  '
            for j in range(8):
                fig = self.get_figure(i, j)
                if fig:
                    if fig.color == 'W':
                        s += 'W ' if not fig.is_king else 'W* '
                    else:
                        s += 'B ' if not fig.is_king else 'B* '
                else:
                    s += '. '
            s += ' ' + str(8 - i) + '\n'
        s += '\n   A B C D E F G H'
        return s

    def get_figure(self, r, c):
        for cell in self.table:
            if cell.get_coords() == (r, c):
                return cell
        return None

    def is_capture_possible(self, color):
        # Проверка, есть ли обязательное взятие для фигур данного цвета
        for fig in self.table:
            if fig.color == color and fig.can_capture(self):
                return True
        return False

    def move(self, r, c, new_r, new_c):
        fig = self.get_figure(r, c)
        if fig is None:
            print('Нет фигуры на указанной клетке.')
            return False

        if (self.queue % 2 == 0 and fig.color == 'W') or (self.queue % 2 == 1 and fig.color == 'B'):
            # Проверка на обязательное взятие
            if self.is_capture_possible(fig.color):
                if not fig.can_capture(self):
                    print('Обязательно выполнить взятие.')
                    return False

            # Проверка, является ли ход взятием
            if abs(new_r - r) == 2 and abs(new_c - c) == 2:
                # Выполнение взятия
                if fig.perform_capture(self, new_r, new_c):
                    # Проверка на превращение в дамку
                    fig.promote_to_king()
                    self.queue += 1
                    return True
                else:
                    print('Неверный ход для взятия.')
                    return False
            else:
                # Обычный ход
                if fig.move(new_r, new_c):
                    # Проверка на превращение в дамку
                    fig.promote_to_king()
                    self.queue += 1
                    return True
                else:
                    print('Неверный ход.')
                    return False
        else:
            print('Ход фигуры не того цвета.')
            return False
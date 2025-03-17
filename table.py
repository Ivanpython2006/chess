from figure import *

class Table:
    def __init__(self):
        self.queue = 0
        self.table = {*[Pawn(6, i, 'W') for i in range(8)],
                      *[Pawn(1, i, 'B') for i in range(8)],
                      Rook(7, 0, 'W'), Rook(7, 7, 'W'), Rook(0, 0, 'B'), Rook(0, 7, 'B'),
                      Knight(7, 1, 'W'), Knight(7, 6, 'W'), Knight(0, 1, 'B'), Knight(0, 6, 'B'),
                      Bishop(7, 2, 'W'), Bishop(7, 5, 'W'), Bishop(0, 2, 'B'), Bishop(0, 5, 'B'),
                      Queen(7, 3, 'W'), King(7, 4, 'W'), Queen(0, 3, 'B'), King(0, 4, 'B')}
        self.all_steps = [] # Ходы записываются в виде (откуда походила, куда походила, кого побила (в теории))

    # Доп. задание под номером 5
    def reverse(self):
        if len(self.all_steps) == 0:
            print('Нет шагов для отмены.')
            return False
        last_step = self.all_steps[-1]
        if len(last_step) == 3:
            self.table.add(last_step[2])
            fig = self.get_exemp_figure(last_step[1][0], last_step[1][1])
            fig.change_coords(last_step[0])
            self.queue -= 1
        else:
            fig = self.get_exemp_figure(last_step[1][0], last_step[1][1])
            fig.change_coords(last_step[0])
            if type(fig) == Pawn:
                fig.first_step -= 1
            self.queue -= 1
        self.all_steps = self.all_steps[:-1]
        return True

    def get_figure(self, r, c):
        for cell in self.table:
            if cell.get_coords() == (r, c):
                if type(cell) == Pawn:
                    if cell.color == 'W':
                        return 'P'
                    else:
                        return 'p'
                if type(cell) == Rook:
                    if cell.color == 'W':
                        return 'R'
                    else:
                        return 'r'
                if type(cell) == Knight:
                    if cell.color == 'W':
                        return 'N'
                    else:
                        return 'n'
                if type(cell) == Bishop:
                    if cell.color == 'W':
                        return 'B'
                    else:
                        return 'b'
                if type(cell) == Queen:
                    if cell.color == 'W':
                        return 'Q'
                    else:
                        return 'q'
                if type(cell) == King:
                    if cell.color == 'W':
                        return 'K'
                    else:
                        return 'k'
        return '.'

    def get_exemp_figure(self, r, c):
        for cell in self.table:
            if cell.get_coords() == (r, c):
                return cell
        return None

    def __repr__(self):
        s = '   A B C D E F G H   \n\n'
        for i in range(8):
            s += str(8-i) + '  '
            for j in range(8):
                s += self.get_figure(i, j) + ' '
            s += ' ' + str(8-i) + '\n'
        s += '\n   A B C D E F G H'
        return s
    
    def is_barrier(self, fig, new_r, new_c): # Если есть баръер, то возвращается True
        if fig.r == new_r and fig.c == new_c:
            return True
        if type(fig) == Knight:
            ano = self.get_exemp_figure(new_r, new_c)
            if ano is None:
                return False
            elif ano.color != fig.color:
                return False
            else:
                return True
        if type(fig) == Pawn:
            if abs(fig.r - new_r) == 1 and abs(fig.c - new_c) == 0:
                return False
            elif abs(fig.r - new_r) == 1 and abs(fig.c - new_c) == 1:
                ano = self.get_exemp_figure(new_r, new_c)
                if ano is None:
                    return False
                if ano.color == fig.color:
                    return True
                return False
            elif abs(fig.r - new_r) == 2:
                ano = self.get_exemp_figure(new_r, new_c)
                if ano is not None:
                    if ano.color == fig.color:
                        return True
                ano = self.get_exemp_figure((fig.r + new_r)//2, new_c)
                # Доделать
                if ano is not None:
                    return True
                return False
        if type(fig) == Rook:
            dir_c = fig.c - new_c
            dir_r = fig.r - new_r
            if dir_c != 0:
                for i in range(min(fig.c, new_c)+1, max(fig.c, new_c)-1):
                    ano = self.get_exemp_figure(new_r, i)
                    if ano is not None:
                        return True
                ano = self.get_exemp_figure(new_r, new_c)
                if ano is None:
                    return False
                if ano.color == fig.color:
                    return True
                return False
            elif dir_r != 0:
                for i in range(min(fig.r, new_r)+1, max(fig.r, new_r)):
                    if ano is not None:
                        return True
                ano = self.get_exemp_figure(new_r, new_c)
                if ano is None:
                    return False
                if ano.color == fig.color:
                    return True
                return False
        if type(fig) == Bishop:
            dir_c = fig.c - new_c
            dir_r = fig.r - new_r
            if dir_r * dir_c > 0:
                for i in range(1, abs(dir_r)):
                    ano = self.get_exemp_figure(min(fig.r, new_r)+i, min(fig.c, new_c)+i)
                    if ano is not None:
                        return True
                ano = self.get_exemp_figure(new_r, new_c)
                if ano is None:
                    return False
                if ano.color == fig.color:
                    return True
                return False
            if dir_r * dir_c < 0:
                for i in range(1, abs(dir_r)):
                    ano = self.get_exemp_figure(min(fig.r, new_r)+i, min(fig.c, new_c)+i)
                    print(type(ano), min(fig.r, new_r)+i, min(fig.c, new_c)-i)
                    if ano is not None:
                        # Доделать
                        return True
                ano = self.get_exemp_figure(new_r, new_c)
                if ano is None:
                    return False
                if ano.color == fig.color:
                    return True
                return False
        if type(fig) == Queen:
            dir_c = fig.c - new_c
            dir_r = fig.r - new_r
            if dir_c != 0 and dir_r == 0:
                for i in range(min(fig.c, new_c)+1, max(fig.c, new_c)-1):
                    ano = self.get_exemp_figure(new_r, i)
                    if ano is not None:
                        return True
                ano = self.get_exemp_figure(new_r, new_c)
                if ano is None:
                    return False
                if ano.color == fig.color:
                    return True
                return False
            elif dir_r != 0 and dir_c == 0:
                for i in range(min(fig.r, new_r)+1, max(fig.r, new_r)):
                    ano = self.get_exemp_figure(i, new_c)
                    if ano is not None:
                        return True
                ano = self.get_exemp_figure(new_r, new_c)
                if ano is None:
                    return False
                if ano.color == fig.color:
                    return True
                return False
            elif dir_r != 0 and dir_c != 0:
                if dir_r * dir_c > 0:
                    for i in range(1, abs(dir_r)):
                        ano = self.get_exemp_figure(min(fig.r, new_r)+i, min(fig.c, new_c)+i)
                        if ano is not None:
                            return True
                    ano = self.get_exemp_figure(new_r, new_c)
                    if ano is None:
                        return False
                    if ano.color == fig.color:
                        return True
                    return False
                if dir_r * dir_c < 0:
                    for i in range(1, abs(dir_r)):
                        ano = self.get_exemp_figure(min(fig.r, new_r)+i, min(fig.c, new_c)-i)
                        if ano is not None:
                            return True
                    ano = self.get_exemp_figure(new_r, new_c)
                    if ano is None:
                        return False
                    if ano.color == fig.color:
                        return True
                    return False
        if type(fig) == King:
            ano = self.get_exemp_figure(new_r, new_c)
            if ano is None:
                return False
            elif ano.color != fig.color:
                return False
            else:
                return True

    def move(self, r, c, new_r, new_c):
        for cell in self.table:
            if cell.get_coords() == (r, c):
                if self.queue % 2 == 0 and cell.color == 'W' or\
                   self.queue % 2 == 1 and cell.color == 'B':
                    vrag = None
                    if self.is_barrier(cell, new_r, new_c):
                        print('На пути препятствие. Ход невозможен.')
                        return False
                    for cell2 in self.table:
                        if cell2.get_coords() == (new_r, new_c):
                            if cell2.color != cell.color:
                                vrag = cell2
                                break
                            if cell2.color == cell.color:
                                print('Нельзя бить свою фигуру.')
                                return False
                    is_pob = False
                    if vrag is not None:
                        if not cell.move(new_r, new_c, True):
                            print('Неверный ход.')
                            return False
                        is_pob = True
                        self.table.remove(cell2)
                    else:
                        if not cell.move(new_r, new_c, False):
                            print(cell.r, cell.c, new_r, new_c)
                            print('Неверный ход.')
                            return False
                    self.queue += 1
                    if is_pob:
                        step = ((r, c), (new_r, new_c), vrag)
                    else:
                        step = ((r, c), (new_r, new_c))
                    self.all_steps.append(step)
                    return True
                else:
                    print('\nХод фигуры не того цвета.\n')
                    return False
        print('Координаты фигуры введены неверно.')
        return False
    
    def print_pos(self, r, c):
        res = self.show_pos(r, c)
        if res is None:
            res = []
        s = '   A B C D E F G H   \n\n'
        for i in range(8):
            s += str(8-i) + '  '
            for j in range(8):
                if (i, j) in res:
                    s += '*' + ' '
                else:
                    s += self.get_figure(i, j) + ' '
            s += ' ' + str(8-i) + '\n'
        s += '\n   A B C D E F G H'
        return s

    def show_pos(self, r, c):
        for cell in self.table:
            if cell.get_coords() == (r, c):
                if type(cell) == King:
                    r, c = cell.get_coords()
                    return [(r+1, c+1), (r+1, c), (r+1, c-1),
                            (r, c+1), (r, c), (r, c-1),
                            (r-1, c+1), (r-1, c), (r-1, c-1)]
                if type(cell) == Queen:
                    return []
                if type(cell) == Bishop:
                    return []
                if type(cell) == Knight:
                    r, c = cell.get_coords()
                    return [(r+2, c+1), (r+2, c-1), (r+1, c+2), (r+1, c-2),
                            (r-1, c+2), (r-1, c-2), (r-2, c+1), (r-2, c-1)]
                if type(cell) == Rook:
                    r, c = cell.get_coords()
                    return [(r, i) for i in range(8)] + [(i, c) for i in range(8)]
                if type(cell) == Pawn:
                    if cell.first_step == 0:
                        if cell.color == 'W':
                            c = cell.get_coords()
                            return [(c[0]+1, c[1]), (c[0]+2, c[1])]
                        else:
                            c = cell.get_coords()
                            return [(c[0]-1, c[1]), (c[0]-2, c[1])]
                    else:
                        if cell.color == 'W':
                            c = cell.get_coords()
                            return [(c[0]+1, c[1])]
                        else:
                            c = cell.get_coords()
                            return [(c[0]-1, c[1])]
        return None
# Строки в индексы
# 0->8, 1->7, 2->6, 3->5, 4->4, 5->3, 6->2, 7->1
# Столбцы в индексы
# 0->A, 1->B, 2->C, 3->D, 4->E, 5->F, 6->G, 7->H

class Figure:
    def __init__(self, r, c, color):
        self.r = r
        self.c = c
        if color not in ['W', 'B']:
            print('Неправильный цвет фигуры.')
            return False
        self.color = color
        return True
    
    def change_coords(self, rc):
        r, c = rc
        self.r = r
        self.c = c

    def move(self, new_r, new_c, attack=False):
        self.r = new_r
        self.c = new_c
    def get_coords(self):
        return self.r, self.c

class King(Figure):
    def __init__(self, r, c, color):
        super().__init__(r, c, color)
    
    def move(self, new_r, new_c, attack=False):
        if abs(new_r-self.r) > 1 or abs(new_c-self.c) > 1:
            return False
        super().move(new_r, new_c)
        return True
    
class Queen(Figure):
    def __init__(self, r, c, color):
        super().__init__(r, c, color)

    def move(self, new_r, new_c, attack=False):
        if new_r - self.r == 0 and abs(new_c - self.c) > 0 or\
           new_c - self.c == 0 and abs(new_r - self.r) > 0 or\
           abs(new_c - self.c) == abs(new_r - self.r):
            super().move(new_r, new_c)
            return True
        return False
    
class Rook(Figure):
    def __init__(self, r, c, color):
        super().__init__(r, c, color)
    
    def move(self, new_r, new_c, attack=False):
        if new_r - self.r == 0 and abs(new_c - self.c) > 0 or\
           new_c - self.c == 0 and abs(new_r - self.r) > 0:
            super().move(new_r, new_c)
            return True
        return False
    
class Bishop(Figure):
    def __init__(self, r, c, color):
        super().__init__(r, c, color)
    
    def move(self, new_r, new_c, attack=False):
        if abs(new_c - self.c) == abs(new_r - self.r):
            super().move(new_r, new_c)
            return True
        return False
    
class Knight(Figure):
    def __init__(self, r, c, color):
        super().__init__(r, c, color)
    
    def move(self, new_r, new_c, attack=False):
        if abs(new_r - self.r) == 2 and abs(new_c - self.c) == 1 or\
           abs(new_r - self.r) == 1 and abs(new_c - self.c) == 2:
            super().move(new_r, new_c)
            return True
        return False
    
class Pawn(Figure):
    def __init__(self, r, c, color):
        super().__init__(r, c, color)
        self.first_step = 0
        self.en_passant_vulnerable = False

    def move(self, new_r, new_c, attack=False):
        if not attack:
            # Обычный ход пешки
            if self.first_step == 0 and abs(self.r - new_r) == 2 and self.c == new_c:
                self.first_step += 1
                self.en_passant_vulnerable = True
                super().move(new_r, new_c)
                return True
            elif abs(self.r - new_r) == 1 and self.c == new_c:
                self.first_step += 1
                super().move(new_r, new_c)
                return True
        else:
            if self.color == 'W' and new_r - self.r == -1 and abs(new_c - self.c) == 1:
                self.first_step += 1
                super().move(new_r, new_c)
                return True
            elif self.color == 'B' and new_r - self.r == 1 and abs(new_c - self.c) == 1:
                self.first_step += 1
                super().move(new_r, new_c)
                return True
        return False

    def can_promote(self):
        # Проверка, достигла ли пешка последней горизонтали
        if (self.color == 'W' and self.r == 0) or (self.color == 'B' and self.r == 7):
            return True
        return False
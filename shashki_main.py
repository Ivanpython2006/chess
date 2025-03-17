from shashki_class import Table

# Преобразование координат
transformer_r = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
transformer_c = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}

# Обратное преобразование координат (для вывода)
reverse_transformer_r = {v: k for k, v in transformer_r.items()}
reverse_transformer_c = {v: k for k, v in transformer_c.items()}

def print_help():
    print("Правила ввода:")
    print("1. Введите координаты фигуры, которой хотите походить (например, 'A3').")
    print("2. Введите координаты клетки, куда хотите походить (например, 'B4').")
    print("3. Для выхода введите 'exit'.")

def main():
    game = Table()  # Создаем игровое поле
    print("Добро пожаловать в игру шашки!")
    print_help()

    while True:
        print(game)  # Выводим текущее состояние доски
        if game.queue % 2 == 0:
            print("Ходят белые (W).")
        else:
            print("Ходят черные (B).")

        # Ввод координат фигуры
        coords = input("Введите координаты фигуры (например, 'A3'): ").upper()
        if coords == 'EXIT':
            print("Игра завершена.")
            break

        if len(coords) != 2 or coords[0] not in transformer_c or coords[1] not in transformer_r:
            print("Неверный формат ввода. Попробуйте снова.")
            continue

        c, r = coords[0], coords[1]
        r = transformer_r[r]
        c = transformer_c[c]

        # Проверка, есть ли фигура на указанной клетке
        fig = game.get_figure(r, c)
        if fig is None:
            print("На указанной клетке нет фигуры.")
            continue

        # Ввод координат для хода
        new_coords = input("Введите клетку, куда хотите походить (например, 'B4'): ").upper()
        if new_coords == 'EXIT':
            print("Игра завершена.")
            break

        if len(new_coords) != 2 or new_coords[0] not in transformer_c or new_coords[1] not in transformer_r:
            print("Неверный формат ввода. Попробуйте снова.")
            continue

        new_c, new_r = new_coords[0], new_coords[1]
        new_r = transformer_r[new_r]
        new_c = transformer_c[new_c]

        # Выполнение хода
        if not game.move(r, c, new_r, new_c):
            print("Невозможно выполнить ход. Попробуйте снова.")

if __name__ == "__main__":
    main()

import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0 for c in range(self.cols)] for c in range(self.rows)]  # список грид заполненный нулями
        if randomize:
            for row in grid:
                for c in range(len(row)):
                    row[c] = random.choice([0, 1])
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        x, y = cell
        neighbours = []
        cg = self.curr_generation
        if x != 0:
            neighbours.append(cg[x - 1][y])
        if y != 0:
            neighbours.append(cg[x][y - 1])
        if y != self.cols - 1:
            neighbours.append(cg[x][y + 1])
        if x != self.rows - 1:
            neighbours.append(cg[x + 1][y])
        if x != 0 and y != 0:
            neighbours.append(cg[x - 1][y - 1])
        if x != 0 and y != self.cols - 1:
            neighbours.append(cg[x - 1][y + 1])
        if x != self.rows - 1 and y != 0:
            neighbours.append(cg[x + 1][y - 1])
        if x != self.rows - 1 and y != self.cols - 1:
            neighbours.append(cg[x + 1][y + 1])
        return neighbours

    def get_next_generation(self) -> Grid:
        next_generation = [[0 for c in range(self.cols)] for c in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                if self.curr_generation[i][j] == 0 and sum(self.get_neighbours((i, j))) == 3:
                    next_generation[i][j] = 1
                elif self.curr_generation[i][j] == 1 and (
                        sum(self.get_neighbours((i, j))) < 2 or sum(self.get_neighbours((i, j))) > 3):
                    next_generation[i][j] = 0
                else:
                    next_generation[i][j] = self.curr_generation[i][j]
        return next_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = list(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations >= self.max_generations:
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.prev_generation[i][j] != self.curr_generation[i][j]:
                    return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as f:
            lines = f.readlines()
            lines = [line for line in lines if (line != "\n") or (line != "")]
            field = [[int(value) for value in line[:-1]] for line in lines]
            y = len(field)
            x = len(field[0])
        game = GameOfLife((y, x))
        game.curr_generation = field
        return game


    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f = open(filename, "w")
        rows = self.rows
        cols = self.cols
        current = self.curr_generation
        for i in range(rows):
            for j in range(cols):
                f.write(str(current[i][j]))
            f.write("\n")

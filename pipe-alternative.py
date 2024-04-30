# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 19:
# 105901 Francisca Almeida
# 106943 José Frazão

pieces = ['FC', 'FE', 'FB', 'FD', 'BC', 'BE', 'BB', 'BD', 'VC', 'VE', 'VB', 'VD', 'LV', 'LH']

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    # Added this method
    def __init__(self, board, n):
        """Construtor da classe Board"""
        self.board = board
        self.n = n

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if row > 0 and row <= self.n and col > 0 and col <= self.n:
            return pieces[self.board[row - 1][col - 1]]
        else:
            return "None"

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        above_valid = (row - 1) > 0 and (row - 1) <= self.n and col > 0 and col <= self.n
        above = pieces[self.board[row - 1][col]] if above_valid else "None"
        below_valid = (row + 1) > 0 and (row + 1) <= self.n and col > 0 and col <= self.n
        below = pieces[self.board[row + 1][col]] if below_valid else "None"
        return (above, below)

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        left_valid = (col - 1) > 0 and (col - 1) <= self.n and row > 0 and row <= self.n
        left = pieces[self.board[row][col - 1]] if left_valid else "None"
        right_valid = (col + 1) > 0 and (col + 1) <= self.n and row > 0 and row <= self.n
        right = pieces[self.board[row][col + 1]] if right_valid else "None"
        return (left, right)

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        board = []
        row = input().split()
        row_indexes = []
        for piece in row:
            row_indexes.append(pieces.index(piece))
        board.append(row_indexes)
        n = len(row)
        for _ in range(n - 1):
            row = input().split()
            row_indexes = []
            for piece in row:
                row_indexes.append(pieces.index(piece))
            board.append(row_indexes)
        return Board(board, n)

    # TODO: outros metodos da classe
    # Added this method
    def __str__(self) -> str:
        """Printa o tabuleiro de jogo"""
        output = ''
        for row in range(self.n):
            for col in range(self.n - 1):
                output += pieces[self.board[row][col]] + '\t'
            output += pieces[self.board[row][col + 1]] + '\n'
        return output[:-1]


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    board = Board.parse_instance()
    pass

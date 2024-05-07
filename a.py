# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 19:
# 105901 Francisca Almeida
# 106943 José Frazão

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
        self.pieces = board
        self.n = n
        self.last = (0, 0)

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if row >= 0 and row < self.n and col >= 0 and col < self.n:
            return self.pieces[row][col]
        else:
            return "None"

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        above_valid = (row - 1) >= 0 and (row - 1) < self.n and col >= 0 and col < self.n
        above = self.pieces[row - 1][col] if above_valid else "None"
        below_valid = (row + 1) >= 0 and (row + 1) < self.n and col >= 0 and col < self.n
        below = self.pieces[row + 1][col] if below_valid else "None"
        return (above, below)

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str): # type: ignore
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        left_valid = (col - 1) >= 0 and (col - 1) < self.n and row >= 0 and row < self.n
        left = self.pieces[row][col - 1] if left_valid else "None"
        right_valid = (col + 1) >= 0 and (col + 1) < self.n and row >= 0 and row < self.n
        right = self.pieces[row][col + 1] if right_valid else "None"
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
        board.append(input().split())
        n = len(board[0])
        for _ in range(n - 1):
            board.append(input().split())
        return Board(board, n)

    # TODO: outros metodos da classe
    # Added this method
    def __str__(self) -> str:
        """Printa o tabuleiro de jogo"""
        output = ''
        for row in range(self.n):
            for col in range(self.n - 1):
                output += self.pieces[row][col] + ' '
            output += self.pieces[row][col + 1] + '\n'
        return output[:-1]


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = PipeManiaState(board)
        # TODO

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO        
        actions = []
        last = state.board.last
        if state.board.last[0] == state.board.n:
            return actions
        actions.append((last[0], last[1], 1))
        actions.append((last[0], last[1], 2))
        actions.append((last[0], last[1], 3))
        state.board.last = (state.board.last[0], state.board.last[1] + 1)
        if state.board.last[1] == state.board.n:
            state.board.last = (state.board.last[0] + 1, 0)
        return actions

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        piece = state.board.pieces[action[0]][action[1]]
        piece_type = piece[0]
        piece_orientation = piece[1]

        if action[2] == 1:
            if piece_orientation == 'C':
                piece_orientation = 'D'
            elif piece_orientation == 'D':
                piece_orientation = 'B'
            elif piece_orientation == 'B':
                piece_orientation = 'E'
            elif piece_orientation == 'E':
                piece_orientation = 'C'
            elif piece_orientation == 'V':
                piece_orientation = 'H'
            elif piece_orientation == 'H':
                piece_orientation = 'V'
        elif action[2] == 2:
            if piece_orientation == 'C':
                piece_orientation = 'B'
            elif piece_orientation == 'D':
                piece_orientation = 'E'
            elif piece_orientation == 'B':
                piece_orientation = 'C'
            elif piece_orientation == 'E':
                piece_orientation = 'D'
        elif action[2] == 3:
            if piece_orientation == 'C':
                piece_orientation = 'E'
            elif piece_orientation == 'E':
                piece_orientation = 'B'
            elif piece_orientation == 'B':
                piece_orientation = 'D'
            elif piece_orientation == 'D':
                piece_orientation = 'C'
            elif piece_orientation == 'V':
                piece_orientation = 'H'
            elif piece_orientation == 'H':
                piece_orientation = 'V'
        

        new_board = state.board.pieces
        new_board[action[0]][action[1]] = piece_type + piece_orientation
        state.board.pieces = new_board
        return state

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO

        ac = {'BC', 'BD', 'BE', 'FC', 'LV', 'VC', 'VD'} # aceita de cima / manda para baixo
        ad = {'BB', 'BC', 'BD', 'FD', 'LH', 'VB', 'VD'} # aceita da direita / manda para a esquerda
        ab = {'BB', 'BD', 'BE', 'FB', 'LV', 'VB', 'VE'} # aceita de baixo / manda para cima
        ae = {'BB', 'BC', 'BE', 'FE', 'LH', 'VC', 'VE'} # aceita da esquerda / manda para a direita
        
        board = state.board.pieces
        n = state.board.n

        for i in range(n):
            for j in range(n):
                piece = board[i][j]
                horizontal = state.board.adjacent_horizontal_values(i ,j)
                vertical = state.board.adjacent_vertical_values(i ,j)
                if piece in ae and horizontal[0] not in ad:
                    return False
                elif piece in ad and horizontal[1] not in ae:
                    return False
                elif piece in ac and vertical[0] not in ab:
                    return False
                elif piece in ab and vertical[1] not in ac:
                    return False
        return True

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

    # Ler grelha do figura 1a:
    board = Board.parse_instance()
    # Criar uma instância de PipeMania:
    problem = PipeMania(board)
    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)
    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board.print(), sep="")
    pass

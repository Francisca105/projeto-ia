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


str_to_piece = {'BC':(True, False, True, True), 'BB':(False, True, True, True),
                'BE':(True, True, True, False), 'BD':(True, True, False, True),
                'FC':(True, False, False, False), 'FB':(False, True, False, False),
                'FE':(False, False, True, False), 'FD':(False, False, False, True),
                'VC':(True, False, True, False), 'VB':(False, True, False, True),
                'VE':(False, True, True, False), 'VD':(True, False, False, True),
                'LV':(True, True, False, False), 'LH':(False, False, True, True),
                None:(False, False, False, False)}

piece_to_str = {(True, False, True, True):'BC', (False, True, True, True):'BB',
                (True, True, True, False):'BE', (True, True, False, True):'BD',
                (True, False, False, False):'FC', (False, True, False, False):'FB',
                (False, False, True, False):'FE', (False, False, False, True):'FD',
                (True, False, True, False):'VC', (False, True, False, True):'VB',
                (False, True, True, False):'VE', (True, False, False, True):'VD',
                (True, True, False, False):'LV', (False, False, True, True):'LH',
                (False, False, False, False): None}

type_to_piece = {'F':[(True, False, False, False), (False, True, False, False),
                      (False, False, True, False), (False, False, False, True)],
                 'B':[(True, False, True, True), (False, True, True, True),
                      (True, True, True, False), (True, True, False, True)],
                 'V':[(True, False, True, False), (False, True, False, True),
                      (False, True, True, False), (True, False, False, True)],
                 'L':[(True, True, False, False), (False, False, True, True)]}


class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self, pieces):
        """Construtor da classe Board."""
        self.pieces = pieces
        self.size = len(pieces)
        self.invalid = False

    def get_type(self, row: int, col: int):
        """Devolve o tipo da peça na respetiva posição do tabuleiro."""
        def aux(piece):
            total = 0
            for direction in piece:
                total = total + 1 if direction else total
            return total

        if 0 <= row < self.size and 0 <= col < self.size:
            piece = self.get_piece(row, col)
            if aux(piece) == 1:
                return 'F'
            elif aux(piece) == 3:
                return 'B'
            elif (piece[0] and piece[1]) or (piece[2] and piece[3]):
                return 'L'
            else:
                return 'V'
        return None

    def get_next_piece(self):
        for possibilities_level in self.remaining_pieces:
                for piece in possibilities_level:
                    return piece
        return None

    def remove_piece(self, row, col):
        for possibilities_level in self.remaining_pieces:
                possibilities_level.discard((row, col))

    def remove_possibility(self, row, col):
        try:
            self.possibilities.pop((row, col))
        except KeyError:
            pass

    def pieces_remaining(self):
        return len(self.remaining_pieces[0]) + len(self.remaining_pieces[1])+ len(self.remaining_pieces[2])

    def get_piece(self, row: int, col: int):
        """Devolve a peça na respetiva posição do tabuleiro."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.pieces[row][col]
        return (False, False, False, False)

    def initial_set_piece(self, row, col, piece, cond):
        pieces = self.pieces
        new_row = pieces[row][:col] + (piece,) + pieces[row][col + 1 :]
        new_pieces = pieces[:row] + (new_row,) + pieces[row + 1 :]
        self.pieces = new_pieces
        self.locked_pieces.add((row, col))
        if cond:
            self.remove_possibility(row, col)
            self.remove_piece(row, col)
            self.update_adjacent(row, col)

    def set_piece(self, row, col, piece):
        pieces = self.pieces
        new_row = pieces[row][:col] + (piece,) + pieces[row][col + 1 :]
        new_pieces = pieces[:row] + (new_row,) + pieces[row + 1 :]
        new_board = Board(new_pieces)

        new_board.locked_pieces = self.locked_pieces.copy()
        new_board.locked_pieces.add((row, col))

        new_board.remaining_pieces = [set(e) for e in self.remaining_pieces]
        new_board.remove_piece(row, col)

        new_board.possibilities = self.possibilities.copy()
        new_board.update_adjacent(row, col)

        return new_board

    def update_adjacent(self, row, col):
        adjacent, direction = self.adjacent_coords(row, col), 0
        piece = self.get_piece(row, col)
        for (adj_row, adj_col) in adjacent:
            if (adj_row, adj_col) not in self.locked_pieces:
                inverse_direction = direction + 1 if not direction % 2 else direction - 1
                try:
                    other_possibilities = [e for e in self.possibilities[(adj_row, adj_col)]]
                except KeyError:
                    direction += 1
                    continue
                for possibility in other_possibilities:
                    if possibility[inverse_direction] != piece[direction]:
                        self.possibilities[(adj_row, adj_col)].remove(possibility)
                if len(self.possibilities[(adj_row, adj_col)]) == 1:
                    self.initial_set_piece(adj_row, adj_col, self.possibilities[(adj_row, adj_col)][0], True)
                elif len(self.possibilities[(adj_row, adj_col)]) == 0:
                    self.invalid = True
                    return
            direction += 1

    def update_own_possibility(self, row, col):
        adjacent, direction = self.adjacent_coords(row, col), 0
        possibilities = [e for e in self.possibilities[(row, col)]]
        for (adj_row, adj_col) in adjacent:
            if (adj_row, adj_col) in self.locked_pieces:
                inverse_direction = direction + 1 if not direction % 2 else direction - 1
                other = self.get_piece(adj_row, adj_col)
                for possibility in possibilities:
                    if possibility[direction] != other[inverse_direction]:
                        try:
                            self.possibilities[(row, col)].remove(possibility)
                        except ValueError:
                            pass
                if len(self.possibilities[(row, col)]) == 1:
                    self.initial_set_piece(row, col, self.possibilities[(row, col)][0], True)
                    return
                elif len(self.possibilities[(row, col)]) == 0:
                    self.invalid = True
                    return
            direction += 1

    def adjacent_vertical_pieces(self, row: int, col: int):
        """Devolve as peças imediatamente acima e abaixo,
        respectivamente."""
        return (self.get_piece(row - 1, col), self.get_piece(row + 1, col))

    def adjacent_horizontal_pieces(self, row: int, col: int):
        """Devolve as peças imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_piece(row, col - 1), self.get_piece(row, col + 1))

    def adjacent_vertical_coords(self, row: int, col: int):
        """Devolve as coordenadas imediatamente acima e abaixo,
        respectivamente."""
        above = (-1, -1) if row + 1 < 0 else row + 1
        below = (-1, -1) if row - 1 < 0 else row - 1
        return ((above, col), (below, col))

    def adjacent_horizontal_coords(self, row: int, col: int):
        """Devolve as coordenadas imediatamente à esquerda e à direita,
        respectivamente."""
        left = (-1, -1) if col + 1 < 0 else col + 1
        right = (-1, -1) if col - 1 < 0 else col - 1
        return ((row, left), (row, right))

    def adjacent_coords(self, row: int, col: int):
        """Devolve as peças imediatamente acima, abaixo, à esquerda e à direita,
        respectivamente."""
        above = (-1, -1) if row - 1 < 0 else (row - 1, col)
        below = (-1, -1) if row + 1 < 0 else (row + 1, col)
        left = (-1, -1) if col - 1 < 0 else (row, col - 1)
        right = (-1, -1) if col + 1 < 0 else (row, col + 1)
        return (above, below, left, right)

    def compute_initial(self):
        self.locked_pieces = {(-1, -1)}
        self.possibilities = {}
        self.remaining_pieces = [set(), set(), set()]

        self.check_corners()
        self.check_edges()

        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in self.locked_pieces:
                    if (row, col) not in self.possibilities:
                        self.possibilities.update({(row, col):[e for e in type_to_piece[self.get_type(row, col)]]}) # cursed mas acho que tem que ser assim
                    self.remaining_pieces[len(self.possibilities[(row, col)]) - 2].add((row, col))

        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in self.locked_pieces:
                    self.update_own_possibility(row, col)
        # TODO: propagar restrições de possibilidades

        return self

    def check_corners(self):
        """Verifica se é possível bloquear as peças dos cantos logo no início."""
        size = self.size - 1
        if self.get_type(0, 0) == 'V':
            self.initial_set_piece(0, 0, (False, True, False, True), False)
        else:
            self.possibilities.update({(0, 0):[(False, True, False, False), (False, False, False, True)]})
        if self.get_type(0, size) == 'V':
            self.initial_set_piece(0, size, (False, True, True, False), False)
        else:
            self.possibilities.update({(0, size):[(False, True, False, False), (False, False, True, False)]})
        if self.get_type(size, 0) == 'V':
            self.initial_set_piece(size, 0, (True, False, False, True), False)
        else:
            self.possibilities.update({(size, 0):[(True, False, False, False), (False, False, False, True)]})
        if self.get_type(size, size) == 'V':
            self.initial_set_piece(size, size, (True, False, True, False), False)
        else:
            self.possibilities.update({(size, size):[(True, False, False, False), (False, False, True, False)]})

    def check_edges(self):
        """Verifica se é possível bloquear as peças das bordas logo no início."""
        size = self.size - 1
        for _ in range(1,size):
            piece_type = self.get_type(0, _)
            if piece_type == 'B' or piece_type == 'L':
                if piece_type == 'B':
                    self.initial_set_piece(0, _, (False, True, True, True), False)
                else:
                    self.initial_set_piece(0, _, (False, False, True, True), False)
            else:
                if piece_type == 'F':
                    self.possibilities.update({(0, _):[(False, True, False, False), (False, False, True, False), (False, False, False, True)]})
                else:
                    self.possibilities.update({(0, _):[(False, True, True, False), (False, True, False, True)]})
            piece_type = self.get_type(_, 0)
            if piece_type == 'B' or piece_type == 'L':
                if piece_type == 'B':
                    self.initial_set_piece(_, 0, (True, True, False, True), False)
                else:
                    self.initial_set_piece(_, 0, (True, True, False, False), False)
            else:
                if piece_type == 'F':
                    self.possibilities.update({(_, 0):[(True, False, False, False), (False, True, False, False), (False, False, False, True)]})
                else:
                    self.possibilities.update({(_, 0):[(True, False, False, True), (False, True, False, True)]})
            piece_type = self.get_type(size, _)
            if piece_type == 'B' or piece_type == 'L':
                if piece_type == 'B':
                    self.initial_set_piece(size, _, (True, False, True, True), False)
                else:
                    self.initial_set_piece(size, _, (False, False, True, True), False)
            else:
                if piece_type == 'F':
                    self.possibilities.update({(size, _):[(True, False, False, False), (False, False, True, False), (False, False, False, True)]})
                else:
                    self.possibilities.update({(size, _):[(True, False, True, False), (True, False, False, True)]})
            piece_type = self.get_type(_, size)
            if piece_type == 'B' or piece_type == 'L':
                if piece_type == 'B':
                    self.initial_set_piece(_, size, (True, True, True, False), False)
                else:
                    self.initial_set_piece(_, size, (True, True, False, False), False)
            else:
                if piece_type == 'F':
                    self.possibilities.update({(_, size):[(True, False, False, False), (False, True, False, False), (False, False, True, False)]})
                else:
                    self.possibilities.update({(_, size):[(True, False, True, False), (False, True, True, False)]})

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
        input_grid = [tuple(input().strip().split())]
        for _ in range(len(input_grid[0]) - 1):
            input_grid.append(tuple(input().strip().split()))
        pieces = []
        for row in input_grid:
            new_row = ()
            for piece in row:
                new_row += str_to_piece[piece],
            pieces.append(new_row)
        return Board(tuple(pieces)).compute_initial()

    def __str__(self):
        """Devolve a representação do tabuleiro como uma string."""
        output = ''
        for row in range(self.size):
            for col in range(self.size):
                if col == self.size - 1:
                    output += piece_to_str[self.pieces[row][col]]
                else:
                    output += piece_to_str[self.pieces[row][col]] + '\t'
            output += '\n'
        return output


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = PipeManiaState(board)
        super().__init__(state)

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        if state.board.invalid or not state.board.pieces_remaining():
            return []
        (row, col) = state.board.get_next_piece()
        possibilities = state.board.possibilities[(row, col)]
        return map(lambda x: (row, col, x), possibilities)

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        (row, col, possibility) = action
        return PipeManiaState(state.board.set_piece(row, col, possibility))

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return state.board.get_next_piece() == None

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""


if __name__ == "__main__":
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    board = Board.parse_instance()
    problem = PipeMania(board)
    # print(problem.initial.board.remaining_pieces)
    # print(problem.initial.board, end='')
    goal_node = depth_first_tree_search(problem)
    print(goal_node.state.board, end='')
    pass
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

pieces_dict = {'BC':(1, 0, 1, 1), 'BB':(0, 1, 1, 1), 'BE':(1, 1, 1, 0), 'BD':(1, 1, 0, 1),
             'FC':(1, 0, 0, 0), 'FB':(0, 1, 0, 0), 'FE':(0, 0, 1, 0), 'FD':(0, 0, 0, 1),
             'VC':(1, 0, 1, 0), 'VB':(0, 1, 0, 1), 'VE':(0, 1, 1, 0), 'VD':(1, 0, 1, 0),
             'LV':(1, 1, 0, 0), 'LH':(0, 0, 1, 1)}


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

    def compute_initial(self):
        """Define o estado inicial de um tabuleiro."""
        size = self.size - 1
        locked_pieces = set(None)
        remaining_pieces = []

        if self.get_type(0, 0) == 'V':
            self.set_piece(0, 0, 'B')
            locked_pieces.add((0, 0))
        if self.get_type(0, size) == 'V':
            self.set_piece(0, size, 'E')
            locked_pieces.add((0, size))
        if self.get_type(size, 0) == 'V':
            self.set_piece(size, 0, 'D')
            locked_pieces.add((size, 0))
        if self.get_type(size, size) == 'V':
            self.set_piece(size, size, 'C')
            locked_pieces.add((size, size))

        for _ in range(1,size):
            piece_type = self.get_type(0, _)
            if piece_type == 'B' or piece_type == 'L':
                if piece_type == 'B':
                    self.set_piece(0, _, 'B')
                else:
                    self.set_piece(0, _, 'H')
                locked_pieces.add((0, _))
            piece_type = self.get_type(_, 0)
            if piece_type == 'B' or piece_type == 'L':
                if piece_type == 'B':
                    self.set_piece(_, 0, 'D')
                else:
                    self.set_piece(_, 0, 'V')
                locked_pieces.add((_, 0))
            piece_type = self.get_type(size, _)
            if piece_type == 'B' or piece_type == 'L':
                if piece_type == 'B':
                    self.set_piece(size, _, 'C')
                else:
                    self.set_piece(size, _, 'H')
                locked_pieces.add((size, _))
            piece_type = self.get_type(_, size)
            if piece_type == 'B' or piece_type == 'L':
                if piece_type == 'B':
                    self.set_piece(_, size, 'E')
                else:
                    self.set_piece(_, size, 'V')
                locked_pieces.add((_, size))

        
        self.locked_pieces = locked_pieces
        self.remaining_pieces = remaining_pieces

        return self
    
    def get_next_piece(self):
        """Devolve a próxima peça a ser rodada."""
        try:
            return self.remaining_pieces[0]
        except IndexError:
            return None

    def get_piece(self, row: int, col: int) -> str:
        """Devolve a peça na respetiva posição do tabuleiro."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.pieces[row][col]
        return None
    
    def get_type(self, row: int, col: int) -> str:
        """Devolve o tipo da peça na respetiva posição do tabuleiro."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.pieces[row][col][0]
        return None
    
    def get_orientation(self, row: int, col: int) -> str:
        """Devolve a orientação da peça na respetiva posição do tabuleiro."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.pieces[row][col][1]
        return None

    def adjacent_vertical_pieces(self, row: int, col: int) -> tuple[str, str]:
        """Devolve as peças imediatamente acima e abaixo,
        respectivamente."""
        return (self.get_piece(row - 1, col), self.get_piece(row + 1, col))

    def adjacent_horizontal_pieces(self, row: int, col: int) -> tuple[str, str]:
        """Devolve as peças imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_piece(row, col - 1), self.get_piece(row, col + 1))
    
    def set_piece(self, row: int, col: int, orientation: str):
        """Atualiza a peça na respetiva posição do tabuleiro."""
        pieces = self.pieces
        piece_type = pieces[row][col][0]
        new_row = pieces[row][:col] + (piece_type + orientation,) + pieces[row][col + 1 :]
        new_pieces = pieces[:row] + (new_row,) + pieces[row + 1 :]
        self.pieces = new_pieces       
    
    def new_board(self, row: int, col: int, orientation: str):
        """Cria um novo tabuleiro mudando a orientação da peça na posição dada."""
        new_row = ()
        for i in range(col):
            new_row += (self.pieces[row][i],)
        new_row += (self.pieces[row][col][0] + orientation,)
        for i in range(self.size - col - 1):
            new_row += (self.pieces[row][col + i + 1],)

        new_pieces = ()
        for i in range(row):
            new_pieces += (self.pieces[i],)
        new_pieces += (new_row,)
        for i in range(self.size - row - 1):
            new_pieces += (self.pieces[row + i + 1],)
        
        new_board = Board(new_pieces)
        new_board.remaining_pieces = self.remaining_pieces[1:]
        return new_board

    def get_corner_possibilities(self, row: int, col: int) -> list[str]:
        """Devolve as possíveis peças para a dada peça do canto (quando há mais que uma possibilidade)."""
        if row == 0:
            if col == 0:
                return [(row, col, 'FB'), (row, col, 'FD')]
            else:
                return [(row, col, 'FB'), (row, col, 'FE')]
        elif row == self.size - 1:
            if col == 0:
                return [(row, col, 'FC'), (row, col, 'FD')]
            else:
                return [(row, col, 'FC'), (row, col, 'FE')]

    def get_edge_possibilites(self, row: int, col: int) -> list[str]:
        """Devolve as possíveis peças para a dada peça da borda (quando há mais que uma possibilidade)."""
        if row == 0:
            return [(row, col, 'VB'), (row, col, 'VE'), (row, col, 'FB'), (row, col, 'FD'), (row, col, 'FE')]
        elif col == self.size - 1:
            return [(row, col, 'VC'), (row, col, 'VE'), (row, col, 'FB'), (row, col, 'FC'), (row, col, 'FE')]
        elif row == self.size - 1:
            return [(row, col, 'VC'), (row, col, 'VD'), (row, col, 'FC'), (row, col, 'FD'), (row, col, 'FE')]
        else:
            return [(row, col, 'VB'), (row, col, 'VD'), (row, col, 'FB'), (row, col, 'FC'), (row, col, 'FD')]

    def get_center_possibilities(self, row: int, col: int) -> list[str]:
        """Devolve as possíveis peças para a dada peça do centro"""
        piece = self.get_piece(row, col)
        if piece[1] == 'L':
            possibilities = ['H', 'V']
        else:
            possibilities = ['C', 'B', 'E', 'D']
        vertical = self.adjacent_vertical_pieces(row, col)
        horizontal = self.adjacent_horizontal_pieces(row, col)


    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""

        input_grid = [tuple(input().strip().split())]
        for _ in range(len(input_grid[0]) - 1):
            input_grid.append(tuple(input().strip().split()))

        grid = []
        for row in input_grid:
            new_row = ()
            for piece in row:
                new_row += (pieces_dict[piece],)
            grid.append(new_row)

        return Board(tuple(grid)).compute_initial()

    def __str__(self) -> str:
        """Devolve a representação do tabuleiro como uma string."""

        output = ''
        for row in range(self.size):
            for col in range(self.size):
                output += pieces_dict[self.pieces[row][col]] + '\t'
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
        piece = state.board.get_next_piece()
        if piece == None:
            return []
        actions = []
        if state.board.get_type(piece[0], piece[1]) == 'L':
            actions.append(piece+('H',))
            actions.append(piece+('V',))
        else:
            actions.append(piece+('C',))
            actions.append(piece+('D',))
            actions.append(piece+('B',))
            actions.append(piece+('E',))
        return actions


    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        return PipeManiaState(state.board.new_board(action[0], action[1], action[2]))

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        ac = {'BC', 'BD', 'BE', 'FC', 'LV', 'VC', 'VD'} # aceita de cima / manda para baixo
        ad = {'BB', 'BC', 'BD', 'FD', 'LH', 'VB', 'VD'} # aceita da direita / manda para a esquerda
        ab = {'BB', 'BD', 'BE', 'FB', 'LV', 'VB', 'VE'} # aceita de baixo / manda para cima
        ae = {'BB', 'BC', 'BE', 'FE', 'LH', 'VC', 'VE'} # aceita da esquerda / manda para a direita

        pieces = state.board.pieces
        size = state.board.size
        rows, cols = [False for _ in range(size)], [False for _ in range(size)]

        for i in range(size):
            for j in range(size):
                value = pieces[i][j]
                horizontal = state.board.adjacent_horizontal_pieces(i ,j)
                vertical = state.board.adjacent_vertical_pieces(i ,j)
                if value in ae:
                    if horizontal[0] not in ad:
                        return False
                    cols[j] = True
                if value in ad:
                    if horizontal[1] not in ae:
                        return False
                    cols[j] = True
                if value in ac:
                    if vertical[0] not in ab:
                        return False
                    rows[i] = True
                if value in ab:
                    if vertical[1] not in ac:
                        return False
                    rows[i] = True

        for i in range(size):
            if (not rows[i] and not cols[i]):
                return False
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass


if __name__ == "__main__":
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    # board = Board.parse_instance()
    # problem = PipeMania(board)
    # goal_node = depth_first_tree_search(problem)
    # print(goal_node.state.board, end='')
    pass
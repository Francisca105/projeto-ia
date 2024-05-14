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


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self, pieces):
        """Construtor da classe Board."""
        self.pieces = pieces
        self.size = len(pieces)

    def compute_initial(self):
        """Define o estado inicial de um tabuleiro."""
        size = self.size - 1
        locked_pieces = set()
        remaining_pieces = []

        for i in range(self.size):
            for j in range(self.size):
                piece = self.get_type(i, j)
                if (i, j) == (0, 0) and piece == 'V':
                    self.set_piece1(i, j, 'B')
                    locked_pieces.add((i, j))
                    continue
                elif (i, j) == (0, size) and piece == 'V':
                    self.set_piece1(i, j, 'E')
                    locked_pieces.add((i, j))
                    continue
                elif (i, j) == (size, 0) and piece == 'V':
                    self.set_piece1(i, j, 'D')
                    locked_pieces.add((i, j))
                    continue
                elif (i, j) == (0, size) and piece == 'V':
                    self.set_piece1(i, j, 'C')
                    locked_pieces.add((i, j))
                    continue
                elif i == 0 and 0 < j < size:
                    if piece == 'B':
                        self.set_piece1(i, j, 'B')
                        locked_pieces.add((i, j))
                        continue
                    elif piece == 'L':
                        self.set_piece1(i, j, 'H')
                        locked_pieces.add((i, j))
                        continue
                elif j == size and 0 < i < size:
                    if piece == 'B':
                        self.set_piece1(i, j, 'E')
                        locked_pieces.add((i, j))
                        continue
                    elif piece == 'L':
                        self.set_piece1(i, j, 'V')
                        locked_pieces.add((i, j))
                        continue
                elif i == size and 0 < j < size:
                    if piece == 'B':
                        self.set_piece1(i, j, 'C')
                        locked_pieces.add((i, j))
                        continue
                    elif piece == 'L':
                        self.set_piece1(i, j, 'H')
                        locked_pieces.add((i, j))
                        continue
                elif j == 0 and 0 < i < size:
                    if piece == 'B':
                        self.set_piece1(i, j, 'D')
                        locked_pieces.add((i, j))
                        continue
                    elif piece == 'L':
                        self.set_piece1(i, j, 'V')
                        locked_pieces.add((i, j))
                        continue
                remaining_pieces.append((i, j))
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
    
    def set_piece1(self, row: int, col: int, orientation: str):
        """Atualiza a peça na respetiva posição do tabuleiro."""
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

        self.pieces = new_pieces       
    
    def set_piece(self, row: int, col: int, orientation: str):
        """Atualiza a peça na respetiva posição do tabuleiro."""
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

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
        pieces = []
        pieces.append(tuple(input().strip().split()))
        for _ in range(len(pieces[0]) - 1):
            pieces.append(tuple(input().strip().split()))
        return Board(tuple(pieces)).compute_initial()

    # TODO: outros metodos da classe

    def __str__(self) -> str:
        """Printa o tabuleiro de jogo"""
        output = ''
        for row in range(self.size):
            for col in range(self.size - 1):
                output += self.pieces[row][col] + '\t'
            output += self.pieces[row][col + 1] + '\n'
        return output[:-1]


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
        return PipeManiaState(state.board.set_piece(action[0], action[1], action[2]))

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

    # Ler grelha do figura 1a:
    board = Board.parse_instance()
    # Criar uma instância de PipeMania:
    problem = PipeMania(board)
    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)
    # Verificar se foi atingida a solução
    print(goal_node.state.board)
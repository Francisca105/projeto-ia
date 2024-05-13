# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

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

    def __init__(self, pieces):
        """Construtor da classe Board."""
        self.pieces = pieces
        self.size = len(pieces)

    def compute_initial(self):
        """Define o estado inicial de um tabuleiro."""
        self.remaining_pieces = []
        for i in range(self.size):
            for j in range(self.size):
                self.remaining_pieces.append((i, j))
        return self
    
    def get_next_piece(self):
        try:
            return self.remaining_pieces.pop()
        except IndexError:
            return None

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.pieces[row][col]
        return None
    
    def set_value(self, row: int, col: int, piece: str):
        """Atualiza o valor na respetiva posição do tabuleiro."""
        if 0 <= row < self.size and 0 <= col < self.size:
            self.pieces[row][col] = piece
    
    def get_piece(self, row: int, col: int) -> str:
        """Devolve a peça na respetiva posição do tabuleiro."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.pieces[row][col][0]
        return None
    
    def get_orientation(self, row: int, col: int) -> str:
        """Devolve a orientação na respetiva posição do tabuleiro."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.pieces[row][col][1]
        return None

    def adjacent_vertical_values(self, row: int, col: int) -> tuple[str, str]:
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (self.get_value(row - 1, col), self.get_value(row + 1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> tuple[str, str]:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_value(row, col - 1), self.get_value(row, col + 1))

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
        pieces = []
        pieces.append(list(input().strip().split()))
        for _ in range(len(pieces[0]) - 1):
            pieces.append(list(input().strip().split()))
        return Board(pieces).compute_initial()

    # TODO: outros metodos da classe

    def __str__(self) -> str:
        """Printa o tabuleiro de jogo"""
        output = ''
        for row in range(self.size):
            for col in range(self.size - 1):
                output += self.pieces[row][col] + ' '
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
        if piece[0] == 'L':
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
        board = state.board.pieces.copy()
        board[action[0]][action[1]] = board[action[0]][action[1]][0] + action[2]
        remaining_pieces = state.board.remaining_pieces.copy()
        ret = Board(board)
        ret.remaining_pieces = remaining_pieces
        return PipeManiaState(ret)

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
                horizontal = state.board.adjacent_horizontal_values(i ,j)
                vertical = state.board.adjacent_vertical_values(i ,j)
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
    print(goal_node.state.board)
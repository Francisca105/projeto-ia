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

                    # up  , down , left, right
str_to_piece = {'BC':(True, False, True, True), 'BB':(False, True, True, True),
                'BE':(True, True, True, False), 'BD':(True, True, False, True),
                'FC':(True, False, False, False), 'FB':(False, True, False, False),
                'FE':(False, False, True, False), 'FD':(False, False, False, True),
                'VC':(True, False, True, False), 'VB':(False, True, False, True),
                'VE':(False, True, True, False), 'VD':(True, False, False, True),
                'LV':(True, True, False, False), 'LH':(False, False, True, True)}

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


class Node:
    """Representation of a double linked list node."""

    def __init__(self, data, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev


class Queue:
    """Representation of a FIFO using a double linked list."""

    def __init__(self, head_data):
        self.head = Node(head_data)
        self.tail = self.head

    def append(self, data):
        """Appends an item at the end of the queue."""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def pop(self):
        """Pops the first item of the queue."""
        first = self.head
        if self.head.next is not None:
            self.head = self.head.next
            self.head.prev = None
        else:
            self.head = None
            self.tail = None
        return first.data

    def is_empty(self):
        """Returns True if the queue is empty, False otherwise."""
        return self.head is None

class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


class Board:
    """Internal representation of a PipeMania board."""

    def __init__(self, pieces):
        self.pieces = pieces
        self.size = len(pieces)
        self.invalid = False

    def get_size(self):
        """Returns the board size."""
        return self.size

    def get_type(self, row: int, col: int):
        """Returns the type of the given piece."""
        def num_connections(piece) -> int:
            """Returns the number of connections between the piece and its adjacent ones."""
            total = 0
            for direction in piece:
                total = total + 1 if direction else total
            return total

        if 0 <= row < self.size and 0 <= col < self.size:
            piece = self.get_piece(row, col)
            if num_connections(piece) == 1:
                return 'F'
            elif num_connections(piece) == 3:
                return 'B'
            elif (piece[0] and piece[1]) or (piece[2] and piece[3]):
                return 'L'
            else:
                return 'V'
        return None

    def get_next_piece(self):
        """Returns the next piece to be locked."""
        for possibilities_level in self.remaining_pieces:
                for piece in possibilities_level:
                    return piece
        return None

    def remove_piece(self, row: int, col: int):
        """Removes the given piece from the list of remaining ones."""
        for possibilities_level in self.remaining_pieces:
                possibilities_level.discard((row, col))

    def remove_possibility(self, row:int, col: int):
        """Removes the given piece possibilities."""
        try:
            self.possibilities.pop((row, col))
        except KeyError:
            pass

    def pieces_remaining(self) -> int:
        """Returns the number of remaining pieces to be locked."""
        return len(self.remaining_pieces[0]) + len(self.remaining_pieces[1])+ len(self.remaining_pieces[2])

    def get_piece(self, row: int, col: int):
        """Returns the piece in the given coords."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.pieces[row][col]
        return (False, False, False, False)

    def initial_set_piece(self, row, col, piece, condition):
        """Locks the given piece in its place and updates the board."""
        if self.invalid:
            return

        pieces = self.pieces
        new_row = pieces[row][:col] + (piece,) + pieces[row][col + 1 :]
        new_pieces = pieces[:row] + (new_row,) + pieces[row + 1 :]
        self.pieces = new_pieces
        self.locked_pieces.add((row, col))

        if condition:
            self.remove_possibility(row, col)
            self.remove_piece(row, col)
            self.update_adjacent(row, col)

    def set_piece(self, row, col, piece):
        """Creates a new board and lock the given piece in the given coordinates."""
        pieces = self.pieces
        new_row = pieces[row][:col] + (piece,) + pieces[row][col + 1 :]
        new_pieces = pieces[:row] + (new_row,) + pieces[row + 1 :]
        new_board = Board(new_pieces)

        new_board.locked_pieces = self.locked_pieces.copy()
        new_board.locked_pieces.add((row, col))

        new_board.remaining_pieces = [set(e) for e in self.remaining_pieces]
        new_board.remove_piece(row, col)

        new_board.possibilities = {}
        for e in self.possibilities.keys():
            new_board.possibilities.update({e:[x for x in self.possibilities[e]]})
        new_board.remove_possibility(row, col)
        new_board.update_adjacent(row, col)

        return new_board

    def update_adjacent(self, row, col):
        """Updates the adjacent pieces knowing that the given piece was locked.
        If possible, it will also lock the adjacent pieces that can be locked.
        It can also detect if the board is invalid."""
        adjacent, direction = self.adjacent_coords(row, col), 0
        piece = self.get_piece(row, col)
        for (adj_row, adj_col) in adjacent:
            inverse_direction = direction + 1 if not direction % 2 else direction - 1
            if (adj_row, adj_col) not in self.locked_pieces:
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
                else:
                    new_possibilities = self.possibilities[(adj_row, adj_col)]
                    self.remove_piece(adj_row, adj_col)
                    self.remaining_pieces[len(new_possibilities) - 2].add((adj_row, adj_col))
            else:
                other = self.get_piece(adj_row, adj_col)
                if other[inverse_direction] != piece[direction]:
                    self.invalid = True
                    return
            direction += 1

    def update_own_possibility(self, row, col):
        """Updates the given piece possibilities given its adjacent pieces.
        If possible, it will also lock the piece. It can also detect if the board is invalid."""
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
                            continue

                if len(self.possibilities[(row, col)]) == 1:
                    self.initial_set_piece(row, col, self.possibilities[(row, col)][0], True)
                    return
                elif len(self.possibilities[(row, col)]) == 0:
                    self.invalid = True
                    return
                
                new_possibilities = self.possibilities[(row, col)]
                self.remove_piece(row, col)
                self.remaining_pieces[len(new_possibilities) - 2].add((row, col))
            direction += 1

    def adjacent_vertical_pieces(self, row: int, col: int):
        """Returns the pieces immediately above and below the given piece."""
        return (self.get_piece(row - 1, col), self.get_piece(row + 1, col))

    def adjacent_horizontal_pieces(self, row: int, col: int):
        """Returns the pieces immediately on the left and on the right of the given piece."""
        return (self.get_piece(row, col - 1), self.get_piece(row, col + 1))

    def adjacent_coords(self, row: int, col: int):
        """Returns the coordinates immediately above, below, on the left and on the
        right of the given piece."""
        above = (-1, -1) if row - 1 < 0 else (row - 1, col)
        below = (-1, -1) if row + 1 < 0 else (row + 1, col)
        left = (-1, -1) if col - 1 < 0 else (row, col - 1)
        right = (-1, -1) if col + 1 < 0 else (row, col + 1)
        return (above, below, left, right)

    def compute_initial(self):
        """Computes the initial state of the board."""
        self.locked_pieces = {(-1, -1)}
        self.possibilities = {}
        self.remaining_pieces = [set(), set(), set()]

        self.lock_corners()
        self.lock_edges()

        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in self.locked_pieces:
                    if (row, col) not in self.possibilities:
                        self.possibilities.update({(row, col):[e for e in type_to_piece[self.get_type(row, col)]]})
                    self.remaining_pieces[len(self.possibilities[(row, col)]) - 2].add((row, col))

        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in self.locked_pieces:
                    self.update_own_possibility(row, col)

        return self

    def lock_corners(self):
        """Locks all the corner pieces that can be locked at the start."""
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

    def lock_edges(self):
        """Locks all the edge pieces that can be locked at the start."""
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

    def get_adjacent(self, row, col):
        """Returns all the adjacent coordinates that connect with the given piece."""
        piece = self.get_piece(row, col)
        adjacent = self.adjacent_coords(row, col)
        ret = []
        for i in range(4):
            if piece[i]:
                ret.append(adjacent[i])
        return ret

    def check_goal(self) -> bool:
        """Returns True if the current board is the solution, False otherwise.
        It uses a BFS to check if all the pieces are connected."""
        visited = [[False] * self.size for _ in range(self.size)]
        visited[0][0] = True
        queue = Queue((0, 0))

        while not queue.is_empty():
            (current_row, current_col) = queue.pop()
            for (row, col) in self.get_adjacent(current_row, current_col):
                if not visited[row][col]:
                    visited[row][col] = True
                    queue.append((row, col))

        for i in range(self.size):
            for j in range(self.size):
                if not visited[i][j]:
                    return False

        return True

    def num_locked_pieces(self):
        """Returns the number of locked pieces."""
        return len(self.locked_pieces)

    @staticmethod
    def parse_instance():
        """Reads the text from stdin that is passed as an argument and returns
        an instance of the Board class.."""
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
        """Returns the board representation as a string."""
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
        """The constructor specifies the initial state."""
        state = PipeManiaState(board)
        super().__init__(state)

    def actions(self, state: PipeManiaState):
        """Returns a list of actions that can be executed from the state passed as an argument."""
        if state.board.invalid or not state.board.pieces_remaining():
            return []
        piece = state.board.get_next_piece()
        possibilities = state.board.possibilities[(piece[0], piece[1])]
        return [(piece[0], piece[1], e) for e in possibilities]

    def result(self, state: PipeManiaState, action):
        """Returns the state resulting from executing the 'action' on the 'state' passed as an argument.
        The action to be executed must be one of those present in the list obtained by executing self.actions(state)."""
        (row, col, possibility) = action
        return PipeManiaState(state.board.set_piece(row, col, possibility))

    def goal_test(self, state: PipeManiaState):
        """Returns True if and only if the state passed as an argument is a goal state.
        It must verify if all positions on the board are filled according to the problem's rules."""
        return state.board.get_next_piece() is None and state.board.check_goal()

    def h(self, node: Node):
        """Heuristic function used for A* search."""
        return node.state.board.get_size()**2 - node.state.board.num_locked_pieces()


if __name__ == "__main__":
    # Read the file from standard input,
    # Use a search technique to solve the instance,
    # Extract the solution from the resulting node,
    # Print to standard output in the indicated format.

    board = Board.parse_instance()
    problem = PipeMania(board)
    goal_node = depth_first_tree_search(problem)
    print(goal_node.state.board, end='')

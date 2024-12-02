# Grupo 25:
# 106340 Francisco Monteiro Paúl de Sousa Uva
# 107482 Pedro Henrique Ventura dos Santos Pais

from copy import deepcopy
import sys
from search import (
    Problem,
    Node,
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
    def __init__(self, board, next_piece=(0, 0)):
        self.board = board
        self.next_piece = next_piece

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (self[row - 1][col], self[row + 1][col])

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self[row][col - 1], self[row][col + 1])

    def size(self) -> int:
        """Devolve o tamanho do tabuleiro."""
        return len(self.board)

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
        for line in sys.stdin:
            row = line.strip().split('\t')
            board.append([[cell, True] for cell in row])
        return Board(board)

    def print_board(self):
        """Imprime o tabuleiro."""
        string = ''
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                string += self.board[i][j][0] + '\t'
            string = string[:-1]
            string += '\n'
        string = string[:-1] 
        print(string)


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        super().__init__(PipeManiaState(board))

    def reduce_actions(self, state: PipeManiaState, board_size: int, piece: str, coords: tuple):
        row, col = coords
        pieces = []
        up_wall, down_wall, left_wall, right_wall = False, False, False, False
        up_connected, down_connected, left_connected, right_connected = False, False, False, False
        if row != 0: up_bool_value, up_value = state.board.get_value(row-1, col)
        else: up_bool_value, up_value = None, None
        if row != board_size-1: down_bool_value, down_value = state.board.get_value(row+1, col)
        else: down_bool_value, down_value = None, None
        if col != 0: left_bool_value, left_value = state.board.get_value(row, col-1)
        else: left_bool_value, left_value = None, None
        if col != board_size-1: right_bool_value, right_value = state.board.get_value(row, col+1)
        else: right_bool_value, right_value = None, None
        
        if piece in {'FC', 'FB', 'FE', 'FD'}:
            pieces = ['FC', 'FB', 'FE', 'FD']
            if row != 0:
                if (up_bool_value == False and up_value in {'FC', 'FB', 'FE', 'FD', 'BC', 'VC', 'VD', 'LH'}) or up_value in {'FC', 'FB', 'FE', 'FD'}:
                    up_wall = True
                elif up_bool_value == False and up_value in {'BB', 'BE', 'BD', 'VB', 'VE', 'LV'}:
                    up_connected = True
            else:
                up_wall = True
            if row != board_size-1:
                if (down_bool_value == False and down_value in {'FC', 'FB', 'FE', 'FD', 'BB', 'VB', 'VE', 'LH'}) or down_value in {'FC', 'FB', 'FE', 'FD'}:
                    down_wall = True
                elif down_bool_value == False and down_value in {'BC', 'BE', 'BD', 'VC', 'VD', 'LV'}:
                    down_connected = True
            else:
                down_wall = True
            if col != 0:
                if (left_bool_value == False and left_value in {'FC', 'FB', 'FE', 'FD', 'BE', 'VC', 'VE', 'LV'}) or left_value in {'FC', 'FB', 'FE', 'FD'}:
                    left_wall = True
                elif left_bool_value == False and left_value in {'BC', 'BB', 'BD', 'VB', 'VD', 'LH'}:
                    left_connected = True
            else:
                left_wall = True
            if col != board_size-1:
                if (right_bool_value == False and right_value in {'FC', 'FB', 'FE', 'FD', 'BD', 'VB', 'VD', 'LV'}) or right_value in {'FC', 'FB', 'FE', 'FD'}:
                    right_wall = True
                elif right_bool_value == False and right_value in {'BC', 'BB', 'BE', 'VC', 'VE', 'LH'}:
                    right_connected = True
            else:
                right_wall = True
            
            if up_wall: pieces.remove('FC')
            if down_wall: pieces.remove('FB')
            if left_wall: pieces.remove('FE')
            if right_wall: pieces.remove('FD')
            
            if up_connected: pieces = ['FC']
            elif down_connected: pieces = ['FB']
            elif left_connected: pieces = ['FE']
            elif right_connected: pieces = ['FD']
        
        elif piece in {'BC', 'BB', 'BE', 'BD'}:
            pieces = ['BC', 'BB', 'BE', 'BD']
            if row != 0:
                if up_bool_value == False and up_value in {'FC', 'FE', 'FD', 'BC', 'VC', 'VD', 'LH'}:
                    up_wall = True
                elif up_bool_value == False and up_value in {'FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'}:
                    up_connected = True
            else:
                up_wall = True
            if row != board_size-1:
                if down_bool_value == False and down_value in {'FB', 'FE', 'FD', 'BB', 'VB', 'VE', 'LH'}:
                    down_wall = True
                elif down_bool_value == False and down_value in {'FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'}:
                    down_connected = True
            else:
                down_wall = True
            if col != 0:
                if left_bool_value == False and left_value in {'FC', 'FB', 'FE', 'BE', 'VC', 'VE', 'LV'}:
                    left_wall = True
                elif left_bool_value == False and left_value in {'FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH'}:
                    left_connected = True
            else:
                left_wall = True
            if col != board_size-1:
                if right_bool_value == False and right_value in {'FC', 'FB', 'FD', 'BD', 'VB', 'VD', 'LV'}:
                    right_wall = True
                elif right_bool_value == False and right_value in {'FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH'}:
                    right_connected = True
            else:
                right_wall = True
            
            if (up_connected and left_connected and right_connected) or down_wall: pieces = ['BC']
            elif (down_connected and left_connected and right_connected) or up_wall: pieces = ['BB']
            elif (up_connected and down_connected and left_connected) or right_wall: pieces = ['BE']
            elif (up_connected and down_connected and right_connected) or left_wall: pieces = ['BD']
            
            if up_connected and down_connected:
                if 'BB' in pieces: pieces.remove('BB')
                if 'BC' in pieces: pieces.remove('BC')
            elif left_connected and right_connected:
                if 'BE' in pieces: pieces.remove('BE')
                if 'BD' in pieces: pieces.remove('BD')
            elif up_connected and left_connected:
                if 'BB' in pieces: pieces.remove('BB')
                if 'BD' in pieces: pieces.remove('BD')
            elif up_connected and right_connected:
                if 'BB' in pieces: pieces.remove('BB')
                if 'BE' in pieces: pieces.remove('BE')
            elif down_connected and left_connected:
                if 'BC' in pieces: pieces.remove('BC')
                if 'BD' in pieces: pieces.remove('BD')
            elif down_connected and right_connected:
                if 'BC' in pieces: pieces.remove('BC')
                if 'BE' in pieces: pieces.remove('BE')
        
        elif piece in {'VC', 'VB', 'VE', 'VD'}:
            pieces = ['VC', 'VB', 'VE', 'VD']
            if row != 0:
                if up_bool_value == False and up_value in {'FC', 'FE', 'FD', 'BC', 'VC', 'VD', 'LH'}:
                    up_wall = True
                elif up_bool_value == False and up_value in {'FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'}:
                    up_connected = True
            else:
                up_wall = True
            if row != board_size-1:
                if down_bool_value == False and down_value in {'FB', 'FE', 'FD', 'BB', 'VB', 'VE', 'LH'}:
                    down_wall = True
                elif down_bool_value == False and down_value in {'FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'}:
                    down_connected = True
            else:
                down_wall = True
            if col != 0:
                if left_bool_value == False and left_value in {'FC', 'FB', 'FE', 'BE', 'VC', 'VE', 'LV'}:
                    left_wall = True
                elif left_bool_value == False and left_value in {'FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH'}:
                    left_connected = True
            else:
                left_wall = True
            if col != board_size-1:
                if right_bool_value == False and right_value in {'FC', 'FB', 'FD', 'BD', 'VB', 'VD', 'LV'}:
                    right_wall = True
                elif right_bool_value == False and right_value in {'FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH'}:
                    right_connected = True
            
            if up_wall or down_connected: 
                if 'VC' in pieces: pieces.remove('VC')
                if 'VD' in pieces: pieces.remove('VD')
            if down_wall or up_connected:
                if 'VB' in pieces: pieces.remove('VB')
                if 'VE' in pieces: pieces.remove('VE')
            if left_wall or right_connected:
                if 'VC' in pieces: pieces.remove('VC')
                if 'VE' in pieces: pieces.remove('VE')
            if right_wall or left_connected:
                if 'VB' in pieces: pieces.remove('VB')
                if 'VD' in pieces: pieces.remove('VD')
                
            if up_connected and left_connected: pieces = ['VC']
            elif down_connected and right_connected: pieces = ['VB']
            elif left_connected and down_connected: pieces = ['VE']
            elif right_connected and up_connected: pieces = ['VD']
        
        elif piece in {'LH', 'LV'}:
            pieces = ['LH', 'LV']
            if row != 0:
                if up_bool_value == False and up_value in {'FC', 'FE', 'FD', 'BC', 'VC', 'VD', 'LH'}:
                    up_wall = True
                elif up_bool_value == False and up_value in {'FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'}:
                    up_connected = True
            else:
                up_wall = True
            if row != board_size-1:
                if down_bool_value == False and down_value in {'FB', 'FE', 'FD', 'BB', 'VB', 'VE', 'LH'}:
                    down_wall = True
                elif down_bool_value == False and down_value in {'FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'}:
                    down_connected = True
            else:
                down_wall = True
            if col != 0:
                if left_bool_value == False and left_value in {'FC', 'FB', 'FE', 'BE', 'VC', 'VE', 'LV'}:
                    left_wall = True
                elif left_bool_value == False and left_value in {'FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH'}:
                    left_connected = True
            else:
                left_wall = True
            if col != board_size-1:
                if right_bool_value == False and right_value in {'FC', 'FB', 'FD', 'BD', 'VB', 'VD', 'LV'}:
                    right_wall = True
                elif right_bool_value == False and right_value in {'FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH'}:
                    right_connected = True
            else:
                right_wall = True
            
            if up_wall or down_wall or left_connected or right_connected: pieces = ['LH']
            elif left_wall or right_wall or up_connected or down_connected: pieces = ['LV']
        
        return pieces

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        next_piece = state.board.next_piece
        board_size = len(state.board.board)
        if next_piece[0] == board_size:
            return actions
        flag = True
        
        while flag:
            while state.board.get_value(next_piece[0], next_piece[1])[1] == False:
                if next_piece[1] == board_size:
                    next_piece = (next_piece[0]+1, 0)
                else:
                    next_piece = (next_piece[0], next_piece[1]+1)
                if next_piece[1] == board_size:
                    next_piece = (next_piece[0]+1, 0)
                if next_piece[0] == board_size:
                    return []
            
            piece = state.board.get_value(next_piece[0], next_piece[1])[0]
            
            pieces = self.reduce_actions(state, board_size, piece, next_piece)
            
            if len(pieces) == 1 and pieces[0] == piece:
                state.board.board[next_piece[0]][next_piece[1]][0] = pieces[0]
                state.board.board[next_piece[0]][next_piece[1]][1] = False
                flag = True
                if next_piece[1] == board_size:
                    next_piece = (next_piece[0]+1, 0)
                else:
                    next_piece = (next_piece[0], next_piece[1]+1)
                if next_piece[1] == board_size:
                    next_piece = (next_piece[0]+1, 0)
                if next_piece[0] == board_size:
                    return []
            else:
                for k in pieces: actions.append((next_piece[0], next_piece[1], k, True))
                flag = False
        return actions

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        new_board = deepcopy(state.board.board)
        new_board[action[0]][action[1]][0] = action[2]
        new_board[action[0]][action[1]][1] = action[3]
        
        if action[1] == len(new_board)-1:
            next_piece = (action[0]+1, 0)
        else:
            next_piece = (action[0], action[1]+1)
        return PipeManiaState(Board(new_board, next_piece))

    def is_connected(self, state: PipeManiaState, row: int, col: int):
        piece = state.board.get_value(row, col)[0]
        board_size_index = len(state.board.board)-1

        if piece == 'FC' and row != 0:
            if state.board.board[row-1][col][0] in {'BB', 'BE', 'BD', 'VB', 'VE', 'LV'}:
                return True
        elif piece == 'FB' and row != board_size_index:
            if state.board.board[row+1][col][0] in {'BE', 'BD', 'BC', 'VC', 'VD', 'LV'}:
                return True
        elif piece == 'FE' and col != 0:
            if state.board.board[row][col-1][0] in {'BB', 'BC', 'BD', 'VB', 'VD', 'LH'}:
                return True
        elif piece == 'FD' and col != board_size_index:
            if state.board.board[row][col+1][0] in {'BB', 'BC', 'BE', 'VC', 'VE', 'LH'}:
                return True
        elif piece == 'BC' and row != 0 and col != 0 and col != board_size_index:
            if state.board.board[row][col-1][0] in {'FD', 'BB', 'BC', 'BD', 'VB', 'VD', 'LH'} and state.board.board[row][col+1][0] in {'FE', 'BB', 'BC', 'BE', 'VC', 'VE', 'LH'} and state.board.board[row-1][col][0] in {'FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'}:
                return True
        elif piece == 'BB' and col != 0 and col != board_size_index and row != board_size_index:
            if state.board.board[row][col-1][0] in {'FD', 'BB', 'BC', 'BD', 'VB', 'VD', 'LH'} and state.board.board[row][col+1][0] in {'FE', 'BB', 'BC', 'BE', 'VC', 'VE', 'LH'} and state.board.board[row+1][col][0] in {'FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'}:
                return True
        elif piece == 'BE' and row != 0 and col != 0 and row != board_size_index:
            if state.board.board[row][col-1][0] in {'FD', 'BB', 'BC', 'BD', 'VB', 'VD', 'LH'} and state.board.board[row+1][col][0] in {'FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'} and state.board.board[row-1][col][0] in {'FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'}:
                return True
        elif piece == 'BD' and row != 0 and row != board_size_index and col != board_size_index:
            if state.board.board[row+1][col][0] in {'FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'} and state.board.board[row-1][col][0] in {'FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'} and state.board.board[row][col+1][0] in {'FE', 'BB', 'BC', 'BE', 'VC', 'VE', 'LH'}:
                return True
        elif piece == 'VC' and row != 0 and col != 0:
            if state.board.board[row][col-1][0] in {'FD', 'BB', 'BC', 'BD', 'VB', 'VD', 'LH'} and state.board.board[row-1][col][0] in {'FB' ,'BB', 'BE', 'BD', 'VB', 'VE', 'LV'}:
                return True
        elif piece == 'VB' and row != board_size_index and col != board_size_index:
            if state.board.board[row][col+1][0] in {'FE', 'BB', 'BC', 'BE', 'VC', 'VE', 'LH'} and state.board.board[row+1][col][0] in {'FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'}:
                return True
        elif piece == 'VE' and row != board_size_index and col != 0:
            if state.board.board[row][col-1][0] in {'FD', 'BB', 'BC', 'BD', 'VB', 'VD', 'LH'} and state.board.board[row+1][col][0] in {'FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'}:
                return True
        elif piece == 'VD' and row != 0 and col != board_size_index:
            if state.board.board[row-1][col][0] in {'FB' ,'BB', 'BE', 'BD', 'VB', 'VE', 'LV'} and state.board.board[row][col+1][0] in {'FE', 'BB', 'BC', 'BE', 'VC', 'VE', 'LH'}:
                return True
        elif piece == 'LH' and col != 0 and col != board_size_index:
            if state.board.board[row][col-1][0] in {'FD' ,'BB', 'BC', 'BD', 'VB', 'VD', 'LH'} and state.board.board[row][col+1][0] in {'FE', 'BB', 'BC', 'BE', 'VC', 'VE', 'LH'}:
                return True
        elif piece == 'LV' and row != 0 and row != board_size_index:
            if state.board.board[row-1][col][0] in {'FB' ,'BB', 'BE', 'BD', 'VB', 'VE', 'LV'} and state.board.board[row+1][col][0] in {'FC', 'BD', 'BC', 'BE', 'VC', 'VD', 'LV'}:
                return True

        return False

    def known_positions(self, state: PipeManiaState):
        result_state = deepcopy(state)
        board_size_index = len(result_state.board.board)-1
        
        #superior esquerdo
        if result_state.board.board[0][0][0] in {'VC', 'VB', 'VE', 'VD'}:
            result_state.board.board[0][0][0] = 'VB'
            result_state.board.board[0][0][1] = False
            if result_state.board.board[0][1][0] in {'VC', 'VB', 'VE', 'VD'}:
                result_state.board.board[0][1][0] = 'VE'
                result_state.board.board[0][1][1] = False
            elif result_state.board.board[0][1][0] in {'FC', 'FB', 'FE', 'FD'}:
                result_state.board.board[0][1][0] = 'FE'
                result_state.board.board[0][1][1] = False
            if result_state.board.board[1][0][0] in {'VC', 'VB', 'VE', 'VD'}:
                result_state.board.board[1][0][0] = 'VD'
                result_state.board.board[1][0][1] = False
            elif result_state.board.board[1][0][0] in {'FC', 'FB', 'FE', 'FD'}:
                result_state.board.board[1][0][0] = 'FC'
                result_state.board.board[1][0][1] = False
        elif result_state.board.board[0][0][0] in {'FC', 'FB', 'FE', 'FD'} and (result_state.board.board[0][1][0] in {'BC', 'BB', 'BE', 'BD'} or result_state.board.board[0][1][0] in {'LH', 'LV'}  or result_state.board.board[1][0][0] in {'FC', 'FB', 'FE', 'FD'}):
            result_state.board.board[0][0][0] = 'FD'
            result_state.board.board[0][0][1] = False
        elif result_state.board.board[0][0][0] in {'FC', 'FB', 'FE', 'FD'} and (result_state.board.board[1][0][0] in {'BC', 'BB', 'BE', 'BD'} or result_state.board.board[1][0][0] in {'LH', 'LV'} or result_state.board.board[0][1][0] in {'FC', 'FB', 'FE', 'FD'}):
            result_state.board.board[0][0][0] = 'FB'
            result_state.board.board[0][0][1] = False
            
        # superior direito
        if result_state.board.board[0][board_size_index][0] in {'VC', 'VB', 'VE', 'VD'}:
            result_state.board.board[0][board_size_index][0] = 'VE'
            result_state.board.board[0][board_size_index][1] = False
            if result_state.board.board[0][board_size_index-1][0] in {'VC', 'VB', 'VE', 'VD'}:
                result_state.board.board[0][board_size_index-1][0] = 'VB'
                result_state.board.board[0][board_size_index-1][1] = False
            elif result_state.board.board[0][board_size_index-1][0] in {'FC', 'FB', 'FE', 'FD'}:
                result_state.board.board[0][board_size_index-1][0] = 'FD'
                result_state.board.board[0][board_size_index-1][1] = False
            if result_state.board.board[1][board_size_index][0] in {'VC', 'VB', 'VE', 'VD'}:
                result_state.board.board[1][board_size_index][0] = 'VC'
                result_state.board.board[1][board_size_index][1] = False
            elif result_state.board.board[1][board_size_index][0] in {'FC', 'FB', 'FE', 'FD'}:
                result_state.board.board[1][board_size_index][0] = 'FC'
                result_state.board.board[1][board_size_index][1] = False 
        elif result_state.board.board[0][board_size_index][0] in {'FC', 'FB', 'FE', 'FD'} and (result_state.board.board[0][board_size_index-1][0] in {'BC', 'BB', 'BE', 'BD'} or result_state.board.board[0][board_size_index-1][0] in {'LH', 'LV'} or result_state.board.board[1][board_size_index][0] in {'FC', 'FB', 'FE', 'FD'}):
            result_state.board.board[0][board_size_index][0] = 'FE'
            result_state.board.board[0][board_size_index][1] = False
        elif result_state.board.board[0][board_size_index][0] in {'FC', 'FB', 'FE', 'FD'} and (result_state.board.board[1][board_size_index][0] in {'BC', 'BB', 'BE', 'BD'} or result_state.board.board[1][board_size_index][0] in {'LH', 'LV'}  or result_state.board.board[0][board_size_index-1][0] in {'FC', 'FB', 'FE', 'FD'}):
            result_state.board.board[0][board_size_index][0] = 'FB'
            result_state.board.board[0][board_size_index][1] = False

        # inferior esquerdo
        if result_state.board.board[board_size_index][0][0] in {'VC', 'VB', 'VE', 'VD'}:
            result_state.board.board[board_size_index][0][0] = 'VD'
            result_state.board.board[board_size_index][0][1] = False
            if result_state.board.board[board_size_index][1][0] in {'VC', 'VB', 'VE', 'VD'}:
                result_state.board.board[board_size_index][1][0] = 'VC'
                result_state.board.board[board_size_index][1][1] = False
            elif result_state.board.board[board_size_index][1][0] in {'FC', 'FB', 'FE', 'FD'}:
                result_state.board.board[board_size_index][1][0] = 'FE'
                result_state.board.board[board_size_index][1][1] = False
            if result_state.board.board[board_size_index-1][0][0] in {'VC', 'VB', 'VE', 'VD'}:
                result_state.board.board[board_size_index-1][0][0] = 'VB'
                result_state.board.board[board_size_index-1][0][1] = False
            elif result_state.board.board[board_size_index-1][0][0] in {'FC', 'FB', 'FE', 'FD'}:
                result_state.board.board[board_size_index-1][0][0] = 'FB'
                result_state.board.board[board_size_index-1][0][1] = False  
        elif result_state.board.board[board_size_index][0][0] in {'FC', 'FB', 'FE', 'FD'} and (result_state.board.board[board_size_index][1][0] in {'BC', 'BB', 'BE', 'BD'} or result_state.board.board[board_size_index][1][0] in {'LH', 'LV'} or result_state.board.board[board_size_index-1][0][0] in {'FC', 'FB', 'FE', 'FD'}):
            result_state.board.board[board_size_index][0][0] = 'FD'
            result_state.board.board[board_size_index][0][1] = False
        elif result_state.board.board[board_size_index][0][0] in {'FC', 'FB', 'FE', 'FD'} and (result_state.board.board[board_size_index-1][0][0] in {'BC', 'BB', 'BE', 'BD'} or result_state.board.board[board_size_index-1][0][0] in {'LH', 'LV'} or result_state.board.board[board_size_index][1][0] in {'FC', 'FB', 'FE', 'FD'}):
            result_state.board.board[board_size_index][0][0] = 'FC'
            result_state.board.board[board_size_index][0][1] = False

        # inferior direito
        if result_state.board.board[board_size_index][board_size_index][0] in {'VC', 'VB', 'VE', 'VD'}:
            result_state.board.board[board_size_index][board_size_index][0] = 'VC'
            result_state.board.board[board_size_index][board_size_index][1] = False
            if result_state.board.board[board_size_index][board_size_index-1][0] in {'VC', 'VB', 'VE', 'VD'}:
                result_state.board.board[board_size_index][board_size_index-1][0] = 'VD'
                result_state.board.board[board_size_index][board_size_index-1][1] = False
            elif result_state.board.board[board_size_index][board_size_index-1][0] in {'FC', 'FB', 'FE', 'FD'}:
                result_state.board.board[board_size_index][board_size_index-1][0] = 'FD'
                result_state.board.board[board_size_index][board_size_index-1][1] = False    
            if result_state.board.board[board_size_index-1][board_size_index][0] in {'VC', 'VB', 'VE', 'VD'}:
                result_state.board.board[board_size_index-1][board_size_index][0] = 'VE'
                result_state.board.board[board_size_index-1][board_size_index][1] = False
            elif result_state.board.board[board_size_index-1][board_size_index][0] in {'FC', 'FB', 'FE', 'FD'}:
                result_state.board.board[board_size_index-1][board_size_index][0] = 'FB'
                result_state.board.board[board_size_index-1][board_size_index][1] = False
        elif result_state.board.board[board_size_index][board_size_index][0] in {'FC', 'FB', 'FE', 'FD'} and (result_state.board.board[board_size_index][board_size_index-1][0] in {'BC', 'BB', 'BE', 'BD'} or result_state.board.board[board_size_index][board_size_index-1][0] in {'LH', 'LV'} or result_state.board.board[board_size_index-1][board_size_index][0] in {'FC', 'FB', 'FE', 'FD'}):
            result_state.board.board[board_size_index][board_size_index][0] = 'FE'
            result_state.board.board[board_size_index][board_size_index][1] = False
        elif result_state.board.board[board_size_index][board_size_index][0] in {'FC', 'FB', 'FE', 'FD'} and (result_state.board.board[board_size_index-1][board_size_index][0] in {'BC', 'BB', 'BE', 'BD'} or result_state.board.board[board_size_index-1][board_size_index][0] in {'LH', 'LV'} or result_state.board.board[board_size_index][board_size_index-1][0] in {'FC', 'FB', 'FE', 'FD'}):
            result_state.board.board[board_size_index][board_size_index][0] = 'FC'
            result_state.board.board[board_size_index][board_size_index][1] = False
        
        past_board = []
        while past_board != result_state.board.board:
            past_board = deepcopy(result_state.board.board)
            for row in range(board_size_index+1):
                for col in range(board_size_index+1):
                    
                    if (row, col) in [(0, 0), (0, board_size_index), (board_size_index, 0), (board_size_index, board_size_index)]: # cantos
                        continue
                    
                    up_wall, down_wall, left_wall, right_wall = False, False, False, False
                    up_connected, down_connected, left_connected, right_connected = False, False, False, False
                    piece = result_state.board.get_value(row, col)[0]
                    if row != 0: up_bool_value, up_value = result_state.board.get_value(row-1, col)[1], result_state.board.get_value(row-1, col)[0]
                    else: up_bool_value, up_value = None, None
                    if row != board_size_index: down_bool_value, down_value = result_state.board.get_value(row+1, col)[1], result_state.board.get_value(row+1, col)[0]
                    else: down_bool_value, down_value = None, None
                    if col != 0: left_bool_value, left_value = result_state.board.get_value(row, col-1)[1], result_state.board.get_value(row, col-1)[0]
                    else: left_bool_value, left_value = None, None
                    if col != board_size_index: right_bool_value, right_value = result_state.board.get_value(row, col+1)[1], result_state.board.get_value(row, col+1)[0]
                    else: right_bool_value, right_value = None, None
                    
                    if piece in {'FC', 'FB', 'FE', 'FD'}:
                        if row != 0:
                            if (up_bool_value == False and up_value in {'FC', 'FB', 'FE', 'FD', 'BC', 'VC', 'VD', 'LH'}) or up_value in {'FC', 'FB', 'FE', 'FD'}:
                                up_wall = True
                            elif up_bool_value == False and up_value in {'BB', 'BE', 'BD', 'VB', 'VE', 'LV'}:
                                up_connected = True
                        else:
                            up_wall = True
                        if row != board_size_index:
                            if (down_bool_value == False and down_value in {'FC', 'FB', 'FE', 'FD', 'BB', 'VB', 'VE', 'LH'}) or down_value in {'FC', 'FB', 'FE', 'FD'}:
                                down_wall = True
                            elif down_bool_value == False and down_value in {'BC', 'BE', 'BD', 'VC', 'VD', 'LV'}:
                                down_connected = True
                        else:
                            down_wall = True
                        if col != 0:
                            if (left_bool_value == False and left_value in {'FC', 'FB', 'FE', 'FD', 'BE', 'VC', 'VE', 'LV'}) or left_value in {'FC', 'FB', 'FE', 'FD'}:
                                left_wall = True
                            elif left_bool_value == False and left_value in {'BC', 'BB', 'BD', 'VB', 'VD', 'LH'}:
                                left_connected = True
                        else:
                            left_wall = True
                        if col != board_size_index:
                            if (right_bool_value == False and right_value in {'FC', 'FB', 'FE', 'FD', 'BD', 'VB', 'VD', 'LV'}) or right_value in {'FC', 'FB', 'FE', 'FD'}:
                                right_wall = True
                            elif right_bool_value == False and right_value in {'BC', 'BB', 'BE', 'VC', 'VE', 'LH'}:
                                right_connected = True
                        else:
                            right_wall = True
                        
                        if up_connected or (down_wall and left_wall and right_wall): result_state.board.board[row][col][0], result_state.board.board[row][col][1] = 'FC', False
                        elif down_connected or (up_wall and left_wall and right_wall): result_state.board.board[row][col][0], result_state.board.board[row][col][1] = 'FB', False
                        elif left_connected or (up_wall and down_wall and right_wall): result_state.board.board[row][col][0], result_state.board.board[row][col][1] = 'FE', False
                        elif right_connected or (up_wall and down_wall and left_wall): result_state.board.board[row][col][0], result_state.board.board[row][col][1] = 'FD', False

                    elif piece in {'BC', 'BB', 'BE', 'BD'}:
                        if row != 0:
                            if up_bool_value == False and up_value in {'FC', 'FE', 'FD', 'BC', 'VC', 'VD', 'LH'}:
                                up_wall = True
                            elif up_bool_value == False and up_value in {'FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'}:
                                up_connected = True
                        else:
                            up_wall = True
                        if row != board_size_index:
                            if down_bool_value == False and down_value in {'FB', 'FE', 'FD', 'BB', 'VB', 'VE', 'LH'}:
                                down_wall = True
                            elif down_bool_value == False and down_value in {'FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'}:
                                down_connected = True
                        else:
                            down_wall = True
                        if col != 0:
                            if left_bool_value == False and left_value in {'FC', 'FB', 'FE', 'BE', 'VC', 'VE', 'LV'}:
                                left_wall = True
                            elif left_bool_value == False and left_value in {'FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH'}:
                                left_connected = True
                        else:
                            left_wall = True
                        if col != board_size_index:
                            if right_bool_value == False and right_value in {'FC', 'FB', 'FD', 'BD', 'VB', 'VD', 'LV'}:
                                right_wall = True
                            elif right_bool_value == False and right_value in {'FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH'}:
                                right_connected = True
                        else:
                            right_wall = True
                        
                        if (up_connected and left_connected and right_connected) or down_wall: result_state.board.board[row][col][0], result_state.board.board[row][col][1] = 'BC', False
                        elif (down_connected and left_connected and right_connected) or up_wall: result_state.board.board[row][col][0], result_state.board.board[row][col][1] = 'BB', False
                        elif (up_connected and down_connected and left_connected) or right_wall: result_state.board.board[row][col][0], result_state.board.board[row][col][1] = 'BE', False
                        elif (up_connected and down_connected and right_connected) or left_wall: result_state.board.board[row][col][0], result_state.board.board[row][col][1] = 'BD', False
                        
                    elif piece in {'VC', 'VB', 'VE', 'VD'}:
                        if row != 0:
                            if up_bool_value == False and up_value in {'FC', 'FE', 'FD', 'BC', 'VC', 'VD', 'LH'}:
                                up_wall = True
                            elif up_bool_value == False and up_value in {'FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'}:
                                up_connected = True
                        else:
                            up_wall = True
                        if row != board_size_index:
                            if down_bool_value == False and down_value in {'FB', 'FE', 'FD', 'BB', 'VB', 'VE', 'LH'}:
                                down_wall = True
                            elif down_bool_value == False and down_value in {'FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'}:
                                down_connected = True
                        else:
                            down_wall = True
                        if col != 0:
                            if left_bool_value == False and left_value in {'FC', 'FB', 'FE', 'BE', 'VC', 'VE', 'LV'}:
                                left_wall = True
                            elif left_bool_value == False and left_value in {'FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH'}:
                                left_connected = True
                        else:
                            left_wall = True
                        if col != board_size_index:
                            if right_bool_value == False and right_value in {'FC', 'FB', 'FD', 'BD', 'VB', 'VD', 'LV'}:
                                right_wall = True
                            elif right_bool_value == False and right_value in {'FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH'}:
                                right_connected = True
                        else:
                            right_wall = True
                            
                        if (up_connected and left_connected) or (down_wall and right_wall) or (up_connected and right_wall) or (left_connected and down_wall): result_state.board.board[row][col][0], result_state.board.board[row][col][1] = 'VC', False
                        elif (down_connected and right_connected) or (up_wall and left_wall) or (down_connected and left_wall) or (right_connected and up_wall): result_state.board.board[row][col][0], result_state.board.board[row][col][1] = 'VB', False
                        elif (left_connected and down_connected) or (up_wall and right_wall) or (left_connected and up_wall) or (down_connected and right_wall): result_state.board.board[row][col][0], result_state.board.board[row][col][1] = 'VE', False
                        elif (right_connected and up_connected) or (left_wall and down_wall) or (up_connected and left_wall) or (right_connected and down_wall): result_state.board.board[row][col][0], result_state.board.board[row][col][1] = 'VD', False

                    elif piece in {'LH', 'LV'}:
                        if row != 0:
                            if up_bool_value == False and up_value in {'FC', 'FE', 'FD', 'BC', 'VC', 'VD', 'LH'}:
                                up_wall = True
                            elif up_bool_value == False and up_value in {'FB', 'BB', 'BE', 'BD', 'VB', 'VE', 'LV'}:
                                up_connected = True
                        else:
                            up_wall = True
                        if row != board_size_index:
                            if down_bool_value == False and down_value in {'FB', 'FE', 'FD', 'BB', 'VB', 'VE', 'LH'}:
                                down_wall = True
                            elif down_bool_value == False and down_value in {'FC', 'BC', 'BE', 'BD', 'VC', 'VD', 'LV'}:
                                down_connected = True
                        else:
                            down_wall = True
                        if col != 0:
                            if left_bool_value == False and left_value in {'FC', 'FB', 'FE', 'BE', 'VC', 'VE', 'LV'}:
                                left_wall = True
                            elif left_bool_value == False and left_value in {'FD', 'BC', 'BB', 'BD', 'VB', 'VD', 'LH'}:
                                left_connected = True
                        else:
                            left_wall = True
                        if col != board_size_index:
                            if right_bool_value == False and right_value in {'FC', 'FB', 'FD', 'BD', 'VB', 'VD', 'LV'}:
                                right_wall = True
                            elif right_bool_value == False and right_value in {'FE', 'BC', 'BB', 'BE', 'VC', 'VE', 'LH'}:
                                right_connected = True
                        else:
                            right_wall = True
                        
                        if up_wall or down_wall or left_connected or right_connected: result_state.board.board[row][col][0], result_state.board.board[row][col][1] = 'LH', False
                        elif left_wall or right_wall or up_connected or down_connected: result_state.board.board[row][col][0], result_state.board.board[row][col][1] = 'LV', False

        return result_state
        
    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        size = state.board.size()
        for i in range(size):
            for j in range(size):
                if not self.is_connected(state, i, j):
                    return False
        return True

    def h(self, node: Node):
        """Heuristic function used for A* search."""
        state = node.state
        unconnected_pipes = 0
    
        # If the current state is a goal state, return 0 (the best possible value for the heuristic)
        #if self.goal_test(state):
            #return 0
    
        # Count the number of unconnected pipes
        for i in range(state.board.size()):
            for j in range(state.board.size()):
                if not self.is_connected(state, i, j):
                    unconnected_pipes += 1
    
        return unconnected_pipes

if __name__ == "__main__":
    initial_board = Board.parse_instance()
    problem = PipeMania(initial_board)
    adjusted_problem = PipeMania(problem.known_positions(problem.initial).board)
    solution = recursive_best_first_search(adjusted_problem)
    solution.state.board.print_board()
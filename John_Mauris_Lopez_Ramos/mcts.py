from board import HexBoard
import math
from xor_hashing import XorHashing
from board_analyzer import BoardAnalyzer
import random
from electrical_heuristic import ElectricalHeuristic
import time
from electric_time_budget import electric_time_budget
from random_sampling import random_sampling

class StatesManager:

    def __init__(self, board):
        board_analyzer = BoardAnalyzer(board)
        self.empty_cells = board_analyzer.get_empty_cells()
        self.empty_cells_length = len(self.empty_cells)
        self.occupied_cells = board_analyzer.get_occupied_cells()
        self.occupied_cells_length = len(self.occupied_cells)
        self.cells = self.occupied_cells + self.empty_cells
        self.cell_positions = {}
        self.last_position = {}
        for i in range(len(self.cells)):
            self.cell_positions[self.cells[i]] = i

    def swap_occupy(self, cell):
        pos = self.cell_positions[cell]
        self.last_position[cell] = pos
        # print("swap", self.occupied_cells_length, pos)
        self.cells[self.occupied_cells_length], self.cells[pos] = self.cells[pos], self.cells[self.occupied_cells_length]
        self.cell_positions[self.cells[pos]] = pos
        self.cell_positions[self.cells[self.occupied_cells_length]] = self.occupied_cells_length
        
    def swap_vacate(self, cell):
        pos = self.last_position[cell]
        # print("swap_vacate", self.occupied_cells_length, pos)
        self.cells[self.occupied_cells_length], self.cells[pos] = self.cells[pos], self.cells[self.occupied_cells_length]
        self.cell_positions[self.cells[pos]] = pos
        self.cell_positions[self.cells[self.occupied_cells_length]] = self.occupied_cells_length

    def occupy(self, cell):
        self.swap_occupy(cell)
        self.occupied_cells_length += 1
        self.empty_cells_length -= 1

    def vacate(self, cell):
        self.occupied_cells_length -= 1
        self.empty_cells_length += 1
        # print("vacate", cell)
        self.swap_vacate(cell)

    def next(self, current_childs_coords):
        valid_idxs = []
        for i in range(self.empty_cells_length):
            if self.empty_cells[i] not in current_childs_coords:
                valid_idxs.append(i)
        print(self.cells)
        for i in valid_idxs:
            print(self.empty_cells[i], end=" ")
        print()
        return self.cells[self.occupied_cells_length + random.choice(valid_idxs)]

class MCTS:
    
    def __init__(self, board, player_id):
        self.board = board
        self.BOARD_SIZE = len(self.board)
        self.root_player = player_id
        self.total_nodes = 1
        self.player = [3 - self.root_player]
        self.dag = [[]]
        self.visits = [0]
        self.wins = [0]
        self.depth = [0]
        self.c = math.sqrt(2)
        self.coordinates = [(-1,-1)]
        self.xor_hashing = XorHashing(self.BOARD_SIZE)
        self.hashed_states = [self.xor_hashing.matrix_hash(self.board)]
        self.dad = [-1]
        self.transposition_table = {self.hashed_states[0]: 0}
        self.win_root = [0]
        self.states_manager = StatesManager(board)
        self.selected = []
    
    def uct(self, node):
        w = self.wins[node]
        n = self.visits[node]
        N = self.visits[self.dad[node]]
        C = self.c
        return w / n + C * math.sqrt( math.log(N) / n )
    
    # case sign = 1: returns the child with the largest uct
    # case sign = -1: returns the child with the smallest uct
    def best_child(self, node, sign):
        best_child = 0
        best_child_uct = -1e18
        for child in self.dag[node]:
            child_uct = self.uct(child) * sign
            if child_uct > best_child_uct:
                best_child_uct = child_uct
                best_child = child
        self.dad[best_child] = node
        self.depth[best_child] = self.depth[node] + 1
        return best_child

    def selection(self, node, max_childs):
        if max_childs == 0:
            return None
        if len(self.dag[node]) < max_childs:
            return node
        sign = 1 if self.player[node] == self.root_player else -1
        child = self.best_child(node, sign)
        (i, j) = self.coordinates[child]
        self.board[i][j] = self.player[child]

        # print("selection", i, j, self.player[child])
        # self.board_analyzer.draw(self.board)

        self.states_manager.occupy(self.coordinates[child])
        self.selected.append(self.coordinates[child])
        return self.selection(child, max_childs - 1)

    def expansion(self, coords_new_node, dad_node):
        node = self.total_nodes
        self.states_manager.occupy(coords_new_node)
        self.total_nodes += 1
        self.coordinates.append(coords_new_node)
        self.dag[dad_node].append(node)
        self.player.append(3 - self.player[dad_node])
        self.dag.append([])
        self.visits.append(0)
        self.wins.append(0)
        self.win_root.append(0)
        new_hash = self.hashed_states[dad_node]
        (i, j) = coords_new_node
        self.board[i][j] = self.player[node]

        # print("expansion", i, j, self.player[node])
        # self.board_analyzer.draw(self.board)
        
        new_hash ^= self.xor_hashing.cell_hash(i, j, 0)
        new_hash ^= self.xor_hashing.cell_hash(i, j, self.board[i][j])
        self.hashed_states.append(new_hash)
        self.dad.append(dad_node)
        self.depth.append(self.depth[dad_node] + 1)
        self.transposition_table[self.hashed_states[node]] = node
        return node

    # returns true iff the winner of the simulation is the root player
    def simulation(self, node) -> bool:
        # cnt = 0
        # cota = 10000
        # for _ in range(cota):
        #     if random_sampling(self.board, self.root_player):
        #         cnt += 1

        # print(self.board)
        # print(self.root_player)
        # print(cnt)

        # print("\n---")
        # self.board_analyzer.draw(self.board)
        # print(cnt)
        # print("---\n")

        # return cnt <= cota // 2
    
        simulation_time_limit = electric_time_budget(self.remaining_ms, self.depth[node], self.visits[node])
        my_heuristic = ElectricalHeuristic(self.board, self.player[node], simulation_time_limit)
        oponents_heuristic = ElectricalHeuristic(self.board, 3 - self.player[node], simulation_time_limit)
        my_resistance = my_heuristic.resistance()
        oponents_resistance = oponents_heuristic.resistance()
        # print("\n---")
        # self.board_analyzer.draw(self.board)
        # print("Simulation: ",((my_resistance <= oponents_resistance) == (self.player[node] == self.root_player)))        
        # print("---\n")
        return (my_resistance <= oponents_resistance) == (self.player[node] == self.root_player)

    def backpropagation(self, node, win_leaf):
        while node:
            self.visits[node] += 1
            self.wins[node] += win_leaf
            (i, j) = self.coordinates[node]
            self.board[i][j] = 0
            self.states_manager.vacate(self.coordinates[node])
            node = self.dad[node]
        self.visits[0] += 1
        self.wins[0] += win_leaf

    def expanded(self, coords, dad_hash, current_player):
        (i, j) = coords
        check_hash = dad_hash ^ self.xor_hashing.cell_hash(i, j, 0)
        check_hash ^= self.xor_hashing.cell_hash(i, j, current_player)
        if check_hash in self.transposition_table:
            return self.transposition_table[check_hash]
        return None

    def create_leaf(self):
        self.selected.clear()
        selected_node = self.selection(0, self.states_manager.empty_cells_length)
        if selected_node != None:
            current_childs_coords = set([self.coordinates[child] for child in self.dag[selected_node]])

            time.sleep(0.008)

            print("selectes_node", selected_node)
            # print(selected_node, self.states_manager.empty_cells_length, current_childs_coords)

            coords_node_to_expand = self.states_manager.next(current_childs_coords)

            print("coords", coords_node_to_expand)

            expanded_node = self.expanded(coords_node_to_expand, self.hashed_states[selected_node], 3 - self.player[selected_node])
            if expanded_node == None:
                expanded_node = self.expansion(coords_node_to_expand, selected_node)
                self.win_root[expanded_node] = self.simulation(expanded_node)
                self.backpropagation(expanded_node, self.win_root[expanded_node])
            else:
                self.visits[expanded_node] += 1
                self.wins[expanded_node] += self.win_root[expanded_node]
                self.backpropagation(selected_node, self.win_root[expanded_node])
        else:
            for (i, j) in self.selected:
                # print("bacano", (i, j))
                self.states_manager.vacate((i, j))
                self.board[i][j] = 0

                # print(i, j, "returning selection back")
                # self.board_analyzer.draw(self.board)
                

    def mcts(self) -> tuple:
        
        # print("AAAAAAAAAAAAAAAAAAAAAA")

        self.board_analyzer = BoardAnalyzer(self.board)

        # self.board_analyzer.draw(self.board)

        start_time = time.time()
        time_limit = 4.5
        while time.time() - start_time < time_limit:
            self.remaining_ms = (start_time + time_limit) - time.time()
            self.create_leaf()

        # print("BBBBBBBBBBBBBBBBBBBBBB")

        print(self.total_nodes)

        for child in self.dag[0]:
            print(child, self.coordinates[child], self.uct(child), self.visits[child], self.wins[child], self.win_root[child])

        return self.coordinates[self.best_child(0, 1)]
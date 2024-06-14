import numpy as np
# import torch
import math
import copy

class Node:
    def __init__(self, game, args, board, parent=None, action_taken=None):
        self.game = game
        self.args = args
        self.board = copy.deepcopy(board)
        self.state = self.board.squares
        self.parent = parent
        self.action_taken = action_taken

        self.children = []
        self.expandable_moves = self.board.valid_moves_list

        self.visit_count = 0
        self.value_sum = 0

    def is_fully_expanded(self):
        return len(self.expandable_moves) == 0
    
    def select(self):
        best_child = None
        best_ucb = -np.inf

        for child in self.children:
            ucb = self._get_ucb(child)
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb

        return best_child
    
    def _get_ucb(self, child):
        q_value = 1 - ((child.value_sum / child.visit_count) + 1) / 2
        return q_value + self.args['C'] * math.sqrt(math.log(self.visit_count) / child.visit_count)
    
    def expand(self):
        action_id = np.random.choice(len(self.expandable_moves))
        action = self.expandable_moves.pop(action_id)
        
        child_state = copy.deepcopy(self.board)
        child_state = child_state.get_next_state(action) 
        # child_state = self.game.change_perspective(child_state, player=-1) #TODO:  next_player???

        child = Node(self.game, self.args, child_state, self, action)
        self.children.append(child)
        return child
    
    def simulate(self):
        text, value, is_terminal = self.board.get_value_and_terminated()
        if is_terminal:
            return value if self.board.next_player == 'white' else (-1 * value)
        
        rollout_state = copy.deepcopy(self.board)
        rollout_state.all_valid_moves()
        # rollout_player = 1
        while True:
            action_id = np.random.choice(len(rollout_state.valid_moves_list))
            action = rollout_state.valid_moves_list.pop(action_id)
            rollout_state = rollout_state.get_next_state(action)
            text, value, is_terminal = rollout_state.get_value_and_terminated()
            if is_terminal:
                return value if rollout_state.next_player == 'white' else (-1 * value)
            
            
    def backpropagate(self, value):
        self.value_sum += value
        self.visit_count += 1
        
        if self.parent is not None:
            self.parent.backpropagate(value)


class MCTS:
    def __init__(self, game, args):
        self.game = game
        self.args = args
        self.board = self.game.board

        self.action_dict = {}
    
    def search(self):
        root = Node(self.game, self.args, self.board)
        
        for search in range(self.args['num_searches']):
            node = root
            
            while node.is_fully_expanded():
                node = node.select()
                
            text, value, is_terminal = self.board.get_value_and_terminated()

            value = -1 * value

            if not is_terminal:
                node = node.expand()
                value = node.simulate()
                
            node.backpropagate(value)
            
        action_probs = np.zeros(self.game.action_size)
        for child in root.children:
            action_str = child.action_taken
            # If the action string is not in the dictionary, add it
            if action_str not in self.action_dict:
                self.action_dict[action_str] = len(self.action_dict)
                action_index = self.action_dict[action_str]
                action_probs[action_index] = child.visit_count
        action_probs /= np.sum(action_probs)
        action = np.argmax(action_probs)
        max_action = None
        for action_str, index in self.action_dict.items():
            if index == action:
                max_action = action_str
                break

        return max_action
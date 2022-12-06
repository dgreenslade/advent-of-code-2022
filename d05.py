import re
import copy

def stack_input(file:str)->list:
    """Specific way of parsing horrible text file.  Rectified stacks into useable nested lists."""
    with open(file) as f:
        moves = []
        stacks = []
        for line in f:
            # Instructions
            if line.startswith('move'):
                move, frm, to = [int(x) for x in re.findall(r'\d+', line)]
                moves.append([move, frm, to])
            # Stacks
            elif line != '\n':
                stack_line = []
                i = 1
                while i in range(len(line)):
                    stack_line.append(line[i])
                    i += 4
                stacks.append(stack_line)
    # Flip columns & rows of starting stacks
    rectified_stack = [list(x[::-1]) for x in zip(*stacks)]
    # Remove blank spaces
    rectified_stack = [[x for x in y if x != ' '] for y in rectified_stack]
    return rectified_stack, moves

class Stack():
    """
    Class to hold individual stack of crates.  
    Methods for moving crates out of and into
    """
    def __init__(self, starting_stack:list):
        self.crates = starting_stack

    def move_from(self, number_to_move:int, mv_type='p1')->list:
        if mv_type == 'p1':
            moved = []
            for i in range(number_to_move):
                moved.append(self.crates.pop())
        elif mv_type == 'p2':
            moved = self.crates[-number_to_move:]
            del self.crates[-number_to_move:]
        else:
            raise ValueError('Move type must be "p1" or "p2"')
        return moved
    
    def move_to(self, list_of_moved:list):
        for i in range(len(list_of_moved)):
            self.crates.append(list_of_moved[i])
    
class StackGroup():
    """Class to hold a list of Stack objects and following move instructions"""
    def __init__(self):
        self.stacks = []
    
    def add_stack(self, starting_stack):
        self.stacks.append(Stack(starting_stack))
            
    def follow_move(self, instructions:list, move_type='p1'):
        num, frm, to = instructions
        moved = self.stacks[frm-1].move_from(num,move_type)
        self.stacks[to-1].move_to(moved)

    def print_stacks(self):
        for s in self.stacks:
            print(s.crates)
    
    def return_top_crates(self):
        top = ''
        for s in self.stacks:
            top += s.crates[-1]
        return top

def main():
    stack_start, moves = stack_input(r'./data/d05.txt')

    # Create Stack Group objects for part 1 and part 2
    p1_stack_group = StackGroup()
    # Populate group with stacks from input
    for i in range(len(stack_start)):
        p1_stack_group.add_stack(stack_start[i])
    # Copy so we don't have to recreate for part 2
    p2_stack_group = copy.deepcopy(p1_stack_group)
    
    # Part 1 moves
    for m in moves:
        p1_stack_group.follow_move(m, move_type='p1')
    # print('All stacks after part 1 moves:'), p1_stack_group.print_stacks()
    print(f'Part 1 crates at top of all stacks:  {p1_stack_group.return_top_crates()}')

    # Part 2 moves
    for m in moves:
        p2_stack_group.follow_move(m, move_type='p2')
    # print('All stacks after part 2 moves:'), p2_stack_group.print_stacks()
    print(f'Part 2 crates at top of all stacks:  {p2_stack_group.return_top_crates()}')

if __name__ == '__main__':
    main()
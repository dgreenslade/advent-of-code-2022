import copy
import numpy as np

def rope_input(input_file):
    with open(input_file) as file:
        return file.read().splitlines()

class rope():
    """
    Class to hold individual rope object.  
    Method for moving head and tail positions of rope accoring to instructions
    """
    def __init__(self, head_pos=[0,0], rope_len=2):
        self.head_pos = head_pos
        self.tail_pos = []
        # Set length of rope - default of two = one knot beyond head
        for x in range(rope_len-1):
            self.tail_pos.append(copy.copy(self.head_pos))
        self.tail_visited = set()
        
        
    def print_position(self):
        print(f'Head position:  {self.head_pos}')
        print(f'Tail position:  {self.tail_pos}')
    
    def move(self, instr):
        """Move head of tail in response to instructions"""
        direction = instr[0]
        distance = int(instr[1:])
        for steps in range(distance):
            if   direction == 'R':
                self.head_pos[0] += 1
            elif direction == 'L':
                self.head_pos[0] -= 1
            elif direction == 'U':
                self.head_pos[1] += 1
            elif direction == 'D':
                self.head_pos[1] -= 1
            # Now move tail in response to head
            self.tail_move()
            # add to record of spots visited
            self.tail_visited.add(tuple(self.tail_pos[-1]))
            # self.print_position()       

    def tail_move(self):
        """
        Tail moves in response to difference.  If greater than one space apart.
        Note that tail will always move to be in same axis in response to movement in that axis
        """
        new_tail = []
        for idx, tail in enumerate(self.tail_pos):
            knot = np.array(tail)
            prev_knot = np.array(self.head_pos) if idx == 0 else np.array(new_tail[idx-1])
            diff = prev_knot - knot
            movement = np.array([0,0])
            if abs(diff[0]) > 1 or abs(diff[1]) > 1:
                movement[0] = 1 if diff[0] > 1 else -1 if diff[0] < -1 else diff[0]
                movement[1] = 1 if diff[1] > 1 else -1 if diff[1] < -1 else diff[1]
            new_tail.append(list(np.add(knot,movement)))
        self.tail_pos = new_tail

def main():
    instr = rope_input(r'./data/d09.txt')

    # Part one
    r1 = rope()
    for i in instr:
        r1.move(i)
    print(f'Part 1 number of positions touched by tail: {len(r1.tail_visited)}')

    # Part two
    r2 = rope(rope_len=10)
    for i in instr:
        r2.move(i)
    print(f'Part 2 number of positions touched by tip of tail: {len(r2.tail_visited)}')

if __name__ == '__main__':
    main()

import numpy as np
import math

def tree_input(file):
    return np.genfromtxt(file, delimiter=1, dtype=int)

def edge_to_one(empty:np.array):
    """Set the edges of empty zero array to ones"""
    for idx, val in np.ndenumerate(empty):
        row, col = idx
        if row == 0 or row == (empty.shape[1] - 1) or\
           col == 0 or col == (empty.shape[1] - 1):
            empty[idx] = 1
    return empty   

def visible_trees(trees:np.array):
    """Create boolean matrix of trees visible (greater than) from perpendicular view outside"""
    visible = np.zeros(trees.shape, dtype=int)
    for idx, height in np.ndenumerate(trees):
        row, col = idx
        # Skip over edges
        if 0 < row < (trees.shape[0]-1) and \
           0 < col < (trees.shape[1]-1):
            # Now check whether value > maximum along any visible axis
            if height > trees[row, col+1:].max() or \
               height > trees[row, :col].max() or \
               height > trees[:row, col].max() or \
               height > trees[row+1:, col].max():
                visible[idx] = 1
    # Include edge trees
    visible = edge_to_one(visible)
    return visible

def scenic_score(trees:np.array):
    """Return matrix of scores for each tree"""
    # Empty score array
    scores = np.zeros(trees.shape, dtype=int)
    for idx, tree in np.ndenumerate(trees):
        row, col = idx
        # Number of visible trees in each direction from current tree
        visible = {'left':0, 'up':0, 'right':0,'down':0}
        # LEFT
        if col != 0: # skip first column as slice doesn't work going left
            for neighbour in trees[row, col-1::-1]:
                visible['left'] += 1
                if neighbour >= tree:
                    break
        # UP
        if row != 0: # skip first row as slice doesn't work going up
            for neighbour in trees[row-1::-1, col]:
                visible['up'] += 1
                if neighbour >= tree:
                    break
        # RIGHT
        for neighbour in trees[row, col+1::]:
            visible['right'] += 1
            if neighbour >= tree:
                break
        # DOWN
        for neighbour in trees[row+1::, col]:
            visible['down'] += 1
            if neighbour >= tree:
                break
        # Multiply and set scores to empy matrix
        scores[idx] = math.prod(visible.values())
    return scores


def main():
    trees = tree_input(r'./data/d08.txt')
    
    ## Part 1
    num_visible = visible_trees(trees).sum()
    print(f'The number visible (sum of boolean array): {num_visible}')
    
    ## Part 2
    score = scenic_score(trees).max()
    print(f'Highest scenic score available is {score}')

if __name__ == '__main__':
    main()
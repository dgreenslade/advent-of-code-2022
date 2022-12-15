import ast

def signal_input(file:set) -> list:
    signal = []
    with open(file) as f:
        # return f.readlines()
        pair = []
        for line in f:
            if line == '\n':
                signal.append(pair)
                pair = []
            else:
                pair.append(ast.literal_eval(line.strip()))
        signal.append(pair)
        return signal
        
def recurse_compare(left:list, right:list) -> bool:
    """ 
    Compare two lists, uses rules to determine whether in 
    correct order (i.e. left < right)
    """
    if right and not left:
        return True
    elif left and not right:
        return False 
    for idx1, l in enumerate(left):
        for idx2, r in enumerate(right):
            if idx1==idx2:
                # If both ints - compare 
                if type(l) == int and type(r) == int:
                    if l < r:
                        return True
                    elif l > r:
                        return False
                else:  # If not both ints, recurse into
                    ints_2_list = lambda x : [x] if type(x) == int else x
                    res = recurse_compare(ints_2_list(l), ints_2_list(r))
                    if res is not None:
                        return res 
    # Having compared component values, now if one list is longer
    if len(left) < len(right):
        return True
    elif len(left) > len(right):
        return False

def sort_signals(signal_list:list[list]) -> list:
    """
    Sort incoming list of lists into new list.  
    Allows use of obscure function to determine 
    sorting between two elements
    """
    sorted_signals = []
    for idx1, sig1 in enumerate(signal_list):
        if idx1 == 0:
            sorted_signals.append(sig1)
        else:
            insert_idx = None
            # Sort - go from highest value (-1) and contine down if less
            for i in range(len(sorted_signals),0,-1):
                if recurse_compare(sorted_signals[i-1], sig1):
                    insert_idx = i
                    break # incoming > present & highest in list. Insert one index above here
                elif i == 1:
                    insert_idx = 0
                    break # Passed against smallest. So nsert new at start
                else:
                    pass # incoming is < present, continue checking down list
            sorted_signals.insert(insert_idx, sig1)
    return sorted_signals


def main():
    signal = signal_input('./data/d13.txt')

    ## Part 1
    correct_order = []
    for idx, line in enumerate(signal):
        l, r = line
        # print(f'------------')
        # print(f'SIGNAL : {idx}')
        # print(l, r)
        order = recurse_compare(l,r)
        correct_order.append(order)
        # print(f'{order} order')
    score = 0
    for idx, bool in enumerate(correct_order):
        if bool == True:
            score += idx + 1
    print(f'--Part 1\nSum of indices of lines in correct order: {score}')

    ## Part 2
    # Combine all signals into single list rather than pairs
    all_signals = []
    for line in signal:
        all_signals.extend(line)
    # Add distress signal packets
    all_signals.append([[2]])
    all_signals.append([[6]])   
    # Sort
    sorted_signals = sort_signals(all_signals)
    # find distress packes:
    distress_1 = sorted_signals.index([[2]]) + 1
    distress_2 = sorted_signals.index([[6]]) + 1
    print(f'--Part 2\nProduct of indices (+1) of two distress signals in sorted signal: {distress_1 * distress_2}')

if __name__ == '__main__':
    main()
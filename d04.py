def input_pairs(file:str)->list:
    """Return nested list of integers"""
    with open(file) as f:
        input = []
        pairs = [line.rstrip().split(',') for line in f]
        for pair in pairs:
            ranges = [y.split('-') for y in pair]
            #convert to integers
            ranges = [[int(a), int(b)] for a,b in ranges]
            input.append(ranges)
    return input

def convert_to_sets(pairs):
    new_pairs = []
    for pair in pairs:
        sections = [set(range(x[0],x[1]+1)) for x in pair]
        new_pairs.append(sections)
    return new_pairs

def p1_section_covered(pairs):
    num_subsets = 0
    for x in pairs:
        if x[0] & x[1] == x[0] or \
           x[0] & x[1] == x[1]:
            num_subsets += 1
    return num_subsets

def p2_pair_overlaps(pairs):
    num_overlaps = 0
    for x in pairs:
        if x[0].isdisjoint(x[1]) is False:
            num_overlaps += 1
    return num_overlaps

def main():
    pairs = input_pairs(r'./data/d04.txt')
    pairs = convert_to_sets(pairs)
    p1 = p1_section_covered(pairs)
    p2 = p2_pair_overlaps(pairs)

    print(f'The number of pairs with assignment sections completely covered: {p1}')
    print(f'The number of pairs with assignment section overlaps: {p2}')

if __name__ == "__main__":
    main()
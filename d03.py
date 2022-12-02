import string

def input_bags(file:str)->list:
    with open(file) as f:
        bags = [line.rstrip() for line in f]
    return bags

def bag_pockets(bag:str)->list:
    """Take list of strings, split each string halfway. Return list of halves(list)"""
    half = len(bag)//2
    bag_pockets = [bag[:half], bag[half:]]
    return bag_pockets

def three_groups(bags:list)->list:
    """Take single list and group into lists of 3 sublists"""
    for i in range(0, len(bags), 3):
        yield bags[i:i+3]

def common_element_priorities(string_list:list)->list:
    """Given a list of strings, find the common characters from all. Return summed priority score"""
    string_sets = [set(x) for x in string_list]
    common = string_sets[0].intersection(*string_sets)
    # List of letters in order of priority
    alpha = string.ascii_letters[:52]
    score = 0
    for x in common:
        # alphabet priority starts at 1, unlike index, so +1
        score += alpha.find(x) + 1
    return score

def part_one_score(bags:list)->int:
    total_score = 0
    for bag in bags:
        pockets = bag_pockets(bag)
        score = common_element_priorities(pockets)
        total_score += score
    return total_score

def part_two_score(bags:list)->int:
    total_score = 0
    for group in three_groups(bags):
        score = common_element_priorities(group)
        total_score += score
    return total_score

def main():
    bags = input_bags('./data/d03.txt')

    # Score for common items within bag pockets
    p1_score = part_one_score(bags)
    print(f'Summed score for common items between pockets of each bag: \n{p1_score}')

    # Score for common items between groups of three bags
    p2_score = part_two_score(bags)
    print(f'Summed score for common items between groups of three bags: \n{p2_score}')

if __name__ == "__main__":
    main()
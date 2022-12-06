def input_datastream(file:str)->str:
    """File is one long string of random characters"""
    with open(file) as f:
        datastream = f.read()
    return datastream

def identify_marker(datastream:str,set_size:int)-> tuple:
    """
    iterates through string and identifies first instance where there 
    are {set_size} unique characters (the packet/message marker) and the 
    index after that (the beginning of the content)
    """
    i = 0
    while i < len(datastream):
        marker = datastream[i:i+set_size]
        if len(set(marker)) == set_size:
            return (i+set_size), marker
        else:
            i += 1

def main():
    datastream = input_datastream(r'./data/d06.txt')

    # Length of markers for both part 1 and part 2
    p1_marker_len = 4
    p2_marker_len = 14

    for x in [p1_marker_len, p2_marker_len]:
        # Print both part results
        index, marker = identify_marker(datastream, x)
        print(f'---{x} repeating characters \nNumber of chars until start of packet {index}')
        print(f'Marker content: {marker}')

if __name__ == '__main__':
    main()
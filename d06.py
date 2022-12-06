def input_datastream(file:str)->str:
    """Return nested list of integers"""
    with open(file) as f:
        datastream = f.read()
    return datastream

def identify_marker(datastream:str,set_size:int):
    """identifies idx & unique slices of strings"""
    i = 0
    while i < len(datastream):
        marker = datastream[i:i+set_size]
        if len(marker) == len(set(marker)):
            return (i+set_size), marker
        else:
            i += 1

def main():
    datastream = input_datastream(r'./data/d06.txt')

    # Sample data
    # tst = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'
    # index, marker = identify_marker(tst, 4)
    # print(f'Number of characters for start of packet: {index}')
    # print(f'Marker content: {marker}')

    # Part 1 marker
    index, marker = identify_marker(datastream, 4)
    print(f'---4 repeating characters \nNumber of chars until start of packet {index}')
    print(f'Marker content: {marker}')

    # Part 2 marker 
    index, marker = identify_marker(datastream, 14)
    print(f'---14 repeating characters \nNumber of chars until start of message {index}')
    print(f'Marker content: {marker}')


if __name__ == '__main__':
    main()
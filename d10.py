def instructions_input(file):
    with open(file) as file:
        return file.read().splitlines()

class CathodeRay():
    """Holds cathoderay object."""
    def __init__(self,cycle_breaks=None,screen_width=40):
        self.cycle = 0
        self.register = 1
        self.cycle_breaks = cycle_breaks
        self.screen_width = screen_width
        self.scores = []
        self.crt_row = ''
        self.crt = []

    def compute(self, instruc:str) -> None:
        """Follow instructions - updates cycle number then updates register if necessary"""
        if instruc == 'noop':
            self.update_cycle()
        elif instruc[:4] == 'addx':
            self.update_cycle()
            self.update_cycle()
            self.register += int(instruc[5:])

    def update_cycle(self) -> None:
        """Progresses cycles and adds result to CRT row"""
        if self.cycle%self.screen_width in range(self.register-1,self.register+2):
            self.crt_row += '#'
        else:
            self.crt_row += '.'
        self.cycle += 1
        self.check_cycle()
    
    def check_cycle(self) -> None:
        """If meets end of cycle break (CRT row) add to scores & CRT monitor list"""
        if self.cycle in self.cycle_breaks:
            self.scores.append(self.cycle * self.register)
            self.crt.append(self.crt_row)
            self.crt_row = ''

    def print_screen(self) -> None:
        """Prints results of CRT monitor at whatever stage. To be run after all instructions"""
        for row in self.crt:
            print(row)


def main():
    instrs = instructions_input(r'./data/d10.txt')

    # Part 1
    cycles = [x for x in range(20,221,40)]
    c1 = CathodeRay(cycle_breaks=cycles)
    for i in instrs:
        c1.compute(i)
    print(sum(c1.scores))

    # Part 2
    cycles = [x for x in range(0,240,40)]
    c2 = CathodeRay(cycle_breaks=cycles, screen_width=40)
    for i in instrs:
        c2.compute(i)
    c2.print_screen()


if __name__=='__main__':
    main()
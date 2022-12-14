import re
import operator
from functools import reduce
import copy

def monkey_input(file:str) -> list:
    """ Parse monkey input.  Almost YAML but not quite.  Use linebreaks to separate"""
    all = []
    a = {}
    with open(file) as f:
        for line in f:
            l = re.findall(r'[^\s\:\,]+',line) # split on every separator
            if not l: # empty line
                all.append(a)
                a = {}
            elif l[0] == 'Monkey':
                a['id'] = int(l[1])
            elif l[0] == 'Starting':
                a['items'] = [int(x) for x in l[2:]]
            elif l[0] == 'Operation':
                a['change'] = l[3:]
            elif l[0] == 'Test':
                a['div_test'] = int(l[3])
            elif l[1] == 'true':
                a['true_recipient'] = int(l[-1])
            elif l[1] == 'false':
                a['false_recipient'] = int(l[-1])
        all.append(a)
        return all

def str_to_operation(num1:float, oper:str, num2:float):
    """Converts a string operator to an evaluation"""
    allowed_operators={
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "//": operator.floordiv
    }
    return allowed_operators[oper](num1, num2)

class Monkey:
    """ Individual monkey - all properties from input.  Methods to inspect & throw and catch"""

    def __init__(
            self, 
            id:int, 
            items:list, 
            change:list, 
            div_test:int, 
            true_recipient:int, 
            false_recipient:int,
            worry_div=3,
            super_modulo:int=None
    ):
        self.id = id
        self.items = items
        self.change = change
        self.div_test = div_test
        self.true_recipient = true_recipient
        self.false_recipient = false_recipient
        self.worry_div = worry_div
        self.items_inspected = 0
        self.super_modulo = super_modulo if not None else None
    
    def inspect_item(self, item:int) -> int:
        """Changes item based on monkey rules"""
        oper, n = self.change[1:]
        try:
            num = int(n)
        except(ValueError): # 'old' rather than int
            num = item
        changed = str_to_operation(item, oper, num)
        changed //= self.worry_div
        # Compress item value so  does not grow too big for memory after 1000 rounds
        if self.super_modulo is not None:
            changed = changed % self.super_modulo
        return changed

    def throw_items(self) -> list[tuple]:
        """Extracts item from list, inspects and throws"""
        thrown = []
        for i in range(len(self.items)):
            item = self.items.pop(0)
            self.items_inspected += 1
            inspected = self.inspect_item(item)
            if inspected % self.div_test == 0:
                thrown.append((self.true_recipient, inspected))
            else:
                thrown.append((self.false_recipient, inspected))
        return thrown

    def catch_item(self, item:tuple[int]) -> None:
        """Checks whether item is for this monkey.  Input is (monkey_id, item)"""
        if item[0] == self.id:
            self.items.append(item[1])
        else:
            pass # not meant for this monkey

    def __str__(self):
        return \
            f'\t...Monkey:{self.id}\n' +\
            f'\titems: {self.items}\n' +\
            f'\toperation: {self.change}\n' +\
            f'\tdivision test: {self.div_test}\n' +\
            f'\tfalse test throw receiver: {self.false_recipient}\n' +\
            f'\ttrue test throw receiver: {self.true_recipient}\n' +\
            f'\tfalse test throw receiver: {self.false_recipient}\n' +\
            f'\tworry divisor: {self.worry_div}\n' +\
            f'\tsuper modulo: {self.super_modulo}\n' +\
            f'\tnumber of items inspected: {self.items_inspected}\n'          


class MonkeyBarrel:
    """Class to hold all monkey objects in and a few wrapper methods"""

    def __init__(self,monkeys=None):
        self.monkeys = [] if monkeys is None else monkeys
        self.inspections = []
        self.score = None
    
    def monkey_throws(self) -> None:
        """Conduct a full round of throws for all monkeys."""
        for monkey in self.monkeys:
            thrown=monkey.throw_items()
            for item in thrown:
                for monkey_catcher in self.monkeys:
                    monkey_catcher.catch_item(item)

    def set_super_modulo(self) -> None:
        """
        Need to update this value for each monkey object.  
        It is common multiplied div_test amongst all monkeys.
        Allows us to compress ints while still passing tests in same way
        """
        all_div_tests = []
        for monkey in self.monkeys:
            all_div_tests.append(monkey.div_test)
        super_modulo = reduce(operator.mul, all_div_tests, 1)
        for monkey in self.monkeys:
            monkey.super_modulo = super_modulo
        
    def set_worry_div(self, worry:int) -> None:
        """Change the worry level for our monkeys"""
        for monkey in self.monkeys:
            monkey.worry_div=worry

    def get_inspections(self) -> list:
        inspections = []
        for monkey in self.monkeys:
            inspections.append(monkey.items_inspected)
        self.inspections = inspections
        return self.inspections

    def get_score(self) -> int:
        """Return score - product of top two numbers from final expection numbers"""
        if self.inspections == []:
            raise ValueError('Need to set inspections with .get_inspections() first')
        sorted_inspections = sorted(self.inspections, reverse=True)
        score = reduce(operator.mul, sorted_inspections[:2], 1)
        self.score = score
        return self.score

    def print_monkeys(self) -> None:
        for monkey in self.monkeys:
            print(monkey)


def main():
    monkey_attrs = monkey_input(f'./data/d11.txt')
    
    # Two groups for each problem part
    monkeybarrel1 = MonkeyBarrel()
    monkeybarrel2 = MonkeyBarrel()
    # Add monkeys from input to monkey groups
    for m in monkey_attrs:
        monkey = Monkey(\
            m['id'], \
            m['items'], \
            m['change'], \
            m['div_test'], \
            m['true_recipient'], \
            m['false_recipient']
        )
        monkeybarrel1.monkeys.append(monkey)
        monkeybarrel2.monkeys.append(copy.deepcopy(monkey)) # Copy otherwise P1 effects P2 objs.

    # Part 1 - 20 rounds
    for turn in range(20):
        monkeybarrel1.monkey_throws()
    print(f'Part 1: Final inspection numbers per monkey: {monkeybarrel1.get_inspections()}')
    print(f'Part 1: Multiplication of top two: {monkeybarrel1.get_score()}')

    # Part 2 - 10000 rounds
    monkeybarrel2.set_worry_div(1) # Update worry so divides by 1 instead of 3
    monkeybarrel2.set_super_modulo() # Compress item ints at each throw otherwise become too big
    # monkeybarrel2.print_monkeys()
    for turn in range(10000):
        monkeybarrel2.monkey_throws()
    print(f'Part 2: Final inspections per monkey compressed by supermodulo: {monkeybarrel2.get_inspections()}')
    print(f'Part 2: Multiplication of top two: {monkeybarrel2.get_score()}')

if __name__ == "__main__":
    main()
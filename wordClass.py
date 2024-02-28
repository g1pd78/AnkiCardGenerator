import collections

class DefinitionContainer:
    def __init__(self, definitions = [], examples = collections.defaultdict(list)) -> None:
        self.definitions = definitions
        self.examples = examples

    def __add__(self, other):
        if isinstance(other, DefinitionContainer):
            return DefinitionContainer(self.definitions + other.definitions, self.examples + self.examples)
        else:
            raise TypeError("Unsupported operand type for +")
        
    def __bool__(self):
        if self.definitions:
            return True
        return False
        
    def __repr__(self) -> str:
        view = str(self.definitions)
        return view

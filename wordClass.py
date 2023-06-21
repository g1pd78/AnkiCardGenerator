import collections

class Word:
    def __init__(self) -> None:
        self.definitions = []
        self.examples = collections.defaultdict(list)
class Lexical:
    def __init__(self):
        self.main = None
        self.prefix = None
        self.infix = None
        self.suffix = None
        self.possible_tags = []
class LexicalRules:
    def __init__(self):
        self.rules = []
    def add_lexical(self,lexical):
        self.rules.append(lexical)
    def get_lexical_rules(self):
        with open("lexical_rules.txt","r") as f:
            for line in f:
                lex = Lexical()
                string = line.strip().split(" ",4)
                lex.main = string[0]
                lex.prefix = string[1] if(string[1]!="_") else None
                lex.infix = string[2] if(string[2]!="_") else None
                lex.suffix = string[3] if(string[3]!="_") else None
                lex.possible_tags = string[4].split()
                self.add_lexical(lex)
        return self.rules

Johnny = LexicalRules()
Johnny.get_lexical_rules()

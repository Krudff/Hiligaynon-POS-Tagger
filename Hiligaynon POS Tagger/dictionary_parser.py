class Word:
    def __init__(self):
        self.content = None
        self.tags = []
    def add_tags(self,tag):
        self.tags.append(tag)
###############################################################################
class Dictionary:
    def __init__(self):
        self.words=[]
    def add_word(self,word):
        self.words.append(word)
    def get_size(self):
        return len(self.words)
    def is_valid(self,words):
        for i in words:
            if(i not in["NOUN","VERB","ADV","ADJ","PRON","DET","ADP","NUM","CONJ","PRT"]):
                return False
        return True
    def get_dictionary(self):
        with open("dictionary.txt","r") as f:
            for line in f:
                word = Word()
                string = line.strip().split("/")
                word.content = string[0].strip()
                word.tags = string[1].split(" ")
                self.add_word(word)
        return self.words
        
webster = Dictionary()
webster.get_dictionary()
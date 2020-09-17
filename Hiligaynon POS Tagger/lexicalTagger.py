from nltk.tokenize import sent_tokenize, word_tokenize,TweetTokenizer
from lexical_parser import LexicalRules
from dictionary_parser import Word, Dictionary
from pickle import load
##############################################################################
dictionary = Dictionary().get_dictionary()
lexical_rules = LexicalRules().get_lexical_rules()
##############################################################################
def tokenizeByTweet():
    tokenizer_words = TweetTokenizer()
    tokens_sentences = [tokenizer_words.tokenize(t) for t in sent_tokenize(getText())]
    return tokens_sentences
###
def tokenizeBySent():
    sent_text = sent_tokenize(getText())
    return sent_text
###
def getText():
    temp = ''
    with open("hiligaynon_corpora_input.txt","r") as f:
        for line in f:
            temp += line
    return temp
###Returns a Boolean
def dictionary_find(word):
    for i in dictionary:
        if(i.content == word):
            return True
    return False 
###Receives string and Returns a List of string
def dictionary_tags(word):
    for i in dictionary:
        if(i.content.lower() == word.lower()):
            return i.tags
    return []
###Returns a List of Words
def convert_to_words_with_tags(words):
    sentence = []
    for i in words:
        w = Word()
        w.content = i
        sentence.append(w)
    return sentence
###Returns a List of string
def lexical_tags(word):
    tags = []
    #lexical rules loop
    for i in lexical_rules:
        tags.extend(prefix_search(i,word))
        tags.extend(suffix_search(i,word))
    return tags
###Uses Lexical and Word datatypes, returns list of string
def prefix_search(lexical,word):
    tags = []
    #Checks if prefix is not Nonetype
    if(lexical.prefix is not None):
        #checks if X2 is in the word
        if("X2V2" in lexical.prefix):
            #for intellectual sentences that repeat the first two syllables only
            possible_tags=[]
            temp = word.content[len(lexical.prefix)-4:]
            #checks if first 2 letters is equal to the actual first 2 letters
            if(temp[0:2] == temp[2:4]):
                possible_tags = dictionary_tags(temp[2:])
            #checks if applicable
            if(lexical.main in possible_tags):
                tags.extend(lexical.possible_tags)
        elif("X2" in lexical.prefix):
            #dis is for uganda!!!
            #for repeating words
            possible_tags = []
            if("-" in word.content):
                #standard X2 conditional
                if((word.content[len(lexical.prefix)-2:word.content.find("-")]==word.content[word.content.find("-")+1:])):
                    possible_tags = dictionary_tags(word.content[word.content.find("-")+1:])
                #for both suffix and prefix
                elif(lexical.prefix and lexical.suffix):
                    
                    if(lexical.prefix[:-2]==word.content[:len(lexical.prefix)-2] and lexical.suffix==word.content[-len(lexical.suffix):]): 
                        temp = word.content[len(lexical.prefix)-2:-len(lexical.suffix)]
                        possible_tags = dictionary_tags(temp[temp.find("-")+1:])
            elif("-" not in word.content):
                # plus two since logic ☺☺
                # same as above, but without da '-' since maybe they forgot??
                w_index=int((len(word.content)-len(lexical.prefix)+2)/2)
                possible_tags = dictionary_tags(word.content[-w_index:])
            if(lexical.main in possible_tags):
                tags.extend(lexical.possible_tags)
        #for special cases of hybrid words on prefix version
        elif(lexical.prefix == "SPECIAL"):
            if("-" in word.content):
                possible_tags = dictionary_tags(word.content[:word.content.find("-")])
                if(lexical.main in possible_tags):
                    tags.extend(lexical.possible_tags)
        #checks if rule applies to any word
        elif(lexical.main == "ANY"):
            if(lexical.prefix.lower() == word.content[:len(lexical.prefix)].lower() and (len(lexical.prefix)<len(word.content))):
                tags.extend(lexical.possible_tags)
        #checks the prefix and infix combination
        elif(lexical.prefix and lexical.infix):
            #first checks prefix
            if(lexical.prefix == word.content[:len(lexical.prefix)]):
                #remove prefix temporarily
                temp1 = word.content[len(lexical.prefix):]
                #remove infix
                if(lexical.infix == temp1[1:1+len(lexical.infix)]):
                    #remove infix temporarily
                    temp2 = temp1[0]+temp1[1+len(lexical.infix):]
                    #searches root
                    possible_tags = dictionary_tags(temp2)
                    if(lexical.main in possible_tags):
                        tags.extend(lexical.possible_tags)
                    
        #checks if prefix is in word.content
        if(lexical.prefix.lower() == word.content[:len(lexical.prefix)].lower()):
            #strips prefix and search dictionary for the tags, and then put on possible tags variable
            possible_tags = dictionary_tags(word.content[len(lexical.prefix):])
            #checks if lexical main tag in possible_tags
            if(lexical.main in possible_tags):
                tags.extend(lexical.possible_tags)
    return tags
###Uses Lexical and Word datatypes, returns list of string
def suffix_search(lexical,word):
    tags = []
    #Checks if suffix is not Nonetype
    if(lexical.suffix is not None):
        #checks if suffix is in word.content
        if(lexical.suffix.lower() == word.content[-len(lexical.suffix):]):
            #strips suffix and search dictionary for the tags, then put on possible tags variable
            possible_tags = dictionary_tags(word.content[:-len(lexical.suffix)])
            if(lexical.main in possible_tags):
                tags.extend(lexical.possible_tags)
        #hybrid words suffix version
        if(lexical.suffix == "SPECIAL"):
            if("-" in word.content):
                possible_tags = dictionary_tags(word.content[word.content.find("-")+1:])
                if(lexical.main in possible_tags):
                    tags.extend(lexical.possible_tags)
    return tags
###Checks if symbol
def is_symbol(word):
    return word in r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
###
def is_number(word):
    return word.isdigit()
###Main Function
def tagWord(word):
    word.tags = dictionary_tags(word.content)
    if(word.tags == []):
        return lexical_tags(word).pop('NOUN')
    if(is_symbol(word.content)):
        return '.'
    if(is_number(word.content)):
        return 'NUM'
    else:
        return 'NOUN'
def taggerSentence(sentence):
    bigList = []
    # Convert string to Word list datatype
    words = convert_to_words_with_tags(word_tokenize(sentence))
    # loops the Word list
    for i in words:
        i.tags = dictionary_tags(i.content)
        if(i.tags == []):
            i.tags.extend(lexical_tags(i))
        if(is_symbol(i.content)):
            i.tags.append(".")
        if(is_number(i.content)):
            i.tags.append("NUM")
        if(i.tags == []):
            i.tags.append("NOUN")
        bigList.append(tuple([i.content,i.tags[0]]))
    return bigList
sent = taggerSentence(tokenizeBySent()[24])
#print(tokenizeBySent()[6])
print(sent)
Input = open('Brill(Revised).pickle', 'rb')
tagger = load(Input)
Input.close()
#print(tagger.tag(word_tokenize(tokenizeBySent()[24])))
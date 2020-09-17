#Imported Libraries
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize,TweetTokenizer
from difflib import get_close_matches as closeWords
from tkinter.ttk import Progressbar
from tkinter.simpledialog import askstring
from tkinter import filedialog,messagebox
import tkinter
from pickle import load,dump
#Imported Python Files
from lexical_parser import LexicalRules
from dictionary_parser import Word, Dictionary
##############################################################################
#Classes
dictionary = Dictionary().get_dictionary()
lexical_rules = LexicalRules().get_lexical_rules()
##############################################################################
properTags = ["NOUN","VERB","ADV","ADJ","PRON","DET","ADP","NUM","CONJ","PRT","."]

recommendations = ""
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
            temp = word.content[len(lexical.prefix)-4:].lower()
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
                    possible_tags = dictionary_tags(word.content[word.content.find("-")+1:].lower())
                #for both suffix and prefix
                elif(lexical.prefix and lexical.suffix):
                    
                    if(lexical.prefix[:-2]==word.content[:len(lexical.prefix)-2].lower() and lexical.suffix==word.content[-len(lexical.suffix):]): 
                        temp = word.content[len(lexical.prefix)-2:-len(lexical.suffix)].lower()
                        possible_tags = dictionary_tags(temp[temp.find("-")+1:])
            elif("-" not in word.content):
                # plus two since logic ☺☺
                # same as above, but without da '-' since maybe they forgot??
                w_index=int((len(word.content)-len(lexical.prefix)+2)/2)
                possible_tags = dictionary_tags(word.content[-w_index:].lower())
            if(lexical.main in possible_tags):
                tags.extend(lexical.possible_tags)
        #for special cases of hybrid words on prefix version
        elif(lexical.prefix == "SPECIAL"):
            if("-" in word.content):
                possible_tags = dictionary_tags(word.content[:word.content.find("-")].lower())
                if(lexical.main in possible_tags):
                    tags.extend(lexical.possible_tags)
        #checks if rule applies to any word
        elif(lexical.main == "ANY"):
            if(lexical.prefix.lower() == word.content[:len(lexical.prefix)].lower() and (len(lexical.prefix)<len(word.content))):
                tags.extend(lexical.possible_tags)
        #checks the prefix and infix combination
        elif(lexical.prefix and lexical.infix):
            #first checks prefix
            if(lexical.prefix == word.content[:len(lexical.prefix)].lower()):
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
        #checks the prefix and suffix combination
        elif(lexical.prefix and lexical.suffix):
            #first checks prefix
            if(lexical.prefix == word.content[:len(lexical.prefix)].lower()):
                #remove prefix temporarily
                temp1 = word.content[len(lexical.prefix):]
                #remove infix
                if(lexical.suffix == temp1[-len(lexical.suffix):]):
                    #remove infix temporarily
                    temp2 = temp1[0:-len(lexical.suffix)]
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
def is_number(word):
    return word.isdigit()
def readFile(filename):
    words = []
    with open(filename) as file:
        for line in file:
            words.append(line)    
    file.close()
    return words
def createDict(fileName,delimiter):
    dictionary = dict()
    for i in readFile(fileName):
        temp = i.split('/')
        dictionary.update({temp[0]:temp[1].split()})
    return dictionary
def loadTagger(filename):
    Input = open(filename, 'rb')
    tagger = load(Input)
    Input.close()
    return tagger
###Main Function
tagger = loadTagger('Hiligaynon tagger.pickle')
diction = createDict('dictionary.txt','/')
def progress(val,total):
    bar['value'] = (val/total)*100
    bar.update()
def sentencesTagger(sentences):
    total,current,output = 0,0,""
    for sent in sentences:#Check length
        total += len(word_tokenize(sent))
    for sent in sentences:
        output += sentenceTagger(sent,current,total)+"\n"
        current += len(sent)
    return output
def sentenceTagger(sentence,current,total):
    output_text = []
    # Convert string to Word list datatype
    words = convert_to_words_with_tags(word_tokenize(sentence))
    # loops the Word list
    recommended = ""
    lel = 1
    index = 0
    contextualTags = tagger.tag(word_tokenize(sentence))
    for i in words:
        progress(current+lel,total)
        finalTag=None
        print("\n")
        print(lel,end=")  ")
        print(i.content)
        i.tags = []
        if i.content[0].isupper() and index != 0 and contextualTags[index-1][1] != '.':
            i.tags.append("NOUN")
        if(i.tags == []):
            i.tags = dictionary_tags(i.content.lower())
            print("Dictionary Tag: ",i.tags)
        if(i.tags == []):
            i.tags.extend(lexical_tags(i))
            print("Lexical Tag: ", lexical_tags(i))
        if(is_symbol(i.content)): 
            i.tags.append(".")
        if(is_number(i.content)):
            i.tags.append("NUM")
        if i.tags==[]:
            finalTag = contextualTags[index][1]
            print("Contextual Tag [1st]: ",finalTag) 
        print("Test point [Dict and Lex]: ",i.tags)
        if len(set(i.tags)) != 1:
            print("Test point [Context]: ",contextualTags[index][1])
            if contextualTags[index][1] in i.tags:
                finalTag = contextualTags[index][1]#Choose contextual
            if finalTag == None and i.tags!=[]:#If there are many tags but no lexical
                finalTag = i.tags[0]
                print("Possible Tag [Many]: ",finalTag)
            if finalTag==None:#If default no tag
                print("Default Tag: ",finalTag)
                finalTag="NOUN"
            if i.tags!=[] and finalTag!=None:#if contextual does not match with lexical
                if finalTag not in i.tags+["NOUN"]:
                    print("Changes in tags ", finalTag, " to ", i.tags)
                    finalTag=i.tags[0]
        else:#If there is only one tag
            finalTag = i.tags[0]
        if finalTag == "NOUN" and i.content.lower() not in diction.keys():
            near = closeWords(i.content, diction.keys(),n=2)
            if len(near):
                recommended += i.content+' = '+" ".join(near)+'\n'
        print("Final Tag: ", finalTag)
        print('Contextual Tags: ',contextualTags)
        output_text.append(str(tuple([i.content,finalTag])))
        lel+=1
        index+=1
    if len(recommended):
        global recommendations
        recommendations = recommended
    print(output_text)
    print(sentence)
    return "  ".join(output_text)
def readPerLine(filename):
    try:
        sentences = ""
        with open(filename) as file:
            for line in file:
                sentences += line
        file.close()
        return sentences
    except FileNotFoundError:
        return
##################### U s e r   I n t e r f a c e #############################
main = tkinter.Tk()
#main box declaration
main.title("Hiligaynon Parts-of-Speech Tagger")
#title declaration
def file_save(output):
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    f.write(output)
    f.close()
def run(event=None):
    # command for the run button
    temp = sentencesTagger(sent_tokenize(input_text.get()))
    output_text.config(state="normal")#to enable editing for a moment
    output_text.delete("1.0",tkinter.END)#delete all text in the textbox
    output_text.insert("1.0",temp)#insert new batch of tagged data
    output_text.config(state="disabled")#disable editing
def append_text(data):
    with open("Hiligaynon Corpus with tags.txt", "a") as myfile:
        myfile.write("\n"+data+"\n"+data)
def select_file():
    #command to select file
    filename = tkinter.filedialog.askopenfilename(title="Select File",filetype=(("text files","*.txt"),))
    #the comma in the filetype parameter is necessary because python said so
    sentences = sent_tokenize(readPerLine(filename))
    output = sentencesTagger(sentences)
    if messagebox.askquestion('Create File','Do you want to create an output txt file for the output?') == 'yes':
    	file_save(output)
    output_text.config(state="normal")#to enable editing for a moment
    output_text.delete("1.0",tkinter.END)#delete all text in the textbox
    output_text.insert("1.0",output)#insert new batch of tagged data
    output_text.config(state="disabled")#disable editing
    print(output)
    #add code here
def help_command():
    showMessage('Help',"Run - tag the contents in the text box \nOpen - tag the text inside the selected file\nAdd - Add contextual sentences with tags. Format (word/tag)\nTags - Shows the corresponding equivalent of tags\nDisclaimer - Shows that the program does not guarantee a 100% accuracy\nRecommend - Shows the possible words for an unrecognized word")
def open_tags():
    showMessage('Tags',readPerLine('Tags.txt'))
def disclaimer():
    showMessage('Disclaimer','The program does not assure a 100% accuracy in tagging the given input.\nOnly Hiligaynon word are recognized by the program.\nAll Rights Reserved.')
def add_data():
    data = checkData(askstring('Add sentence', 'Add sentence. Please check proper data. Format (word/tag). (e.g.: Ang/DET kabaw/NOUN ./.)'))
    if data != False:
        append_text(data)
def recommend_words():
	if recommendations.rstrip() == "":
		showMessage('Recommended','No words to be recommended!')
	else:
		showMessage('Recommended',recommendations)
def showError(title,message):
    tkinter.messagebox.showerror(title,message)
def showMessage(title,message):
    tkinter.messagebox.showinfo(title,message)
def checkData(data):
    try:
        temp = data.split()
        words,tags = [],[]
        for i in temp:
            word = i.split('/')
            words.append(word[0])
            tags.append(word[1])
        if len(words) == len(tags) and len(words): #Check if there are same amount of tags added
            if len(set(tags) - set(properTags)): #If there are invalid tags added
                showError('Invalid Format','Input with invalid tags.')
                return False
            else:
                showMessage('Input Complete','Input data added to corpus!')
                return data
    except Exception:
        if len(data.rstrip()):
            showError('Invalid Format','Please fix data format.')
        return False
def readCorpus(filename):
    corpus = []
    with open(filename) as file:
        for line in file:
            sentences = []
            for pair in line.split():
                sentences.append(tuple(pair.split('/')))
            corpus.append(sentences)
    file.close()
    return corpus

#Toolbars
toolbar = tkinter.Menu(main)
toolbar.add_command(label="Run",command = run)
toolbar.add_command(label="Open",command = select_file)
toolbar.add_command(label="Help", command = help_command)
toolbar.add_command(label="Disclaimer", command = disclaimer)
toolbar.add_command(label="Tags", command = open_tags)
toolbar.add_command(label="Add", command = add_data)
toolbar.add_command(label="Recommend", command = recommend_words)
#toolbar.add_command(label="Train", command = train_data)
#do not put brackets on function because it causes errors

input_text = tkinter.Entry(main,width=60)#input

frame= tkinter.Frame(main,width=360,height=200)#to restrict the geometry of output_text

output_text = tkinter.Text(frame,wrap="word")#output
output_text.config(state="disabled")#disable editing

input_text.pack(pady=20,padx=20)

output_text.place(x=0,y=0,height=200,width=360)
frame.pack()#pack frame

main.bind('<Return>',run)
main.resizable(False,False)
main.geometry("400x300") # define width and height of window
main.config(menu=toolbar)

bar = Progressbar(main,orient="horizontal",length=300,mode="determinate")
bar.pack(pady = 10)
#display menu
main.mainloop()
################## E n d   o f   U s e r   I n t e r f a c e ##################

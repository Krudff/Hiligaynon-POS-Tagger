def readPerLine(filename):
    corpus = []
    with open(filename) as file:
        for line in file:
            sentences = []
            for pair in line.split():
                sentences.append(tuple(pair.split('/')))
            corpus.append(sentences)
    file.close()    
    return corpus
corpus = readPerLine('Hiligaynon Corpus with tags.txt') 
words = dict()
unique = set()

for i in corpus:
    for j in i:
        unique.add(j[0])
        if j[0] not in words.keys():
            words.update({j[0]:dict()})
        if j[1] not in words[j[0]]:
            words[j[0]].update({j[1]:0})
        words[j[0]][j[1]] += 1
freq = dict()
for i in unique:
    freq.update({i:0})
for i in corpus:
    for j in i:
        freq[j[0]] += 1
sortByFreq = sorted(freq,key = freq.get,reverse=True)
file = open('Frequency Report.txt','w') 
for i in sortByFreq:
    file.write(str(i)+': '+str(freq[i])+' '+str(words[i])+'\n')
file.close()

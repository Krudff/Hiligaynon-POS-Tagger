def readPerLine(filename):
    sentences = []
    with open(filename) as file:
        for line in file:
            extract = line.split('=')
            sentences.append((extract[0]).lower()+'='+extract[1])
    file.close()
    return sentences
a = readPerLine('dictionary.txt')
a.sort()
print(a)
file = open('sortedDictionary.txt', "w")
for i in a:
    file.write(i)
file.close()
        	
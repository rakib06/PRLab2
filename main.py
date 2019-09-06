from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import string
import math

#global variables
names=[]
a=[]
b=[]
mainfile=[]
file=[]
testfile=[]
categories=[]
total_training_word=[]
cat=[]
token=[]
testtoken=[]
priorProbability=[]
token2=[]
filtered_word=[]
last_words=[]
total_category=[]
count=0
testcategory=[]
testname=[]
trainFile = ''
n = ''
filename = ''
def inputStart(file):
    global n,trainFile,filename
    n=int(input("Enter the value of Test size:"))
    filename  = file
    #filename = 'bioCorpus.txt'
    trainFile=open(filename).read()

inputStart('bioCorpus.txt')

#Tokeinze them word by word
tokenized_word=word_tokenize(trainFile)
#All in small Letter
for w in tokenized_word:
    filtered_word.append(w.lower())

with open(filename, "r") as input:
    text= input.read().split("\n\n" or '\n\n\n')
#Saving The original Copy in other File:
mainfile=text


#Tokenize By sentence:
for i in range(len(text)-6):
    text[i]=sent_tokenize(text[i])
    file.append(text[i])


#Converting in String:
for i in range(len(file)):
    file[i]=str(file[i])


#Splitting it by New Line
for i in range(len(file)):
    file[i]=file[i].split('\\n')


#All Categories with Index
for i in range(len(file)):
    if ((str(file[i][0])).isspace()):
        categories.append(str(file[i][2]))
        names.append(str(file[i][1]))
    else:
        categories.append(str(file[i][1]))
        names.append(str(file[i][0]))

#StrippingOut all WhiteSpaces from categories:
for i in range(len(categories)):
    item = categories[i].strip()
    item=item.lower()
    categories[i] = item


#non Duplicate Categories saved in Cat:
cat=list(categories)
for item in range(len(cat)):
    i=cat[item].strip()
    cat[item]=i.lower()
cat=list(dict.fromkeys(cat))


#Calculating PriorProbabilities of Ever Class:
for i in range(len(cat)):
    count=0
    for j in range(len(categories)):
        if cat[i]==categories[j]:
            count+=1
    priorProbability.append(count/(len(categories)+1))

#Working with File:

#Removing All White Space:
for i in range(len(file)):
    for j in range(len(file[i])):
        item=str(file[i][j]).strip()
        file[i][j]=item
#All_Stop Words are conceting
stp_words=list(stopwords.words("english"))
#removing all white space from names
for i in range(len(names)):
    item=str(names[i])
    item=item.strip()
    names[i]=item
names=str(names)
names=names.split()
#removing all punction from names
for i in range(len(names)):
    item=str(names[i])
    item=item.translate(str.maketrans('','',string.punctuation))
    item=item.lower()
    names[i]=item

#Concatening All stop Words
stop_words=open('stopwords.txt').read()
stop_words=word_tokenize(stop_words)
stop_words=list(stop_words)
stop_words=list(stop_words+stp_words)
stop_words=list(stop_words+names)


#Tokenize Word By Word And save it to Token:
for i in range(len(file)):
    item=file[i]
    item=str(item)
    item=word_tokenize(item)
    token.append(item)

#Lower Case
for i in range(len(token)):
    for j in range(len(token[i])):
        token[i][j]=token[i][j].lower()

for i in range(len(token)):
    token[i]=str(token[i])
    token[i]=token[i].translate(str.maketrans('','',string.punctuation))
    token[i]=token[i].split()

#removing all whilespace from token

for i in range(len(token)):
    for j in range(len(token[i])):
        item=str(token[i][j]).strip()
        token[i][j]=item
tokennew=[[] for i in range(len(token))]


#removing All stopWords from Token:
for i in range(len(token)):
    for w in token[i]:
        if w not in stop_words:
            tokennew[i].append(w)

#Now TokenNew Has all The Letters with 1st index is as it's category
allWord=[[] for i in range(len(cat))]
for i in range(len(cat)):
    for j in range(len(tokennew)):
        if(cat[i]==tokennew[j][0]):
            allWord[i].append(tokennew[j])
allWordnew=[[] for i in range(len(allWord))]
for i in range(len(allWord)):
    for j in range(len(allWord[i])):
        for k in range (len(allWord[i][j])):
            if k==0:
                continue
            allWordnew[i].append(allWord[i][j][k])

#Removing the Category word from the List
for i in range(len(cat)):
    item=cat[i]
    j=0
    length=len(allWordnew[i])
    while(j<length):
        if(allWordnew[i][j]==item):
            allWordnew[i].remove(item)
            length=length-1
            continue
        j=j+1
#saving all training word in one array
for i in range(len(allWordnew)):
    for j in range(len(allWordnew[i])):
        total_training_word.append(allWordnew[i][j])


#Counting every element:
#All Distinct Element:
allWordnewDist=[[] for i in range(len(allWordnew))]
for i in range(len(allWordnew)):
    allWordnewDist[i]=list(dict.fromkeys(allWordnew[i]))

#Now Counting every element and save it to countDist array:
countDist=[[] for i in range(len(allWordnewDist))]
for i in range(len(allWordnewDist)):
    counter=0
    a=allWordnewDist[i]
    b=allWordnew[i]

    for j in range(len(a)):
        counter=0
        for k in range(len(b)):
            if(a[j]==b[k]):
                counter+=1
        countDist[i].append(counter)

#Total Class_number
for i in range(len(cat)):
    count=0
    for j in range(len(categories)):
        if(cat[i]==categories[j]):
            count+=1
    total_category.append(count)
#Now Making Freq_T
freq_t=[[] for i in range(len(countDist))]
for i in range(len(total_category)):
    for j in range(len(countDist[i])):
        ab=countDist[i][j]/total_category[i]
        freq_t[i].append(ab)

######## 3.1 Step 1 Has Ended...freq_t has the thing!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Step 2:
 # calculating P(C)--->with Logarithm
p_c=[]
for i in range(len(priorProbability)):
    p_c.append(-(math.log2(priorProbability[i]+.1)/(((len(cat)*.1))+1)))

 #calculating L(w|c)-->logarithm
p_wc=[[] for i in range(len(freq_t))]
p_wc1=[[] for i in range(len(freq_t))]
for i in range(len(freq_t)):
    for j in range(len(freq_t[i])):
        temp=(freq_t[i][j]+.1)/(1+2*.1)
        p_wc[i].append(-(math.log2(temp)))
        p_wc1[i].append(temp)

#....................................###Testing##...................................
with open(filename, "r") as input:
    test= input.read().split("\n\n" or '\n\n\n')
    maintest=test

#Tokenize By sentence:
for i in range(n):
    test[i+15]=sent_tokenize(test[i+15])
    testfile.append(test[i+15])

#Converting in String:
for i in range(len(testfile)):
    testfile[i]=str(testfile[i])

#Splitting it by New Line
testcategories=[]
for i in range(len(testfile)):
    testfile[i]=testfile[i].split('\\n')
for i in range(len(testfile)):
    item=testfile[i][1]
    item=item.lower()
    testcategories.append(item)

#All Categories with Index
for i in range(len(file)):
    if ((str(file[i][0])).isspace()):
        categories.append(str(file[i][2]))
        names.append(str(file[i][1]))
    else:
        categories.append(str(file[i][1]))
        names.append(str(file[i][0]))
#StrippingOut all WhiteSpaces from categories:
for i in range(len(categories)):
    item = categories[i].strip()
    item=item.lower()
    categories[i] = item

#Working with testFile:

#Removing All White Space:
for i in range(len(testfile)):
    for j in range(len(testfile[i])):
        item=str(testfile[i][j]).strip()
        testfile[i][j]=item
#Tokenize Word By Word And save it to testtoken:
for i in range(len(testfile)):
    item=testfile[i]
    item=str(item)
    item=word_tokenize(item)
    testtoken.append(item)

#Lower Case
for i in range(len(testtoken)):
    for j in range(len(testtoken[i])):
        testtoken[i][j]=testtoken[i][j].lower()

for i in range(len(testtoken)):
    testtoken[i]=str(testtoken[i])
    testtoken[i]=testtoken[i].translate(str.maketrans('','',string.punctuation))
    testtoken[i]=testtoken[i].split()

#removing all whilespace from testtoken

for i in range(len(testtoken)):
    for j in range(len(testtoken[i])):
        item=str(testtoken[i][j]).strip()
        testtoken[i][j]=item

testtokennew=[[] for i in range(len(testtoken))]

#removing All stopWords from testtoken:
for i in range(len(testtoken)):
    for w in testtoken[i]:
        if w not in stop_words:
            testtokennew[i].append(w)
testcategory=[]
#Removing the Category word from the List
for i in range(n):
    item=testtokennew[i][0]
    testcategory.append(item)
    j=0
    length=len(testtokennew[i])
    while(j<length):
        if(testtokennew[i][j]==item):
            testtokennew[i].remove(item)
            length=length-1
            continue
        j=j+1

#removing all elements that are not in training set
for i in range(n):
    for w in testtokennew[i]:
        if w not in total_training_word:
            testtokennew[i].remove(w)
#removing all the duplicates
for i in range(len(testtokennew)):
    testtokennew[i]=list(dict.fromkeys(testtokennew[i]))
l_cb=[]
p_sum=0
psum=0
total_lcb=[[] for i in range(n)]
total_pcb=[[] for i in range(n)]
for i in range(n):
    a=testtokennew[i]
    for j in range (len(cat)):
        b=allWordnew[j]
        p_sum=0
        psum=0
        for w in a:
            if w in b:
                index=b.index(w)
                p_sum=p_sum+p_wc[j][index]
                psum=psum+p_wc1[j][index]
        total_lcb[i].append(p_sum)
        total_pcb[i].append(psum)
for i in range(len(total_lcb)):
    for j in range(len(total_lcb[i])):
        total_lcb[i][j]=total_lcb[i][j]+p_c[j]
        total_pcb[i][j]=total_pcb[i][j]*priorProbability[j]
category=[]
for i in range(len(total_lcb)):
    a=total_lcb[i]
    maxpos=a.index(max(a))
    category.append(cat[maxpos])
percent=0
rightPrediction = 0;
for i in range(n):
    print(testtoken[i][0],testtoken[i][1],'Precdiction=',category[i], ' Original=',testcategories[i])
    category[i] = category[i].replace(" ", "")
    testcategories[i] = testcategories[i].replace(" ", "")
    if category[i]== testcategories[i]:
        rightPrediction+=1
        print("Right")
    print(cat[0],total_pcb[i][0],cat[1],total_pcb[i][1],cat[2],total_pcb[i][2],cat[3],total_pcb[i][3],"\n")

print("Overall Accuracy: ", rightPrediction ,"out of ",n, " = ",rightPrediction/n)


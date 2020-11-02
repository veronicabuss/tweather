# this script is first testing of textblob package
# make textblob imports
from textblob import TextBlob

print('*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*\/*')
print('hello world')

testH = 'this is a fun test string and i am very happy'
testM = 'this test is horrible and i am extremely mad'

fname = 'testTEXT.txt'          # test text from file
fid = open(fname,'r')
fstring = fid.read().lower()
print(fstring)

#sUse = testH
#sUse = testM
sUse = fstring

sUseTB = TextBlob(sUse)
print(sUseTB.tags)
print(sUseTB.sentiment)
print(sUseTB.sentiment.polarity)
print(sUseTB.sentiment.subjectivity)

print(sUseTB.sentences)
xx = sUseTB.sentences

print('1111111111111111111111111')
#sentiment for each sentence
for ii in range(len(xx)-1):
    print(xx[ii])
    x = str(xx[ii])
    xxTB = TextBlob(x)
    print(xxTB.sentiment)


print(sUseTB.word_counts['i'])


#end of script
print('*/\*/\*/\*/\*/\*/\*/\*/\*/\*/\*/\*/\*/\*/\*/\*/\*/\*/\*/\*/\*/\*/\*/\*')#
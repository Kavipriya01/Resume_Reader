import docx2txt
import io
import nltk
from nltk.corpus import stopwords
import re
import numpy as np


filename=r"C:\Users\Kavi Priya\MY_PROJECTS\RESUME_READER\Resume_1.docx"
text=docx2txt.process(filename)
with open("docxdata.txt","w") as f:
    f.write(text)


print("\n\n\n\n\*******************************************************\n\n\n\n")
stop=stopwords.words('english')
docu="docxdata.txt"



def find_mobile_num(text):
     r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
     #r=re.compile(r'(\D?(\d{0,3}?)\D{0,2}(\d{3})?\D{0,2}(\d{3})\D?(\d{4})$)')
     phone_numbers = r.findall(text)
     for number in phone_numbers:
             return re.sub(r'\D', '', number) 

def find_email(text):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(text)

def pre_pro(docu):
    doc=''.join([i for i in docu.split() if i not in stop ])
    sentences=nltk.sent_tokenize(doc)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences=[nltk.pos_tag(sent) for sent in sentences]
    return sentences

def name(text):
    names = []
    sentences =pre_pro(text)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names


mobile_num=find_mobile_num(text)
names=name(text)
print(names)
print(find_email(text))
print(mobile_num)





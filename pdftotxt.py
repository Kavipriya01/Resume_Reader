import PyPDF2
import textract
import io
import os
#from pdfminer.pdfinterp import PDFPageInterpreter
#from pdfminer.pdfinterp import PDFResourceManager
#from pdfminer.pdfpage import PDFPage
#import slate
import nltk
from nltk.corpus import stopwords
import re
import numpy as np
import pandas as pd



#file_path=r"C:\Users\Kavi Priya\MY_PROJECTS\RESUME_READER\Resume_1.pdf"
filename="Resume_mine.pdf"

os.system("pdftotext {} {}".format(filename, "pdfdata.txt"))

    

stop=stopwords.words('english')
docu="pdfdata.txt"

with open("pdfdata.txt","r") as f:
    text=f.read() 




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
email=find_email(text)
print(email)
print(mobile_num)

#np.savetxt("pdf_op.csv",[p for p in zip(find_email,mobile_num)],delimiter="," , fmt="%s")

np.savetxt("pdf_op.csv",(names,email,mobile_num),delimiter=",",fmt="%s")

data=pd.DataFrame({'email':email,'mobile_num':[mobile_num],'names':[names]})

writer=pd.ExcelWriter('pdf_op.xlsx', engine='xlsxwriter')

data.to_excel(writer, sheet_name='Sheet1')
writer.close()
'''
workbook = xlsxwriter.Workbook('pdf_op.xlsx') 
worksheet = workbook.add_worksheet()
for data in enumerate(email):
    worksheet.write_column(data)
workbook.close()
'''








# writing data in variable
#pdftotext Resume_1.pdf  pdfdata.txt
 
#text = os.popen("pdftotext {}".format(filename)).read() 
#print(text)  

'''
with open(filename) as f:
    doc=slate.PDF(f,password="",just_text=1)
    for page in doc:
        print(page)

def pdfdata(filename):
    re_ma=PDFResourceManager
    file_handle=io.StringIO()
    convert=TextConverter(re_ma,file_handle)
    page_intp=PDFPageInterpreter(re_ma,convert)
    with open(filename,"rb") as f:
        for page in PDFPage.get_pages(f,caching=True,check_extractable=True):
            page_intp.process_page(page)
        text=file_handle.getvalue()       
    convert.close()
    file_handle.close()
    return text
       
pdfdata(filename)

'''



'''
pdfobj=open(filename,"rb")

pdfreader=PyPDF2.PdfFileReader(pdfobj)

pages=pdfreader.numPages
count=0
text=""

while count<pages:
    pageobj=pdfreader.getPage(count)
    count+=1
    text=pageobj.extractText().split("\n")
    print(text)
    for i in range(len(text)):
        with open("pdfdata.txt","a+") as txt_file:
            txt_file.write(text[i])    
    print()

#print(text)
print(pages)

line_count=0
pdffile=open(filename,"rb")
while 1:
    buffer=pdffile.read(8192*1024)
    if not buffer:
        break
    line_count += buffer.count("\n")

line_count=len(open(filename).readlines( ))    
#pdffile.close()  
print(line_count)  

'''

#text=textract.process(r"C:\Users\Kavi Priya\MY_PROJECTS\RESUME_READER\Resume_1.pdf")
#print(text)
'''
with open("Resume_1.pdf","rb") as f:
    text=pdftotext.PDF(f)
'''






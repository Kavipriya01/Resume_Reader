import os
from flask import Flask,render_template,request,redirect,make_response,send_file,send_from_directory
from werkzeug.utils  import secure_filename
import PyPDF2
import textract
import io
import os
import docx2txt
import nltk
from nltk.corpus import stopwords
import re
import numpy as np
import pandas as pd

#from werkzeug.classes import FileStorage
app=Flask(__name__)

app.config["allowed_file_formats"]=['pdf','docx']
app.config["upload_folders"]="./"

def pdftotext(pdffile):
    os.system("pdftotext {} {}".format(pdffile, "pdfdata.txt"))
    stop=stopwords.words('english')
    fname="pdfdata.txt"

    with open("pdfdata.txt","r") as f:
        text=f.read() 
    def find_mobile_num(text):
        r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
        #r=re.compile(r"(\+\d{1,2})?[\s.-]?\d{3}[\s.-]?\d{4}")
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

    def extract_linkedin_url(fname):
        with open(fname) as f:
            return re.findall('http[s]?://www.linkedin(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', f.read())

    mobile_num=find_mobile_num(text)
    names=name(text)
    email=find_email(text)
    linkedin_link=extract_linkedin_url(fname)

    np.savetxt("pdf_op.csv",(names,email,mobile_num,linkedin_link),delimiter=",",fmt="%s")

    data=pd.DataFrame({'email':email,'mobile_num':[mobile_num],'names':[names],'linkedin':[linkedin_link]})

    writer=pd.ExcelWriter('pdf_op.xlsx', engine='xlsxwriter')

    data.to_excel(writer, sheet_name='Sheet1')
    writer.close()


    return names,mobile_num,email,linkedin_link

def docxtotext(pdffile):
    text=docx2txt.process(pdffile)
    fname="docxdata.txt"
    with open("docxdata.txt","w") as f:
        f.write(text)
    stop=stopwords.words('english')
    #docu="docxdata.txt"
    def find_mobile_num(text):
        r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
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
    def extract_urls(fname):
        with open(fname) as f:
            return re.findall('http[s]?://www.linkedin.com(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', f.read())

    mobile_num=find_mobile_num(text)
    names=name(text)
    print(names)
    email=find_email(text)
    linkedin_link=extract_urls(fname)
    np.savetxt("docx_op.csv",(names,email,mobile_num,linkedin_link),delimiter=",",fmt="%s")

    data=pd.DataFrame({'email':email,'mobile_num':[mobile_num],'names':[names],'linkedin':[linkedin_link]})

    writer=pd.ExcelWriter('docx_op.xlsx', engine='xlsxwriter')

    data.to_excel(writer, sheet_name='Sheet1')
    writer.close()
    return names,mobile_num,email,linkedin_link

def valid_file(filename):
    if not '.' in filename:
        return False
    name=filename.rsplit('.',1)[1]
    if name.lower() in app.config["allowed_file_formats"]:
        val=True
        extension=name.lower()
    else:
        val=False
        extension=None
    return val,extension
'''class FileStorage():
    def fun(self,filename):
         fun_var=filename.read()
         return fun_var     

def get_pdf(pdf_file):
    binary_pdf=get_binary_pdf_data_from_database()
    response=make_response(binary_pdf)
    response.headers['content-type']='application/pdf/docx'
    response.headers['content-Disposition']= 'inline; filename= %s.pdf' % 'yourfilename' 
    return response

def return_file(fun_file):
    return send_from_directory(app.config["upload_folders"],fun_file)
'''
@app.route('/')
def hello():
    return render_template("file_upload.html")


@app.route('/file_upload',methods=['GET','POST'])
def file_upload():
    validity=" "
    name=" "
    num=" "
    email=" "
    linkedin_link=" "
    if request.method =="POST":
        resume=request.files["file"]
        
        if resume.filename =="":
            validity= "The uploaded file must contain a name"
        val,extension=valid_file(resume.filename)    
        if val ==True:
            #temp_var=FileStorage()
            #validity=temp_var.fun(resume)
            secure_file=secure_filename(resume.filename)
            #org_file=open(secure_file,"wb")
            resume.save(os.path.join(app.config["upload_folders"],secure_file))
            validity="Good"
            if extension == 'pdf':
                name,num,email,linkedin_link=pdftotext(resume.filename)
            elif extension == 'docx':
                name,num,email,linkedin_link=docxtotext(resume.filename)
        else:
            validity=".pdf or .docx types of files only accepted for resume"
    if validity == "Good":
        return render_template("after_file_upload_success.html" ,name=name,num=num,email=email,linkedin_link=linkedin_link)
    else:
        return render_template("after_file_upload.html" , validity=validity)
@app.route('/csv_download')
def csv_download():
    path="pdf_op.csv"  
    return send_file(path,as_attachment=True)
@app.route('/xlsx_download')    
def xlsx_download():
    path="pdf_op.xlsx"  
    return send_file(path,as_attachment=True)    

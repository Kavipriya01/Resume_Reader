
import re

file_lines=[]
urls=[]
line_count=0
text_char_count=0
with open("pdfdata.txt","rt") as myfile:
    for line in myfile:
        line_count+=1
        file_lines.append(line.rstrip("\n"))
#print(file_lines)  
print(line_count)      
for element in file_lines:
    print(element)
    #r= re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+$',element)
    r=re.compile(r'[http://www.linkedin.].[0-9a-zA-Z/]+')
    urls.append(r.findall(element))
    #print(get_net_target(element))
    #match = re.search('<a +href="(.+?)" *>',element)
    #if match:
       # print(match.group(1))
    #for word in element:
        #print(word)
        #text_char_count+=1
#print(text_char_count)    
#print(urls)
fname="pdfdata.txt"
def extract_urls(fname):
    with open(fname) as f:
        return re.findall('http[s]?://www.linkedin.com(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', f.read())
print(extract_urls(fname))        

'''

with open('pdfdata.txt',"r") as f:
    text = f.read()
    links = re.findall('"((http)s?://.*?)"',text)
for url in links:
    print(url[0])


#href_regex = r'href=[\'"]?([^\'" >]+)'
#url = re.findall(href_regex, text)

#print(url)

from urlextract import URLExtract

extractor = URLExtract()
with open("pdfdata.txt","r") as f:
    text=f.read()
    urls = extractor.find_urls(text)
print(urls)
'''
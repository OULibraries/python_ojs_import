import csv
import xml.etree.ElementTree as ET
import ojs_builder

importlist=[]
input_file = csv.DictReader(open("import.csv"))
issues=[]
articles=dict()
sections={}
for i in input_file:
    importlist.append(i)

for importdict in importlist:
    if 'authorEmail1' not in importdict:
        importdict['authorEmail1']=''
    if 'authorEmail2' not in importdict:
        importdict['authorEmail2']=''
    if 'href' not in importdict:
        importdict['href']='http://ul-theatreorgan.s3-website-us-east-1.amazonaws.com/pdf/'

ET.register_namespace("", "http://pkp.sfu.ca")
tb=ET.TreeBuilder()
tb.start("issue",{"xmlns":"http://pkp.sfu.ca", "xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance", "xsi:schemaLocation":"http://pkp.sfu.ca native.xsd"})
ojs_builder.buildIdentification(tb,importlist[0])
ojs_builder.buildSections(tb,importlist[0])

tb.start("articles", {})

for i in importlist:
    ojs_builder.buildArticle(tb,i)
    tb.end("article")

tb.end("articles")
tb.end("issue")
tree=ET.ElementTree()
tree._setroot(tb.close())

tree.write('importfile.xml')

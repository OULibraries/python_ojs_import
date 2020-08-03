from os import remove
import csv
import xml.etree.ElementTree as ET


def buildSections(children):
    """
    Build OJS Sections XML Element

    Parameters:
    children (dict): A Dictionary containing section key,value pairs for OJS import

    Returns:
    Element: XML Element Object containing OJS Sections
    """
    tb=ET.TreeBuilder()
    tb.start("sections",{})
    for i in children:
        tb.start("section", {"ref":i['sectionAbbrev']})
        tb.start("abbrev",{})
        tb.data(i['sectionAbbrev'])
        tb.end("abbrev")
        tb.start("policy",{})
        tb.end("policy")
        tb.start("title",{})
        tb.data(i['sectionTitle'])
        tb.end("title")
        tb.end("section")
    tb.end("sections")
    return(tb.close())

def buildIdentification(children):
    """
    Build OJS Identification XML Element

    Parameters:
    children (dict): A Dictionary containing section key,value pairs for OJS import

    Returns:
    Element: XML Element Object containing OJS Identification
    """
    
    tb=ET.TreeBuilder()
    tb.start("issue_identification",{})
    tb.start("volume",{})
    tb.data(children['issueVolume'])
    tb.end("volume")
    tb.start("number",{})
    tb.data(children['issueNumber'])
    tb.end("number")
    tb.start("year",{})
    tb.data(children['issueYear'])
    tb.end("year")
    tb.start("title",{})
    tb.data(children['issueTitle'])
    tb.end("title")
    tb.end("issue_identification")
    return tb.close()

def buildPublication(children):
    """
    Build OJS Publication XML Element

    Parameters:
    children (dict): A Dictionary containing section key,value pairs for OJS import

    Returns:
    Element: XML Element Object containing OJS Publication
    """

    tb=ET.TreeBuilder()
    tb.start("date_published",{})
    tb.data(children['issueDatepublished'])
    tb.end("date_published")
    return tb.close()




def buildArticle(children):
    """
    Build OJS Article XML Element

    Parameters:
    children (dict): A Dictionary containing section key,value pairs for OJS import

    Returns:
    Element: XML Element Object containing OJS Article
    """
    
    tb=ET.TreeBuilder()
    tb.start("articles",{})
    tb.start("article", {"section_ref": children['sectionAbbrev'],"stage": "production",
                        "date_published": children['issueDatepublished'],
                        "seq": children['seq']})
    tb.start("title",{})
    tb.data(children['title'])
    tb.end("title")
    tb.start("abstract",{})
    tb.data(children['abstract'])
    tb.end("abstract")
    # Subject/Keywords are seperated by a ';' in the spreadsheet therefore parse it
    if('keywords' in children):
        keywordAry = children['keywords'].split(';')
        tb.start('subjects',{})
        for k in keywordAry:
            tb.start('subject',{})
            tb.data(k)
            tb.end("subject")
        tb.end("subjects")
    else:
        tb.start("subjects",{})
        tb.start("subject",{})
        tb.end("subject")
        tb.end("subjects")
    tb.start("authors",{})
    tb.start("author",{"user_group_ref":"Author"})
    tb.start("givenname",{})
    tb.data(children['authorgivenname1'])
    tb.end("givenname")
    tb.start("familyname",{})
    tb.data(children['authorfamilyname1'])
    tb.end("familyname")
    tb.start("affiliation",{})
    tb.data(children['authorAffiliation1'])
    tb.end("affiliation")
    tb.start("email",{})
    tb.data(children['authorEmail1'])
    tb.end("email")
    tb.end("author")
    tb.start("author",{"user_group_ref":"Author"})
    tb.start("givenname",{})
    tb.data(children['authorgivenname2'])
    tb.end("givenname")
    tb.start("familyname",{})
    tb.data(children['authorfamilyname2'])
    tb.end("familyname")
    tb.start("affiliation",{})
    tb.data(children['authorAffiliation2'])
    tb.end("affiliation")
    tb.start("email",{})
    tb.data(children['authorEmail2'])
    tb.end("email")
    tb.end("author")
    tb.end("authors")
    tb.start("submission_file",    {"id": children['seq'], "stage":"proof"})
    tb.start("revision", {"genre": children['fileGenre1'],"number": children['seq'],
    "filetype": "application/pdf", "filename": children['file1']})
    tb.start("name",{});
    tb.data(children['file1']);
    tb.end("name");
    tb.start("href", {"src": "http://ul-theatreorgan.s3-website-us-east-1.amazonaws.com/pdf/"+ children['file1']
    ,"mime_type": "application/pdf"})
    tb.end("href");
    tb.end("revision");
    tb.end("submission_file");
    tb.start("article_galley",{});
    tb.start("id",{});
    tb.data(children['seq']);
    tb.end("id");
    tb.start("name",{});
    tb.data("PDF");
    tb.end("name");
    tb.start("seq",{});
    tb.data(children['seq']);
    tb.end("seq");
    tb.start("submission_file_ref",{"id": children['seq'],"revision": children['seq']});
    tb.end("submission_file_ref");
    tb.end("article_galley");
    tb.start("pages",{});
    tb.data(children['pages']);
    tb.end("pages");
    tb.end("article");
    tb.end("articles")
    return tb.close()

#####
# Takes a CSV and parses it into a Python Dict containing Key,Value Mappings from CSV
# The Dict is then passed to XML builder functions
# The final XML Tree that is build is then dumped to a file for import into OJS
#
# Parameters:
# import.csv: CSV containing OJS fields to conver to XML
# conversion.xml: Resulting XML document for OJS Import 
#####
importlist=[]
input_file = csv.DictReader(open("import.csv"))
issues=[]
articles=dict()
sections={}
for i in input_file:
    importlist.append(i)

for m in importlist:
    issues.append(m['issueTitle'])

issues = set(issues)

for it in issues:
    sections[it]=[]

    for o in importlist:
        if o['issueTitle']==it:
            section= {"sectionTitle":o['sectionTitle'], "sectionAbbrev":o['sectionAbbrev']}
            sections[it].append(section)

with open("pyout.xml", "w") as f:
    f.write("<?xml version=\"1.0\"?><issues xmlns=\"http://pkp.sfu.ca\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://pkp.sfu.ca native.xsd\"></issues>")


ET.register_namespace("", "http://pkp.sfu.ca")
article = ET.parse("pyout.xml")

root = article.getroot()
for importdict in importlist:
    articles[importdict['issueTitle']]=importdict

articles=set(articles)
tr=ET.TreeBuilder()
tr.start("issue",{})
tr.end("issue")
issue=(tr.close())

for importdict in importlist:
    if 'authorEmail1' not in importdict:
        importdict['authorEmail1']=''
    if 'authorEmail2' not in importdict:
        importdict['authorEmail2']=''

    tr=ET.TreeBuilder()
    tr.start("issue",{})
    tr.end("issue")
    issue=(tr.close())
    issue.append(buildIdentification(importdict))
    issue.append(buildPublication(importdict))
    issue.append(buildSections(sections[importdict['issueTitle']]))
    issue.append(buildArticle(importdict))
    root.append(issue)

article.write("conversion.xml")
remove("pyout.xml")

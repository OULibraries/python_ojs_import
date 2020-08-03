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
    xmlTreeBuilder = ET.TreeBuilder()
    xmlTreeBuilder.start("sections",{})
    for i in children:
        xmlTreeBuilder.start("section", {"ref":i['sectionAbbrev']})
        xmlTreeBuilder.start("abbrev",{})
        xmlTreeBuilder.data(i['sectionAbbrev'])
        xmlTreeBuilder.end("abbrev")
        xmlTreeBuilder.start("policy",{})
        xmlTreeBuilder.end("policy")
        xmlTreeBuilder.start("title",{})
        xmlTreeBuilder.data(i['sectionTitle'])
        xmlTreeBuilder.end("title")
        xmlTreeBuilder.end("section")
    xmlTreeBuilder.end("sections")
    return(xmlTreeBuilder.close())

def buildIdentification(children):
    """
    Build OJS Identification XML Element

    Parameters:
    children (dict): A Dictionary containing section key,value pairs for OJS import

    Returns:
    Element: XML Element Object containing OJS Identification
    """
    
    xmlTreeBuilder = ET.TreeBuilder()
    xmlTreeBuilder.start("issue_identification",{})
    xmlTreeBuilder.start("volume",{})
    xmlTreeBuilder.data(children['issueVolume'])
    xmlTreeBuilder.end("volume")
    xmlTreeBuilder.start("number",{})
    xmlTreeBuilder.data(children['issueNumber'])
    xmlTreeBuilder.end("number")
    xmlTreeBuilder.start("year",{})
    xmlTreeBuilder.data(children['issueYear'])
    xmlTreeBuilder.end("year")
    xmlTreeBuilder.start("title",{})
    xmlTreeBuilder.data(children['issueTitle'])
    xmlTreeBuilder.end("title")
    xmlTreeBuilder.end("issue_identification")
    return xmlTreeBuilder.close()

def buildPublication(children):
    """
    Build OJS Publication XML Element

    Parameters:
    children (dict): A Dictionary containing section key,value pairs for OJS import

    Returns:
    Element: XML Element Object containing OJS Publication
    """

    xmlTreeBuilder = ET.TreeBuilder()
    xmlTreeBuilder.start("date_published",{})
    xmlTreeBuilder.data(children['issueDatepublished'])
    xmlTreeBuilder.end("date_published")
    return xmlTreeBuilder.close()




def buildArticle(children):
    """
    Build OJS Article XML Element

    Parameters:
    children (dict): A Dictionary containing section key,value pairs for OJS import

    Returns:
    Element: XML Element Object containing OJS Article
    """
    
    xmlTreeBuilder = ET.TreeBuilder()
    xmlTreeBuilder.start("articles",{})
    xmlTreeBuilder.start("article", {"section_ref": children['sectionAbbrev'],"stage": "production",
                        "date_published": children['issueDatepublished'],
                        "seq": children['seq']})
    xmlTreeBuilder.start("title",{})
    xmlTreeBuilder.data(children['title'])
    xmlTreeBuilder.end("title")
    xmlTreeBuilder.start("abstract",{})
    xmlTreeBuilder.data(children['abstract'])
    xmlTreeBuilder.end("abstract")
    # Subject/Keywords are seperated by a '' in the spreadsheet therefore parse it
    if('keywords' in children):
        keywordAry = children['keywords'].split('')
        xmlTreeBuilder.start('subjects',{})
        for k in keywordAry:
            xmlTreeBuilder.start('subject',{})
            xmlTreeBuilder.data(k)
            xmlTreeBuilder.end("subject")
        xmlTreeBuilder.end("subjects")
    else:
        xmlTreeBuilder.start("subjects",{})
        xmlTreeBuilder.start("subject",{})
        xmlTreeBuilder.end("subject")
        xmlTreeBuilder.end("subjects")
    xmlTreeBuilder.start("authors",{})
    xmlTreeBuilder.start("author",{"user_group_ref":"Author"})
    xmlTreeBuilder.start("givenname",{})
    xmlTreeBuilder.data(children['authorgivenname1'])
    xmlTreeBuilder.end("givenname")
    xmlTreeBuilder.start("familyname",{})
    xmlTreeBuilder.data(children['authorfamilyname1'])
    xmlTreeBuilder.end("familyname")
    xmlTreeBuilder.start("affiliation",{})
    xmlTreeBuilder.data(children['authorAffiliation1'])
    xmlTreeBuilder.end("affiliation")
    xmlTreeBuilder.start("email",{})
    xmlTreeBuilder.data(children['authorEmail1'])
    xmlTreeBuilder.end("email")
    xmlTreeBuilder.end("author")
    xmlTreeBuilder.start("author",{"user_group_ref":"Author"})
    xmlTreeBuilder.start("givenname",{})
    xmlTreeBuilder.data(children['authorgivenname2'])
    xmlTreeBuilder.end("givenname")
    xmlTreeBuilder.start("familyname",{})
    xmlTreeBuilder.data(children['authorfamilyname2'])
    xmlTreeBuilder.end("familyname")
    xmlTreeBuilder.start("affiliation",{})
    xmlTreeBuilder.data(children['authorAffiliation2'])
    xmlTreeBuilder.end("affiliation")
    xmlTreeBuilder.start("email",{})
    xmlTreeBuilder.data(children['authorEmail2'])
    xmlTreeBuilder.end("email")
    xmlTreeBuilder.end("author")
    xmlTreeBuilder.end("authors")
    xmlTreeBuilder.start("submission_file",    {"id": children['seq'], "stage":"proof"})
    xmlTreeBuilder.start("revision", {"genre": children['fileGenre1'],"number": children['seq'],
    "filetype": "application/pdf", "filename": children['file1']})
    xmlTreeBuilder.start("name",{})
    xmlTreeBuilder.data(children['file1'])
    xmlTreeBuilder.end("name")
    xmlTreeBuilder.start("href", {"src": "http://ul-theatreorgan.s3-website-us-east-1.amazonaws.com/pdf/"+ children['file1']
    ,"mime_type": "application/pdf"})
    xmlTreeBuilder.end("href")
    xmlTreeBuilder.end("revision")
    xmlTreeBuilder.end("submission_file")
    xmlTreeBuilder.start("article_galley",{})
    xmlTreeBuilder.start("id",{})
    xmlTreeBuilder.data(children['seq'])
    xmlTreeBuilder.end("id")
    xmlTreeBuilder.start("name",{})
    xmlTreeBuilder.data("PDF")
    xmlTreeBuilder.end("name")
    xmlTreeBuilder.start("seq",{})
    xmlTreeBuilder.data(children['seq'])
    xmlTreeBuilder.end("seq")
    xmlTreeBuilder.start("submission_file_ref",{"id": children['seq'],"revision": children['seq']})
    xmlTreeBuilder.end("submission_file_ref")
    xmlTreeBuilder.end("article_galley")
    xmlTreeBuilder.start("pages",{})
    xmlTreeBuilder.data(children['pages'])
    xmlTreeBuilder.end("pages")
    xmlTreeBuilder.end("article")
    xmlTreeBuilder.end("articles")
    return xmlTreeBuilder.close()

#####
# Takes a CSV and parses it into a Python Dict containing Key,Value Mappings from CSV
# The Dict is then passed to XML builder functions
# The final XML Tree that is build is then dumped to a file for import into OJS
#
# Parameters:
# import.csv: CSV containing OJS fields to conver to XML
# conversion.xml: Resulting XML document for OJS Import 
#####
importlist = []
input_file = csv.DictReader(open("import.csv"))
issues = []
articles = dict()
sections = {}
for row in input_file:
    importlist.append(row)

for issueTitle in importlist:
    issues.append(issueTitle['issueTitle'])

issues = set(issues)

for issueTitle in issues:
    sections[issueTitle]=[]

    for row in importlist:
        if row['issueTitle'] == issueTitle:
            section = {"sectionTitle":row['sectionTitle'], "sectionAbbrev":row['sectionAbbrev']}
            sections[issueTitle].append(section)

with open("pyout.xml", "w") as f:
    f.write("<?xml version=\"1.0\"?><issues xmlns=\"http://pkp.sfu.ca\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://pkp.sfu.ca native.xsd\"></issues>")


ET.register_namespace("", "http://pkp.sfu.ca")
article = ET.parse("pyout.xml")

root = article.getroot()
for importdict in importlist:
    articles[importdict['issueTitle']] = importdict

articles = set(articles)
xmlTree = ET.TreeBuilder()
xmlTree.start("issue",{})
xmlTree.end("issue")
issue = (xmlTree.close())

for importdict in importlist:
    if 'authorEmail1' not in importdict:
        importdict['authorEmail1'] = ''
    if 'authorEmail2' not in importdict:
        importdict['authorEmail2'] = ''

    xmlTree = ET.TreeBuilder()
    xmlTree.start("issue",{})
    xmlTree.end("issue")
    issue = (xmlTree.close())
    issue.append(buildIdentification(importdict))
    issue.append(buildPublication(importdict))
    issue.append(buildSections(sections[importdict['issueTitle']]))
    issue.append(buildArticle(importdict))
    root.append(issue)

article.write("conversion.xml")
remove("pyout.xml")

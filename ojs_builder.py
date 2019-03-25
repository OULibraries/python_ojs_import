import xml.etree.ElementTree as ET
def buildSections(tb,children):
    """
    Build OJS Sections XML Element

    Parameters:
    children (dict): A Dictionary containing section key,value pairs for OJS import

    Returns:
    Element: XML Element Object containing OJS Sections
    """
    #tb=ET.TreeBuilder()
    tb.start("sections",{})
    tb.start("section", {"ref":children['sectionAbbrev']})
    tb.start("abbrev",{})
    tb.data(children['sectionAbbrev'])
    tb.end("abbrev")
    tb.start("policy",{})
    tb.end("policy")
    tb.start("title",{})
    tb.data(children['sectionTitle'])
    tb.end("title")
    tb.end("section")
    tb.end("sections")

def buildIdentification(tb,children):
    """
    Build OJS Identification XML Element

    Parameters:
    children (dict): A Dictionary containing section key,value pairs for OJS import

    Returns:
    Element: XML Element Object containing OJS Identification
    """

    #tb=ET.TreeBuilder()
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
    #return tb.close()

def buildPublication(tb,children):
    """
    Build OJS Publication XML Element

    Parameters:
    children (dict): A Dictionary containing section key,value pairs for OJS import

    Returns:
    Element: XML Element Object containing OJS Publication
    """

    #tb=ET.TreeBuilder()
    tb.start("date_published",{})
    tb.data(children['issueDatepublished'])
    tb.end("date_published")
    return tb.close()




def buildArticle(tb,children):
    """
    Build OJS Article XML Element

    Parameters:
    children (dict): A Dictionary containing section key,value pairs for OJS import

    Returns:
    Element: XML Element Object containing OJS Article
    """

    #tb=ET.TreeBuilder()
    #tb.start("articles",{})
    tb.start("article", {"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance","section_ref": children['sectionAbbrev'],"stage": "production",
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
    tb.start("firstname",{})
    tb.data(children['authorFirstname1'])
    tb.end("firstname")
    tb.start("lastname",{})
    tb.data(children['authorLastname1'])
    tb.end("lastname")
    tb.start("affiliation",{})
    tb.data(children['authorAffiliation1'])
    tb.end("affiliation")
    tb.start("email",{})
    tb.data(children['authorEmail1'])
    tb.end("email")
    tb.end("author")
    tb.start("author",{"user_group_ref":"Author"})
    tb.start("firstname",{})
    tb.data(children['authorFirstname2'])
    tb.end("firstname")
    tb.start("lastname",{})
    tb.data(children['authorLastname2'])
    tb.end("lastname")
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
    tb.start("href", {"src": children['href']+ children['file1']
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
    #tb.end("article");
    #tb.end("articles")
    #return tb.close()

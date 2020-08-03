"""
 OJS Import XML builder functions

 Functions:
    build_sections: Builds SECTIONS Element, a set of Key, Value mappings
    build_article: Builds individual ARTICLE Element,
                   OJS ISSUES comprise of multiple articles
    build_identification: Builds ISSUE IDENTIFICATION Element,
                          ARTICLES use this to map parent-child relationship
"""

import xml.etree.ElementTree as ElementTree
import base64


def build_sections(children):
    """
    Build OJS Sections XML Element

    Parameters:
    children (dict): A Dictionary containing section key,value pairs for OJS
    import

    Returns:
    Element: XML Element Object containing OJS Sections
    """
    TREE_BUILDER = ElementTree.TreeBuilder()
    TREE_BUILDER.start("sections", {})
    for element in children:
        TREE_BUILDER.start("section", {"ref": element['sectionAbbrev']})
        TREE_BUILDER.start("abbrev", {})
        TREE_BUILDER.data(element['sectionAbbrev'])
        TREE_BUILDER.end("abbrev")
        TREE_BUILDER.start("policy", {})
        TREE_BUILDER.end("policy")
        TREE_BUILDER.start("title", {})
        TREE_BUILDER.data(element['sectionTitle'])
        TREE_BUILDER.end("title")
        TREE_BUILDER.end("section")
    TREE_BUILDER.end("sections")
    return TREE_BUILDER.close()


def build_identification(children):
    """
    Build OJS Identification XML Element

    Parameters:
    children (dict): A Dictionary containing section key,value pairs for OJS
    import

    Returns:
    Element: XML Element Object containing OJS Identification
    """

    TREE_BUILDER = ElementTree.TreeBuilder()
    TREE_BUILDER.start("issue_identification", {})
    TREE_BUILDER.start("volume", {})
    TREE_BUILDER.data(children['issueVolume'])
    TREE_BUILDER.end("volume")
    TREE_BUILDER.start("number", {})
    TREE_BUILDER.data(children['issueNumber'])
    TREE_BUILDER.end("number")
    TREE_BUILDER.start("year", {})
    TREE_BUILDER.data(children['issueYear'])
    TREE_BUILDER.end("year")
    TREE_BUILDER.start("title", {})
    TREE_BUILDER.data(children['issueTitle'])
    TREE_BUILDER.end("title")
    TREE_BUILDER.end("issue_identification")
    return TREE_BUILDER.close()


def build_publication(children):
    """
    Build OJS Publication XML Element

    Parameters:
    children (dict): A Dictionary containing section key,value pairs for OJS
    import

    Returns:
    Element: XML Element Object containing OJS Publication
    """

    TREE_BUILDER = ElementTree.TreeBuilder()
    TREE_BUILDER.start("date_published", {})
    TREE_BUILDER.data(children['issueDatepublished'])
    TREE_BUILDER.end("date_published")
    return TREE_BUILDER.close()


def build_article(children):
    """
    Build OJS Article XML Element

    Parameters:
    children (dict): A Dictionary containing section key,value pairs for OJS
    import

    Returns:
    Element: XML Element Object containing OJS Article
    """

    TREE_BUILDER = ElementTree.TreeBuilder()
    TREE_BUILDER.start("article", {
        "section_ref": children['sectionAbbrev'],
        "stage": "production",
        "date_published": children['issueDatepublished'],
        "seq": children['seq']
        }
                      )
    TREE_BUILDER.start("title", {})
    TREE_BUILDER.data(children['title'])
    TREE_BUILDER.end("title")
    TREE_BUILDER.start("abstract", {})
    TREE_BUILDER.data(children['abstract'])
    TREE_BUILDER.end("abstract")
    # Subject/Keywords are seperated by a ';' in the spreadsheet therefore
    # parse it
    if 'keywords' in children:
        TREE_BUILDER.start('keywords', {})
        for keyword in children['keywords'].split(';'):
            TREE_BUILDER.start('keyword', {})
            TREE_BUILDER.data(keyword)
            TREE_BUILDER.end("keyword")
        TREE_BUILDER.end("keywords")
    elif 'keywords' in children:
        TREE_BUILDER.start('keywords', {})
        for keyword in children['keywords'].split(';'):
            TREE_BUILDER.start('subject', {})
            TREE_BUILDER.data(keyword)
            TREE_BUILDER.end("subject")
        TREE_BUILDER.end("subjects")
    else:
        TREE_BUILDER.start("subjects", {})
        TREE_BUILDER.start("subject", {})
        TREE_BUILDER.end("subject")
        TREE_BUILDER.end("subjects")
    TREE_BUILDER.start("authors", {"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance", "xsi:schemaLocation":"http://pkp.sfu.ca native.xsd"})
    TREE_BUILDER.start("author", {"user_group_ref": "Author"})
    TREE_BUILDER.start("givenname", {"locale":"en_US"})
    TREE_BUILDER.data(children['authorGivenname1'])
    TREE_BUILDER.end("givenname")
    TREE_BUILDER.start("familyname", {"locale":"en_US"})
    TREE_BUILDER.data(children['authorFamilyname1'])
    TREE_BUILDER.end("familyname")
    TREE_BUILDER.start("affiliation", {})
    TREE_BUILDER.data(children['authorAffiliation1'])
    TREE_BUILDER.end("affiliation")
    TREE_BUILDER.start("email", {})
    TREE_BUILDER.data(children['authorEmail1'])
    TREE_BUILDER.end("email")
    TREE_BUILDER.end("author")
    if children['authorGivenname2'] is not '':
        TREE_BUILDER.start("author", {"user_group_ref": "Author"})
        TREE_BUILDER.start("givenname", {"locale":"en_US"})
        TREE_BUILDER.data(children['authorGivenname2'])
        TREE_BUILDER.end("givenname")
        TREE_BUILDER.start("familyname", {"locale":"en_US"})
        TREE_BUILDER.data(children['authorFamilyname2'])
        TREE_BUILDER.end("familyname")
        TREE_BUILDER.start("affiliation", {})
        TREE_BUILDER.data(children['authorAffiliation2'])
        TREE_BUILDER.end("affiliation")
        TREE_BUILDER.start("email", {})
        TREE_BUILDER.data(children['authorEmail2'])
        TREE_BUILDER.end("email")
        TREE_BUILDER.end("author")
    TREE_BUILDER.end("authors")
    TREE_BUILDER.start("submission_file", {
        "id": children['file_number'],
        "stage": children['submission_stage']
        })
    TREE_BUILDER.start("revision", {
        "genre": children['fileGenre1'],
        "number": children['revision_number'],
        "filetype": "application/pdf",
        "filename": children['file1']
        })
    TREE_BUILDER.start("name", {})
    TREE_BUILDER.data(children['file1'])
    TREE_BUILDER.end("name")
    if 'bucket_location' in children:
        TREE_BUILDER.start("href", {
            "src": children['bucket_location'] + children['file1'],
            "mime_type": "application/pdf"
        })
        TREE_BUILDER.end("href")
    if 'pdf_folder' in children:
        TREE_BUILDER.start("embed", {
            "encoding": "base64",
            "mime_type": "application/pdf"
        })
        TREE_BUILDER.data(str(base64.b64encode(open(children['pdf_folder'] + children['file1'], "rb").read()), "utf-8"))
        TREE_BUILDER.end("embed")
    TREE_BUILDER.end("revision")
    TREE_BUILDER.end("submission_file")
    TREE_BUILDER.start("article_galley", {})
    TREE_BUILDER.start("id", {})
    TREE_BUILDER.data(children['file_number'])
    TREE_BUILDER.end("id")
    TREE_BUILDER.start("name", {})
    TREE_BUILDER.data("PDF")
    TREE_BUILDER.end("name")
    TREE_BUILDER.start("seq", {})
    TREE_BUILDER.data(children['seq'])
    TREE_BUILDER.end("seq")
    TREE_BUILDER.start("submission_file_ref", {
        "id": children['file_number'],
        "revision": children['revision_number']
    })
    TREE_BUILDER.end("submission_file_ref")
    TREE_BUILDER.end("article_galley")
    TREE_BUILDER.start("pages", {})
    TREE_BUILDER.data(children['pages'])
    TREE_BUILDER.end("pages")
    TREE_BUILDER.end("article")
    return TREE_BUILDER.close()

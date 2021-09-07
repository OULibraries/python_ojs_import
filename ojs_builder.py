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
import urllib3

"""
Instantiate object to handle http connections to retrieve covers
from s3 bucket (see build_cover function for more details).
"""
http = urllib3.PoolManager()

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

def build_cover(children):
    TREE_BUILDER = ElementTree.TreeBuilder()
    TREE_BUILDER.start("covers")
    TREE_BUILDER.start("cover")
    TREE_BUILDER.start("cover_image")
    TREE_BUILDER.data(children['issueCover'])
    TREE_BUILDER.end("cover_image")
    TREE_BUILDER.start("cover_image_alt_text")
    TREE_BUILDER.data("")
    TREE_BUILDER.end("cover_image_alt_text")
    TREE_BUILDER.start("embed", {
            "encoding": "base64",
            "mime_type": "image/jpeg"
        })
    # OJS expects cover images to be encoded in the XML as base64. The code
    # below retrieves the relevant cover images from the s3 bucket using the
    # urllib3 library, encodes the image, and converts it to a string to be
    # appended to the embed XML element.
    TREE_BUILDER.data(str(base64.b64encode(http.request('GET', 'https://ul-theatreorgan.s3.amazonaws.com/pdf/'
        + children['issueCover']).data), "utf-8"))
    TREE_BUILDER.end("embed")
    TREE_BUILDER.end("cover")
    TREE_BUILDER.end("covers")
    return TREE_BUILDER.close()

def build_date_published(children):
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
    TREE_BUILDER.start("article", {"stage": "production"})
    TREE_BUILDER.start("publication", {
        "date_published": children['issueDatepublished'],
        "seq": children['seq'],
        "section_ref": children['sectionAbbrev']
    })
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
    TREE_BUILDER.start("author", {
        "user_group_ref": "Author",
        "seq": 1,
        "id": ""
        })
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
    if children['authorGivenname2'] != '':
        TREE_BUILDER.start("author", {
            "user_group_ref": "Author",
            "seq": 2,
            "id": ""
            })
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
    TREE_BUILDER.end("publication")    
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
    # When using this file in conjunction with the generate_xml_embedded.py
    # script to create the XML file locally, bucket_location below needs 
    # to be switched to pdf_folder.
    TREE_BUILDER.start("href", {
        "section_ref": children['sectionAbbrev'],
        "src": children['bucket_location'] + children['file1'],
        "mime_type": "application/pdf"
    })
    TREE_BUILDER.end("href")
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
    })
    TREE_BUILDER.end("submission_file_ref")
    TREE_BUILDER.end("article_galley")
    TREE_BUILDER.start("pages", {})
    TREE_BUILDER.data(children['pages'])
    TREE_BUILDER.end("pages")
    TREE_BUILDER.end("article")
    return TREE_BUILDER.close()


"""
 Takes a CSV and parses it into a Python Dict containing Key,Value Mappings
 from CSV
 The Dict is then passed to XML builder functions
 The final XML Tree that is built is then dumped to a file for import into OJS

 Vars:
    INPUT_CSV: CSV containing OJS fields to conver to XML
    conversion.xml: Resulting XML document for OJS Import
"""

from os import remove
import csv
import xml.etree.ElementTree as ET
from ojs_builder import (build_identification,
                         build_article,
                         build_sections,
                         build_publication)


IMPORTLIST = []
INPUT_FILE = csv.DictReader(open("import.csv"))
ISSUES = []
ARTICLES = dict()
SECTIONS = {}
for i in INPUT_FILE:
    IMPORTLIST.append(i)

for m in IMPORTLIST:
    ISSUES.append(m['issueTitle'])

ISSUES = set(ISSUES)

for it in ISSUES:
    SECTIONS[it] = []

    for o in IMPORTLIST:
        if o['issueTitle'] == it:
            section = {"sectionTitle": o['sectionTitle'],
                       "sectionAbbrev": o['sectionAbbrev']}
            SECTIONS[it].append(section)
        #    articles[it].append(o)
XML_VERSION = "<?xml version=\"1.0\"?>"
XMLNS = "xmlns=\"http://pkp.sfu.ca\""
XMLNS_XSI = "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""
SCHEMA_LOCATION = "xsi:schemaLocation=\"http://pkp.sfu.ca native.xsd\">"
XML_HEADER = (XML_VERSION + " <issues " + XMLNS
              + " " + XMLNS_XSI + " " + SCHEMA_LOCATION + "</issues>")
with open("pyout.xml", "w") as f:
    f.write(XML_HEADER)


ET.register_namespace("", "http://pkp.sfu.ca")
ARTICLE = ET.parse("pyout.xml")

ROOT = ARTICLE.getroot()
for importdict in IMPORTLIST:
    ARTICLES[importdict['issueTitle']] = importdict

ARTICLES = set(ARTICLES)
TREE_BUILDER = ET.TreeBuilder()
TREE_BUILDER.start("issue", {})
TREE_BUILDER.end("issue")
ISSUE = (TREE_BUILDER.close())

for importdict in IMPORTLIST:
    if 'authorEmail1' not in importdict:
        importdict['authorEmail1'] = ''
    if 'authorEmail2' not in importdict:
        importdict['authorEmail2'] = ''

    bucket_schema = "http://"
    bucket_url = "ul-theatreorgan.s3-website-us-east-1.amazonaws.com"
    bucket_prefix = "/pdf/"
    bucket_location = bucket_schema + bucket_url + bucket_prefix
    importdict['bucket_location'] = bucket_location
    TREE_BUILDER = ET.TreeBuilder()
    TREE_BUILDER.start("issue", {})
    TREE_BUILDER.end("issue")
    issue = (TREE_BUILDER.close())
    issue.append(build_identification(importdict))
    issue.append(build_publication(importdict))
    issue.append(build_sections(SECTIONS[importdict['issueTitle']]))
    issue.append(build_article(importdict))
    ROOT.append(issue)

ARTICLE.write("conversion.xml")
remove("pyout.xml")

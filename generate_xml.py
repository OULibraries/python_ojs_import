"""
 Takes a CSV and parses it into a Python Dict containing Key,Value Mappings
 from CSV
 The Dict is then passed to XML builder functions
 The final XML Tree that is built is then dumped to a file for import into OJS

 Vars:
    pdf_folder: Full path to directory containing article/issue PDF's, defaults to current working directory
    input_csv: CSV containing OJS fields to conver to XML
    output_file: Resulting XML document for OJS Import
"""

import csv
import os
import xml.dom.minidom
import xml.etree.ElementTree as ElementTree
from ojs_builder import (build_identification,
                         build_date_published,
                         build_article,
                         build_sections,
                         build_cover,
                         build_issue_galleys,
                         build_issue_id)

import_list = []
bucket = "mybucket"
bucket_schema = "http://"
bucket_url = bucket + ".s3.amazonaws.com"
bucket_prefix = "/pdf/"
bucket_location = bucket_schema + bucket_url + bucket_prefix
input_csv = "import.csv"
input_file = csv.DictReader(open(input_csv))
#output_file = "conversion.xml"
issues = {}
articles = {}
sections = {}
xml_version = "<?xml version=\"1.0\"?>"
xmlns = "xmlns=\"http://pkp.sfu.ca\""
xmlns_xsi = "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""
schema_location = "xsi:schemaLocation=\"http://pkp.sfu.ca native.xsd\">"
xml_header = (xml_version + " <issues " + xmlns
              + " " + xmlns_xsi + " " + schema_location + "</issues>")

#ElementTree.register_namespace("", "http://pkp.sfu.ca")
#doc = ElementTree.ElementTree(ElementTree.fromstring(xml_header))
#root = doc.getroot()

for row in input_file:
    import_list.append(row)

for import_dict in import_list:
    if import_dict['issueTitle'] not in issues:
        issues[import_dict['issueTitle']] = {
            "issueYear": import_dict['issueYear'],
            "issueVolume": import_dict['issueVolume'],
            "issueNumber": import_dict['issueNumber'],
            "issueDatepublished": import_dict['issueDatepublished'],
            "issueTitle": import_dict['issueTitle'],
            "issueCover": import_dict['issueCover']}

for issue_title in issues:
    sections[issue_title] = []
    articles[issue_title] = []
    for import_row in import_list:
        if import_row['issueTitle'] == issue_title:
            section = {"sectionTitle": import_row['sectionTitle'],
                       "sectionAbbrev": import_row['sectionAbbrev']}
            sections[issue_title].append(section)
            articles[issue_title].append(import_row)

file_number = 0
issue_identifier = 1
for issue_key, issue_metadata in issues.items():
    ElementTree.register_namespace("", "http://pkp.sfu.ca")
    doc = ElementTree.ElementTree(ElementTree.fromstring(xml_header))
    root = doc.getroot()
    # The issue element in the resulting XML can take a published attribute
    # of either a 0 or a 1. This logic tells OJS whether the article should
    # show as published or not in OJS.
    if datetime.datetime.strptime(issue_metadata['issueDatepublished'], "%Y-%m-%d") < datetime.datetime.today():
        is_published = 1
    elif datetime.datetime.strptime(issue_metadata['issueDatepublished'], "%Y-%m-%d") > datetime.datetime.today():
        is_published = 0
    issue = ElementTree.Element("issue", attrib={"current":"0", "published": str(is_published)})
    issue.append(build_issue_id(issue_identifier))

    issue.append(build_identification(issue_metadata))
    issue.append(build_date_published(issue_metadata))
    issue.append(build_sections(sections[issue_key]))
    if issue_metadata['issueCover'] != '':
        issue.append(build_cover(issue_metadata))
    issue.append(build_issue_galleys())
    doc_articles = ElementTree.Element("articles", {})
    for import_dict in articles[issue_key]:
        if 'authorEmail1' not in import_dict:
            import_dict['authorEmail1'] = ''
        if 'authorEmail2' not in import_dict:
            import_dict['authorEmail2'] = ''
        if 'submission_stage' not in import_dict:
            import_dict['submission_stage'] = 'submission'
        if import_dict['fileGenre1'] == '':
            import_dict['fileGenre1'] = 'Article Text'
        if 'revision_number' not in import_dict:
            import_dict['revision_number'] = "1"
        if import_dict['authorFamilyname1'] == '' or import_dict['authorFamilyname1'] == None or 'authorFamilyname1' not in import_dict:
            import_dict['authorFamilyname1'] = "Unknown"
        if import_dict['authorGivenname1'] == '' or import_dict['authorGivenname1'] == None or 'authorGivenname1' not in import_dict:
            import_dict['authorGivenname1'] = "Unknown"
        

        import_dict['bucket_location'] = bucket_location
        file_number += 1
        import_dict['file_number'] = str(file_number)
        doc_articles.append(build_article(import_dict))
    issue.append(doc_articles)
    root.append(issue)

    output_file = "conversion" + str(issue_identifier) + ".xml"
    
    issue_identifier += 1

    doc._setroot(root)
    pretty_xml = xml.dom.minidom.parseString(ElementTree.tostring(doc.getroot()))
    open(output_file, 'w').write((pretty_xml.toprettyxml()))

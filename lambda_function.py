import json
import csv
import boto3
import xml.etree.ElementTree as ElementTree
from ojs_builder import (build_identification,
                         build_publication,
                         build_article,
                         build_sections)


"""
 Takes a CSV and parses it into a Python Dict containing Key,Value Mappings
 from CSV
 The Dict is then passed to XML builder functions
 The final XML Tree that is built is then dumped to a file for import into OJS

 Vars:
    INPUT_CSV: CSV containing OJS fields to conver to XML
    OUTPUT_FILE: Resulting XML document for OJS Import
"""


def lambda_handler(event, context):
    """
    AWS Lambda Hanlder Function, main driver for Lambda.
    Parameters:
    event : Source that triggered Lambda Function;in this case CSV Upload to S3
    context: This object provides methods, properties, and information
             about the invocation, function, and execution environment.

    Returns:
    json: Response and Status of Lambda Function
    """
    IMPORTLIST = []
    bucket = "mybucket"
    bucket_schema = "http://"
    bucket_url = "mybucket.s3.amazonaws.com"
    bucket_prefix = "/pdf/"
    bucket_location = bucket_schema + bucket_url + bucket_prefix
    s3 = boto3.resource('s3')
    client = boto3.client('s3')
    s3.meta.client.download_file(bucket, 'csv/import.csv', '/tmp/import.csv')
    INPUT_CSV = "/tmp/import.csv"
    INPUT_FILE = csv.DictReader(open(INPUT_CSV))
    OUTPUT_FILE = "/tmp/conversion.xml"
    ISSUES = {}
    ARTICLES = {}
    SECTIONS = {}
    TREE_BUILDER = ElementTree.TreeBuilder()
    XML_VERSION = "<?xml version=\"1.0\"?>"
    XMLNS = "xmlns=\"http://pkp.sfu.ca\""
    XMLNS_XSI = "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""
    SCHEMA_LOCATION = "xsi:schemaLocation=\"http://pkp.sfu.ca native.xsd\">"
    XML_HEADER = (XML_VERSION + " <issues " + XMLNS
                  + " " + XMLNS_XSI + " " + SCHEMA_LOCATION + "</issues>")

    ElementTree.register_namespace("", "http://pkp.sfu.ca")
    DOC = ElementTree.ElementTree(ElementTree.fromstring(XML_HEADER))
    ROOT = DOC.getroot()
    ISSUE = ElementTree.Element("issue")

    # Tag Uploaded CSV for object lifecycle management
    key = 'csv/import.csv'
    client.put_object_tagging(
        Bucket=bucket,
        Key=key,
        Tagging={
            'TagSet': [
                {
                    'Key': 'upload_type',
                    'Value': 'csv'
                },
            ]
        }
    )

    for row in INPUT_FILE:
        IMPORTLIST.append(row)

    for import_dict in IMPORTLIST:
        if import_dict['issueTitle'] not in ISSUES:
            ISSUES[import_dict['issueTitle']] = {
                    "issueYear": import_dict['issueYear'],
                    "issueVolume": import_dict['issueVolume'],
                    "issueNumber": import_dict['issueNumber'],
                    "issueDatepublished": import_dict['issueDatepublished'],
                    "issueTitle": import_dict['issueTitle']
                            }

    for ISSUE_TITLE in ISSUES.keys():
        SECTIONS[ISSUE_TITLE] = []
        ARTICLES[ISSUE_TITLE] = []
        for IMPORT_ROW in IMPORTLIST:
            if IMPORT_ROW['issueTitle'] == ISSUE_TITLE:
                SECTION = {"sectionTitle": IMPORT_ROW['sectionTitle'],
                           "sectionAbbrev": IMPORT_ROW['sectionAbbrev']}
                SECTIONS[ISSUE_TITLE].append(SECTION)
                ARTICLES[ISSUE_TITLE].append(IMPORT_ROW)

    for ISSUE_KEY, ISSUE_METADATA in ISSUES.items():
        ISSUE.append(build_identification(ISSUE_METADATA))
        ISSUE.append(build_publication(ISSUE_METADATA))
        ISSUE.append(build_sections(SECTIONS[ISSUE_KEY]))
        DOC_ARTICLES = ElementTree.Element("articles")
        for IMPORTDICT in ARTICLES[ISSUE_KEY]:
            if 'authorEmail1' not in IMPORTDICT:
                IMPORTDICT['authorEmail1'] = ''
            if 'authorEmail2' not in IMPORTDICT:
                IMPORTDICT['authorEmail2'] = ''

            IMPORTDICT['bucket_location'] = bucket_location
            DOC_ARTICLES.append(build_article(IMPORTDICT))
        ISSUE.append(DOC_ARTICLES)
        ROOT.append(ISSUE)

    DOC._setroot(ROOT)
    DOC.write(OUTPUT_FILE)
    s3.meta.client.upload_file(OUTPUT_FILE, bucket, 'conversion.xml')
    return {
        'statusCode': 200,
        'body': json.dumps('Converted:\n\t'
                           + 'Articles: ' + str(len(ARTICLES)) + '\n\t'
                           + 'Issues: ' + str(len(ISSUES)))
    }


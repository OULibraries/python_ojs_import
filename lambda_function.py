"""
 Takes a CSV and parses it into a Python Dict containing Key,Value Mappings
 from CSV
 The Dict is then passed to XML builder functions
 The final XML Tree that is built is then dumped to a file for import into OJS

 Vars:
    input_csv: CSV containing OJS fields to conver to XML
    output_file: Resulting XML document for OJS Import
"""

import json
import csv
import xml.dom.minidom
import xml.etree.ElementTree as ElementTree
import boto3
from ojs_builder import (build_identification,
                         build_publication,
                         build_article,
                         build_sections)


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
    import_list = []
    bucket = "mybucket"
    bucket_schema = "http://"
    bucket_url = bucket + ".s3.amazonaws.com"
    bucket_prefix = "/pdf/"
    bucket_location = bucket_schema + bucket_url + bucket_prefix
    s3_resource = boto3.resource('s3')
    client = boto3.client('s3')
    s3_resource.meta.client.download_file(bucket,
                                          'csv/import.csv',
                                          '/tmp/import.csv')
    input_csv = "/tmp/import.csv"
    input_file = csv.DictReader(open(input_csv))
    output_file = "/tmp/conversion.xml"
    issues = {}
    articles = {}
    sections = {}
    xml_version = "<?xml version=\"1.0\"?>"
    xmlns = "xmlns=\"http://pkp.sfu.ca\""
    xmlns_xsi = "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\""
    schema_location = "xsi:schemaLocation=\"http://pkp.sfu.ca native.xsd\">"
    xml_header = (xml_version + " <issues " + xmlns
                  + " " + xmlns_xsi + " " + schema_location + "</issues>")

    ElementTree.register_namespace("", "http://pkp.sfu.ca")
    doc = ElementTree.ElementTree(ElementTree.fromstring(xml_header))
    root = doc.getroot()

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

    for row in input_file:
        import_list.append(row)

    for import_dict in import_list:
        if import_dict['issueTitle'] not in issues:
            issues[import_dict['issueTitle']] = {
                "issueYear": import_dict['issueYear'],
                "issueVolume": import_dict['issueVolume'],
                "issueNumber": import_dict['issueNumber'],
                "issueDatepublished": import_dict['issueDatepublished'],
                "issueTitle": import_dict['issueTitle']}

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
    for issue_key, issue_metadata in issues.items():
        issue = ElementTree.Element("issue")
        issue.append(build_identification(issue_metadata))
        issue.append(build_publication(issue_metadata))
        issue.append(build_sections(sections[issue_key]))
        doc_articles = ElementTree.Element("articles")
        for import_dict in articles[issue_key]:
            if 'authorEmail1' not in import_dict:
                import_dict['authorEmail1'] = ''
            if 'authorEmail2' not in import_dict:
                import_dict['authorEmail2'] = ''
            if 'submission_stage' not in import_dict:
                import_dict['submission_stage'] = 'submission'
            if import_dict['fileGenre1'] == '':
                import_dict['fileGenre1'] = 'Article Text'
            if import_dict['revision_number'] not in import_dict:
                import_dict['revision_number'] = "0"

            import_dict['bucket_location'] = bucket_location
            file_number += 1
            import_dict['file_number'] = str(file_number)
            doc_articles.append(build_article(import_dict))
        issue.append(doc_articles)
        root.append(issue)

    pretty_xml = xml.dom.minidom.parseString(ElementTree.tostring(root))
    open(output_file, 'w').write((pretty_xml.toprettyxml()))
    s3_resource.meta.client.upload_file(output_file, bucket, 'conversion.xml')
    return {
        'statusCode': 200,
        'body': json.dumps('Converted:\n\t'
                           + 'Articles: ' + str(file_number) + '\n\t'
                           + 'Issues: ' + str(len(issues)))}

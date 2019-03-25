import json
import csv
import xml.etree.ElementTree as ET
import boto3
import ojs_builder


"""
XML to CSV Conversion Script for Batch Import to OJS
"""
bucket='mybucket'
bucket_location= "https://" + bucket + ".s3.amazon.com/"

#Main Lambda Handler
def lambda_handler(event, context):
    """
    AWS Lambda Hanlder Function, main driver for Lambda.
    Parameters:
    event : Source that triggered Lambda Function; in this case CSV Upload to S3.
    context: This object provides methods and properties that provide information about the invocation, function, and execution environment.

    Returns:
    json: Response and Status of Lambda Function
    """

    importlist=[]
    s3 = boto3.resource('s3')
    client = boto3.client('s3')
    s3.meta.client.download_file(bucket, 'csv/import.csv', '/tmp/import.csv')

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

    input_file = csv.DictReader(open("/tmp/import.csv"))
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
            #    articles[it].append(o)

    with open("/tmp/pyout.xml", "w") as f:
        f.write("<?xml version=\"1.0\"?><issues xmlns=\"http://pkp.sfu.ca\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://pkp.sfu.ca native.xsd\"></issues>")


    ET.register_namespace("", "http://pkp.sfu.ca")
    article = ET.parse("/tmp/pyout.xml")

    root = article.getroot()
    for importdict in importlist:
        articles[importdict['issueTitle']]=importdict

    articles=set(articles)
    #pprint(articles)
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

    article.write("/tmp/otherypy.xml")

    s3.meta.client.upload_file('/tmp/otherypy.xml',bucket,'conversion.xml')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

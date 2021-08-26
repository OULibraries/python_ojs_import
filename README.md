# python_ojs_import
XML to CSV Conversion Script for Batch Import to OJS

_Adapted from [OJSXML Plugin](https://github.com/ualbertalib/ojsxml)_

Requirements
------------

This role requires the following Python Plugins:

  * Python >=3.6
  * Boto3
      Can be installed using `pip install boto3`, [ visit pip installation instructions for more information.](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation)  
  * XML ElementTree (Part of Python Core)
  * urllib3

General Usage
------------

**_Local Conversion_**

>Local conversion can use a local directory as the source for PDF files by using the generate_xml_embedded.py script

>* **NOTE: When locally embedding PDFs this may result in a very large XML that cannot be uploaded and smaller "batches" must be done** 

>* _Ensure pdf_folder variable is defined correctly when using generate_xml_embedded.py, by default the script will utilize a directory entitled `pdf/` located in the current directory it is run in and will look for respective PDF files there._

1. Copy examples/import.csv to ./import.csv

2. Add metadata to respective CSV fields

4. Upload PDF files to PDF directory in defined S3 Bucket

3. Run `generate_xml.py`. This will create an XML file named `conversion.xml`



**_Lambda Conversion_**

1. Copy exmaples/import.csv to ./import.csv

2. Add metadata to respective CSV fields

3. Upload PDF files to PDF directory in provided S3 Bucket
 * Upload CSV to Provided S3 Bucket

* _Lambda function will trigger on CSV upload and create file `conversion.xml`, download said file_


---


4. In OJS Admin click "Import/Export" under Tools 

 * Click Native Import/Export 

5. Drag and Drop or Click "Add Files", upload `conversion.xml`

6. Click "Import"

 * A progress bar will be shown, after which you will be taken to a completion summary screen

_You may recieve warnings stating:_
> Existing issue with id ### matches the given issue identification "<issue_identification><volume>##</volume><number>##</number><year>#####</year><title/></issue_identification>". This issue will not be modified, but articles will be added.

_This is OJS telling you that the issue exists but it is importing approprate Article Metadata; it should be noted that this can result in duplicate articles if they are imported more than once_

_Further information is located below indicating completed imports_
> The import completed successfully. The following items were imported:

> Vol 17 No 10 (1975)

> Vol 17 No 10 (1975)

> Vol 17 No 10 (1975)

> Vol 17 No 10 (1975)

> Vol 17 No 10 (1975)

> Vol 17 No 10 (1975)

> Vol 17 No 10 (1975)

> Vol 17 No 10 (1975)

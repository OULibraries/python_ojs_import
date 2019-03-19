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

General Usage
------------
1. Copy exmaples/import.csv to ./import.csv

2. Add meta-data to respective CSV fields

3. Run generateXml.py, this will create an XML file named `conversion.xml`

4. In OJS Admin click "Import/Export" under Tools 

* Click Native Import/Export 

5. Drag and Drop or Click "Add Files", upload `conversion.xml`

6. Click "Import"

* A progress bar will be shown, after which you will be taken to a completion summary screen

_You may recieve warnings stating:_
> Existing issue with id ### matches the given issue identification "<issue_identification><volume>##</volume><number>##</number><year>#####</year><title/></issue_identification>". This issue will not be modified, but articles will be added.

_This is OJS telling you that the issue exists but it is importing approprate Article Metadata_

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

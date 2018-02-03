# Google_Analytics_Database_Dumper

## Main goal is to bring google analytics to the local environment for building more intelligence reports.

### 1. Idea is Linking Google Analytics with Big query
### 2. In big query - export table as csv/json/avro to Google Cloud Storage
### 3. Download data from Google Cloud storage to local machine 

I have written simple framework to dump the google analytics data from big query by exporting to cloud storage.

#### Please configure the config.ini file in etc directory.
#### You need to enable the apis like big query and storage api in cloud consoles
#### You need a service account along with credentials as json file to the furhter processing 

<object data="https://github.com/vijayanandrp/vijayanandrp.github.io/raw/master/Google_Analytics_%20export_database_to_local.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="https://github.com/vijayanandrp/vijayanandrp.github.io/raw/master/Google_Analytics_%20export_database_to_local.pdf">
        This browser does not support PDFs. Please download the PDF to view it: <a href="https://github.com/vijayanandrp/vijayanandrp.github.io/raw/master/Google_Analytics_%20export_database_to_local.pdf">Download PDF</a>.</p>
    </embed>
</object>

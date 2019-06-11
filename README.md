# MutualFundDataCrawler #

## Function: ##

Python code that parses fund holdings pulled from EDGAR, given a ticker or CIK, and generates a .tsv file from them. 

## Process: ##

* Input (Example - CIK: 0001166559).
* Uses http://www.sec.gov/edgar/searchedgar/companysearch.html to gather forms.
* Finds the most recent “13F” report documents from the ones listed (Example - A 13F-HR form).
* Parse and generate tab-delimited text from the xml.
* Creates a .tsv file on the file directory for that form.

# Scrape the # of Reads for each listed sample corresponding w GSE id.

(Only tested with single-end bulk rnaseq data)

## Required libraries:<br/>
requests: For making HTTP requests to fetch the GSE and SRA pages.

beautifulsoup4: For parsing the HTML content of the web pages.

## Installing the required libraries:
```pip install requests beautifulsoup4```

## Running the script:
```/path/to/script/python SRA-READS-SCRAPER.py```

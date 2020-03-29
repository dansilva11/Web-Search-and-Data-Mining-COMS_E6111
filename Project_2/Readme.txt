# COMS 6111 Project 2
# Authors
Yousef Elsendiony (ye2194) and Daniel Carpenter Silva (dcs2180)

# Files
run.py
Readme.txt
transcript.txt

# Final Design
- Using the seed query from the user input we performed a google search and parsed the first 20000 characters of each page. For each page we ran the raw text through pipeline 1 which is an NER pipeline that checks the text for the relation specified by the user. If a sentence contains the appropriate NER relationship then we will run the sentence through pipeline 2 which is a KBP pipeline which will give us an estimated confidence for our KBP relation. If the sentence holds the relation with confidence higher than the target threshold then we will extract the tuple and add to the list of extracted tuples. After parsing the 10 queried pages, if our extracted tuples list holds enough relations we will terminate. Otherwise, we re-query with the highest confidence tuple that has yet to have been used in hopes of finding more high confidence relations.



# Implementation
- run.py can be called with 6 terms to similar to the example provided by the TA's to execute the google search. All the source code is located in this one file.

- python3 run.py <google api key> <google engine id> <r> <t> <q> <k>

# Dependencies

GCP VM Install Commands:

- sudo apt-get update

- sudo apt-get python3-pip

- sudo apt-get install unzip

- unzip stanford-corenlp-full-2018-10-05.zip

- wget https://download.java.net/java/GA/jdk13.0.2/d4173c853231432d94f001e99d882ca7/8/GPL/openjdk-13.0.2_linux-x64_bin.tar.gz

- tar -xvzf openjdk-13.0.2_linux-x64_bin.tar.gz

- export PATH=/home/⟨your_UNI⟩/jdk-13.0.2/bin:$PATH

- export JAVA_HOME=/home/⟨your_UNI⟩/jdk-13.0.2

- export CORENLP_HOME=/home/⟨your_UNI⟩/stanford-corenlp-full-2018-10-05

- python3 -m pip install stanfordnlp
    ( if torch is required please run 'python3 -m pip install torch===1.4.0 torchvision===0.5.0 -f https://download.pytorch.org/whl/torch_stable.html')

- python3 -m pip install bs4

- python3 -m pip install google-api-python-client

3rd party libraries include:
- googleapiclient.discovery build() : for google search capabilities
- BeautifulSoup4 : for pulling the page contents from the URL
- stanfordnlp : for creating the kbp pairs from text

# Transcript 
python3 run.py AIzaSyDizICDRG4vBY5_F6mzfADnbxDAKt78LYs 001513741995706822325:jzoyxarodil 2 0.7 "bill gates microsoft" 10

# References
http://www.cs.columbia.edu/~gravano/cs6111/proj2.html

https://www.crummy.com/software/BeautifulSoup/bs4/doc/



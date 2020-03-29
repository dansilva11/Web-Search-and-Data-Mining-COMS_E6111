# COMS 6111 Project 2
# Authors
Yousef Elsendiony (ye2194) and Daniel Carpenter Silva (dcs2180)

# Files
run.py
Readme.txt
transcript.txt

# Final Design



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

# References
http://www.cs.columbia.edu/~gravano/cs6111/proj2.html

https://www.crummy.com/software/BeautifulSoup/bs4/doc/



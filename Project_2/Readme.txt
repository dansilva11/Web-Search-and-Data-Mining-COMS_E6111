# COMS 6111 Project 2
# Authors
Yousef Elsendiony (ye2194) and Daniel Carpenter Silva (dcs2180)

# Final Design

# Implementation
- run.py can be called with 6 terms to similar to the example provided by the TA's to execute the google search. All the source code is located in this one file.

# Dependencies

GCP VM Install Commands:

- sudo apt-get update

- sudo apt-get python3-pip

- python3 -m pip install bs4

- python3 -m pip install google-api-python-client

- python3 -m pip install stanfordnlp
    ( if torch is required please run 'python3 -m pip install torch===1.4.0 torchvision===0.5.0 -f https://download.pytorch.org/whl/torch_stable.html')

3rd party libraries include:
- googleapiclient.discovery build() : for google search capabilities
- BeautifulSoup4 : for pulling the page contents from the URL
- stanfordnlp : for creating the kbp pairs from text

# References
http://www.cs.columbia.edu/~gravano/cs6111/proj2.html

https://www.crummy.com/software/BeautifulSoup/bs4/doc/



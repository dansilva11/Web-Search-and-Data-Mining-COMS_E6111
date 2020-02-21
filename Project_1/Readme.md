# COMS 6111 Project 1
# Authors
Yousef Elsendiony (ye2194) and Daniel Carpenter Silva (dcs2180)

# Final Design
- We choose to use Rocchio's Algorithm for information retrieval since it was recommended in the paper "Modern Information Retrieval: A Brief Overview" by Amit Singhal which the Professor recommended.

- We are first doing the rocchio's algorithm and then doing stopword elimination to avoid appending a stopword to the query which wouldn't increase the precision in the next 10 results.

- Wikipedia link recommneded optimal alpha, beta, gamma values for rocchios as a = 1, b = 0.8, and c = 0.1 respectively.

# Implementation
- run.py can be called with 4 terms to similar to the example provided by the TA's to execute the google search. All the source code is located in this one file.

- We originally were looking to pick the two most frequent terms found in the relevant documents (similar to going off the term frequency only). As we saw in class, this can lead to unfavorable results so we then implemented the rocchio's algorithm.

- Our aim was to keep the algorithm in a different function so if we wanted to try out another algorithm (say the probabilistic approach) we could call that algorithm without rewriting / refactoring the code heavily.

# Dependencies

3rd party libraries include:
- googleapiclient.discovery build() : for google search capabilities
- nltk.corpus import stopwords : for downloading and removing stopwords
- nltk.download('punkt') : for tokenization to extract terms from snippets

# References
http://www.cs.columbia.edu/~gravano/cs6111/proj1.html

http://www.cs.columbia.edu/~gravano/cs6111/Readings/singhal.pdf

https://en.wikipedia.org/wiki/Rocchio_algorithm
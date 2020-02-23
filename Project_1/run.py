import sys
import nltk
import math
from collections import defaultdict
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
import re
from googleapiclient.discovery import build


def algorithmRocchioTfIdf(rel_pages, irrel_pages, query_count, q_tok):
    docs     = rel_pages + irrel_pages
    N        = len(docs)
    releventVector, irreleventVector,  = [], []
    documentFrequencies = defaultdict(set)
    finalScores = defaultdict(float)

    for page in docs:
        termVector  = defaultdict(int)
        doc     = page['title'] + " " + page['snippet']
        tokens  = tokenizer(doc)

        # Counter of query words in current doc
        for token in tokens:
            documentFrequencies[token].add(docs.index(page))
            termVector[token] += 1
        if page in rel_pages:
            releventVector.append(termVector)
        else:
            irreleventVector.append(termVector)

    # Update tftd for the current doc
    for termVector in (releventVector + irreleventVector):
        for term in termVector:
            termVector[term] = math.log(1+termVector[term], 10) * math.log(float(N)/len(documentFrequencies[term]), 10) * 1000

    for termVector in releventVector:
        for term in termVector:
            finalScores[term] += termVector[term] * .6 / len(releventVector)
    for termVector in irreleventVector:
        for term in termVector:
            finalScores[term] = max(0, finalScores[term] - termVector[term] * .1 / len(irreleventVector))

    # Remove the stop words (Not sure if we do this earlier or now is better?)
    stop_words = set(stopwords.words('english'))
    for word in stop_words:
        if word in finalScores:
            finalScores.pop(word)

    # Sort based on score and append 2 highest words to query
    finalScores = sorted(finalScores.items(), key=lambda item: str(item[1]), reverse=True)
    term1 = finalScores[0][0]
    term2 = finalScores[1][0]
    q_tok.append(term1)
    q_tok.append(term2)

    print("Augmenting query with two words:" + str(term1) + " and " + str(term2))
    return q_tok


def algorithmTop2Words(rel_pages, query_count, q_tok):
    wordfreq = {}
    for page in rel_pages:
        doc = page['title'] + " " + page['snippet']
        tokens = tokenizer(doc)

        for token in tokens:
            if token not in set(wordfreq.keys()):
                wordfreq[token] = 1
            else:
                wordfreq[token] += 1

    wordfreq = {k: v for k, v in sorted(wordfreq.items(), reverse=True, key=lambda item: item[1])}

    # Remove the stop words
    stop_words = set(stopwords.words('english'))
    words = [x for x in list(wordfreq.keys()) if x not in stop_words]

    top_words = words[0:query_count+2] # Grab top  2 words
    for word in q_tok:
        if word not in top_words:
            for i in range(1,len(top_words)):
                if top_words[-i] not in q_tok:
                    top_words[-i]=word
                    break
    return top_words

def main(api_key, engine_id, precision, query):
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    cal_perc = 0
    precision = float(precision)

    while cal_perc < precision:
        q_tok = tokenizer(query)
        query_count = len(q_tok)

        service = build("customsearch", "v1",
                        developerKey=api_key)

        res = service.cse().list(
            q=query,
            cx=engine_id,
        ).execute()

        #Add code to get relavency input from user on each document
        rel_pages   = []
        irrel_pages = []
        i=0
        for page in res['items']:
            i+=1
            print("")
            print("PAGE #: "+ str(i))
            print("URL: " + page['htmlFormattedUrl'] )
            print('TITLE: ' + page['title'])
            print('SNIPPET: ' + page['snippet'])
            print('')
            answer = None
            while answer not in ("y", "n"):
                answer = input("Is this page relevant. Enter y/n: ")
                # answer = 'y'
                if answer == "y":
                    rel_pages.append(page)
                elif answer == "n":
                    irrel_pages.append(page)
                    continue
                else:
                    print("Please enter y or n")

        cal_perc = len(rel_pages)/10
        print("")
        print("RELEVANCE SCORE: " + str(cal_perc))
        print('')

        if cal_perc>precision:
            print("")
            print("Precision Achieved!")
            break

        print("Refining Search..." )
        print('')

        #top_words = algorithmTop2Words(rel_pages, query_count, q_tok)
        top_words = algorithmRocchioTfIdf(rel_pages, irrel_pages, query_count, q_tok)

        query = " ".join(top_words)

def tokenizer(doc):
    corpus = nltk.sent_tokenize(doc)
    for i in range(len(corpus)):
        corpus[i] = corpus[i].lower()
        corpus[i] = re.sub(r'\W', ' ', corpus[i])
        corpus[i] = re.sub(r'\s+', ' ', corpus[i])
    tokens= []
    for sentence in corpus:
        tokens = tokens + nltk.word_tokenize(sentence)

    return tokens


if __name__ == '__main__':
    api_key = sys.argv[1]
    engine_id = sys.argv[2]
    precision = sys.argv[3]
    query = sys.argv[4]

    #api_key = "AIzaSyDizICDRG4vBY5_F6mzfADnbxDAKt78LYs"
    #engine_id = '001513741995706822325:jzoyxarodil'
    #precision = 0.9
    #query = 'jaguar'

    main(api_key, engine_id, precision, query)
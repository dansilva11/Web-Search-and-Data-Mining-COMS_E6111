import pprint
import sys
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
import re
from googleapiclient.discovery import build


def main(api_key, engine_id, percision, query):
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    cal_perc = 0

    while cal_perc<percision:
        q_tok = tokenizer(query)
        query_count = len(q_tok)

        service = build("customsearch", "v1",
                        developerKey=api_key)

        res = service.cse().list(
            q=query,
            cx=engine_id,
        ).execute()

        #Add code to get relavency input from user on each document
        rel_pages = []
        i=0
        for page in res['items']:
            i+=1
            print("")
            print("PAGE #: "+ str(i))
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
                    continue
                else:
                    print("Please enter y or n")

        cal_perc = len(rel_pages)/10

        print("")
        print("RELEVANCE SCORE: " + str(cal_perc))
        print('')

        if cal_perc>percision:
            print("")
            print("Precision Achieved!")
            break

        print("Refining Search..." )
        print('')

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
        stop_words = set(stopwords.words('english'))
        words = [x for x in list(wordfreq.keys()) if x not in stop_words]
        top_words = words[0:query_count+2]
        for word in q_tok:
            if word not in top_words:
                for i in range(1,len(top_words)):
                    if top_words[-i] not in q_tok:
                        top_words[-i]=word
                        break

        query = " ".join(top_words)




    # pprint.pprint(res)

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
    percision = sys.argv[3]
    query = sys.argv[4]

    # api_key = "AIzaSyDizICDRG4vBY5_F6mzfADnbxDAKt78LYs"
    # engine_id = '001513741995706822325:jzoyxarodil'
    # percision = 0.9
    # query = 'per se'

    main(api_key, engine_id, percision, query)
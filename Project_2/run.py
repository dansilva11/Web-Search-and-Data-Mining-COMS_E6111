import sys
from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from stanfordnlp.server import CoreNLPClient

relations = {
1: "Schools_Attended",
2: "Work_For",
3: "Live_In",
4: "Top_Member_Employees"
}

annotators_ner = ['tokenize','ssplit','pos','lemma','ner']
annotators_kbp = ['tokenize','ssplit','pos','lemma','ner','depparse','coref','kbp']

# Filter out certain elements in text
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def main(api_key, engine_id, r, t, q, k):
    extractedTuples = 0
    queryIteration = 0
    pageNumberVisited = 0
    r = relations[r]

    # Initial Print of Parameters
    print("\nParameters:")
    print("Client key   = ", api_key)
    print("Engine key   = ", engine_id)
    print("Relation     = ", r)
    print("Threshold    = ", api_key)
    print("Query        = ", q)
    print("# of Tuples  = ", k)
    print("Loading necessary libraries; This should take a minute or so ...")

    while (extractedTuples < k) and (queryIteration < 9) :
        print("=========== Iteration: %s - Query: %s ===========" % (queryIteration, q))

        # Google search API (returns top 10 pages)
        service = build("customsearch", "v1",
                        developerKey=api_key)

        res = service.cse().list(
            q=q,
            cx=engine_id,
        ).execute()

        # Dissect the 10 pages
        for page in res['items']:

            # Print URL and mark as visited
            pageNumberVisited+=1
            url = page['formattedUrl']
            print(("URL (%s / 10): " + url) % pageNumberVisited )



            # Get the 20000 characters from page
            print("Fetching text from url ...")
            rawPage = requests.get(url)
            contents = BeautifulSoup(rawPage.text, 'html.parser')
            pageText = contents.findAll(text=True)
            rawText = filter(tag_visible, pageText)
            rawText = u" ".join(t.strip() for t in rawText)

            if len(rawText) > 20000:
                print(("Truncating webpage text from size (num characters) %s to 20000 ..."), len(rawText))
                rawText = rawText[:20000]

            print("Webpage length (num characters):",  len(rawText))

            # Do the annotation
            print("Annotating the webpage using [tokenize, ssplit, pos, lemma, ner] annotators ...")

            with CoreNLPClient(timeout=30000, memory='4G', be_quiet=False) as pipeline:
                for j in range(100):
                    print(f">>> Repeating {j}th time.")
                    ann_ner = pipeline.annotate(rawText, annotators=annotators_ner)
                    ann_kbp = pipeline.annotate(rawText, annotators=annotators_kbp)
                    for sentence in ann_kbp.sentence:
                        for kbp_triple in sentence.kbpTriple:
                            print(f"\t Confidence: {kbp_triple.confidence};\t Subject: {kbp_triple.subject};\t Relation: {kbp_triple.relation}; Object: {kbp_triple.object}")


        # Next iteration, need new query based off high confidence tuple
        queryIteration += 1


if __name__ == '__main__':
    '''
    api_key = sys.argv[1]
    engine_id = sys.argv[2]
    r = sys.argv[3]
    t = sys.argv[4]
    q = sys.argv[5]
    k = sys.argv[5]
    '''
    api_key = "AIzaSyDizICDRG4vBY5_F6mzfADnbxDAKt78LYs"
    engine_id = '001513741995706822325:jzoyxarodil'
    r = 2
    t = 0.7
    q = "bill gates microsoft"
    k = 10

    main(api_key, engine_id, r, t, q, k)
import sys
from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from stanfordnlp.server import CoreNLPClient
from stanfordnlp.server import to_text

extractedTuples = set()
visitedURLs = set()
sentenceNers = set()

relations = {
1: "per:schools_attended", #Schools_Attended
2: "per:employee_or_member_of",#Work_For
3: "per:cities_of_residence",#Live_In
4: "org:top_members_employees"#Top_Member_Employees
}

nersRelationtype1 = ["ORGANIZATION","PERSON"]
nersRelationtype2 = ["LOCATION","CITY", "STATE_OR_PROVINCE", "COUNTRY"]

annotators_ner = ['tokenize','ssplit','pos','lemma','ner']
annotators_kbp = ['tokenize','ssplit','pos','lemma','ner','depparse','coref','kbp']

# Filter out certain elements in text
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True



def checkKBPConfidence(ann_kbp, r, counterExtractedTuples):
    # check confidence > threshold
    for sentence in ann_kbp.sentence:
        for kbp_triple in sentence.kbpTriple:
            if kbp_triple.relation == r:
                print("\t=== Extracted Relation ===")
                print("\tSentence: ", to_text(sentence))
                print(f"\tConfidence: {kbp_triple.confidence}; Subject: {kbp_triple.subject}; Object: {kbp_triple.object}")
                if kbp_triple.confidence > t:
                    extractedTuples.add((kbp_triple.confidence,str(kbp_triple.subject)+","+str(kbp_triple.object)))
                    print("\tAdding to set of extracted relations")
                    counterExtractedTuples +=1
                else:
                    print("\tConfidence is lower than threshold confidence. Ignoring this.")
                print("\t==========")
    return counterExtractedTuples

def main(api_key, engine_id, r, t, q, k):
    queryIteration = 0
    pageNumberVisited = 0
    r = relations[r]
    counterExtractedTuples = 0

    # Initial Print of Parameters
    print("\nParameters:")
    print("Client key   = ", api_key)
    print("Engine key   = ", engine_id)
    print("Relation     = ", r)
    print("Threshold    = ", t)
    print("Query        = ", q)
    print("# of Tuples  = ", k)
    print("Loading necessary libraries; This should take a minute or so ...")

    while (len(extractedTuples) < k) and (queryIteration < 9) :
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
            url = page['formattedUrl']
            if(url in visitedURLs):
                print("Already seen URL ... skipping")
                continue;
            else:
                visitedURLs.add(url)
            pageNumberVisited+=1
            print(("URL (%s / 10): " + url) % pageNumberVisited )



            # Get the 20000 characters from page
            print("Fetching text from url ...")
            try:
                rawPage = requests.get(url)
            except:
                print("Unable to fetch URL. Continuing.")
                continue
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


            counterLastIterationExtractedTuples = counterExtractedTuples

            # TA PROVIDED CODE For KBP TRIPLE EXTRACTION
            try:
                with CoreNLPClient(timeout=30000, memory='4G', be_quiet=True) as pipeline:
                    ann_ner = pipeline.annotate(rawText, annotators=annotators_ner)
                    # print 330 lines

                    # check ner tags  ( CHECK THE RELATION HERE )
                    for sentence in ann_ner.sentence:
                        sentenceText = to_text(sentence)
                        #print("Sentence: ", sentenceText)

                        for token in sentence.token:
                            #print(f"****Token word:: {token.word};\t ner : {token.ner}; ")
                            if (token.ner not in sentenceNers):
                                if r == "per:cities_of_residence":
                                    if(token.ner in nersRelationtype2):
                                        sentenceNers.add(token.ner)
                                else:
                                    if(token.ner in nersRelationtype1):
                                        sentenceNers.add(token.ner)
                        #print("Sentence NERS: ", sentenceNers)

                        if r == "per:cities_of_residence":
                            if (nersRelationtype2[0] in sentenceNers) and (nersRelationtype2[1] in sentenceNers) \
                                or (nersRelationtype2[2] in sentenceNers) or (nersRelationtype2[3] in sentenceNers):
                                # KBP Annotate for more detailed analysis
                                ann_kbp = pipeline.annotate(sentenceText, annotators=annotators_kbp)
                                counterExtractedTuples = checkKBPConfidence(ann_kbp, r, counterExtractedTuples)
                            else:
                                #print("~~~~~~NO MATCHING NERS")
                                pass
                        else:
                            if nersRelationtype1[0] in sentenceNers and nersRelationtype1[1] in sentenceNers:
                                # KBP Annotate for more detailed analysis
                                ann_kbp = pipeline.annotate(sentenceText, annotators=annotators_kbp)
                                counterExtractedTuples = checkKBPConfidence(ann_kbp, r, counterExtractedTuples)
                            else:
                                #print("~~~~~~NO MATCHING NERS")
                                pass
                        sentenceNers.clear()
                # End of webPage
                print(f"Relations extracted from this website {counterExtractedTuples - counterLastIterationExtractedTuples} (Overall: {counterExtractedTuples})")
            except:
                print("Timeout Stanford NLP Server --- Continuing")
                pass
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
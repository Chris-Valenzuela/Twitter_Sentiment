from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# TextBlob aims to provide access to common text-processing operations through a familiar interface. 
# You can treat TextBlob objects as if they were Python strings that learned how to do Natural Language Processing
# Sentiment analysis is a text analysis method that detects polarity (e.g. a positive or negative opinion) within the text, whether a whole document, paragraph, sentence, or clause.
# Sentiment analysis aims to measure the attitude, sentiments, evaluations, attitudes, and emotions of a speaker/writer based on the computational treatment of subjectivity in a text.


analysis = TextBlob("TextBlob sure looks like it has some interesting features!")

# print(dir(analysis))

# print(analysis.translate(to='es'))

# print(analysis.tags)

# polarity = -1 to 1 is negative to positive sentiment. subjective = 0 -1, 0 = objective 1 = subjective
# print(analysis.sentiment)


# ========= TEXTBLOB ========================

# pos_count = 0
# pos_correct = 0

# with open("assets/positive.txt","r") as f:
#     for line in f.read().split('\n'):
#         analysis = TextBlob(line)
#         if analysis.subjectivity > .8:
#             if analysis.sentiment.polarity > 0:
#                 pos_correct += 1
#             pos_count +=1


# neg_count = 0
# neg_correct = 0

# with open("assets/negative.txt","r") as f:
#     for line in f.read().split('\n'):
#         analysis = TextBlob(line)
#         if analysis.subjectivity > .8:
#             if analysis.sentiment.polarity <= 0:
#                 neg_correct += 1
#             neg_count +=1


# Trying to figure out a way to get the right postive and negative reading with a good amount of samples
# print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
# print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))



# ================== Vader Sentiment =======================
analyzer = SentimentIntensityAnalyzer()

# 2.) 

# pos_count = 0
# pos_correct = 0


# threshold = .5

# with open("assets/positive.txt","r") as f:
#     for line in f.read().split('\n'):
#         vs = analyzer.polarity_scores(line)
#         if vs['compound'] >= threshold or vs['compound'] <= -threshold:
#             if vs['compound'] > 0:   
#                 pos_correct += 1
#             pos_count +=1


# neg_count = 0
# neg_correct = 0

# with open("assets/negative.txt","r") as f:
#     for line in f.read().split('\n'):
#         vs = analyzer.polarity_scores(line)
#         if vs['compound'] >= threshold or vs['compound'] <= -threshold:
#             if vs['compound'] < 0:
#                 neg_correct += 1
#             neg_count +=1

# print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
# print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))

# 3.)

# pos_count = 0
# pos_correct = 0

# with open("assets/positive.txt","r") as f:
#     for line in f.read().split('\n'):
#         vs = analyzer.polarity_scores(line)
#         if not vs['neg'] > 0.1:
#             if vs['pos']-vs['neg'] > 0:
#                 pos_correct += 1
#             pos_count +=1


# neg_count = 0
# neg_correct = 0

# with open("assets/negative.txt","r") as f:
#     for line in f.read().split('\n'):
#         vs = analyzer.polarity_scores(line)
#         if not vs['pos'] > 0.1:
#             if vs['pos']-vs['neg'] <= 0:
#                 neg_correct += 1
#             neg_count +=1

# print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
# print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))



# vs = analyzer.polarity_scores("VADER Sentiment looks intersting. I have high hopes!")
# print(vs) # {'neg': 0.0, 'neu': 0.694, 'pos': 0.306, 'compound': 0.4753} Compound score is most useful metric if u just wanted a single metric. This is saying that theres no negative
        # and more neutral and positive sentiments
        # Positive = compound score >= .5
        # neutral = -0.5 < compound score < 0.5
        # negative = compound score < -0.5



# ====== TextBLOB with a neutral zone ================


pos_count = 0
pos_correct = 0

with open("assets/positive.txt","r") as f:
    for line in f.read().split('\n'):
        analysis = TextBlob(line)

        if analysis.sentiment.polarity >= 0.0001:
            if analysis.sentiment.polarity > 0:
                pos_correct += 1
            pos_count +=1


neg_count = 0
neg_correct = 0

with open("assets/negative.txt","r") as f:
    for line in f.read().split('\n'):
        analysis = TextBlob(line)
        print(analysis.sentiment.polarity)
        if analysis.sentiment.polarity <= -0.0001:
            if analysis.sentiment.polarity <= 0:
                neg_correct += 1
            neg_count +=1

print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))

# 100 % but not many samples unless we lower the polarity. TextBlob is slower than SentimentVader more accurate than SentimentVader so long as u classify the polarities correctly 
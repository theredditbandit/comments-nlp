import pandas as pd
import string
from cleantext import clean
from textblob import TextBlob, Word     # correct the words in the sentences 

# stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 
# 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
# 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
# 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
# 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 
# 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
# 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 
# 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', 
# "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

# def stopwords_removal(sentence):
#     word_tokens = sentence.split()
#     filtered_sentence = [w for w in word_tokens if not w in stopwords]
#     return " ".join(filtered_sentence)


def correct_sentence_spelling(sentence):
    sentence = TextBlob(sentence)
    result = sentence.correct()
    return(result)


def remove_emoji(sentence):
    result = clean(sentence, no_emoji=True)
    return(result)

def remove_specialchar(sentence):
    new_string = sentence.translate(str.maketrans('', '', string.punctuation))

    return(new_string)

data = pd.read_csv(r"A6zQV9e2S1M_comments.csv")    # keep it dynamic 
#print(data.head())
#print(data.shape)
data['Comment'] = data['Comment'].str.lower()
data['Comment'] = data['Comment'].apply(lambda x: correct_sentence_spelling(x))
data['Comment'] = data['Comment'].apply(lambda x: remove_emoji(x))
data['Comment'] = data['Comment'].apply(lambda x: remove_specialchar(x))
#data['Comment'] = data['Comment'].apply(lambda x : stopwords_removal(x))
data['polarity'] = data['Comment'].apply(lambda x: TextBlob(x).sentiment.polarity)
data['pol_cat']  = 0

data['pol_cat'][data.polarity > 0] = 1
data['pol_cat'][data.polarity == 0] = 0
data['pol_cat'][data.polarity < 0] = -1

# data_pos = data[data['pol_cat'] == 1]
# data_pos = data_pos.reset_index(drop = True)

# data_neg = data[data['pol_cat'] == -1]
# data_neg = data_neg.reset_index(drop = True)

# print(data_pos.head())
# print(data_neg.head())

# data_pos.to_csv('positive_comments.csv')  # change the naming convention 
# data_neg.to_csv('negative_comments.csv')  # change the naming convention 
data.to_csv('Clean_comments.csv')
print(data.head())
#data.pol_cat.value_counts().plt.bar()
print(data.pol_cat.value_counts())
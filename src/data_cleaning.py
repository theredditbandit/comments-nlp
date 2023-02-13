import pandas as pd
import string
from cleantext import clean
from tqdm import tqdm
from comments import downloadComments
from textblob import TextBlob    # correct the words in the sentences 
from Stopwords import stopwords


filename = downloadComments()


def stopwords_removal(sentence):
    word_tokens = sentence.split()
    filtered_sentence = [w for w in word_tokens if not w in stopwords]
    return " ".join(filtered_sentence)


def correct_sentence_spelling(sentence):
    if isinstance(sentence, str):
        sentence = TextBlob(sentence)
        sentence = sentence.correct()
        return str(sentence)
    else:
        return str(sentence)


def remove_emoji(sentence):
    result = clean(sentence, no_emoji=True)
    return(result)

def remove_specialchar(sentence):
    new_string = sentence.translate(str.maketrans('', '', string.punctuation))

    return(new_string)


data = pd.read_csv(filename) 

total_operations = 4  # number of operations performed
with tqdm(total=total_operations, desc='Training Data cleaning', unit='op') as pbar:

    data['Comment'] = data['Comment'].str.lower()
    pbar.update(1)

    data['Comment'] = data['Comment'].apply(lambda x: correct_sentence_spelling(x))
    pbar.update(1)

    data['Comment'] = data['Comment'].apply(lambda x: remove_emoji(x))
    pbar.update(1)

    data['Comment'] = data['Comment'].apply(lambda x: remove_specialchar(x))
    pbar.update(1)

    data['Comment'] = data['Comment'].apply(lambda x : stopwords_removal(x))
    pbar.update(1)

    data['polarity'] = data['Comment'].apply(lambda x: TextBlob(x).sentiment.polarity)
    data['pol_cat']  = 0


data['pol_cat'][data.polarity > 0] = 1
data['pol_cat'][data.polarity <= 0] = -1


data_pos = data[data['pol_cat'] == 1]
data_pos = data_pos.reset_index(drop = True)

data_neg = data[data['pol_cat'] == -1]
data_neg = data_neg.reset_index(drop = True)

cleaned_data = f'Cleaned{filename}'
data.to_csv(cleaned_data)
print('Cleaned the data saved to file '+cleaned_data)


print('Positive Comments: ',data_pos.count())
print('Negative Comments: ',data_neg.count())


## Abstract

Sentiment analysis, also known as opinion mining, is a process of determining the sentiment expressed in a piece of text. The sentiment can be positive, negative, or neutral. The goal of sentiment analysis is to automatically classify the polarity of text based on its content.

Sentiment Analysis is increasingly becoming more and more important in the Data Science field for a variety of reasons:
- Social Media Monitoring: As these comments are unsolicited, social media posts can include some of the most frank assessments of goods, services, and companies.
- Brand Monitoring and Reputation Management: Bad reviews can snowball reputation and the longer that they are left unaddressed online, the worse the situation will become. 
- Product Ananlysis: Comments are wonderful at expressing public opinion and audience perception. This can be used to search reviews about a particluar product feature by using keywords and find only the information needed.
- Market and Competitior Analysis: Some companies are incredibly successful inspite of an alredy diluted market. With sentiment analysis, spying on your competitiors stratergy has never been easier! Understanding stratergies and approaches used by competitors or market leaders can help in building newer and better customer approaches and products.

## Introduction to our Project
Our project aims to provide a simple way to harvest the power of Machine Learning and Natural Language Processing to easily understand public sentiment on a YouTube video.

With everyone having a presence on the internet today, the amount of data generated is ginormous. This data provides valuable insights to understanding the public opinion and creating products and tools aimed at specific problems.



## Literature
### <u> Getting Started: Prerequisites </u>

1. The latest version of Python
2. Google-API-Python-Client - To recieve the comments from YouTube
3. tqdm - It adds a smart progress bar. (To make our code look less boring 😉)
4. For cleaning and processing our data, we will need the following libraries: 
  - `pandas`

  - `numpy`

  - `clean-text`

  - `textblob`

  - `string`

  - `csv`

  - `scikit-learn`


###<u>GET SET GO:</u>
####<u>Getting the Comments:</u>
The first step is to get all the comments from YouTube through the Google API. For this ,we first need to ask the user for the link to the video that needs to be analysed.

We'll start by defining a fuction `theInput`. The `theInput` function is used to prompt the user for a YouTube video URL, which we will validate using the `isvalid` function to make sure it's a valid YouTube URL. If the URL is valid, the `getId` function is called to extract the video ID from the URL.

The code for this process will look like this:

```

def theInput():
    return input(c.LIGHTBLUE_EX + "Enter a Youtube URL >" + c.WHITE + "> ")


def isvalid(url):
    """_summary_ : Validate whether the given url belongs to a youtube video or not
    Args:
        url (_str_): The video url
    Returns:
        _bool_
    """
    global regex
    regex = r"https:\/\/(?:youtu\.be\/|www\.youtube\.com\/watch\?v=)([^&#]+)"
    if re.search(regex, url):
        return True
    else:
        print(
            c.RED + "Please enter the URL to a Youtube Video ",
            c.WHITE + "Example : https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            sep="\n",
        )
        return False


def getId(url):
    """_summary_ : Extract video ID from the youtube URL for the youtube API
    Args:
        url (_str_): The video url
    Returns: The video id
    """
    id = re.search(regex, url).group(1)
    print(c.LIGHTGREEN_EX + "Video ID Found : " + c.WHITE + id)
    return id

```

### Getting the API Key:

Now we need the API Key. The API key is a unique callsign that will be used to request the comments from YouTube.

We will define a function called `getKey`. We will ask the user if they have an API Key already. If so they can enter it directly using the Input function. If the user does not have an API Key, then we will direct them to `https://console.cloud.google.com/apis/library/youtube.googleapis.com` from where they can generate API Keys.

Our code for the following will look like this:


```
def getKey():
    """_summary_ : Function to prompt the user for their API key
    Returns:
        string : The api key
    """
    API_KEY = ""
    if path.isfile(".env"):
        with open(".env") as env:
            API_KEY = env.readline()
        print(c.GREEN + "Got API KEY! ✔️")
    else:
        print(
            c.YELLOW
            + "You can get your API key from : "
            + c.BLUE
            + "https://console.cloud.google.com/apis/library/youtube.googleapis.com"
        )
        API_KEY = input(c.WHITE + "Enter API Key (Use Ctrl+Shift+V to paste):")
        validateApi(API_KEY)
        print(c.GREEN + "Saving API key . . " + c.WHITE + ". ")
        with open(".env", "w") as env:
            env.write(API_KEY)
    return API_KEY
```

#### Validating the API Key:

For this, we will define a function called `validateApi` that takes a string key as an argument, which is the user's API key. The function will be responsible for validating the key by using it to make a test request to the YouTube Data API, specifically the commentThreads method.

First we need to confirm that the API key is not an empty string. If it is empty, the we call the `exitProg` function with an error message and exit code 1.

If the API Key is not empty, we will building a YouTube object with the API Key and make a request for the `commentThreads().list()` method.

The code for this will look as follows:

```

def validateApi(key: str) -> None:
    """_summary_ : to validate the user input."""
    if key:
        pass
    else:
        exitProg("API key Invalid! ❌", 1)
    youtube = build("youtube", "v3", developerKey=key)
    request = youtube.commentThreads().list(
        part="id", maxResults=0, videoId="fT2KhJ8W-Kg"
    )
    try:
        for _ in tqdm(range(5), desc="Validating API key . . ."):
            request.execute()
    except Exception:
        exitProg(f"API key {key} is invalid! ❌", 1)
    else:
        print("API Key is Valid ✔️")
```        

#### Getting the Comments:

Now that we have our Video ID and a valid API Key, we can now request YouTube for the comments.

The `getInput()` function will prompt the user to input the number of results they want to request and then returns that number as an integer. The input is expected to be a number, with the maximum being 100 but if the user enters anything other than a number, an exception is raised and the function sets the number of results to a default value of 20. 

The `getComments()` function will take four parameters: the API key, video ID, the number of comments, and the number of results to be returned. The function then builds a YouTube object with the API key and sets the video ID, part, and maximum results. 

We will add a try-except block to execute the request, and a for loop to write the comments to a csv file. 

We will also check conditional statement that checkto see if either `allComments` is true or `results` is greater than 100. If either of these conditions is true, then the function `getAllComments()` is called and its output is returned. Otherwise, the function `getComments()` is called and its output is returned.

We will use the tqdm function to track the progress of the comments retrieval and display a progress bar. At the end of execution, the filename is returned.

The code for this task is as follows:

```
def getInput():
    try:
        results = int(
            input(
                c.YELLOW
                + "Enter the number of results you want to request (max is 100)"
                + c.WHITE
                + ": "
            )
        )
    except Exception:
        print(c.RED + "Invalid character")
        print(c.YELLOW + "Taking the default value as 20")
        results = 20

    return results

def getComments(API_KEY, vidId, numberOfComments, results=20, allComments=False):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    if allComments:
        filename = f"{vidId}_{numberOfComments}_comments.csv"
    else:
        filename = f"{vidId}_{results}_comments.csv"
    part = "id,snippet"

    def getComments():
        request = youtube.commentThreads().list(
            part=part, maxResults=results, order="time", videoId=vidId
        )
        print(c.GREEN + "Fetching  Comments . . .")
        response = request.execute()

        with open(f"{filename}", "w", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Author", "Likes", "Comment"])

            for comment in response["items"]:
                writer.writerow(
                    [
                        comment["snippet"]["topLevelComment"]["snippet"][
                            "authorDisplayName"
                        ],
                        comment["snippet"]["topLevelComment"]["snippet"]["likeCount"],
                        comment["snippet"]["topLevelComment"]["snippet"][
                            "textOriginal"
                        ],
                    ]
                )
        print(
            c.GREEN + "Comments saved to file " +
            c.WHITE + f"{filename} ✔️"
        )
        return f"{filename}"

    def getAllComments():
        next_page_token = ""
        with open(f"{filename}", "w", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Author", "Likes", "Comment"])
            pbar = tqdm(total=numberOfComments, desc=c.GREEN +
                        "Fetching  All Comments . . .")
            while True:
                request = youtube.commentThreads().list(
                    part=part,
                    maxResults=results,
                    order="time",
                    videoId=vidId,
                    pageToken=next_page_token,
                )
                response = request.execute()
                for comment in response["items"]:
                    writer.writerow(
                        [
                            comment["snippet"]["topLevelComment"]["snippet"][
                                "authorDisplayName"
                            ],
                            comment["snippet"]["topLevelComment"]["snippet"][
                                "likeCount"
                            ],
                            comment["snippet"]["topLevelComment"]["snippet"][
                                "textOriginal"
                            ],
                        ]
                    )
                    # comments += 1
                    pbar.update(2)
                next_page_token = response.get("nextPageToken", None)
                # pbar.update(1)
                if not next_page_token:
                    pbar.close()
                    print(c.GREEN + "Comments saved to file " +
                          c.WHITE + f"{filename} ✔️")
                    return f"{filename}"

    if allComments or results > 100:
        return getAllComments()  # returns filename
    else:
        return getComments()  # returns filename
```

#### Downloading the comments

The `getNumberOfComments` function takes two parameters, API_KEY and vidId, and it uses them to query the YouTube API to get the number of comments on a particular video. It returns the number of comments.

The `downloadComments` function is the main function that prompts the user for the URL of the video, gets the video ID from the URL using the `getId` function, and then calls the `getNumberOfComments` function to get the total number of comments on the video.

We will then ask the user to choose whether to download all the comments or just a certain number of results. It uses the `getInput` function to get the number of results to request. If the user chooses to download all the comments, it sets the `allComments` flag to True and sets the number of results to 100.

The `getComments` function is called with the appropriate parameters to download the comments and save them to a CSV file. If the allComments flag is True, it calls the `getAllComments` function to download all the comments.

Finally, the `downloadComments` function is called inside a try-except block, which catches the KeyboardInterrupt exception (when the user presses Ctrl+C) and exits the program.

```
def getNumberOfComments(API_KEY, vidId):
    yt = build("youtube", "v3", developerKey=API_KEY)
    request = yt.videos().list(part="statistics", id=vidId)
    response = request.execute()
    return response["items"][0]["statistics"]["commentCount"]


def downloadComments():
    API_KEY = getKey()
    while True:
        URL = theInput()
        if isvalid(URL):
            break
        else:
            continue

    id = getId(URL)

    totalComments = getNumberOfComments(API_KEY, id)
    print(c.LIGHTGREEN_EX + "Total Number of Comments : " + c.WHITE + totalComments)

    allComments = input(
        c.YELLOW +
        "Do you want to get all the comments ?[Y/N] " + c.WHITE + ": "
    )
    if allComments.upper() == "N":
        allComments = False
        results = getInput()  # gets the number of results to request
    elif allComments.upper() == "Y":
        allComments = True
        results = 100
    else:
        exitProg("Invalid Choice!")

    # returns filename
    return getComments(API_KEY, id, int(totalComments), results, allComments)


if __name__ == "__main__":
    try:
        downloadComments()
    except KeyboardInterrupt as k:
        exitProg()        
```

### STOPWORDS:

Stop words, are common words in a language that are usually removed from text when performing natural language processing tasks such as text classification or sentiment analysis.

Stop words dont contribute to the sentiment of the text and can safely be removed. This reduces the anount of space needed to store all the text data.

The stop words are as follows:


```
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves',
             'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
             'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
             'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
             'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
             'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
             'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
             'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn',
             "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
```

### Data Cleaning:

Now its time for data cleaning and processing. We need to clean and categorize comments from a CSV file. We import the necessary libraries such as pandas, string, cleantext, tqdm, comments, and textblob for this operation.

The `filename` variable downloads the comments from the internet and stores them in a CSV file. We will then define four functions for performing different operations on the comments. These functions include stopword removal, correcting spelling mistakes, removing emojis and special characters, and categorizing the comments as either positive or negative based on their polarity scores. The `pd.readcsv()` function is used to read the comments from the CSV file and load them into a Pandas DataFrame, and a progress bar is used to track the status of the data cleaning operations. The polarity scores of the comments are calculated using TextBlob and are used to categorize them as positive, negative, or neutral. Two new DataFrames, `data_pos` and `data_neg`, are created containing the positive and negative comments respectively, and the cleaned data is saved to a new CSV file. We then finally print the number of positive and negative comments in the cleaned data.

The code for all these operations is:

```
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
    return (result)


def remove_specialchar(sentence):
    new_string = sentence.translate(str.maketrans('', '', string.punctuation))

    return (new_string)


data = pd.read_csv(filename)

total_operations = 4  # number of operations performed
with tqdm(total=total_operations, desc='Training Data cleaning', unit='op') as pbar:

    data['Comment'] = data['Comment'].str.lower()
    pbar.update(1)

    data['Comment'] = data['Comment'].apply(
        lambda x: correct_sentence_spelling(x))
    pbar.update(1)

    data['Comment'] = data['Comment'].apply(lambda x: remove_emoji(x))
    pbar.update(1)

    data['Comment'] = data['Comment'].apply(lambda x: remove_specialchar(x))
    pbar.update(1)

    data['Comment'] = data['Comment'].apply(lambda x: stopwords_removal(x))
    pbar.update(1)

    data['polarity'] = data['Comment'].apply(
        lambda x: TextBlob(x).sentiment.polarity)
    data['pol_cat'] = 0


data['pol_cat'][data.polarity > 0] = 1
data['pol_cat'][data.polarity <= 0] = -1


data_pos = data[data['pol_cat'] == 1]
data_pos = data_pos.reset_index(drop=True)

data_neg = data[data['pol_cat'] == -1]
data_neg = data_neg.reset_index(drop=True)

cleaned_data = f'Cleaned{filename}'
data.to_csv(cleaned_data)
print('Cleaned the data saved to file '+cleaned_data)


print('Positive Comments: ', data_pos.count())
print('Negative Comments: ', data_neg.count())
```

### Training and Testing the Model:

Now is the final step. To train and test our sentiment analysis model. 
- Firstly, we import the necessary libraries and modules. We are using `pandas`, `sklearn` and `data_cleaning` libraries. 
- Next we will read and split the data into training and testing sets, then convert the comments to numerical feature vectors with `CountVectorizer`.
- Then, we build the model with `LinearSVC` and evaluate the model using 5-fold cross-validation. The for loop is run 100 times to get an average score for the model's accuracy and the accuracy of the model is printed using the mean score from the 5-fold cross-validation. 
- The output can be used to provide insight into the sentiment of different types of comments and can help create more accurate models to analyze sentiments.

The code for this is given below:

```
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from data_cleaning import cleaned_data
from sklearn.model_selection import cross_val_score

# Loading the data
data = pd.read_csv(cleaned_data)

# Split the data into 80% training data and 20% testing data
train_data, test_data, train_labels, test_labels = train_test_split(
    data.drop("Likes", axis=1), data["pol_cat"], test_size=0.1)

# Convert the comments to numerical feature vectors using the CountVectorizer
vectorizer = CountVectorizer()
train_data = train_data.dropna()
train_features = vectorizer.fit_transform(train_data['Comment'])
test_data = test_data.dropna()
test_features = vectorizer.transform(test_data['Comment'])


model = LinearSVC()
model.fit(train_features, train_data["pol_cat"])


for i in range(0, 100):
    scores = cross_val_score(model, train_features,
                             train_data["pol_cat"], cv=5)


print(f"Accuracy of {model.__class__.__name__}: {scores.mean()}")
```

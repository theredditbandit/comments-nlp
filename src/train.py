import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
#from sklearn import metrics
from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

# Load the data
data1 = pd.read_csv("Clean1_comments.csv")
#data2 = pd.read_csv("Clean2_comments.csv")

# Split the data into training and testing sets
# train_data = data1
# test_data = data2

# Split the data into 80% training data and 20% testing data
train_data, test_data, train_labels, test_labels = train_test_split(data1.drop("Likes", axis=1), data1["pol_cat"], test_size=0.1)

# Convert the comments to numerical feature vectors using the CountVectorizer
vectorizer = CountVectorizer()
train_data = train_data.dropna()
train_features = vectorizer.fit_transform(train_data['Comment'])
test_data = test_data.dropna()
test_features = vectorizer.transform(test_data['Comment'])

# Train a logistic regression model on the training data
# model = LogisticRegression()
# model.fit(train_features, train_data["pol_cat"])


# model = RandomForestClassifier()
# model.fit(train_features, train_data["pol_cat"])

models = [
    RandomForestClassifier(),
    SVC(),
    GaussianNB(),
    KNeighborsClassifier(),
    MLPClassifier(),
    LinearSVC(),
    LogisticRegression()
]

train_features = train_features.toarray()

# Predict the sentiment of the comments in the testing set
# predictions = model.predict(test_features)

for model in models:
    scores = cross_val_score(model, train_features, train_data["pol_cat"], cv=5)
    print(f"Accuracy of {model.__class__.__name__}: {scores.mean()}")

# Calculate the accuracy of the model
# accuracy = accuracy_score(test_data["pol_cat"], predictions)
# print("Accuracy:", accuracy)


# f1 = f1_score(test_data["pol_cat"], predictions, average='weighted')
# print("F1 Score:", f1)


# Load the dataset into a pandas DataFrame
#df = pd.read_csv("dataset.csv")

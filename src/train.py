import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import accuracy_score

# Load the data
data = pd.read_csv("Cleaned_comments.csv")

# Split the data into training and testing sets
# train_data = data[:800]
# test_data = data[800:]

# Split the data into 80% training data and 20% testing data
train_data, test_data, train_labels, test_labels = train_test_split(data.drop("Likes", axis=1), data["pol_cat"], test_size=0.2)

# Convert the comments to numerical feature vectors using the CountVectorizer
vectorizer = CountVectorizer()
train_features = vectorizer.fit_transform(train_data["Comment"])
test_features = vectorizer.transform(test_data["Comment"])

# Train a logistic regression model on the training data
model = LogisticRegression()
model.fit(train_features, train_data["pol_cat"])

# Predict the sentiment of the comments in the testing set
predictions = model.predict(test_features)


# Calculate the accuracy of the model
accuracy = accuracy_score(test_data["pol_cat"], predictions)
print("Accuracy:", accuracy)


# Load the dataset into a pandas DataFrame
#df = pd.read_csv("dataset.csv")

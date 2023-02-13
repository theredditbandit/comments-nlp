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

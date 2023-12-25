import pandas as pd
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

# Load the dataset
data = pd.read_csv('data.csv')

# Clean and preprocess the queries
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation
    text = ''.join([char for char in text if char not in string.punctuation])
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stopwords
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    # Join tokens back into text
    text = ' '.join(tokens)
    return text

data['Clean_Query'] = data['Query'].apply(preprocess_text)
# Splitting the dataset into train and test sets
X = data['Clean_Query']
y = data['Category']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize text using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Train the model (Using Naive Bayes classifier as an example)
classifier = MultinomialNB()
classifier.fit(X_train_tfidf, y_train)
# Predict on the test set
y_pred = classifier.predict(X_test_tfidf)

# Evaluate the model
print(classification_report(y_test, y_pred))

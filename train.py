import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, ne_chunk

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Load your dataset
data = pd.read_csv('data.csv')

# Function for NLP tasks
def perform_nlp_tasks(text):
    # Tokenization
    tokens = word_tokenize(text)
    print("Tokens:", tokens)
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]
    print("Lemmas:", lemmas)
    
    # Named Entity Recognition (NER)
    pos_tags = pos_tag(tokens)
    named_entities = ne_chunk(pos_tags)
    print("Named Entities:")
    print(named_entities)

# Example usage on the queries from your dataset (assuming 'Query' is in the 2nd column)
for query in data['Query']:
    print(f"Performing NLP tasks for query: {query}")
    perform_nlp_tasks(query)
    print("===============================")

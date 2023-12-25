import tensorflow as tf
from keras.layers import Embedding, Bidirectional, LSTM, Dense
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import re

# Updated dataset with user queries and corresponding ReactJS code snippets
query_code_dataset = [
    ("generate a button", "const MyButton = () => { return <button>Click me</button>; }"),
    ("create a functional component", "const MyComponent = () => { return <div>Content</div>; }"),
    ("add state to a class component", "class MyComponent extends React.Component { state = { data: '' }; render() { return <div>{this.state.data}</div>; } }"),
    ("how to make a primary button", "const PrimaryButton = () => { return <button className='primary'>Click me</button>; }"),
    ("create a button with an icon", "const IconButton = () => { return <button><i className='icon'></i>Click me</button>; }"),
    ("generate a disabled button", "const DisabledButton = () => { return <button disabled>Click me</button>; }"),
    ("add an onClick event to a button", "const ClickableButton = () => { const handleClick = () => { console.log('Button clicked!'); }; return <button onClick={handleClick}>Click me</button>; }"),
    # Add more query-code pairs as needed
]
# Separate queries and code snippets
queries, code_snippets = zip(*query_code_dataset)

# Tokenize the input sequences
tokenizer = Tokenizer()
tokenizer.fit_on_texts(queries + code_snippets)
total_words = len(tokenizer.word_index) + 1


# Convert text sequences to numerical sequences
input_sequences = tokenizer.texts_to_sequences(queries)
output_sequences = tokenizer.texts_to_sequences(code_snippets)

# Pad sequences to have a consistent length
max_sequence_length = max(len(seq) for seq in input_sequences)
padded_input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_length, padding='post')
padded_output_sequences = pad_sequences(output_sequences, maxlen=max_sequence_length, padding='post')

# Create input and output sequences for training
X = padded_input_sequences
y = padded_output_sequences

# Define the Bi-LSTM model
model = Sequential()
model.add(Embedding(input_dim=total_words, output_dim=100, input_length=max_sequence_length))
model.add(Bidirectional(LSTM(100, return_sequences=True)))
model.add(Dense(total_words, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=10, verbose=1)

# Front-end integration and text preprocessing
def preprocess_user_input(user_input, tokenizer, max_sequence_length):
    # Basic cleaning (adjust as needed)
    user_input = re.sub(r'[^\w\s]', '', user_input)
    
    # Tokenization
    tokenized_text = tokenizer.texts_to_sequences([user_input])[0]
    
    # Padding
    padded_text = pad_sequences([tokenized_text], maxlen=max_sequence_length, padding='post')
    
    return padded_text

# Code Correction
def fine_tune_model(model, X, y, epochs=5):
    # Fine-tune the model for code correction
    model.fit(X, y, epochs=epochs, verbose=1)

# Beam search with correction focus
def generate_corrected_code(seed_text, model, tokenizer, max_sequence_length, beam_size=3):
    generated_candidates = [{'code': seed_text, 'score': 1.0}]  # Initial seed with a high score

    for _ in range(max_sequence_length):
        new_candidates = []

        for candidate in generated_candidates:
            current_text = candidate['code']
            tokenized_text = tokenizer.texts_to_sequences([current_text])[0]
            padded_text = pad_sequences([tokenized_text], maxlen=max_sequence_length, padding='post')

            # Predict probabilities for the next word
            predicted_probs = model.predict(padded_text, verbose=0)

            # Top-k candidates with the highest probabilities
            top_k_indices = tf.argsort(predicted_probs, axis=-1)[:, -beam_size:]

            # Extract candidate words from the vocabulary
            candidate_words = [tokenizer.index_word.get(index, "") for index in top_k_indices.numpy().flatten()]

            for word in candidate_words:
                new_text = current_text + " " + word

                # Calculate a score based on correction criteria
                correction_score = 1.0  # Default score for valid candidates

                # Check and penalize for syntax errors
                try:
                    compile(new_text, '<string>', 'exec')
                except SyntaxError:
                    correction_score *= 0.5  # Penalize for syntax errors

                # Reward for improving variable names or simplifying expressions
                if 'var' in word or 'complex_expression' in word:
                    correction_score *= 1.2  # Reward for improving variable names or simplifying expressions

                new_candidates.append({'code': new_text, 'score': candidate['score'] * correction_score})

        # Select top-k candidates based on the combined score
        generated_candidates = sorted(new_candidates, key=lambda x: x['score'], reverse=True)[:beam_size]

    # Extract the best corrected code based on the final score
    best_corrected_code = max(generated_candidates, key=lambda x: x['score'])['code']

    return best_corrected_code

# User input
user_input = input("Ask for specific code (e.g., 'generate a button'): ")
preprocessed_input = preprocess_user_input(user_input, tokenizer, max_sequence_length)

# Generate ReactJS code based on user query
generated_code = generate_corrected_code(user_input, model, tokenizer, max_sequence_length)

# Print the generated code
print("User Query:", user_input)
print("Generated Code:", generated_code)
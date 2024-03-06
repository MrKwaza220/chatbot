import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# Define dataset of conversation pairs
conversations = [
    ("Hello", "Hi, how can I help you?"),
    ("Hi", "Hello, how can i help you?"),
    ("Can you find course for me", "Yhha sure, Give your name and surname"),
    ("Sakhumzi Kwaza", "Give me your email address"),
    ("kwaza@gmail.com", "your phone number?"),
    ("0730974288", "create your password!"),
    ("12345", "confirm your password!"),
    ("How are you?", "I'm doing well, thanks.And How are you?"),    
    ("I'm also doing well", "Nice to meet you, How can i help you?"),
    ("What is your name?", "I'm a chatbot.")  
]

# Tokenize the conversation pairs
tokenizer = Tokenizer()
tokenizer.fit_on_texts([pair[0] for pair in conversations])  # Fit on questions

# Determine vocabulary size
vocab_size = len(tokenizer.word_index) + 1

# Convert conversation pairs to sequences of integers
X_sequences = tokenizer.texts_to_sequences([pair[0] for pair in conversations])
y_sequences = tokenizer.texts_to_sequences([pair[1] for pair in conversations])

# Determine maximum sequence length
max_sequences_len = max([len(seq) for seq in X_sequences])

# Pad sequences to ensure uniform length
X = pad_sequences(X_sequences, maxlen=max_sequences_len, padding='post')
y = pad_sequences(y_sequences, maxlen=max_sequences_len, padding='post')

# Define the model architecture
model = Sequential([
    Embedding(vocab_size, 64, input_length=max_sequences_len, mask_zero=True),
    LSTM(100, return_sequences=True),
    Dense(vocab_size, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=50, verbose=1)

# Define function to generate response using trained model
def generate_response(input_text):
 
    """  #input_seq = tokenizer.texts_to_sequences([input_text])
    #padded_input = pad_sequences(input_seq, maxlen=max_sequences_len, padding='post')
    #predicted_output = model.predict(padded_input)
    #predicted_word_index = tf.argmax(predicted_output, axis=-1).numpy()
    #response = tokenizer.sequences_to_texts(predicted_word_index)
    #return response[0]"""
    
    for question, answer in conversations:
       if user_input.lower() == question.lower():
            return answer
    return "I don't have an answer for now."
    
# Test the chatbot

while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye")
        break
    response = generate_response(user_input)
    print(f"Chatbot: {response}")
    
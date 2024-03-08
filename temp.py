import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# Define dataset of conversation pairs
conversations = [
    ("Hello", "Hello!, how can I help you?"),
    ("Hi", "Hello!, how can I help you?"),
    ("Hey", "Hello!, How can I help you?"),
    ("hlw", "Hello!, How can I help you?"),
    ("h", "Hello!, How can I help you?")
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
    for question, answer in conversations:
        if input_text.lower() == question.lower():
            return answer
    return "I don't have an answer for now. Try another question"

# Function to handle options
def handle_options(option):
    if option.lower() == "find me a course":
        print("Chatbot: Sure! Please provide us your full name.")
        full_name = input("User: ")
        print("Chatbot: Provide us your email address.")
        email_address = input("User: ")
        print("Chatbot: Provide us your phone number.")
        phone_number = input("User: ")
        
        print("Thank you, check your details are correct.")
        print(f"Full Name: {full_name}")
        print(f"Email address: {email_address}")
        print(f"Phone number: {phone_number}")        
    elif option.lower() == "advise me":
        print("Chatbot: Sure! What do you need advice on?")
        advice_topic = input("User: ")
        print(f"Chatbot: Here's some advice on {advice_topic}.")
    else:
        print("Chatbot: Sorry, I didn't understand your option. Can you please repeat?")
        
# Test the chatbot
while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye")
        break
    response = generate_response(user_input)
    print(f"Chatbot: {response}")
    
    # Check for options
    if response == "Hello!, how can I help you?":
        print("Chatbot: Here are your options:")
        print("1. Find me a course")
        print("2. Advise me")
        option = input("User: ")
        handle_options(option)

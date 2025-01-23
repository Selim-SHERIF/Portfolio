import numpy as np
from nltk.corpus import stopwords
import re
import contractions
STOPWORDS = set(stopwords.words('english'))
from symspellpy import SymSpell, Verbosity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Initialize WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# Initialize SymSpell
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
sym_spell.load_dictionary("en-80k.txt", term_index=0, count_index=1)

# Function: Load labeled tweets from tuples
def load_tweets_from_tuples(file_path):
    """
    Load labeled tweets from a file containing Python tuple-like lines.

    Parameters:
    - file_path (str): Path to the file containing tuples.

    Returns:
    - list: A list of tuples (label, tokens), where label is an integer and tokens is a list of strings.
    """
    tweets = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                # Evaluate the string to convert it into a Python tuple
                tweet_tuple = eval(line.strip())
                
                # Check if it's a valid tuple with label and tokens
                if isinstance(tweet_tuple, tuple) and len(tweet_tuple) == 2:
                    label, tokens = tweet_tuple
                    if isinstance(label, int) and isinstance(tokens, list):
                        tweets.append((label, tokens))
                    else:
                        print(f"Skipping invalid tuple: {line.strip()}")
                else:
                    print(f"Skipping invalid format: {line.strip()}")
            except Exception as e:
                print(f"Error parsing line: {line.strip()}, Error: {e}")
    
    return tweets

# Function: Load GloVe embeddings
def load_glove_embeddings(glove_file_path):
    """
    Load GloVe word embeddings from a file.

    Parameters:
    - glove_file_path (str): Path to the GloVe embedding file.

    Returns:
    - dict: A dictionary mapping words to their corresponding embedding vectors.
    """
    embeddings_index = {}
    with open(glove_file_path, "r", encoding="utf-8") as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = vector
    print(f"Loaded {len(embeddings_index)} word vectors from GloVe.")
    return embeddings_index

# Function: Map vocabulary to GloVe embeddings
def map_vocab_to_glove(vocab, glove_embeddings, embedding_dim=200):
    """
    Map a vocabulary to GloVe embeddings and create an embedding matrix.

    Parameters:
    - vocab (dict): A dictionary mapping words to indices.
    - glove_embeddings (dict): Preloaded GloVe embeddings.
    - embedding_dim (int): Dimension of the embeddings.

    Returns:
    - np.array: An embedding matrix with rows corresponding to the vocabulary indices.
    """
    max_index = max(vocab.values())
    embedding_matrix = np.zeros((max_index + 1, embedding_dim))
    for word, idx in vocab.items():
        if word in glove_embeddings:
            embedding_matrix[idx] = glove_embeddings[word]
        else:
            # Initialize missing words with random small values
            embedding_matrix[idx] = np.random.uniform(-0.1, 0.1, embedding_dim)
    return embedding_matrix

# Function: Process tweets
def process_tweets(l_merged_tweets, vocab, exclude_stopwords=False):
    """
    Process a list of labeled and already lemmatized tweets.

    Parameters:
    - l_merged_tweets (list of tuples): A list where each element is a tuple (label, tokens).
    - vocab (set): A set of valid vocabulary words.
    - exclude_stopwords (bool): If True, excludes tokens that are stopwords.

    Returns:
    - list: A list of tuples (label, tokens), where label is an integer and tokens are valid.
    """
    processed_data = []

    for label, tokens in l_merged_tweets:
        # Filter tokens based on vocab and stopword flag
        filtered_tokens = [
            token for token in tokens
            if token in vocab and (not exclude_stopwords or token not in STOPWORDS)
        ]

        # Ensure the tweet is valid (has at least one valid token)
        if filtered_tokens:
            processed_data.append((label, filtered_tokens))
        else:
            print(f"Skipping invalid tweet with label {label}: {tokens}")
    
    return processed_data

# Function: Build vocabulary from tweets
def build_vocab(all_tweets, min_freq=300):
    """
    Build a vocabulary from tokenized tweets.

    Parameters:
    - merged_tweets (list of list of str): A list of tokenized tweets.
    - min_freq (int): Minimum frequency for a word to be included in the vocabulary.

    Returns:
    - vocab (dict): A dictionary mapping words to unique indices.
    - word_counts (Counter): A Counter object with word frequencies.
    """
    from collections import Counter
    word_counts = Counter()

    # Update word counts from tokenized tweets
    for tokens in all_tweets:
        word_counts.update(tokens)

    # Build vocabulary based on minimum frequency
    vocab = {
        word: idx for idx, (word, count) in enumerate(word_counts.items())
        if count >= min_freq
    }
    
    return vocab, word_counts

# Function: Load unlabeled tweets
def load_unlabeled_tweets(file_path):
    """
    Load tokenized tweets from a file where each line is a list of tokens.

    Parameters:
    - file_path (str): Path to the file containing tokenized tweets.

    Returns:
    - list: A list of tokenized tweets.
    """
    tweets = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                # Evaluate the line to convert it into a Python list
                tokens = eval(line.strip())
                
                # Ensure it's a valid list of tokens
                if isinstance(tokens, list):
                    tweets.append(tokens)
                else:
                    print(f"Skipping invalid line: {line.strip()}")
            except Exception as e:
                print(f"Error parsing line: {line.strip()}, Error: {e}")
    
    return tweets

# Function: Load preprocessed data in batches
def load_preprocessed_data_in_batches(processed_data, batch_size=10000):
    """
    Load pre-tokenized and labeled data in mini-batches.

    Args:
        processed_data (List[Tuple[int, List[str]]]): Pre-tokenized and labeled data.
        batch_size (int): Number of records to yield in each batch.

    Yields:
        Tuple[List[List[str]], List[int]]: A batch of tokenized tweets and their corresponding labels.
    """
    for i in range(0, len(processed_data), batch_size):
        batch = processed_data[i:i + batch_size]
        labels = [label for label, tokens in batch]
        tokenized_tweets = [tokens for label, tokens in batch]
        yield tokenized_tweets, labels

# Function: Convert tokenized tweets to embeddings
def get_batch_embeddings(tokenized_tweets, vocab, embedding_matrix):
    """
    Convert a batch of tokenized tweets to embeddings.

    Args:
        tokenized_tweets (List[List[str]]): List of tokenized tweets.
        vocab (dict): Vocabulary mapping words to indices.
        embedding_matrix (np.array): Pretrained embedding matrix.

    Returns:
        np.array: Embedding vectors for the batch.
    """
    embeddings = []
    for tokens in tokenized_tweets:
        indices = [vocab.get(token) for token in tokens if vocab.get(token) is not None]
        if len(indices) == 0:
            embeddings.append(np.zeros(embedding_matrix.shape[1]))  # Zero vector for empty or unknown tweets
        else:
            embeddings.append(np.mean(embedding_matrix[indices], axis=0))
    return np.array(embeddings)

# Function: Remove duplicates and empty tweets
def remove_duplicates_and_empty(tweets):
    """
    Remove duplicate and empty tweets from a list.

    Parameters:
    - tweets (list): List of tweet strings.

    Returns:
    - list: Cleaned list with unique and non-empty tweets.
    """
    unique_tweets = list(set(tweets))  # Remove duplicates
    non_empty_tweets = [tweet for tweet in unique_tweets if tweet.strip()]  # Remove empty tweets
    return non_empty_tweets

# Function: Clean raw tweets
def clean_tweets(tweets):
    """
    Clean tweets by removing URLs, user mentions, numbers, and redundant characters.

    Parameters:
    - tweets (list): List of raw tweet strings.

    Returns:
    - list: List of cleaned tweet strings.
    """
    cleaned_tweets = []
    for tweet in tweets:
        if not isinstance(tweet, str):  # Check if tweet is a string
            continue
        
        # Replace "<3" with "heart"
        tweet = re.sub(r"<3", "heart", tweet)
        # Remove URLs
        tweet = re.sub(r"<url>", "", tweet)
        # Remove user mentions
        tweet = re.sub(r"<user>", "", tweet)
        # Remove redundant whitespace
        tweet = re.sub(r"\s+", " ", tweet).strip()
        # Remove "RT" as a standalone marker
        tweet = re.sub(r"\brt\b", "", tweet)
        # Remove the # symbol but keep the word after it
        tweet = re.sub(r"#", "", tweet)
        # Remove numbers
        tweet = re.sub(r"\d+", "", tweet)
        # Convert to lowercase
        tweet = tweet.lower()
        # Normalize repeated characters (e.g., "cooool" -> "cool")
        tweet = re.sub(r'(.)\1{2,}', r'\1', tweet)
        
        # Append cleaned tweet to the list
        cleaned_tweets.append(tweet)
    
    return cleaned_tweets

# Function: Tokenize and correct tweets
def tokenize_and_correct_tweets(cleaned_tweets):
    """
    Tokenize and correct tweets using SymSpell spell checker.

    Parameters:
    - cleaned_tweets (list): List of cleaned tweet strings.

    Returns:
    - list: List of tokenized and corrected tweets.
    """
    corrected_tweets = []
    for tweet in cleaned_tweets:
        # Expand contractions
        tweet = contractions.fix(tweet)
        
        if not isinstance(tweet, str):  # Check if tweet is a string
            continue
        
        # Tokenize the tweet, keeping punctuation as separate tokens
        tokens = re.findall(r'\w+|[^\w\s]', tweet)  # Matches words and punctuation

        # Spell correction with SymSpell for word tokens only
        corrected_tokens = []
        for token in tokens:
            if re.match(r'\w+', token):  # Apply SymSpell only to words
                suggestions = sym_spell.lookup(token, Verbosity.CLOSEST, max_edit_distance=2)
                corrected_token = suggestions[0].term if suggestions else token
            else:
                corrected_token = token  # Keep punctuation unchanged
            corrected_tokens.append(corrected_token)
        
        # Append the tokenized and corrected tokens for the tweet
        corrected_tweets.append(corrected_tokens)
    
    return corrected_tweets

# Function: Lemmatize tweets
def lemmatize_tweets(tokenized_tweets):
    """
    Lemmatize tokenized tweets using WordNet lemmatizer.

    Parameters:
    - tokenized_tweets (list): List of tokenized tweets.

    Returns:
    - list: List of lemmatized tweets.
    """
    lemmatized_tweets = []
    for tokens in tokenized_tweets:
        # Lemmatize each word, preserve punctuation
        lemmatized_tokens = [
            lemmatizer.lemmatize(token) if re.match(r'\w+', token) else token
            for token in tokens
        ]
        lemmatized_tweets.append(lemmatized_tokens)
    return lemmatized_tweets

# Function: Save sorted word frequencies
def save_sorted_frequencies(word_counts, output_file):
    """
    Save word frequencies to a file in ascending order.

    Parameters:
    - word_counts (Counter): A Counter object with word frequencies.
    - output_file (str): Path to the output file.
    """
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1])  # Sort words by frequency
    
    # Save to a file
    with open(output_file, "w", encoding="utf-8") as f:
        for word, freq in sorted_word_counts:
            f.write(f"{word}\t{freq}\n")

    print(f"Words sorted by frequency saved to {output_file}")

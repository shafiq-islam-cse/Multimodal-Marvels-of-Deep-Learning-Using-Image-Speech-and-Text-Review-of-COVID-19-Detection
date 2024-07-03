# -*- coding: utf-8 -*-
"""CNN_LSTM

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/cnn-lstm-a25c9337-ff67-42c9-9d89-52f455a0aefa.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20240703/auto/storage/goog4_request%26X-Goog-Date%3D20240703T051424Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3Dae62e7f01dcf2e4991ce94d6d4a6bab3dd8a5c58e9bc05a2eff7136191ba5867a16e18f6b76e9c5155a9f0bef972bb47ec5e3240cf43a82e11866fb75ca72335bf127bb48a98d8c50eb03bf24114e8cda862e555adfbdb91d01761105ff5f1807607d1408ebd8b35a7eb0ca25db9ec8bf50a48c0634a066014270c75221921db0df24dc02377562644755b3b8fb1eec970069f39b6f2890c6eb9ce5fc0e013f8c246b9957c872f574174847b150755483ba4a5fc2bdc188aae5e06c2da3b82ccef1a2921f067cb07148f1be4f8a95ac12185ebe83785993f43420316bb87f5bd4db68e1387e35e8a389e7f11b4f37643f646e74b63b3de5ee202625a68e1f149
"""


import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'covid-19-nlp-text-classification:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F863934%2F1472453%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240703%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240703T051424Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D76c9cf9cc84fc6187588f948c72f13e2cb66eadf66acde2e9059f2347f4e889810310cb6bd0675d62caced13a5a81945fea336d8846afb7d064372dcec634e78d2d61a4fef0a54ae2b1a521428ebe2885c7265ee6523d1cf77f9a3cd272a8033a9fe5729793bed0f643efa41d4c3d8206c8e1a34c420d785d870d0f3861d564239a1cd47b554cd1c9f8270679470076cd5c8f6c7981a73496708899d5095e6b3330074f846cc1c195e313136a9d9779e8a3cc50c6af6744af62fd92fc4421ce3cfcef6ff16ccff3af1869be8ccb9f0066aa9ce6ad5e514f28a5e6c0c0a5aedbadc229ebff9cc78f612b3fe9b7a70cf48580414bedf8506438212303597e64118'

INPUT_PATH='/input'
WORKING_PATH='/working'
SYMLINK=''

!umount /input/ 2> /dev/null
shutil.rmtree('input', ignore_errors=True)
os.makedirs(INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.models import Model
from keras.layers import Input, Embedding, LSTM, Conv1D, GlobalMaxPooling1D, Concatenate, Dense
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def create_cnn_branch(embedding_layer, num_filters=150, region_sizes=[3, 5, 7]):
    cnn_layers = []
    for region_size in region_sizes:
        cnn_layer = Conv1D(filters=num_filters, kernel_size=region_size, activation='relu')(embedding_layer)
        cnn_layer = GlobalMaxPooling1D()(cnn_layer)
        cnn_layers.append(cnn_layer)
    cnn_concat = Concatenate()(cnn_layers) if len(cnn_layers) > 1 else cnn_layers[0]
    return cnn_concat

def create_bigru_branch(embedding_layer, gru_units=128):
    bigru_layer = Bidirectional((gru_units)(embedding_layer))
    return bigru_layer

def create_model(max_sequence_length=100, vocab_size=20000, embedding_dim=200, gru_units=128,
                 num_filters=150, region_sizes=[3, 5, 7], dense_units=100, num_classes=2):
    # Input layer
    input_layer = Input(shape=(max_sequence_length,), dtype='int32')

    # Embedding layer
    embedding_layer = Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_sequence_length)(input_layer)

    # CNN branch
    #cnn_branch = create_cnn_branch(embedding_layer, num_filters=num_filters, region_sizes=region_sizes)

    # LSTM branch
    bigru_branch = create_bigru_branch(embedding_layer, gru_units=gru_units)

    # Concatenation
    #concat_layer = Concatenate()([lstm_branch, cnn_branch])

    # Dense layer
    dense_layer = Dense(dense_units, activation='relu')(bigru_branch)

    # Output layer
    output_layer = Dense(num_classes, activation='softmax')(dense_layer)

    # Create the model
    model = Model(inputs=input_layer, outputs=output_layer)

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model

df_train = pd.read_csv('/input/covid-19-nlp-text-classification/Corona_NLP_train.csv', encoding = 'latin')
df_test = pd.read_csv('/input/covid-19-nlp-text-classification/Corona_NLP_test.csv', encoding = 'latin')

df_train.head()

X_train = df_train['OriginalTweet']
y_train = df_train['Sentiment']

import nltk
from nltk.corpus import stopwords

import re
def text_cleaner(tweet):
    # remove urls
    tweet = re.sub(r'http\S+', ' ', tweet)
    # remove html tags
    tweet = re.sub(r'<.*?>',' ', tweet)
    # remove digits
    tweet = re.sub(r'\d+',' ', tweet)
    # remove hashtags
    tweet = re.sub(r'#\w+',' ', tweet)
    # remove mentions
    tweet = re.sub(r'@\w+',' ', tweet)
    #removing stop words
    tweet = tweet.split()
    tweet = " ".join([word for word in tweet if not word in stop_words])
    return tweet

stop_words = stopwords.words('english')

X_train = X_train.apply(text_cleaner)
X_train.head()

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)
X = tokenizer.texts_to_sequences(X_train)
vocab_size = len(tokenizer.word_index)+1

X = pad_sequences(X, padding='post')

sentiments = {'Extremely Negative': 0,
            'Negative': 0,
            'Neutral': 1,
            'Positive':2,
            'Extremely Positive': 2
           }
y_train = y_train.map(sentiments)
labels = ['Negative', 'Neutral', 'Positive']

y_train

# Build the model
model = create_model(max_sequence_length=X.shape[1], vocab_size=vocab_size, embedding_dim=30,
                     lstm_units=15, num_filters=15, region_sizes=[3], dense_units=10,
                     num_classes=3)

model.summary()

y = to_categorical(y_train)

early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# Train the model
history = model.fit(X, y, epochs=7, batch_size=32, validation_split=0.2, callbacks=[early_stopping])

# Extracting history
train_loss = history.history['loss']
val_loss = history.history['val_loss']

# Creating epochs range
epochs = range(1, len(train_loss) + 1)

# Plotting loss
plt.figure(figsize=(10, 6))
plt.plot(epochs, train_loss, 'bo-', label='Training Loss')
plt.plot(epochs, val_loss, 'ro-', label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.show()

X_test = df_test['OriginalTweet'].copy()
y_test = df_test['Sentiment'].copy()

X_test = X_test.apply(text_cleaner)
X_test = tokenizer.texts_to_sequences(X_test)
X_test = pad_sequences(X_test, padding='post', maxlen = X.shape[1])

y_test = y_test.map(sentiments)

y_test = to_categorical(y_test)

y_test.shape

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Accuracy: {accuracy * 100:.2f}%')


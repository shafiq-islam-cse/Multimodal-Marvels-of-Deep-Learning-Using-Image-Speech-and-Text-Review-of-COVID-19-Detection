# -*- coding: utf-8 -*-
"""Coughvid-19 CNN

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/coughvid-19-crnn-attention-4c8288be-0475-489a-9a12-e07bfef35ffd.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20240703/auto/storage/goog4_request%26X-Goog-Date%3D20240703T041941Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3Dab19b479c1a57cc6d0e1e723f1cc38520d13f266d28fdf097698cc7dcc21fa375f504dcf6bcfe11982dbfdfd40b36966035cfaaaefdc52f263b6357d298c08434f830bf5349aefedfeeb18723bf162822292a5daedef532f0144d59da1d80ff5d184454bd7680802840fb21c7f25ad4f00beaee746714c2e90163fef420f1c30f18d463f84f103d0c86e82a469c26f304c0c5a9c85a96ac401d0ee9237b6027e91554bd33aac2f89581cb75bf8cc741490f08e9fb9b443f0cb958e6ecc246e4d131750bc0db5cf5ba227bc583b737fe3f3d851950f0663975f76cbbe776e2ec2813c8473c370f401f435655536ec95795c9470df6aab7c28a770df552ae78f31
"""

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES
# TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.

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
DATA_SOURCE_MAPPING = 'coughclassifier-trial:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F1087067%2F2314323%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240703%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240703T041941Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D5573f03f923921a56fa309dafe040fd9bd0e8e9bae9a8ba1a66c1fe6de64e35df7c1fc20adec66e77257a8b844de5c8a1f9ab07e2bfe9978da415284514d87f5b05251a76aaf044833e1eb19dbf45561b077c9079881a4f92f8280dc5bc93a2da4015b459c8d5b9c9d2911451f2d2f204cba0010d4adc8849f832e79b87941d2867ebc9b064192ac39de90e3b2737ff93d96d70a1eb2f301cb15d7ee9ec11af6778eb3ccbc2dc111bf36629633d84627f99fcad6ebd98adb559183e187fb4cf80ecf1921e36e829cb4f33361a625b09deec37e6073df7eb615dd97027aba6a98c94d3c25ef7ae30dce727c9a4bbcc771e65ad4535e59f9caed5e4c4744e4e42c,aicovidvn115m:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F1426873%2F2362365%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240703%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240703T041941Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D6bf718ee8a92847b59790d87dbde6a33229918dd518f4bab038bef1d77ac80a60b339caafddb1fc5cde6dd2595f30043f677c97695e5633158c683f4e5525590cc33ced2bf57e4db17be0e706d46c7d4dc42bd54ddcd6536b51b411667548234aeb307da2db0476dd376f6b5edd73a046d09ca968c5f6bbe5a859c5719e5dfb1ac2177071628bd4bc59cedadb62465f95ef0800c9a3f60c3e7c6b9f07cd90e62f1a4ab86e9f17cdb16a9789f6832a5f52e631b6cc0fec4bdfd8514ebe36e0e815ae89a3bb05c0bbb756b39a89025da20f8e33bfaa3e8e48dd43fac33bbb6acb216b8ef8a1e60339bf58591e6f5befde8a72c739cb8db09cf676a3c770a69e67a'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
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

# Commented out IPython magic to ensure Python compatibility.
# feature extractoring and preprocessing data
# %matplotlib inline
import os
import pathlib
import csv
import cv2
import librosa
import librosa.display
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import pyplot
import IPython.display as ipd

#Keras and Tensorflow
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.utils import np_utils
# Preprocessing
from sklearn.preprocessing import LabelEncoder, StandardScaler,MinMaxScaler,scale
from sklearn.utils import shuffle
from sklearn.model_selection import GridSearchCV, train_test_split, RepeatedStratifiedKFold, cross_val_score, KFold,StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score,roc_curve,roc_auc_score, auc

import warnings
warnings.filterwarnings('ignore')



metadata_train_challenge = pd.read_csv('../input/aicovidvn115m/aicv115m_public_train/aicv115m_public_train/metadata_train_challenge.csv')
print('len metadata_train_challenge',len(metadata_train_challenge.iloc[:,-1]))
metadata_train_challenge.head(4)

"""In the file cough_trial_extended.csv have sowm information that the author have done before."""

cough_trial_extended = pd.read_csv('../input/coughclassifier-trial/cough_trial_extended.csv')
print('len cough_trial_extended',len(cough_trial_extended.iloc[:,-1]))
cough_trial_extended.head(4)

"""The ideal is to combine the 2 data into 1 csv file with 2 column, The first one is the file path and the second one is encoded labels (0: negative, 1:positive)"""

header = 'filePath label'
header = header.split()

file = open('data_file_Path.csv', 'w')
with file:
    writer = csv.writer(file)
    writer.writerow(header)
data =[]
for i,label in enumerate(cough_trial_extended['class']):
    if label =='not_covid':
        label = '0'
    else:
        label = '1'
    filename = cough_trial_extended.iloc[i ,0]
    filePath = '../input/coughclassifier-trial/trial_covid/' + str(filename)
    data = [filePath, label]
    file = open('data_file_Path.csv', 'a')
    with file:
        writer = csv.writer(file)
        writer.writerow(data)

data =[]
for i,label in enumerate(metadata_train_challenge['assessment_result']):
    filename = metadata_train_challenge.iloc[i ,-1]
    filePath = '../input/aicovidvn115m/aicv115m_public_train/aicv115m_public_train/train_audio_files_8k/train_audio_files_8k/' + str(filename)
    data = [filePath, label]
    file = open('data_file_Path.csv', 'a')
    with file:
        writer = csv.writer(file)
        writer.writerow(data)
data = pd.read_csv('./data_file_Path.csv')
print ('len data', len(data.iloc[:,1]))
data.head(8)

"""# PREPROCESSING
I will extract 2D features like:
* Mel-frequency Spectrogram
* chroma

And then combine them into image to feed into the model
I may add 1D features and mean them through time (not mean them on the whole audio like phase 1):
* MFCCs
* Spectral Centroid
* Spectral Bandwidth
* Spectral Roll-off
* ZCR + energy

"""

Features = []
Number = len(data.iloc[:,1]) #Number of files I want to try on Number = len(data.iloc[:,1]) for all data
for file in data['filePath'][:Number]:

    y,sr=librosa.load(file)
    if librosa.get_duration(y=y, sr=sr) > 30:
        y,sr=librosa.load(file, duration = 30)

    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, S=None, n_fft=2048,
                                              hop_length=512, win_length=None, window='hann',
                                              center=True, pad_mode='reflect', power=2.0)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr, S=None, norm=None, n_fft=2048,
                                hop_length=512, win_length=None, window='hann',
                                center=True, pad_mode='reflect', tuning=None, n_chroma=12)
    MFCC = librosa.feature.mfcc(y=y, sr=sr, S=None, n_mfcc=20, dct_type=2, norm='ortho', lifter=0)

    ZCR = librosa.feature.zero_crossing_rate(y, frame_length=2048, hop_length=512, center=True)

    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr, S=None, n_fft=2048,
                                      hop_length=512, freq=None, win_length=None, window='hann',
                                                          center=True, pad_mode='reflect')

    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr, S=None, n_fft=2048,
                                       hop_length=512, win_length=None, window='hann',
                                       center=True, pad_mode='reflect', freq=None, centroid=None, norm=True, p=2)

    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, S=None, n_fft=2048,
                                     hop_length=512, win_length=None, window='hann',
                                     center=True, pad_mode='reflect', freq=None, roll_percent=0.85)
    feature = np.concatenate((mel_spec,chroma_stft,MFCC,ZCR,spectral_centroid,spectral_bandwidth,spectral_rolloff),
                             axis=0)
    feature = librosa.power_to_db(feature, ref=np.max)
    Features.append(feature)
    #print ('feature',feature.shape)
print ('Features',len(Features) )



plt.figure(num='Features',figsize=(9,9))
for i, img in enumerate(Features[:3]):
    plt.subplot(3,1,i+1)
    plt.title('Feature {}'.format(i))
    #S_dB = librosa.power_to_db(img, ref=np.max)
    #img = librosa.display.specshow(S_dB, x_axis='time',y_axis='mel', sr=sr,fmax=8000)
    plt.imshow(img)
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout(pad=3.0)
    #plt.axis('off')
plt.show()

"""**Saving features**

Because our audio lengths are diferent from each others, so how can we recover data from flatten array?

`len(data)/164`. The number of column are the same and equal to 164. I need to save it for my project, so I'll hide it from you guys
"""

#header = 'features label'
#header = header.split()
#file = open('raw_features.csv', 'w')
#with file:
#    writer = csv.writer(file)
#    writer.writerow(header)
#value =[]
#for i,feature in enumerate (Features):
#    feature = feature.flatten()
#    feature = ( " ".join( str(e) for e in feature ) )
#    label  = data['label'][i]
#   value = [feature, label]
#    file = open('raw_features.csv', 'a')
#    with file:
#        writer = csv.writer(file)
#        writer.writerow(value)
#raw_feature = pd.read_csv('./raw_features.csv')
#raw_feature.head(8)

"""# PREPARE FOR TRAINING

This part is for displaying the length of data.

As you can see, the majority of the files are around 15 seconds long. Only two files are longer than that, and they're far too lengthy (over 1 min). So I'm going to shorten that file to 30 seconds. And it won't make much of a difference. Not to mention if I use the length of that file to padding other pictures. The dataset would be significantly distorted
"""

Time = np.array([x.shape[1] for x in Features])
unique, counts = np.unique(Time, return_counts=True)
#print (dict(zip(unique, counts)))
max_length = np.max(Time)
print ('max_length',max_length)

width = 3  # the width of the bars
plt.figure(num='Time',figsize=(9,9))
plt.xlabel('Duration')
plt.ylabel('Number of files')

plt.title('time duration')
plt.bar(unique,counts, width ,ec='blue')
plt.show()

"""Here I want to see the range of file duration. We have 2 options:
1. Sorted padding with Batch
2. Padding on all the dataset based on the longest file
I know it's hard but tensorflow doesn't allow me to feed data with variable lengths into the model

I'd choose the first option because it's much more simple and faster

Cause the original file is so big, so I set newSize into a quarter of original size. The file length would be padding as the longest file
"""

def preprocess(feature, featureSize):

    widthTarget, heightTarget = featureSize
    height, width = feature.shape

    # scale according to factor
    newSize = (int(width / 4),41)
    #print ('newSize ={}, old size = {}'.format(newSize, feature.shape ))
    feature = cv2.resize(feature, newSize)
    # Normalization
    feature = scaler.fit_transform(feature)
    feature = np.pad(feature, ((0, 0), (0, widthTarget - feature.shape[1])), 'constant')
    #transpose
    feature = np.transpose(feature)

    return feature

"""We'll scale data and encode label"""

scaler = StandardScaler()
#print ('raw Features', Features[1])
scale_features =[]
for feature in Features[:Number]:
    feature = preprocess(feature,featureSize = (int(max_length/4),41)) #41 = 164/4
    scale_features.append(feature)

#print ('scale feature',scale_features[1])
plt.figure(num='Features transpose',figsize=(9,9))

for i, img in enumerate(scale_features[:6]):
    plt.subplot(3,3,i+1)
    plt.tight_layout(pad=3.0)
    plt.title('Feature {}'.format(i))
    plt.imshow(img)
    #plt.axis('off')
plt.show()

genre_list = data.iloc[:Number, -1]
#print ('genre_list\n',genre_list)
encoder = LabelEncoder()
y = encoder.fit_transform(genre_list) #Gán nhãn 0,1 cho class. Có thể nói là đưa về one hot coding
neg, pos = np.bincount(y)
total = neg + pos
print ('positive: {} ({:.2f}% of total) \nnegative cases: {}'.format(pos, 100 * pos/total ,neg))

"""Now we will padding the files

# Dividing data into TRAINING, VALIDATION and TEST set

I will save the indices for the Data Augmentation stage
"""

scale_features = np.array(scale_features).reshape(-1, int(max_length/4), 41, 1)
indices = range(len(scale_features))

x_train, x_test, y_train, y_test, indices_train,indices_test = train_test_split(scale_features, y, indices, test_size=0.15, shuffle = True,
                                                    random_state = None, stratify = y)

X_train, X_valid, Y_train, Y_valid,Indices_train,Indices_valid = train_test_split(x_train, y_train,indices_train, test_size=0.2, shuffle = True,
                                                    random_state = None, stratify = y_train )

Y_train = np_utils.to_categorical(Y_train, 2)
Y_valid = np_utils.to_categorical(Y_valid, 2)
print (len(Y_valid))

print ('\nlen(X_train)',len(X_train))
print ('len(X_valid)',len(X_valid))
print ('\n X_train.shape',X_train.shape)
print ('\n X_valid.shape',X_valid.shape)

"""# BUILDING MODEL

I used CNN due to it's power on time series data. The output will be flatten to classify
"""

def build_model(img_width = int(max_length/4),img_height = 41):
    # Inputs to the model

    input_img = layers.Input(
        shape=(img_width, img_height, 1), name="image", dtype="float32"
    )

    # First conv block
    x = layers.Conv2D(
        64,
        (3, 3),
        activation="relu",
        kernel_initializer="he_normal",
        padding="same",
        name="Conv1",
    )(input_img)
    x = layers.MaxPooling2D((2, 2),strides = 2, name="pool1")(x)


    # The number of filters in the last layer is 512. Reshape accordingly before
    # passing the output to the RNN part of the model

    new_shape = (int(max_length/16)-1,512) #Không cần downsampling #Nên coi shape lớp trước

    x = layers.Reshape(target_shape=new_shape, name="reshape")(x)


    x = layers.BatchNormalization(momentum = 0.8)(x)
    x = layers.Dense(512 , activation="relu")(x)
    x = layers.Dense(256 , activation="relu")(x) #

    y_pred = layers.Dense(2 , activation="softmax", name="last_dense")(x) # y pred
    model = keras.models.Model(inputs=input_img, outputs=y_pred, name="model")

    return model
model = build_model()
model.summary()

"""# TRAINING"""

epochs = 50
batch_size = 32
early_stopping_patience = 10

def scheduler(epoch):
    if epoch <= 10:
        return 1e-3
    elif 10 < epoch <=15:
        return 1e-4
    else:
        return 1e-5

# Add early stopping
my_callbacks = [
    tf.keras.callbacks.LearningRateScheduler(scheduler),
    tf.keras.callbacks.ModelCheckpoint(filepath='./covid_model/covid_model_{epoch:02d}.h5',
                                    save_freq='epoch',
                                    monitor='val_loss',
                                    mode='min',
                                    save_best_only=True,
                                    period = 5),
    tf.keras.callbacks.EarlyStopping(
    monitor="val_loss", patience=early_stopping_patience, restore_best_weights=True
    )
]

model.compile(optimizer=keras.optimizers.Adam(),loss='categorical_crossentropy')

history = model.fit(x= X_train, y= Y_train,
                validation_data=(X_valid, Y_valid),
                epochs = epochs,
                batch_size = batch_size,
                callbacks = my_callbacks,
                )

# list all data in history
print(history.history.keys())

# summarize history for loss

fig, ax = plt.subplots()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'valid'], loc='upper left')
plt.savefig('./covid_model/covid_model_loss.png')
plt.show()

"""# TESTING

I want to utilize the best model here, thus I loaded the best weights into the model. Otherwise, it would use the last model, which appears to be overfit to forecast, and that prediction is often poorer.

Choosing which output weights to use is based on the training history, and I have to change the path manualy all the time
"""

load_model =0
load_model = build_model()
load_model.load_weights('./covid_model/covid_model_10.h5')

predictions = []
predictions = model.predict(x_test)
y_predict =[]
for i in range(len(predictions)):
    predict = np.argmax(predictions[i])
    y_predict.append(predict)
#print ('y_predict',y_predict)
#print ('y test\n', y_test)

import seaborn as sns
def evaluate_matrix(y_test, y_predict, name):
    cm = confusion_matrix(y_test, y_predict)
    cm_df = pd.DataFrame(cm, index=["Negative", "Positive"], columns=["Negative", "Positive"])

    plt.figure(figsize=(10, 10))

    sns.set(font_scale=1)

    ax = sns.heatmap(cm_df, annot=True, square=True, fmt='d', linewidths=.2, cbar=0, cmap=plt.cm.Blues)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

    plt.ylabel("True labels",fontsize = 'x-large')
    plt.xlabel("Predicted labels",fontsize = 'x-large')
    plt.tight_layout()
    plt.title(name,fontsize = 'xx-large',pad = 20)

    plt.show()

    print(classification_report(y_test, y_predict, target_names=["Negative", "Positive"]))

#evaluate_matrix(y_test, y_predict,'Evaluate_matrix on orginal data')

def ROC_curve(y_test,predictions,name):

    # calculate roc curves
    lr_fpr, lr_tpr, _ = roc_curve(y_test, predictions[:,1])
    print ('AUC = {:.3f}'. format( auc(lr_fpr, lr_tpr)))
    # plot the roc curve for the model
    lw = 2
    plt.plot(lr_fpr, lr_tpr, color="darkorange",
             lw=lw, label="ROC curve (area = %0.2f)" % auc(lr_fpr, lr_tpr))
    plt.plot([0, 1], [0, 1], color="navy", lw=lw, linestyle="--")
    plt.xlim([-0.02, 1.0])
    plt.ylim([0.0, 1.05])
    # axis labels
    pyplot.xlabel('False Positive Rate',fontsize = 'x-large')
    pyplot.ylabel('True Positive Rate',fontsize = 'x-large')
    plt.title(name,fontsize = 'xx-large', pad =20)
    # show the legend
    pyplot.legend()
    # show the plot
    pyplot.show()

#ROC_curve(y_test,predictions,'AUC on original data')

"""# DATA AUGMENTATION
So the result above is quite bad and it can't be used in real life. I guess that Data Augmentation would help improve the outcome

Methods:
* Time Shift
* Adding background noise
* Stretching the sound (just a little bit)
* Changing Gain

I try not to generate fake sounds that rarely happen in real life, and distort the sound so much. So I don't recommend
* Time stretch (too much)
* Mix up

Note: You have to use data augmentation on just the train and valid set
"""

#print ('indices_train',indices_train)  # This is the dataset that I used to split train, validation set
#print ('y_train',y_train)

pos_indices = []
Aug_feature = []
for i,value in enumerate(y_train):
    if value == 1:
        pos_indices.append(indices_train[i])

y, sr = librosa.load(data['filePath'][pos_indices[1]])

def white_noise(y):
    wn = np.random.randn(len(y))
    y_wn = y + random.uniform(0, 0.005)*wn
    return y_wn

def time_shift(y):
    y = np.roll(y, random.randint(-10000,10000))
    return y

def Gain(y):
    y = y + random.uniform(-0.2,0.2)*y
    return y

def stretch(y, rate=random.uniform(0.8,1.2)):
    y = librosa.effects.time_stretch(y, rate)
    return y

plt.figure(num='Data Augmentation',figsize=(9,9))

plt.title ('original sound')
plt.plot(y)
plt.show()

plt.title ('time_shift')
plt.plot(time_shift(y))
plt.show()

plt.title ('Gain')
plt.plot(Gain(y))
plt.show()

plt.title ('Time stretch')
plt.plot(stretch(y))
plt.show()

plt.title ('white_noise')
plt.plot(white_noise(y))

plt.tight_layout(pad=3.0)
#plt.axis('off')
plt.show()

"""You can listen to these file to point out the diferences"""

print ('white noise')
ipd.Audio(white_noise(y), rate=sr)

print ('time shift')
ipd.Audio(time_shift(y), rate=sr)

print ('Gain')
ipd.Audio(Gain(y), rate=sr)

print ('time stretch')
ipd.Audio(stretch(y),rate=sr)

"""Due to the dataset imbalanced problems as the result above
> positive: 481 (35.14% of total)
> negative cases: 888

I need to generate around 200 to 250 positive cases more
"""

num_aug = (neg - pos)/1.5
if num_aug > len(pos_indices):
    iteration = int(num_aug/len(pos_indices))
else:
    iteration =1
print ('Number of file generated based on one positive case',iteration)

for file in data['filePath'][pos_indices]:
    if librosa.get_duration(y=y, sr=sr) > 30:
        y,sr=librosa.load(file, duration = 30)
    for i in range (iteration):
        y,sr=librosa.load(file)

        chance = random.randint(0,100)
        if chance <=20:
            stretch(y)
        if chance <=40:
            time_shift(y)
        if chance <=60:
            Gain(y)
        if chance <=80:
            white_noise(y)

        ZCR = librosa.feature.zero_crossing_rate(y, frame_length=2048, hop_length=512, center=True)
        if ZCR.shape[1] >= max_length:
            continue
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, S=None, n_fft=2048,
                                                  hop_length=512, win_length=None, window='hann',
                                                  center=True, pad_mode='reflect', power=2.0)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr, S=None, norm=None, n_fft=2048,
                                    hop_length=512, win_length=None, window='hann',
                                    center=True, pad_mode='reflect', tuning=None, n_chroma=12)
        MFCC = librosa.feature.mfcc(y=y, sr=sr, S=None, n_mfcc=20, dct_type=2, norm='ortho', lifter=0)


        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr, S=None, n_fft=2048,
                                          hop_length=512, freq=None, win_length=None, window='hann',
                                                              center=True, pad_mode='reflect')

        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr, S=None, n_fft=2048,
                                           hop_length=512, win_length=None, window='hann',
                                           center=True, pad_mode='reflect', freq=None, centroid=None, norm=True, p=2)

        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, S=None, n_fft=2048,
                                         hop_length=512, win_length=None, window='hann',
                                         center=True, pad_mode='reflect', freq=None, roll_percent=0.85)
        aug_feature = np.concatenate((mel_spec,chroma_stft,MFCC,ZCR,spectral_centroid,spectral_bandwidth,spectral_rolloff),
                                 axis=0)
        aug_feature = librosa.power_to_db(aug_feature, ref=np.max)
        Aug_feature.append(aug_feature)
    #print ('Aug_feature',Aug_feature.shape)
print ('Aug_feature',len(Aug_feature) )

plt.figure(num='Aug_feature',figsize=(9,9))
for i, img in enumerate(Aug_feature[:3]):
    plt.subplot(3,1,i+1)
    plt.title('Aug_feature {}'.format(i))
    plt.imshow(img)
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout(pad=3.0)
    #plt.axis('off')
plt.show()

y_aug = np.ones((1,len(Aug_feature)),dtype = np.uint8)[0]
#print (y_aug)

scale_aug_features =[]
for feature in Aug_feature:
    feature = preprocess(feature,featureSize = (int(max_length/4),41)) #41 = 164/4
    scale_aug_features.append(feature)

#print ('scale feature',scale_features[1])
plt.figure(num='Features transpose',figsize=(9,9))

for i, img in enumerate(scale_aug_features[:3]):
    plt.subplot(3,3,i+1)
    plt.tight_layout(pad=3.0)
    plt.title('scale_aug_features {}'.format(i))
    plt.imshow(img)
    #plt.axis('off')
plt.show()

"""I'll combine augmented data with x_train data, then divide it into train and valid sets."""

scale_aug_features = np.array(scale_aug_features).reshape(-1, int(max_length/4), 41, 1)
x_train = np.concatenate((x_train,scale_aug_features), axis=0)
print (len(x_train))

y_train = np.concatenate((y_train,y_aug), axis=0)

X_train, X_valid, Y_train, Y_valid = train_test_split(x_train, y_train, test_size=0.2, shuffle = True,
                                                    random_state = None, stratify = y_train )

Y_train = np_utils.to_categorical(Y_train, 2)
Y_valid = np_utils.to_categorical(Y_valid, 2)
#print (Y_valid)
print (len(Y_valid))
print('X_train.shape',X_train.shape)
print('X_valid.shape',X_valid.shape)

new_model = 0
new_model = build_model()

my_callbacks = [
    tf.keras.callbacks.LearningRateScheduler(scheduler),
    tf.keras.callbacks.ModelCheckpoint(filepath='./covid_model/new_covid_model_{epoch:02d}.h5',
                                    save_freq='epoch',
                                    monitor='val_loss',
                                    mode='min',
                                    save_best_only=True,
                                    period = 5),
    tf.keras.callbacks.EarlyStopping(
    monitor="val_loss", patience=early_stopping_patience, restore_best_weights=True
    )
]

new_model.compile(optimizer=keras.optimizers.Adam(),loss='categorical_crossentropy')

new_history = new_model.fit(x= X_train, y= Y_train,
                validation_data=(X_valid, Y_valid),
                epochs = epochs,
                batch_size = batch_size,
                callbacks = my_callbacks,
                )

# list all data in history
print(new_history.history.keys())

# summarize history for loss

fig, ax = plt.subplots()
plt.plot(new_history.history['loss'])
plt.plot(new_history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'valid'], loc='upper left')
plt.savefig('./covid_model/new_covid_model_loss.png')
plt.show()

new_load_model = 0
new_load_model = build_model()
new_load_model.load_weights('./covid_model/new_covid_model_10.h5')

new_predictions = []
new_predictions = new_load_model.predict(x_test)
y_new_predict =[]
for i in range(len(new_predictions)):
    predict = np.argmax(new_predictions[i])
    y_new_predict.append(predict)
#print ('y_predict',y_predict)
#print ('y test\n', y_test)

evaluate_matrix(y_test, y_new_predict,'Evaluate_matrix on Augmented data')
ROC_curve(y_test,new_predictions,'AUC on Augmented data')

evaluate_matrix(y_test, y_predict,'Evaluate_matrix on Original data')
ROC_curve(y_test,predictions,'AUC on Original data')

"""After using Data Augmentation, Our predictions were undeniably better
The accuracy rise but it's not the matter cause the topic like this usually evaluate with other metrics
* the positive metrics are all increase (that's good)
"""
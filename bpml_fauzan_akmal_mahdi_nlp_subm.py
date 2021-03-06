# -*- coding: utf-8 -*-
"""BPML Fauzan Akmal Mahdi - NLP Subm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e6AZenkxrddZDi_AahHgJQ9wDR1xRXMj

Fauzan Akmal Mahdi
"""

import pandas as pd

"""Panggil dataset dan beri header"""

# dataset didapat dari link berikut https://zenodo.org/record/3355823#.YMyyV_LiuUk
filename = 'ecommerceDataset.csv'

#beri header
header = ['label', 'sentence']

#baca file menjadi dataframe
df = pd.read_csv(filename, names=header)

df

"""Karena data berbentuk kategorikal maka dilakukan tahap
;
Tahap: One Hot Encoding dan membuat dataframe baru
"""

category = pd.get_dummies(df.label)
df_baru = pd.concat([df, category], axis=1)
df_baru = df_baru.drop(columns='label')
#50 ribu baris diambil sekitar 0.05 sehingga data berisi sekitar 2500 baris
df_baru = df_baru.sample(frac=0.05)

df_baru

#ubah tipe kolom menjadi string agar bisa diolah oleh tokenizer
kalimat = df_baru['sentence'].astype(str)
label = df_baru[['Books','Clothing & Accessories','Electronics','Household']].values
#label = df['label'].values

"""Membagi data training dan data testing"""

#bagi data dengan library sklearn.model_selection, data testing 0.2 atau sekitar 500 data
from sklearn.model_selection import train_test_split
kalimat_latih, kalimat_test, label_latih, label_test = train_test_split(kalimat, label, test_size=0.2)

"""Tokenisasi"""

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

#ambil 2000 data untuk dilakukan tokenisasi
tokenizer = Tokenizer(num_words=2000, oov_token="'")
tokenizer.fit_on_texts(kalimat_latih)
tokenizer.fit_on_texts(kalimat_test)

#ubah sekuens kalimat menjadi token
sekuens_latih = tokenizer.texts_to_sequences(kalimat_latih)
sekuens_test = tokenizer.texts_to_sequences(kalimat_test)

"""Embedding"""

#beri padding agar sama rata
padded_latih = pad_sequences(sekuens_latih)
padded_test = pad_sequences(sekuens_test)

"""Membuat Model"""

import tensorflow as tf
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=2000, output_dim=16),  #input dimensi sebesar jumlah kata yang ditokenisasi & dimensi embedding 16
    tf.keras.layers.LSTM(128), #dimensi output 64
    tf.keras.layers.Dense(128, activation='relu'), #layer dengan 128 perceptron
    tf.keras.layers.Dense(32, activation='relu'), #layer dengan 32 perceptron
    tf.keras.layers.Dense(32, activation='relu'), #layer dengan 32 perceptron
    tf.keras.layers.Dense(4, activation='softmax') # layer output dengan 4 perceptron
])
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

"""Buat Kelas Callback"""

#buat kelas callback untuk mempercepat proses tuning
class myCallback(tf.keras.callbacks.Callback ):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.9):
      print("\nAkurasi telah mencapai >90%!")
      self.model.stop_training = True
callbacks = myCallback()

"""Fit Model"""

#15 epochs
num_epochs = 15
#fitting model dengan batchsize 128 dan menggunakan callback
history = model.fit(padded_latih, label_latih, 
                    epochs=num_epochs, batch_size=128, 
                    validation_data=(padded_test, label_test), 
                    verbose=2, callbacks=[callbacks])

"""Plot Loss dan Akurasi dari Trained Model

Plot Loss
"""

import matplotlib.pyplot as plt
plt.plot(history.history['loss'])
plt.title('Loss Model')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train'], loc='upper right')
plt.show()

"""Plot Akurasi"""

plt.plot(history.history['accuracy'])
plt.title('Akurasi Model')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train'], loc='lower right')
plt.show()
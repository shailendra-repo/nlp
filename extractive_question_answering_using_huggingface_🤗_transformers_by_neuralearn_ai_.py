# -*- coding: utf-8 -*-
"""Extractive Question Answering using HuggingFace 🤗 Transformers by Neuralearn.ai--.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sSbGvZVH4td8v5TgMKMAMhvw3F1MhAC_

# Installation
"""

!pip install evaluate

!pip install transformers datasets

"""# Imports"""

import tensorflow as tf### models
import numpy as np### math computations
import matplotlib.pyplot as plt### plotting bar chart
import sklearn### machine learning library
import cv2## image processing
from sklearn.metrics import confusion_matrix, roc_curve### metrics
import seaborn as sns### visualizations
import datetime
import pathlib
import io
import os
import re
import string
import time
from numpy import random
import gensim.downloader as api
from PIL import Image
import tensorflow_datasets as tfds
import tensorflow_probability as tfp
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Layer
from tensorflow.keras.layers import Dense,Flatten,InputLayer,BatchNormalization,Dropout,Input,LayerNormalization
from tensorflow.keras.losses import BinaryCrossentropy,CategoricalCrossentropy, SparseCategoricalCrossentropy
from tensorflow.keras.metrics import Accuracy,TopKCategoricalAccuracy, CategoricalAccuracy, SparseCategoricalAccuracy
from tensorflow.keras.optimizers import Adam
from google.colab import drive
from google.colab import files
from datasets import load_dataset
from transformers import (DataCollatorWithPadding,create_optimizer,DebertaTokenizerFast)

BATCH_SIZE=32
MAX_LENGTH=512

"""# Data Preparation for Bert Model"""

dataset=load_dataset("covid_qa_deepset")
#dataset=load_dataset("squad")

dataset

dataset['train'][0]

answer='Mother-to-child transmission (MTCT) is the main cause of HIV-1 infection in children worldwide.'
print(len(answer)+370)

# from transformers import DistilBertTokenizerFast
# tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

# model_id="microsoft/deberta-base"
# tokenizer=DebertaTokenizerFast.from_pretrained(model_id)

from transformers import LongformerTokenizerFast,TFLongformerForQuestionAnswering
model_id="allenai/longformer-large-4096-finetuned-triviaqa"
tokenizer = LongformerTokenizerFast.from_pretrained(model_id)

tokenized_examples = tokenizer(
    dataset['train'][0]['question'],
    dataset['train'][0]["context"],
    truncation="only_second",
    max_length=MAX_LENGTH,
    stride=64,
    return_overflowing_tokens=True,
    return_offsets_mapping=True,
    padding="max_length",
)

len(tokenized_examples["input_ids"])

list_token=tokenizer.tokenize("[CLS]What is the main cause of HIV-1 infection in children?[SEP]Functional Genetic Variants in DC-SIGNR Are Associated with Mother-to-Child Transmission of HIV-1\n\nhttps://www.ncbi.nlm.nih.gov/pmc/articles/PMC2752805/\n\nBoily-Larouche, Geneviève; Iscache, Anne-Laure; Zijenah, Lynn S.; Humphrey, Jean H.; Mouland, Andrew J.; Ward, Brian J.; Roger, Michel\n2009-10-07\nDOI:10.1371/journal.pone.0007211\nLicense:cc-by\n\nAbstract: BACKGROUND: Mother-to-child transmission (MTCT) is the main cause of HIV-1 infection in children worldwide.")
print(list_token)
for i in range(len(list_token)):
  if list_token[i]=='Ġchildren':
    print(i)

tokenizer.encode("What is the main cause of HIV-1 infection in children?")

for ids in tokenized_examples["input_ids"]:
  print(ids)
  print('-->',tokenizer.decode(ids))
  #break

offset_mapping_list=[(0, 4), (4, 7), (7, 11), (11, 16), (16, 22), (22, 25), (25, 29), (29, 30), (30, 31), (31, 41), (41, 44), (44, 53), (53, 54), (0, 0), (0, 8), (8, 10), (10, 18), (18, 23), (23, 27), (27, 30), (30, 33), (33, 34), (34, 38), (38, 39), (39, 43), (43, 54), (54, 59), (59, 66), (66, 67), (67, 69), (69, 70), (70, 75), (75, 88), (88, 91), (91, 95), (95, 96), (96, 97), (97, 98), (98, 99), (99, 104), (104, 107), (107, 110), (110, 111), (111, 113), (113, 115), (115, 116), (116, 118), (118, 119), (119, 120), (120, 123), (123, 124), (124, 127), (127, 128), (128, 130), (130, 131), (131, 132), (132, 140), (140, 141), (141, 143), (143, 144), (144, 146), (146, 148), (148, 151), (151, 152), (152, 153), (153, 154), (154, 156), (156, 159), (159, 160), (160, 161), (161, 163), (163, 165), (165, 168), (168, 169), (169, 174), (174, 176), (176, 177), (177, 179), (179, 180), (180, 183), (183, 188), (188, 189), (189, 194), (194, 195), (195, 197), (197, 200), (200, 201), (201, 203), (203, 205), (205, 207), (207, 209), (209, 210), (210, 215), (215, 217), (217, 219), (219, 225), (225, 228), (228, 229), (229, 234), (234, 236), (236, 238), (238, 242), (242, 246), (246, 247), (247, 254), (254, 256), (256, 258), (258, 263), (263, 264), (264, 270), (270, 272), (272, 274), (274, 280), (280, 281), (281, 288), (288, 289), (289, 293), (293, 294), (294, 296), (296, 297), (297, 299), (299, 300), (300, 302), (302, 303), (303, 304), (304, 306), (306, 307), (307, 309), (309, 311), (311, 312), (312, 319), (319, 320), (320, 321), (321, 324), (324, 325), (325, 328), (328, 330), (330, 332), (332, 333), (333, 340), (340, 341), (341, 343), (343, 344), (344, 346), (346, 347), (347, 348), (348, 356), (356, 357), (357, 362), (362, 368), (368, 369), (369, 376),]
print(len(offset_mapping_list))

tokenized_examples

#[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,1,1,1,2,2,2,2,2,3,3,3,...



sample_mapping = tokenized_examples.pop("overflow_to_sample_mapping")
offset_mapping = tokenized_examples.pop("offset_mapping")

tokenized_examples["start_positions"] = []#[152,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
tokenized_examples["end_positions"] = []#[172,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

for i, offsets in enumerate(offset_mapping):
  if len(dataset['train'][0]['answers']['answer_start'])==0:
    tokenized_examples["start_positions"].append(0)
    tokenized_examples["end_positions"].append(0)
  else:

    start_char=dataset['train'][0]['answers']['answer_start'][0]
    end_char=start_char+len(dataset['train'][0]['answers']['text'][0])
    found=0
    start_token_position=0
    end_token_position=0

    for j,offset in enumerate(offsets):
      if offset[0]<=start_char and offset[1]>=start_char and found==0:
        start_token_position=j
        end_token_position=MAX_LENGTH

        found=1
      if offset[1]>=end_char and found==1:
        end_token_position=j
        break
    tokenized_examples["start_positions"].append(start_token_position)
    tokenized_examples["end_positions"].append(end_token_position)

print(tokenized_examples['start_positions'])
print(tokenized_examples['end_positions'])

print(tokenized_examples['input_ids'])

def preprocess_function(dataset):

  questions = [q.lstrip() for q in dataset["question"]]
  paragraphs = [p.lstrip() for p in dataset["context"]]

  tokenized_examples = tokenizer(
    questions,
    paragraphs,
    truncation="only_second",
    max_length=MAX_LENGTH,
    stride=64,
    return_overflowing_tokens=True,
    return_offsets_mapping=True,
    padding="max_length",
  )
  sample_mapping = tokenized_examples.pop("overflow_to_sample_mapping")
  offset_mapping = tokenized_examples.pop("offset_mapping")

  tokenized_examples["start_positions"] = []#[152,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  tokenized_examples["end_positions"] = []#[172,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

  for i, offsets in enumerate(offset_mapping):
    sample_index = sample_mapping[i]

    start_char=dataset["answers"][sample_index]['answer_start'][0]
    end_char=start_char+len(dataset["answers"][sample_index]['text'][0])
    found=0
    start_token_position=0
    end_token_position=0

    for j,offset in enumerate(offsets):
      if offset[0]<=start_char and offset[1]>=start_char and found==0:
        start_token_position=j
        end_token_position=MAX_LENGTH
        found=1
      if offset[1]>=end_char and found==1:
        end_token_position=j
        break
    tokenized_examples["start_positions"].append(start_token_position)
    tokenized_examples["end_positions"].append(end_token_position)

  return tokenized_examples

tokenized_dataset=dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=dataset["train"].column_names,
)

tokenized_dataset

tf_dataset = tokenized_dataset["train"].to_tf_dataset(
    shuffle=True,
    batch_size=BATCH_SIZE,
)

for i in tf_dataset.take(10):
  print(i)

train_dataset=tf_dataset.take(int(0.9*len(tf_dataset)))

val_dataset=tf_dataset.skip(int(0.9*len(tf_dataset)))

"""# Modeling"""

from transformers import LongformerTokenizer, TFLongformerForQuestionAnswering

model = TFLongformerForQuestionAnswering.from_pretrained("allenai/longformer-large-4096-finetuned-triviaqa")



model.summary()

optimizer=Adam(learning_rate=1e-5)
model.compile(optimizer=optimizer)

history=model.fit(train_dataset,validation_data=val_dataset,epochs=3)



"""# Evaluation"""

from evaluate import load

squad_metric = load("squad")
predictions = [{'prediction_text': '1999', 'id': '56e10a3be3433e1400422b22'}]
references = [{'answers': {'answer_start': [97], 'text': ['1976']}, 'id': '56e10a3be3433e1400422b22'}]
results = squad_metric.compute(predictions=predictions, references=references)
print(results)



"""# Testing"""

question="How is the virus spread?"
text="We know that the disease is caused by the SARS-CoV-2 virus, which spreads between people in several different ways.Current evidence suggests that the virus spreads mainly between people who are in close contact with each other, for example at a conversational distance.The virus can spread from an infected person’s mouth or nose in small liquid particles when they cough, sneeze, speak, sing or breathe. Another person can then contract the virus when infectious particles that pass through the air are inhaled at short range (this is often called short-range aerosol or short-range airborne transmission) or if infectious particles come into direct contact with the eyes, nose, or mouth (droplet transmission). The virus can also spread in poorly ventilated and/or crowded indoor settings, where people tend to spend longer periods of time. This is because aerosols can remain suspended in the air or travel farther than conversational distance (this is often called long-range aerosol or long-range airborne transmission). People may also become infected when touching their eyes, nose or mouth after touching surfaces or objects that have been contaminated by the virus. Further research is ongoing to better understand the spread of the virus and which settings are most risky and why. Research is also under way to study virus variants that are emerging and why some are more transmissible. For updated information on SARS-CoV-2 variants, please read the weekly epidemiologic updates."
inputs = tokenizer(question, text, return_tensors="tf")
outputs = model(**inputs)

answer_start_index = int(tf.math.argmax(outputs.start_logits, axis=-1)[0])
answer_end_index = int(tf.math.argmax(outputs.end_logits, axis=-1)[0])

predict_answer_tokens = inputs.input_ids[0, answer_start_index : answer_end_index + 1]
tokenizer.decode(predict_answer_tokens)


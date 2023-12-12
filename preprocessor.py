import os
import re
import random
import pandas as pd

#Global variables
PATTERN = r'\d+¦'
SAMPLES_PER_CLASS = 1250

# Labels dictionary
predition_mapper = {
   0: 'undefined', #not identified yet
   1: 'no_winner', #extinction or settlement 
   2: 'author',    #active party winning
   3: 'defendant', #passive party winning
}

samples = {}    
dataset_path = os.path.join(os.getcwd(), 'dataset')
files = os.listdir(dataset_path)
raw_text = ""
print(files)

#Preprocessing raw data and creating a consolidated dataset
for file in files:
    raw_text = ""
    with open(os.path.join(dataset_path, file), 'r') as f:
        raw_text = f.read()    
        label = int(file[0])
        sentences = re.split(PATTERN, raw_text)[1:]
        #Extracting the same number of random samples from each class
        samples[predition_mapper[label]] = random.sample(list(map(lambda x: (label ,x.replace("||BDC_DECISION_SEP||", " ").replace(";", "").replace("\n", " ").lower()), sentences)), SAMPLES_PER_CLASS)

consolidated_dataset = sum(samples.values(), [])
random.shuffle(consolidated_dataset)
print(len(consolidated_dataset))

#Exporting consolidated dataset to csv
df = pd.DataFrame(consolidated_dataset, columns=['label', 'text'])
df.to_csv('consolidated_dataset.csv', index=False)

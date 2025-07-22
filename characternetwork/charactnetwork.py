import sys
import os
import pathlib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import spacy
from nltk import sent_tokenize

# folderpath = pathlib.Path().parent.resolve()
# sys.path.append(os.path.join(folderpath,'../'))
import pandas as pd
from ast import literal_eval
from utils.dataloader import load_subtitles

class CharacterNetwork:
    def __init__(self):
        self.model = self.load_model()
    
    def load_model(self):
        nlp = spacy.load("en_core_web_trf")
        return nlp
    def load_sub(self):
        df = load_subtitles()
    def get_enr(self,script):
        outputners=[]
        script_sent = sent_tokenize(script)
        for sentence in script_sent:
            doc = self.model(sentence)
            ners = set()
            for entity in doc.ents:
                if entity.label_ == "PERSON":
                    fullname = entity.text
                    firstname = fullname.split(' ')[0]
                    firstname = firstname.split('!')[0]
                    firstname = firstname.split("?")[0]
                    firstname = firstname.lower()
                    ners.add(firstname)
            outputners.append(ners)
        return outputners
    def get_ners(self,dataset_path,save_path=None):
        # print("Calling load_subtitles from:", load_subtitles)
        df = load_subtitles(dataset_path)
        df = df.head(10)  # OPtional

        if save_path is not None and os.path.exists(save_path):
            df=pd.read_csv(save_path)
            df['ners']=df['ners'].apply(lambda x:literal_eval(x) if isinstance(x,str) else x)
        #RUN INFERENCE
        df['ners'] = df['script'].apply(self.get_enr)
        if save_path is not None:
            df.to_csv(save_path,index=False)

        return df
    
# ner = CharacterNetwork()  # ✅ instantiate
# dftest = ner.get_ners(
#     dataset_path="C:/Users/khatt/Documents/DemonSlayer/data/*.ass",
#     save_path="C:/Users/khatt/Documents/DemonSlayer/output/test4.csv"
# )

# print(dftest)

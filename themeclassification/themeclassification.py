import torch
from transformers import pipeline
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize
import pandas as pd
import os
import sys
import pathlib
folder_path = pathlib.Path(__file__).parent.resolve()
#sys.path.append(os.path.join(folder_path),'..')
from utils import load_subtitles
nltk.download('punkt_tab')



class ThemeClassifier():
    def __init__(self,theme_list):
        self.model_name = "facebook/bart-large-mnli"
        self.device = 0 if torch.cuda.is_available() else 'cpu'
        self.theme_list = theme_list
        self.theme_classifier = self.load_model(self.device)


    def load_model(self,device):
            themeclassifier = pipeline(
                "zero-shot-classification",
                model=self.model_name,
                device=device
        )
            return themeclassifier
        

    def themeinterference(self,script):
        script_sentence = sent_tokenize(script)
        batchsize=20
        script_batches=[]
        for i in range(0, len(script_sentence), batchsize):
            batch = " ".join(script_sentence[i:i+batchsize])
            script_batches.append(batch)

        
        themeoutput = self.theme_classifier(
            script_batches,
            self.theme_list,
            multi_label=True
        )   
        theme = {}
        for theme_list in themeoutput:
            labels = theme_list['labels']
            scores = theme_list['scores']
            for label, score in zip(labels, scores):
                if label not in theme:
                    theme[label] = []
                    theme[label].append(score)

        for keys,values in theme.items():
            theme[keys] = np.mean(values)

        return theme
    
    def get_themes(self,dataset_path,save_path=None):


        if save_path is not None and os.path.exists(save_path):
            df = pd.read_csv("save_path")
            return df
        
        #Load Dataset
        df = load_subtitles(dataset_path)
        ### Option
        df = df.head(2)

        #Run
        outputtheme = df['script'].apply(self.themeinterference)

        themes_df = pd.DataFrame(outputtheme.tolist())
        df[themes_df.columns]=themes_df


        #Save Output
        if save_path is not None:
            df.to_csv(save_path,index=False)

        return df

            


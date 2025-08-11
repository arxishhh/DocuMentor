from main.backend.utils.code_comment_extractor import comment_extractor
import torch
import pandas as pd
from torch.utils.data import DataLoader,TensorDataset
from transformers import AutoTokenizer,AutoModelForSequenceClassification
import torch.nn as nn
from huggingface_hub import hf_hub_download
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
MODEL_REPO = "archishhh/documentor-alignment-model"
model_path = hf_hub_download(repo_id=MODEL_REPO, filename="alignment_model_weights.pth")
tokenizer = AutoTokenizer.from_pretrained('microsoft/codebert-base')
classes = ['Not Aligned','Aligned']
class AlignmentClassifier(nn.Module):
  def __init__(self):
    super().__init__()
    self.codebert = AutoModelForSequenceClassification.from_pretrained('microsoft/codebert-base',num_labels = 2)
    for param in self.codebert.parameters():
      param.requires_grad = False
    for param in self.codebert.roberta.encoder.layer[-4:].parameters():
      param.requires_grad = True
    for param in self.codebert.classifier.parameters():
      param.requires_grad = True
  def forward(self,input_ids,am):
    return self.codebert(input_ids=input_ids,attention_mask=am)

def tokenizer_function(code,comment):
    tokens = tokenizer(code,comment,padding = True,return_tensors = 'pt')
    return tokens['input_ids'],tokens['attention_mask']

def process(file):
    code_comment = comment_extractor(file)
    df = pd.DataFrame(code_comment)
    ids,am = tokenizer_function(df['Code'].values.tolist(),df['Comment'].values.tolist())
    dataset = TensorDataset(ids,am)
    loader = DataLoader(dataset,batch_size=len(dataset),shuffle = False)
    return loader,df

def aligner(file):
    loader,df = process(file)
    model = AlignmentClassifier()
    model.load_state_dict(torch.load(model_path))
    model = model.to(device)
    model.eval()
    labels = []
    with torch.no_grad():
        for batch in loader:
            ids,am = batch[0],batch[1]
            ids = ids
            am = am
            output = model(ids,am)
            logits = output.logits
            pred = logits.argmax(dim = 1)
            labels.extend(pred.numpy())
    df['Labels'] = labels
    df['Labels'] = df['Labels'].map({0:'Not Aligned',1:'Aligned'})
    return df
if __name__ == '__main__':
    df = aligner('sample.py')
    print(df.head())
    print(df.columns)
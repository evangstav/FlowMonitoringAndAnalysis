import torch
from torch.utils.data import Dataset
import pandas as pd


class SupervisedDataset(Dataset):
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        # do the preprocessing here
        # self.data = preprocess(self.data)
        self.X = self.data.drop(columns='labels').values
        self.y = self.data.labels.values

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        sample = (torch.Tensor(self.X[idx], self.y[idx]))
        return sample

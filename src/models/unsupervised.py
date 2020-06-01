import pytorch_lightning as pl
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, random_split


class EncoderLSTM(pl.LightningModule):
    def __init__(self, input_dim, hidden_dim, num_layers):
        super(EncoderLSTM, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        self.lstm = nn.LSTM(input_dim,
                            hidden_dim,
                            num_layers,
                            batch_first=True)
        self.activation - nn.ReLU()

        # weight initialization
        nn.init.xavier_uniform(self.lstm.weight_ih_l0, gain=np.sqrt(2))
        nn.init.xavier_uniform(self.lstm.weight_hh_l0, gain=np.sqrt(2))

    def forward(self, x):
        pass

    def cross_entropy_loss(self, y_hat, y):
        return nn.CrossEntropy()(y_hat, y)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        return {"train_loss": self.cross_entropy_loss(y_hat, y)}

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        return {"val_loss": self.cross_entropy_loss(y_hat, y)}

    def validation_epoch_end(self, outputs):
        avg_loss = torch.stack([x["val_loss"] for x in outputs]).mean()
        tensorboard_logs = {"val_loss": avg_loss}
        return {"val_loss": avg_loss, "log": tensorboard_logs}

    def prepare_data(self):
        # get_data
        # create train_dataset
        # create val_dataset
        # possibly store them
        # return train_DS, test_DS
        pass

    def train_dataloader(self):
        # return Dataloader(get_dataset)
        pass

    def val_dataloader(self):
        pass

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=1.0e-3)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=3)
        return [optimizer], [scheduler]

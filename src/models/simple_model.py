import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torch.utils.data import DataLoader, random_split
import pytorch_lightning as pl


class Net(pl.LighningModule):
    def __init__(self, input_dim, out_dim):
        super(Net, self).__init__()
        self.lin1 = nn.Linear(input_dim, 128)
        self.lin2 = nn.Linear(128, 64)
        self.lin3 = nn.Linear(64, 32)
        self.out = nn.Linear(32, out_dim)

    def forward(self, x):
        x = F.dropout(F.relu(self.lin1(x)), p=0.5, training=self.trainig)
        x = F.dropout(F.relu(self.lin2(x)), p=0.5, training=self.trainig)
        x = F.dropout(F.relu(self.lin3(x)), p=0.5, training=self.trainig)
        out = self.out(x)
        return out

    def cross_entropy_loss(self, y_hat, y):
        return nn.CrossEntropy()(y_hat, y)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        return {'train_loss': self.cross_entropy_loss(y_hat, y)}

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        return {'val_loss': self.cross_entropy_loss(y_hat, y)}

    def validation_epoch_end(self, outputs):
        avg_loss = torch.stack([x['val_loss'] for x in outputs]).mean()
        tensorboard_logs = {'val_loss': avg_loss}
        return {'val_loss': avg_loss, 'log': tensorboard_logs}

    def prepare_data(self):
        #get_data
        #create train_dataset
        #create val_dataset
        #possibly store them
        #return train_DS, test_DS
        pass

    def train_dataloader(self):
        # return Dataloader(get_dataset)
        pass

    def val_dataloader(self):
        pass

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=1.e-3)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=3)
        return [optimizer], [scheduler]

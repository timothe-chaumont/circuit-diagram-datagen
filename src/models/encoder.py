import torch
import torch.nn as nn
import torch.nn.functional as F


class ImageEncoder(nn.Module):
    def __init__(self, ouptut_size: int, nb_input_channels: int = 1):
        super().__init__()
        # 1 input channel because images are greyscale
        self.conv1 = nn.Conv2d(nb_input_channels, 64, (3, 3), padding="valid")
        self.conv2 = nn.Conv2d(64, 128, (3, 3), padding="valid")
        self.pool1 = nn.MaxPool2d(2, 2)
        self.conv3 = nn.Conv2d(128, 256, (3, 3), padding="valid")
        self.pool2 = nn.MaxPool2d(2, 2)
        self.conv4 = nn.Conv2d(256, 512, (3, 3), padding="valid")
        self.pool3 = nn.MaxPool2d(2, 2)
        self.conv5 = nn.Conv2d(512, 512, (3, 3), padding="valid")
        self.pool4 = nn.MaxPool2d(2, 2)
        # last conv is meant to make a smaller output to feed the decoder
        self.conv6 = nn.Conv2d(512, 1, (1, 1), padding="valid")
        # the previous layer outputs a tensor of shape (batch_size, 1, 19, 19)
        self.lin1 = nn.Linear(19 * 19, ouptut_size)

    def forward(self, x):
        # scale the pixel values to be between 0 and 1
        x = F.relu(self.conv1(x))
        x = self.pool1(F.relu(self.conv2(x)))
        x = self.pool2(F.relu(self.conv3(x)))
        x = self.pool3(F.relu(self.conv4(x)))
        x = self.pool4(F.relu(self.conv5(x)))
        x = F.relu(self.conv6(x))
        # dims are (batch_size, nb_prev_channels=1, H', W')
        x = torch.flatten(x, start_dim=1)
        x = F.relu(self.lin1(x))
        return x


if __name__ == "__main__":
    net = ImageEncoder()

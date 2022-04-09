import torch
import torch.nn as nn
import torch.nn.functional as F


class ImageEncoder(nn.Module):
    def __init__(self, nb_input_channels: int = 1):
        super().__init__()
        # 1 input channel because images are greyscale
        self.conv1 = nn.Conv2d(nb_input_channels, 64, (3, 3), padding="valid")
        self.conv2 = nn.Conv2d(64, 128, (3, 3), padding="valid")
        self.conv3 = nn.Conv2d(128, 256, (3, 3), padding="valid")
        self.conv4 = nn.Conv2d(256, 512, (3, 3), padding="valid")
        self.pool1 = nn.MaxPool2d(2, 2)
        self.conv5 = nn.Conv2d(512, 512, (3, 3), padding="valid")
        self.pool2 = nn.MaxPool2d(2, 2)

    def forward(self, x):
        # scale the pixel values to be between 0 and 1
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = self.pool1(F.relu(self.conv4(x)))
        x = self.pool2(F.relu(self.conv5(x)))
        return x


if __name__ == "__main__":
    net = ImageEncoder()

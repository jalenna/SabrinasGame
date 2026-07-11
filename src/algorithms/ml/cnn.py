import torch
from . import config
import torch.nn as nn
from typing import Optional
import torch.nn.functional as F


class CNN(nn.Module):
    def __init__(self, output_size: Optional[int] = None):
        super().__init__()
        max_size: int = max(config.board_sizes[0]) * max(config.board_sizes[1])

        self.conv1 = nn.Conv2d(2, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.AdaptiveAvgPool2d((4, 4))
        self.fc1 = nn.Linear(64 * 4 * 4, 128)
        self.fc2 = nn.Linear(128, output_size if output_size else max_size)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

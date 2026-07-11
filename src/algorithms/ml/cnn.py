import torch.nn as nn


class CNN(nn.Module):
    def __init__(self, out_channels=1):
        super(CNN, self).__init__()

        self.network = nn.Sequential(
            nn.Conv2d(in_channels=2, out_channels=32,
                      kernel_size=3, padding=1),
            nn.ReLU(),

            nn.Conv2d(in_channels=32, out_channels=64,
                      kernel_size=3, padding=1),
            nn.ReLU(),

            nn.Conv2d(in_channels=64, out_channels=32,
                      kernel_size=3, padding=1),
            nn.ReLU(),

            # Use the parameter here
            nn.Conv2d(in_channels=32, out_channels=out_channels,
                      kernel_size=3, padding=1)
        )

    def forward(self, x):
        out = self.network(x)

        return out.squeeze(1)

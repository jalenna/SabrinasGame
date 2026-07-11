import torch
from . import config
from .cnn import CNN
import torch.nn as nn
import torch.optim as optim
from .board import BoardMLTrainData
from torch.utils.data import DataLoader

board_dataset: BoardMLTrainData = BoardMLTrainData(config.board_sizes)
board_dataset.generate(config.costs_range, config.sample_multiplier)

trainloader: DataLoader[BoardMLTrainData] = DataLoader(board_dataset)

model = CNN()

criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

print("Training CNN...")

for epoch in range(config.epochs):
    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        inputs, labels = data

        optimizer.zero_grad()

        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if i % 2000 == 1999:
            print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
        running_loss = 0.0

torch.save(model.state_dict(), config.save_path)

print('Finished Training, model saved to:', config.save_path)

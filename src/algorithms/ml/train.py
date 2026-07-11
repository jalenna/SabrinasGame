import torch
from . import config
from .cnn import CNN
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from .board_generator import BoardMLTrainData

board_dataset: BoardMLTrainData = BoardMLTrainData(config.board_sizes)
board_dataset.generate(config.costs_range, config.sample_multiplier)

trainloader: DataLoader[BoardMLTrainData] = DataLoader(board_dataset)

model = CNN()

criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=config.learn_rate, momentum=0.9)

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
        if i % config.log_steps == 0:
            print(
                f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / config.log_steps:.3f}')
        running_loss = 0.0

torch.save(model.state_dict(), config.save_path)

print('Finished training. Model saved to:', config.save_path)

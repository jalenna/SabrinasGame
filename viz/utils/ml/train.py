import torch
import torch.nn as nn
import torch.optim as optim
from cnn import CNN
from board import BoardGenerator

from config import save_path, board_size_options, lr, epochs, steps_per_epoch

data_gen = BoardGenerator(board_size_options)
model = CNN()

criterion = nn.L1Loss()
optimizer = optim.Adam(model.parameters(), lr)

val_x, val_y, _ = data_gen.generate_ml_sample()
val_tensor_x = torch.tensor(val_x, dtype=torch.float32).unsqueeze(0)

print("Beginning training on dynamic board dimensions...")

for epoch in range(epochs):
    model.train()
    running_loss = 0.0

    for step in range(steps_per_epoch):
        x, y, _ = data_gen.generate_ml_sample()

        batch_x = torch.tensor(x, dtype=torch.float32).unsqueeze(0)
        batch_y = torch.tensor(y, dtype=torch.float32).unsqueeze(0)

        optimizer.zero_grad()

        predictions = model(batch_x)
        loss = criterion(predictions, batch_y)

        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    epoch_loss = running_loss / steps_per_epoch
    if (epoch + 1) % 5 == 0 or epoch == 0:
        print(
            f"Epoch {epoch+1:02d}/{epochs} | Training MAE Loss: {epoch_loss:.4f}")

print("\nTraining Phase Complete.")

save_path.parent.mkdir(parents=True, exist_ok=True)

torch.save(model.state_dict(), save_path)
print(f"Model weights successfully saved to {save_path}")

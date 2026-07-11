from pathlib import Path

save_path = Path("models/checkpoints/tiler/cnn.pt")

epochs = 100
steps_per_epoch = 200
lr = 0.001

board_size_options = [4, 6, 8, 10]

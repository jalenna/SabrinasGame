import torch
from algorithms.ml.cnn import CNN
from algorithms.ml.config import save_path

loaded_model = CNN()

loaded_model.load_state_dict(torch.load(save_path))

loaded_model.eval()

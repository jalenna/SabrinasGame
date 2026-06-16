import torch
from cnn import CNN
from config import save_path

loaded_model = CNN()

loaded_model.load_state_dict(torch.load(save_path))

loaded_model.eval()

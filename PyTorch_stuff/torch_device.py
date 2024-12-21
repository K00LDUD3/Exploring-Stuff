import torch

DEVICE = 'cuda' if torch.cuda.is_available() else (
    torch.device('mps') if torch.backends.mps.is_available() else 'cpu')

print(DEVICE)

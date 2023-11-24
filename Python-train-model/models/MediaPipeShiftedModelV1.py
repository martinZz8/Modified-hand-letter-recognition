import torch
from torch import nn


class MediaPipeShiftedModelV1(nn.Module):
    def __init__(self,
                 input_shape: int,
                 hidden_units: int,
                 output_shape: int):
        super().__init__()
        self.layer_stack = nn.Sequential(
            nn.Flatten(),  # flatten inputs into a single vector (e.g. from shape (x, 21, 2) into (x, 42))
            nn.Linear(in_features=input_shape,
                      out_features=80),
            nn.LeakyReLU(),
            nn.Linear(in_features=80,
                      out_features=250),
            nn.LeakyReLU(),
            nn.Linear(in_features=250,
                      out_features=300),
            nn.LeakyReLU(),
            nn.Linear(in_features=300,
                      out_features=500),
            nn.LeakyReLU(),
            nn.Linear(in_features=500,
                      out_features=500),
            nn.LeakyReLU(),
            nn.Linear(in_features=500,
                      out_features=800),
            nn.LeakyReLU(),
            nn.Linear(in_features=800,
                      out_features=500),
            nn.LeakyReLU(),
            nn.Linear(in_features=500,
                      out_features=output_shape),
            nn.LeakyReLU()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layer_stack(x)

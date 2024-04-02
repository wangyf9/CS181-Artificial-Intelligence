import torch
import torch.nn as nn


class ChessModel(nn.Module):
    def __init__(self, input_size = 16*64, configs: dict = None):
        super(ChessModel, self).__init__()
        self.num_of_chess = configs.get("num_of_chess", 6)
        self.grid_priority = configs.get("grid_priority", None)
        self.priority_weight = configs.get("priority_weight", torch.ones(self.num_of_chess))
        self.rules = configs.get("rules", None)
        self.person_style = configs.get("person_style", None)
        self.full_connected = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.Sigmoid(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 6)
        )
    def process_input_with_config(self, x):
        if self.rules is not None:
            x = self.rules(x)
        if self.person_style is not None:
            x = self.person_style(x)
        return x
    def transform_output_to_probability(self, x: torch.Tensor):
        x = torch.abs(x * self.priority_weight)
        return x / torch.sum(x)

    def forward(self, x):
        x = self.process_input_with_config(x)
        # Check for grid priority
        if self.grid_priority is not None:
            x = x * self.grid_priority
        x = self.full_connected(x)
        return self.transform_output_to_probability(x)

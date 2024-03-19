import torch.nn as nn
from torch.nn import functional as F


class PreNormTransformerEncoderLayer(nn.Module):
    def __init__(self, d_model):
        super().__init__()
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)


class PreNormTransformerEncoder(nn.Module):
    def __init__(self, num_layers):  # Please fill in all the related parameters
        # remember to save layers and parameters to self
        super().__init__()
        self.layers = nn.ModuleList(
            [PreNormTransformerEncoderLayer() for i in range(num_layers)]
        )
        self.num_layers = num_layers

    def forward(self, source, source_attn_mask=None, source_key_padding_mask=None):
        # implement the forward process using defined layers in __init__
        # source_attn_mask and source_key_padding_mask are optional
        # source_attn_mask is the attention mask
        # source_key_padding_mask is for the padding tokens
        output = source

        for mod in self.layers:
            output = mod(
                output,
                source_attn_mask=source_attn_mask,
                source_key_padding_mask=source_key_padding_mask,
            )

        return output

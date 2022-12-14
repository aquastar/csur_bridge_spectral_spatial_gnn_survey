import torch
from torch.nn import Linear
from torch_geometric.nn import MLP, GCNConv, ChebConv, SAGEConv, GINConv, ARMAConv, GCN2Conv, SGConv, GATv2Conv, \
    global_add_pool, GATConv, GraphConv, APPNP, Sequential, GINEConv
import torch.nn.functional as F


class GCN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def forward(self, x, edge_index, edge_weight=None):
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv1(x, edge_index, edge_weight).relu()
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index, edge_weight)
        return x


class Sage(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, out_channels)

    def forward(self, x, edge_index, edge_weight=None):
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv1(x, edge_index, edge_weight).relu()
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index, edge_weight)
        return x


class ChebNet(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, K=5):
        super().__init__()
        self.conv1 = ChebConv(in_channels, hidden_channels, K)
        self.conv2 = ChebConv(hidden_channels, out_channels, K)

    def forward(self, x, edge_index, edge_weight=None):
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv1(x, edge_index, edge_weight).relu()
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index, edge_weight)
        return x


class SGC(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = SGConv(in_channels, out_channels, K=5,
                            cached=True)

    def forward(self, x, edge_index, edge_weight=None):
        x, edge_index = x, edge_index
        x = self.conv1(x, edge_index)
        return F.log_softmax(x, dim=1)


class ARMA(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = ARMAConv(in_channels, hidden_channels, num_layers=5)
        self.conv2 = ARMAConv(hidden_channels, out_channels, num_layers=5)

    def forward(self, x, edge_index, edge_weight=None):
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv1(x, edge_index, edge_weight).relu()
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index, edge_weight)
        return x


class GAPP(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.lin1 = Linear(in_channels, hidden_channels)
        self.lin2 = Linear(hidden_channels, out_channels)
        self.prop1 = APPNP(K=5, alpha=0.5, dropout=0.5, add_self_loops=True, normalize=True)

    def forward(self, x, edge_index, edge_weight=None):
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.lin1(x).relu()
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.lin2(x)
        x = self.prop1(x, edge_index)
        return x


# complete
# Linear: GCN, Sage, GIN, GAT?
# Poly: ChebNet, SGC, HCG?, GCN2?
# Rat: ARMA, GAPP

#
__all__ = ['GCN', 'Sage', 'ChebNet', 'SGC', 'ARMA', 'GAPP']

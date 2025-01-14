
from torch import nn  
import torch
class Weighted_Attention_Gate(nn.Module):
    def __init__(self,F_g,F_l,F_int, groupnorm):
        super(Weighted_Attention_Gate,self).__init__()
        self.W_g = nn.Sequential(
            nn.GroupNorm(groupnorm,F_g),
            nn.Conv2d(F_g, F_int, kernel_size=1,stride=1,padding=0,bias=True),
            )
        
        self.W_x = nn.Sequential(
            nn.GroupNorm(groupnorm,F_l) ,
            nn.Conv2d(F_l, F_int, kernel_size=1,stride=1,padding=0,bias=True),
        )

        self.psi = nn.Sequential(
            nn.GroupNorm(groupnorm,F_int), 
            nn.Conv2d(F_int, 1, kernel_size=1,stride=1,padding=0,bias=True),
            nn.Sigmoid()
        )
        
        
        
        self.relu = nn.ReLU(inplace=True) 
    def forward(self,g,x, w_x=0.7):   
        g1 = self.W_g(g) 
        x1 = self.W_x(x) 
        psi = self.relu(g1+x1)
        psi = self.psi(psi)
        out = ( psi*x *(1-w_x) ) + (x* w_x)
        return out
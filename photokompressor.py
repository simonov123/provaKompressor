#backend.py
import numpy as np
import matplotlib.pyplot as plt
import sys

def compression(q,A):
 # Estrazione RGB
 Ared = A[:,:,0]
 Agreen=A[:,:,1]
 Ablue=A[:,:,2]
 #ricomposizione rgb
 A_red   = svd_compression(A[:, :, 0], q)
 A_green = svd_compression(A[:, :, 1], q)
 A_blue  = svd_compression(A[:, :, 2], q)
 A_compressed = np.stack([A_red, A_green, A_blue], axis=2)
 return A_compressed

def svd_compression(channel, q):
    U, S, Vt = np.linalg.svd(channel, full_matrices=False)
    compressed = np.zeros(channel.shape)
    for i in range(q):
        compressed += S[i] * np.outer(U[:, i], Vt[i, :])
    return compressed







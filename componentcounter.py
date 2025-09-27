import numpy as np
import matplotlib.pyplot as plt

def counterscript(A):
 #A = plt.imread('foto.jpg') #lettura immagine
 #plt.figure("immagine originale")
 #plt.imshow(A)
 #plt.axis('off')
 # Estrazione RGB
 Ared = A[:,:,0]
 Agreen=A[:,:,1]
 Ablue=A[:,:,2]
 num=svd_counter(A[:,:,0])
 print(num)
 return num

def svd_counter(channel):
    U, S, Vt = np.linalg.svd(channel, full_matrices=False)
    compressed = np.zeros(channel.shape)
    counter=len(S)
    return counter


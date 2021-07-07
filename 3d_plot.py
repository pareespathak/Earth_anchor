import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm
#variables
# A1, A3 = angle of failure plane
#Psi = soil friction angle
#Y = soil unit weight
#B = width of strip anchor
#L = lamba (H/B)
#P = angle of uplift with verticle
#pun = uplift
#case 1

rad = np.pi / 180
sr_no = 0
Alpha1, Alpha3, PUN = [], [], []
max_pun, max_A1, max_A3, max_P = 0, 0, 0, 0
L = 1
Psi = 30
P = 15
for A1 in np.arange(1,90,0.5):
    for A3 in np.arange(1,90,0.5):
          W = ((1/(np.tan(A1*rad)+ 1e-8)) + (1/(np.tan(A3*rad)+ 1e-8))) + (2 /L)
          W = W * np.cos(P*rad)
          # soil reaction
          R1 = np.sin((A1+Psi)*rad) * np.cos((A1+Psi+P)*rad) / (np.square(np.sin(A1*rad)) + 1e-8)
          R2 = np.sin((A3+Psi)*rad) * np.cos((A3+Psi-P)*rad) / (np.square(np.sin(A3*rad)) + 1e-8)
          R = R1 + R2
          Pun = (W - R) * 0.5
          if Pun >=0:
            PUN.append(Pun)
            Alpha1.append(A1)
            Alpha3.append(A3)
          if Pun > max_pun:
              max_pun = Pun
              max_A1 = A1
              max_A3 = A3

### For 2d Plots
'''
# Create two subplots and unpack the output array immediately
f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
#f.xlabel("K value")
ax1.scatter(PUN, Alpha1, s = 2)
#ax1.xlabel('K values')
ax1.set_xlabel('K')
ax1.set_ylabel('Alpha 1')
ax2.set_xlabel('K')
ax2.set_ylabel('Alpha3')
f.suptitle('lamda = 3, Phi = 40 (degree), Beta = 15(degree)', fontsize=16)
ax1.set_title('Alpha1 vs K')
ax2.set_title('Alpha3 vs K ')
ax2.scatter(PUN, Alpha3, s = 2)
'''
############### For 3d plots ##################
Alpha3, Alpha1, PUN = np.array(Alpha3).reshape(-1,1), np.array(Alpha1).reshape(-1,1), np.array(PUN).reshape(-1,1)
x = np.outer(np.linspace(-3, 3, 32), np.ones(32))
print(x.shape, Alpha3.shape, Alpha3.shape, PUN.shape)
fig = plt.figure(figsize = (14,9))
ax = plt.axes(projection ='3d')
ax.scatter(Alpha3, Alpha1, PUN, c = np.arange(PUN.shape[0]), cmap='viridis')
ax.set_xlabel(' Alpha 3 (degree)')
ax.set_ylabel(' Alpha 1 (degree)')
ax.set_zlabel(' K')
#text = "{}: {:.4f}".format(max_pun, max_A1)
print(max_pun, max_A1, max_A3)
ax.set_title('lamda =1, Phi = 30, Beta = 15, \n max: K=1.5783, A1= 45.0, A3= 75.0', fontsize = 10)
#ax.set_suptitle('hii')
#################### mesh grid plots ##########
#Alpha3, Alpha1 = np.meshgrid(Alpha3, Alpha1)
#ax.plot_wireframe(Alpha3, Alpha1, PUN, color ='green')

plt.show()

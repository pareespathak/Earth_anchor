import numpy as np
import matplotlib.pyplot as plt
#############################################
'''
H = depth of anchor center from ground surface
R1, R2 are = soil reaction
2B = length of anchor
pud = uplift perpendicular to anchor
psi = soil fric angle
th = angle of inclination of anchor with horizontal
Y = unit weight of soil
A1, A2 = alpha
'''
Y = 15
psi = 32
pud = 0
B = 0.0508/2
H = 0.0508*8
A1 = 90 - psi
A2 = 90 - psi
rad = np.pi / 180
matplot_colors = ['red','green','orange','purple','cyan','olive','pink','gray','blue']
i = 0
for A1 in range(45,55):
  for A2 in range(45,55):
    theta, Pud = [], []
    i = i+1
    if i >= 9:
        i = 0
    for th in range(0,70):
      #weight of soil
      W1 = Y*0.5*(np.square(H-(B*np.sin(th*rad))))/(np.tan((A2 + th)*rad) + 1e-8)
      W2 = Y*0.5*(np.square(H+(B*np.sin(th*rad))))/(np.tan((A1 - th)*rad) + 1e-8)
      W3 = 2*Y*B*H*np.cos(th*rad)
      # total weight along pud
      W = np.cos(th*rad)*(W1 + W2 + W3)

      #R calculation
      #R1
      R1 = np.sin((A1 - th + psi)*rad) * np.square(H+(B*np.sin(th*rad)))
      R1 = R1/(np.square(np.sin((A1 - th)*rad)) + 1e-8)
      #R1 along Pud
      R1 = R1*np.cos((A1+psi)*rad)
      #R2
      R2 = np.sin((A2 + th + psi)*rad) * np.square(H-(B*np.sin(th*rad)))
      R2 = R2 / (np.square(np.sin((A2 + th)*rad)) + 1e-8)
      ######################
      R2 = R2*np.cos((A2 + psi)*rad)
      #net R
      R = (R1 + R2)* Y * 0.5
      ########################3
      pud = W - R
      if pud >= -1 and pud < 10:
          Pud.append(pud)
      elif pud >= 10:
          Pud.append(10)
      elif pud < -1:
          Pud.append(-1)
      else:
          Pud.append(0)
      theta.append(th)
      plt.plot(theta, Pud, color = matplot_colors[i])              # points highlight
      #plt.scatter(theta, Pud, s=3)

plt.xlabel("theta (degree)")
plt.ylabel("Pun (kN)")
plt.title("Pun vs theta graph from theta value 0 to 90 degrees")
#printing text on graph
plt.legend()
plt.show()

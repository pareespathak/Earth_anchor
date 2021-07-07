# importing necessary lib
import numpy as np
import matplotlib.pyplot as plt

#variables
B = 0.0508                           # width m
lamda = 8                            # H/B
Y = 16.8                            # gamma  kN/m3
#storing results:
Up_lift0, Up_lift30, Up_lift45, Up_lift60, Up_lift90 = [], [], [], [], []
#storing angle
Alpha = []
#loop over
for i in range (0,91,30):
    #declaring variables for max value
    max_pun, max_alpha = 0,0
    phi = i*np.pi / 180                # soil fric angle
    for A in range(1,90):
        #converting degrees to radians
        A = A* np.pi / 180
        # total weight
        W = np.square(B)* Y*((np.square(lamda)/(np.tan(A) + 1e-8) + lamda))
        Rv = -1*np.square(B)*np.square(lamda)*Y*np.sin(A + phi)*np.cos(A + phi)/(np.square(np.sin(A)) + 1e-8)
        # uplift
        Pun = (W + Rv)
        #Storing max value of Pun and angle of that corresponding value
        if Pun >= max_pun:
            max_pun = Pun
            max_alpha = A * 180 / np.pi
        # appending values of Pun in list
        if i == 0:
            if Pun >= 0:
                Up_lift0.append(Pun)
            else:
                Up_lift0.append(0)
        elif i == 30:
            if Pun >= 0:
                Up_lift30.append(Pun)
            else:
                Up_lift30.append(0)
        elif i == 60:
            if Pun >= 0:
                Up_lift60.append(Pun)
            else:
                Up_lift60.append(0)
        elif i == 90:
            if Pun >= 0:
                Up_lift90.append(Pun)
            else:
                Up_lift90.append(0)
        else:
            continue
        #print(max_pun, max_alpha,i)

phi = 45*np.pi / 180                # soil fric angle
for A in range(1,90):
    #converting degrees to radians
    Alpha.append(A)
    A = A* np.pi / 180
    # total weight
    W = np.square(B)* Y*((np.square(lamda)/(np.tan(A) + 1e-8) + lamda))
    Rv = -1*np.square(B)*np.square(lamda)*Y*np.sin(A + phi)*np.cos(A + phi)/(np.square(np.sin(A)) + 1e-8)
    # uplift
    Pun = (W + Rv)
    #Storing max value of Pun and angle of that corresponding value
    if Pun >= max_pun:
        max_pun = Pun
        max_alpha = A * 180 / np.pi
    if Pun >= 0:
        Up_lift45.append(Pun)
    else:
        Up_lift45.append(0)


#plotting results
plt.plot(Alpha, Up_lift0, color = 'black', label = "phi = 0")              # points highlight
plt.plot(Alpha, Up_lift30, color = 'red', label = "phi = 30")              # points highlight
plt.plot(Alpha, Up_lift45, color = 'green', label = "phi = 45")              # points highlight
plt.plot(Alpha, Up_lift60, color = 'blue', label = "phi = 60")              # points highlight
#plt.plot(Alpha, Up_lift90, color = 'orange', label = "phi = 0")              # points highlight
plt.scatter(Alpha, Up_lift0, s=3)
plt.scatter(Alpha, Up_lift30, s=3)
plt.scatter(Alpha, Up_lift45, s=3)
plt.scatter(Alpha, Up_lift60, s=3)
#plt.scatter(Alpha, Up_lift0)

plt.xlabel("alpha (degree)")
plt.ylabel("Pun (kN)")
plt.title("Pun vs alpha graph from alpha value 0 to 90 degrees")
#printing text on graph
plt.legend()
plt.show()

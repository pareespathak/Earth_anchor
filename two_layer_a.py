import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm
import xlwt
from xlwt import Workbook

# Workbook is created
wb = Workbook()
# add_sheet is used to create sheet.
sheet1 = wb.add_sheet("sheet 1", cell_overwrite_ok=True)

sheet1.write(0, 0,'sr_no')
sheet1.write(0, 1, 'Yr')
sheet1.write(0, 2, 'Lamda')
sheet1.write(0, 3, 'Hr')
sheet1.write(0, 4, 'Alpha_1')
sheet1.write(0, 5, 'Alpha_3')
sheet1.write(0, 6, 'K')


'''
Beta = inclination of anchor from vertical
B = width of anchor
L = lamda
########## Layer 1
H = Total Depth
P1 = psi / soil friction angle
A1,A3 = Alpha
Y1 = gamma

######### Layer 2
H2 = Depth
P2 = psi / soil friction angle
A2,A4 = Alpha
Y2 = gamma
'''
'''
L = 2                  ####### 2,4,6
Hr =                   ######## H/H1
Yr =                   ######## y2/y1 ## 1,1.25
P1 =
P2 =
'''

def Pun_calculator(L, Hr, Beta, P1, P2, Yr, A1, A2, A3, A4):
    rad = np.pi / 180
    ############# Body
    ## terms of weight
    W_1 = 0.5 / (np.tan(A1*rad) + 1e-8)
    W_2 = (Hr-1) / (np.tan(A2*rad) + 1e-8)
    W_3 = 1 / (L + 1e-8)
    W_4 = (Hr - 1) / (np.tan(A4*rad) + 1e-8)
    W_5 = 0.5 / (np.tan(A3*rad) + 1e-8)
    #######
    WT_1 = W_1 + W_2 + W_3 + W_4 + W_5
    #######
    W_6 = np.square(Hr-1) * 0.5 / (np.tan(A4*rad) + 1e-8)
    W_7 = (Hr-1) / (L + 1e-8)
    W_8 = np.square(Hr-1) * 0.5 / (np.tan(A2*rad) + 1e-8)
    ############ Total
    WT_2 =  (W_6 + W_7 + W_8) * Yr
    WT = (WT_1 + WT_2) * np.cos(Beta*rad)

    ####################### R terms as per rakesh sir derivation
    R1 = np.sin((A1+P1)*rad)* 0.5 * np.cos((A1 + Beta + P1)*rad) / (np.square(np.sin(A1*rad)) + 1e-8)
    #########################
    R_2_1 = Yr * np.square(Hr-1) * np.sin((A2 + P2)*rad)*0.5/(np.square(np.sin(A2*rad)) + 1e-8)
    #
    R_2_2 = np.sin((A1+P1)*rad)*(Hr-1)/(np.sin(A1*rad) + 1e-8)
    R_2_2 = R_2_2 / (np.sin(A2*rad) + 1e-8)

    R2 = (R_2_1 + R_2_2)*np.cos((A2+Beta+P2)*rad) #########

    ##################
    R3 = np.sin((A3+P1)*rad) * 0.5 * np.cos((A3 - Beta + P1)*rad) / (np.square(np.sin(A3*rad)) + 1e-8)
    #########################
    R_4_1 = Yr * np.square(Hr-1) * np.sin((A4 + P2)*rad)*0.5 / (np.square(np.sin(A4*rad)) + 1e-8)
    #
    R_4_2 = np.sin((A3+P1)*rad)*(Hr-1)/(np.sin(A3*rad) + 1e-8)
    R_4_2 = R_4_2 / (np.sin(A4*rad) + 1e-8)

    R4 = (R_4_1 + R_4_2)*np.cos((A4-Beta+P2)*rad) #########
    ##############
    RT = R1 + R2 + R3 + R4
    ############################################
    Pun = WT - RT

    return Pun



#### main loops

### list for plotting
Alpha1, Alpha2, Alpha3, Alpha4, K_max = [], [], [], [], []

## storing max values
m_Alpha1, m_Alpha2, m_Alpha3, m_Alpha4, m_K = 0, 0, 0, 0, 0

############ Cases for soil properties
'''
status = 0
if P1 > P2:
    status = 1
else:
    status = 0

if status == 1:
    for A4 in np.arange(1,90):
        for A2 in np.arange(1,A4):
            for A3 in np.arange(A4+1,91):
                for A1 in np.arange(A2+1,A3):
                    Pun = Pun_calculator(L, Hr, Beta, P1, P2, Yr, A1, A2, A3, A4)  #### parameters
                    if Pun >= 0:
                        Alpha1.append(A1)
                        Alpha2.append(A2)
                        Alpha3.append(A3)
                        Alpha4.append(A4)
                        K_max.append(Pun)
                    if Pun > m_K:
                        m_Alpha1 = A1
                        m_Alpha2 = A2
                        m_Alpha3 = A3
                        m_Alpha4 = A4
                        m_K = Pun


if status == 0:
    for A4 in np.arange(2,91):
        for A2 in np.arange(2,A4):
            for A3 in np.arange(1,A4):
                for A1 in np.arange(1,A2):
                    Pun = Pun_calculator(L, Hr, Beta, P1, P2, Yr, A1, A2, A3, A4)  #### parameters
                    if Pun >= 0:
                        Alpha1.append(A1)
                        Alpha2.append(A2)
                        Alpha3.append(A3)
                        Alpha4.append(A4)
                        K_max.append(Pun)
                    if Pun > m_K:
                        m_Alpha1 = A1
                        m_Alpha2 = A2
                        m_Alpha3 = A3
                        m_Alpha4 = A4
                        m_K = Pun

'''
Beta = 0
####### 2,4,6
######## H/H1
Yr = 1                  ######## y2/y1 ## 1,1.25
P1 = 40
P2 = 40
sr_no = 0
#HR_list = [1, 4/3, 2, 4]
HR_list = [1]
YR_list = [1, 1.4]
for Yr in YR_list:
    for L in range(3,6,2):
        for Hr in HR_list:
            sr_no = sr_no + 1
            m_Alpha1, m_Alpha2, m_Alpha3, m_Alpha4, m_K = 0, 0, 0, 0, 0
            for A2 in np.arange(2,91):
                for A1 in np.arange(1,A2):
                    A4 = A2
                    A3 = A1
                    Pun = Pun_calculator(L, Hr, Beta, P1, P2, Yr, A1, A2, A3, A4)  #### parameters
                    Pun = Pun * L
                    if Pun >= 0:
                        Alpha1.append(A1)
                        Alpha2.append(A2)
                        Alpha3.append(A3)
                        Alpha4.append(A4)
                        K_max.append(Pun)
                    if Pun > m_K:
                        m_Alpha1 = A1
                        m_Alpha2 = A2
                        m_Alpha3 = A3
                        m_Alpha4 = A4
                        m_K = Pun

            sheet1.write(sr_no,0,sr_no)
            sheet1.write(sr_no,1,Yr)
            sheet1.write(sr_no,2,L)
            sheet1.write(sr_no,3,Hr)
            sheet1.write(sr_no,4,int(m_Alpha1))
            sheet1.write(sr_no,5,int(m_Alpha2))
            sheet1.write(sr_no,6,m_K)
            sheet1.write(sr_no, 7, 'P1 = 30, P2 = 40')



wb.save('Paper_check1.xls')
#plt.legend()
print("done")













###########################################################################

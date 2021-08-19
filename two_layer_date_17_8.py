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
sheet1.write(0, 5, 'Alpha_2')
sheet1.write(0, 6, 'Alpha_3')
sheet1.write(0, 7, 'Alpha_4')
sheet1.write(0, 8, 'K')

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
P1 = 30
P2 = 40
rad = np.pi / 180
HR_list = [0, 0.25, 0.5, 0.75, 1]
YR_list = [1, 1.25]
Beta = 0
sr_no = 0
############ Cases for soil properties
status = 0
if P1 > P2:
    status = 1
    print("P1>P2")
else:
    status = 0
    print("P2>P1")
for Yr in YR_list:
    print("Yr = ", Yr)
    for L in range(2,7,2):
        print("lamda", L)
        for Hr in HR_list:
            W1_mat = []
            W5_mat = []
            W2_mat = []
            W4_mat = []
            W6_mat = []
            W8_mat = []
            R1_mat = []
            R3_mat = []
            print("hr = ", Hr)
            Hr_1square = np.square(1-Hr) 
            Hr_1 = 1-Hr
            W3 = L*Yr*Hr ##d
            W7 = Hr_1 * L ## d
            print(type(W1_mat))
            for A1 in range(1,91):
                W1_mat.append(0.5*Yr*np.square(L*Hr)/ (np.tan(A1*rad) + 1e-8)) ##d
                R1_mat.append(np.square(Hr)*np.sin((A1+P1)*rad)* 0.5 * np.cos((A1 + Beta + P1)*rad) / (np.square(np.sin(A1*rad)) + 1e-8))
            print("done A1")
            for A3 in range(1,91):
                W5_mat.append(0.5*Yr*np.square(L*Hr) / (np.tan(A3*rad) + 1e-8)) ##d
                R3_mat.append(np.square(Hr)*np.sin((A3+P1)*rad) * 0.5 * np.cos((A3 - Beta + P1)*rad) / (np.square(np.sin(A3*rad)) + 1e-8))
            print("done A3")
            for A2 in range(1,91):
                W2_mat.append(Hr_1*Hr*Yr*np.square(L)/ (np.tan(A2*rad) + 1e-8)) ##d
                W8_mat.append(Hr_1square* 0.5*np.square(L) / (np.tan(A2*rad) + 1e-8)) ##d
            print("done A2")
            for A4 in range(1,91):
                W4_mat.append(Hr_1*Hr*Yr*np.square(L) / (np.tan(A4*rad) + 1e-8)) ##d
                W6_mat.append(Hr_1square * 0.5*np.square(L) / (np.tan(A4*rad) + 1e-8)) ##d
            print("done A4")

            W1_mat = np.array(W1_mat).reshape(-1,1)
            W5_mat = np.array(W5_mat).reshape(-1,1)
            W2_mat = np.array(W2_mat).reshape(-1,1)
            W4_mat = np.array(W4_mat).reshape(-1,1)
            W6_mat = np.array(W6_mat).reshape(-1,1)
            W8_mat = np.array(W8_mat).reshape(-1,1)
            R1_mat = np.array(R1_mat).reshape(-1,1)
            R3_mat = np.array(R3_mat).reshape(-1,1)
            print("done array convsersion ")
            sr_no = sr_no + 1
            m_Alpha1, m_Alpha2, m_Alpha3, m_Alpha4, m_K = 0, 0, 0, 0, 0
            Alpha1, Alpha2, Alpha3, Alpha4, K_max = [], [], [], [], []
            if status == 1:
                print(status)
                #### case 1 
                for A4 in range(1,90):
                    for A3 in range(A4,91):
                        for A2 in range(1,A4+1):
                            for A1 in range(A2,91):
                                WT_1 = W1_mat[A1-1] + W2_mat[A2-1] + W4_mat[A4-1] + W5_mat[A3-1]
                                WT_2 = W6_mat[A4-1] + W8_mat[A2-1] + W7 + W3
                                WT = (WT_1 + WT_2) * np.cos(Beta*rad)
                                ###############
                                R_2_1 = Hr_1square * np.sin((A2 + P2)*rad)*0.5/(np.square(np.sin(A2*rad)) + 1e-8)
                                R_2_2 = Yr*np.sin((A1+P1)*rad)* Hr_1/(np.sin(A1*rad) + 1e-8)
                                R_2_2 = R_2_2*Hr / (np.sin(A2*rad) + 1e-8)
                                R2 = (R_2_1 + R_2_2)*np.cos((A2+Beta+P2)*rad) 
                                ###################################
                                R_4_1 = Hr_1square * np.sin((A4 + P2)*rad)*0.5 / (np.square(np.sin(A4*rad)) + 1e-8)
                                R_4_2 = Yr*np.sin((A3+P1)*rad)*(Hr_1)/(np.sin(A3*rad) + 1e-8)
                                R_4_2 = R_4_2*Hr / (np.sin(A4*rad) + 1e-8)
                                
                                R4 = (R_4_1 + R_4_2)*np.cos((A4-Beta+P2)*rad) #########
                                ###
                                RT = (R1_mat[A1-1] + R3_mat[A3-1])*Yr
                                RT = RT + R4 + R2
                                ###########
                                Pun = WT - (RT*np.square(L))
                                if Pun > m_K and Pun > 0:
                                    m_Alpha1 = A1
                                    m_Alpha2 = A2
                                    m_Alpha3 = A3
                                    m_Alpha4 = A4
                                    m_K = Pun
            if status == 0:
                print(status)
                for A4 in range(1,91):
                    #print("Alpha 4 =", A4)
                    for A3 in range(1,A4):
                        for A2 in range(1,A4):
                            for A1 in range(1,A2):
                                WT_1 = W1_mat[A1-1] + W2_mat[A2-1] + W4_mat[A4-1] + W5_mat[A3-1]
                                WT_2 = W6_mat[A4-1] + W8_mat[A2-1] + W7 + W3
                                WT = (WT_1 + WT_2) * np.cos(Beta*rad)
                                ###############
                                R_2_1 = Hr_1square * np.sin((A2 + P2)*rad)*0.5/(np.square(np.sin(A2*rad)) + 1e-8)
                                R_2_2 = Yr*np.sin((A1+P1)*rad)* Hr_1/(np.sin(A1*rad) + 1e-8)
                                R_2_2 = R_2_2*Hr / (np.sin(A2*rad) + 1e-8)
                                R2 = (R_2_1 + R_2_2)*np.cos((A2+Beta+P2)*rad) 
                                ###################################
                                R_4_1 = Hr_1square * np.sin((A4 + P2)*rad)*0.5 / (np.square(np.sin(A4*rad)) + 1e-8)
                                R_4_2 = Yr*np.sin((A3+P1)*rad)*(Hr_1)/(np.sin(A3*rad) + 1e-8)
                                R_4_2 = R_4_2*Hr / (np.sin(A4*rad) + 1e-8)
                                
                                R4 = (R_4_1 + R_4_2)*np.cos((A4-Beta+P2)*rad) #########
                                ###
                                RT = (R1_mat[A1-1] + R3_mat[A3-1])*Yr
                                RT = RT + R4 + R2
                                ###########
                                Pun = WT - (RT*np.square(L))

                                if Pun > m_K and Pun > 0:
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
            sheet1.write(sr_no,6,int(m_Alpha3))
            sheet1.write(sr_no,7,int(m_Alpha4))
            sheet1.write(sr_no,8,float(m_K))
            sheet1.write(sr_no,9, 'P1 = 30, P2 = 40')
            print("loop",sr_no,"completed")
            print(sr_no, Yr, L, Hr, int(m_Alpha1), int(m_Alpha2), int(m_Alpha3), int(m_Alpha4), m_K)


wb.save('double_layer_beta0.xls')
#plt.legend()
print("done")

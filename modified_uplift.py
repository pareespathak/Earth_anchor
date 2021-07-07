# importing necessary lib
import numpy as np
import matplotlib.pyplot as plt
import xlwt
from xlwt import Workbook
import datetime

# Workbook is created
wb = Workbook()
# add_sheet is used to create sheet.
sheet1 = wb.add_sheet("sheet 1", cell_overwrite_ok=True)
sheet1.write(0, 0,'sr_no')
sheet1.write(0, 1, 'Psi')
sheet1.write(0, 2, 'Lamda')
sheet1.write(0, 3, 'Beta')
sheet1.write(0, 4, 'Alpha_1')
sheet1.write(0, 5, 'Alpha_3')
sheet1.write(0, 6, 'K')

#variables
# A1, A3 = angle of failure plane
#Psi = soil friction angle
#Y = soil unit weight
#B = width of strip anchor
#L = lamba (H/B)
#P = angle of uplift with verticle
#pun = uplift
#case 1
#taking A1 = A3
rad = np.pi / 180
sr_no = 0
max_pun, max_A1, max_A3, max_P = 0, 0, 0, 0
for Psi in range(20,50,10):
    for L in range(1,8,2):
        for P in range(0,45,5):
            sr_no = sr_no + 1
            max_pun, max_A1, max_A3 = 0, 0, 0
            for A3 in range(2,81):
                for A1 in range(1,A3):
                     W = ((1/(np.tan(A1*rad)+ 1e-8)) + (1/(np.tan(A3*rad)+ 1e-8))) + (2 /L)
                     W = W * np.cos(P*rad)
                     # soil reaction
                     R1 = np.sin((A1+Psi)*rad) * np.cos((A1+Psi+P)*rad) / (np.square(np.sin(A1*rad)) + 1e-8)
                     R2 = np.sin((A3+Psi)*rad) * np.cos((A3+Psi-P)*rad) / (np.square(np.sin(A3*rad)) + 1e-8)
                     R = R1 + R2
                     Pun = (W - R) * 0.5
                     if Pun > max_pun:
                         max_pun = Pun
                         max_A1 = A1
                         max_A3 = A3

            sheet1.write(sr_no,0,sr_no)
            sheet1.write(sr_no,1,Psi)
            sheet1.write(sr_no,2,L)
            sheet1.write(sr_no,3,P)
            sheet1.write(sr_no,4,max_A1)
            sheet1.write(sr_no,5,max_A3)
            sheet1.write(sr_no,6,max_pun)


wb.save('presentation_till_80.xls')
#plt.legend()
print("done")

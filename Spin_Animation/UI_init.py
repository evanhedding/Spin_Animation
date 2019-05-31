#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import attitude
import math
import numpy as np
import sys
from PyQt5 import QtWidgets
import Attitude_ui 
import visual_T_handle


#######Constants###
Q0 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
steps = 5000
time = 60
animation_length = 1000
        
class MyDialog(QtWidgets.QDialog):
    def __init__(self):
        super(MyDialog, self).__init__()
        self.ui = Attitude_ui.Ui_Attitude()
        self.ui.setupUi(self)
        self.ui.calculate.clicked.connect(self.calc)
        self.ui.clear.clicked.connect(self.clearplots)
        self.ui.simulate.clicked.connect(self.sim)
        
    def sim(self):
        if attitude.ode.Q4.size > 20:
            visual_T_handle.simulate(animation_length)
        else:
            print("Need to Calculate first")
            
    def clearplots(self):
        self.ui.graphicsView_x.clear()
        self.ui.graphicsView_y.clear()
        self.ui.graphicsView_z.clear()
        attitude.ode.Q4 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        
    def calcJmax(J):
        Jxx = J[0,0]
        Jyy = J[1,1]
        Jzz = J[2,2]
        Jmax = 0
        if Jxx > Jyy and Jxx > Jzz:
            Jmax = Jxx
        elif Jyy > Jxx and Jyy > Jzz:
            Jmax = Jyy
        elif Jzz > Jyy and Jzz > Jxx:
            Jmax = Jzz
        return Jmax
            
    def calc(self):
        Wx = self.ui.Wx.value()
        if Wx == 0: Wx = 0.001
        Wy = self.ui.Wy.value()
        if Wy == 0: Wy = 0.001
        Wz = self.ui.Wz.value()
        if Wz == 0: Wz = 0.001
        Jxx = self.ui.Jxx.value()
        if Jxx == 0: Jxx = 0.001
        Jyy = self.ui.Jyy.value()
        if Jyy == 0: Jyy = 0.001
        Jzz = self.ui.Jzz.value()
        if Jzz == 0: Jzz = 0.001
        W0 = np.array([Wx, Wy, Wz])
        J = np.array([[Jxx, 0, 0], [0, Jyy, 0], [0, 0, Jzz]])
        
        # hr is zero for no superspin stabilization   
        hr = 0
        
        ## For spin stabilization about the x-axis...
        ## And assuming Wy and Wz are zero...
        #Jmax = MyDialog.calcJmax(J)
        #hr = (1.2*Jmax - J[0,0])*Wx
        
        sol = attitude.ode.calc(Q0,W0,J,hr,steps,time)
        self.ui.graphicsView_x.plot(sol[0])   
        self.ui.graphicsView_y.plot(sol[1])   
        self.ui.graphicsView_z.plot(sol[2])   
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


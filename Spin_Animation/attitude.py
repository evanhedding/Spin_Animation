#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 16:53:26 2019

@author: evan
"""

import numpy as np
from scipy.integrate import odeint

class ode():
    Q4 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    
    def att_ode(init, t, hr, J):
        P = np.split(init, [9])
        w = P[1]
        Q = np.reshape(P[0], [3, 3])
        Jxx = J[0,0]
        Jyy = J[1,1]
        Jzz = J[2,2]
        wcross = np.array([[0, -w[2],  w[1]], [w[2], 0, -w[0]], [-w[1], w[0], 0]])
        Qdot = np.dot(Q, wcross)
        wx = -(Jzz-Jyy)*w[1]*w[2]/Jxx
        wy = -((Jxx-Jzz)*w[0]+hr)*w[2]/Jyy
        wz = -((Jyy-Jxx)*w[0]-hr)*w[1]/Jzz
        wdot = np.array([wx, wy, wz])
        xdot = np.append(np.reshape(Qdot, 9), wdot)
        return xdot
    
    def calc(Q0, W0, J, hr, steps, time):
        a = np.reshape(Q0, 9)
        x = np.append(a, W0)
        t = np.linspace(0,time,steps)
        sol = odeint(ode.att_ode, x, t, args=(hr,J))
        Wx = W0[0]
        Wy = W0[1]
        Wz = W0[2]
        i = 0
        while i < (steps-1):
            speed = sol[np.array([i]), np.array([9,10,11])]
            x = sol[np.array([i]), np.array([0,1,2,3,4,5,6,7,8])]
            Qnew = np.split(x,3)
            x1 = np.append(Qnew[0], np.array([0]))
            x2 = np.append(Qnew[1], np.array([0]))
            x3 = np.append(Qnew[2], np.array([0]))
            Qnewnew = [x1, x2, x3, np.array([0, 0, 0, 1])]
            ode.Q4 = np.append(ode.Q4, Qnewnew)
            Wx = np.append(Wx, speed[0])
            Wy = np.append(Wy, speed[1]) 
            Wz = np.append(Wz, speed[2])
            i += 1
        return np.array([Wx,Wy,Wz])


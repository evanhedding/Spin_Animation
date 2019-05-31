#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 10:40:57 2019

@author: evan
"""

import numpy as np
import open3d as o3d
import math as m
import time
import rotation as r
import attitude


def simulate(animation_length):  
    #Retrieves transformation matrices from ode solution
    Q4 = attitude.ode.Q4
    number_of_arrays = Q4.size/16
    Q = np.hsplit(Q4,number_of_arrays)
    
    #Creates the T_handle
    c1 = o3d.geometry.create_mesh_cylinder(radius=0.2, height=2.0)
    c1.compute_vertex_normals()
    c1.paint_uniform_color([0.7, 0.7, 0.3])
    c2 = o3d.geometry.create_mesh_cylinder(radius=0.15, height=1.0)
    c2.compute_vertex_normals()
    c2.paint_uniform_color([0.3, 0.3, 0.3])
    c2.transform(r.roty(m.pi/2))
    c2.transform(r.translate(-0.5, 0, 0))
    
    #Main animation loop code
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.register_key_callback(ord("Q"), vis.destroy_window())
    vis.create_window(width=600, height=400)
    vis.add_geometry(c1)
    vis.add_geometry(c2)
    for i in range(animation_length):
        trans = Q[i].reshape(4,4)
        inv = np.linalg.inv(trans)
        c2.transform(trans)
        c1.transform(trans)
        vis.update_geometry()
        vis.poll_events()
        vis.update_renderer()
        time.sleep(0.0005)
        c2.transform(inv)
        c1.transform(inv)
    vis.destroy_window()
    
   
    

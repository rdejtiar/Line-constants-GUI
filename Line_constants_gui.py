# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 18:41:55 2024

@author: Ricardo

This is a Graphical interfase to the Line Constanst calculation developed by
 2017 Julius Susanto
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
"""

import line_constants as lc
import PySimpleGUIQt as psg
import numpy as np
line_dict = {
    'mode' : 'carson',
    'f' :           50,                         # Nominal frequency (Hz)
    'rho' :         1000,                        # Earth resistivity (Ohm.m)
    'phase_h' :     [12, 14, 16],               # Phase conductor heights (m)
    'phase_x' :     [-1.8, 1.8, -1.8],                  # Phase conductor x-axis coordinates (m)
    'phase_cond' :  ['solid','solid','solid'],     # Phase conductor types ('tube' or 'solid')
    'phase_R' :     [0.1199, 0.1199, 0.1199],   # Phase conductor AC resistances (Ohm/km)
    'phase_r' :     [10.895, 10.895, 10.895],   # Phase conductor radi (mm)
    'phase_q' :     [0, 0, 0],                  # Phase conductor inner tube radii (mm)
    'earth_h' :     [30],                       # Earth conductor heights (m)
    'earth_x' :     [0],                        # Earth conductor x-axis coordinates (m)
    'earth_cond' :  ['solid'],                  # Earth conductor types ('tube' or 'solid')
    'earth_R' :     [0.5],                   # Earth conductor AC resistances (Ohm/km)
    'earth_r' :     [5],                   # Earth conductor radi (mm)
    'earth_q' :     [0]                         # Earth conductor inner tube radii (mm)
}

line_dict2 = {
    'mode' : 'carson',
    'f' :     'Nominal frequency (Hz)',
    'rho' :   'Earth resistivity (Ohm.m)',
    'phase_h' : 'Phase conductor heights (m)',
    'phase_x' :  'Phase conductor x-axis coordinates (m)',
    'phase_cond' : 'Phase conductor types (tube or solid)',
    'phase_R' :  'Phase conductor AC resistances (Ohm/km)',
    'phase_r' :   'Phase conductor radi (mm)',
    'phase_q' :   'Phase conductor inner tube radii (mm)',
    'earth_h' :    'Earth conductor heights (m)',
    'earth_x' :    'Earth conductor x-axis coordinates (m)',
    'earth_cond' : 'Earth conductor types (tube or solid)',
    'earth_R' :     'Earth conductor AC resistances (Ohm/km)',
    'earth_r' :     'Earth conductor radi (mm)',
    'earth_q' :    'Earth conductor inner tube radii (mm)',
}







coluna1= psg.Column([[psg.T(x,size=(8,0.8)),psg.In(line_dict[x],size=(20,0.8),key=x),psg.T(line_dict2[x],size=(28,0.8))]
         for x in line_dict])
coluna2=psg.Column([[psg.Multiline(key='ML2',size=(40,20))]])
layout= [[coluna1,coluna2],[psg.Button('Calculate')]]

window = psg.Window("Line Constants", layout)
psg.cprint_set_output_destination(window, 'ML2')

counter =0 

while True:
   event, values = window.read()
   #print( values)
   
   if event == psg.WIN_CLOSED:
      break
   if event == 'Calculate':
       
      
      values_1=values 
      del values_1['ML2']
      for x in values_1 :
          if x != 'mode' :
             values_1[x]= eval(values_1[x])
      #print ('values \n',values_1)
      
      line_dict= values_1
       
       
       
      Zp, n_p, n_e =lc.calc_Z_matrix(line_dict)
      Z = lc.calc_kron_Z(Zp,n_e)
      counter +=1
      psg.cprint('\nCalculation n° ',str(counter),'\n')
      psg.cprint('Impedance Matrix\n',np.round(Z,4))
      U =Z[0,0]-Z[0,1]
    
      psg.cprint('\n Equilibrated System \n Z=', np.round(U,4))
      # Admittance matrix
      Yp, n_p, n_e = lc.calc_Y_matrix(line_dict)
      Y = lc.calc_kron_Z(Yp,n_e)

      psg.cprint('\nAdmitance matrix\n',Y)
window.close()
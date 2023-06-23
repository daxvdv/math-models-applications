import numpy as np
import math
import numpy as np
from numpy.linalg import eig
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from sensitivity import SensitivityAnalyzer

#Ported from original Colab notebook. Various functions to run sensitivity analysis evaluating the sensitivity of can toad growth rates to lifecycle factors.

def growth_rate_model(toadFecundity, eggToTadRate, tadToJuvRate, juvToAdultRate, adultToAdultRate):
  toads_lefkovitch = np.array([[0, 0, 0, toadFecundity], [eggToTadRate, 0, 0, 0], [0, tadToJuvRate, 0, 0], [0, 0, juvToAdultRate, adultToAdultRate]])
  eVal,evec = eig(toads_lefkovitch)

  eVal = np.real(eVal)

  return max(eVal.min(), eVal.max(), key=abs)

def testerValGenerator(central_val, percent_change, stepsize):
  testerVals = []
  steps = int(2*(percent_change/stepsize))
  for i in range(steps):
    newPercent = -1*(percent_change/100) + (i*stepsize/100)
    newVal = central_val + (central_val*newPercent)
    testerVals.append(newVal)
  return testerVals

def runSensitivityAnalysis():

  sensitivity_dict = {
    'toadFecundity': testerValGenerator(7500,30,5),
    'eggToTadRate': testerValGenerator(0.718,30,5),
    'tadToJuvRate': testerValGenerator(0.05, 30, 5),
    'juvToAdultRate': testerValGenerator(0.05, 30, 5),
    'adultToAdultRate': testerValGenerator(0.5, 30, 5)
  }
  
  sa = SensitivityAnalyzer(sensitivity_dict, growth_rate_model, grid_size=5)
  plot = sa.plot()
  styled_dict = sa.styled_dfs()

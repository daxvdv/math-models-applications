import math
import matplotlib.pyplot as plt
import numpy as np

#hostas index 0
#ferns index 1
#sedums index 2
#cone_flowers index 3

def plantGrowth(plotArea, starterFlowers, rainyGrowRates, dryGrowRates, numTrees, initTreeRadius, yearsOfSim):
  plantsInGarden = starterFlowers
  currentRates = list()
  yearsPassed = list()
  hostasPerYear = list()
  fernsPerYear = list()
  sedumsPerYear = list()
  coneflowersPerYear = list()
  treeRadius = 0
  treeCover = 0

  for day in range (0,365*yearsOfSim):
    treeRadius = getTreeRadius(numTrees, treeRadius, 0.8, day, 5, 15)
    treeCover = math.pi * (treeRadius**2) * numTrees
    sunnyAreaPercent = (plotArea - treeCover)/plotArea
    if (day < 181) or (day % 365 == 1):
      currentRates = rainyGrowRates
      if sunnyAreaPercent < 0.7:
        currentRates[3] = currentRates[3] - 0.1
      if sunnyAreaPercent < 0.5:
        currentRates[2] = currentRates[2] - 0.05
        currentRates[3] = currentRates[3] - 0.1
    elif day % 365 == 181:
      currentRates = dryGrowRates
      if sunnyAreaPercent < 0.7:
        currentRates[3] = currentRates[3] - 0.1  
      if sunnyAreaPercent < 0.5:
        currentRates[2] = currentRates[2] - 0.05
        currentRates[3] = currentRates[3] - 0.1

    totalPlantPop = sum(plantsInGarden)

    for index, value in enumerate(plantsInGarden):
      plantsInGarden[index] = value + incrementPlant(totalPlantPop, currentRates, plantsInGarden, plotArea-numTrees, index)
      

    if day % 365 == 0:
      yearsPassed.append(day/365)
      hostasPerYear.append(plantsInGarden[0])
      fernsPerYear.append(plantsInGarden[1])
      sedumsPerYear.append(plantsInGarden[2])
      coneflowersPerYear.append(plantsInGarden[3])

  return [plantsInGarden, yearsPassed, hostasPerYear, fernsPerYear, sedumsPerYear, coneflowersPerYear]



def getTreeRadius(numTrees, initTreeRadius, growthRate, day, growthStartYear, growthEndYear):
  treeRadius = initTreeRadius
  if day == 365*growthStartYear:
    treeRadius = growthRate
  
  if (day > 365*growthStartYear) and (day < 365*growthEndYear) and (day % 365 == 0):
    treeRadius = treeRadius + growthRate

  return treeRadius


def incrementPlant(totalPlantPop, currentRates, plantPopulations, carryCap, plantIndex):
  additionalPlants = currentRates[plantIndex]*(1-(totalPlantPop/carryCap))*plantPopulations[plantIndex]

  return additionalPlants

starterFlowers = [19, 7, 14, 12]
rainyGrowRates = [-0.01, 0.02, -0.01, 0.02]
dryGrowRates = [0.02, -0.01, 0.03, -0.01]

myGardenInfo = plantGrowth(1600, starterFlowers, rainyGrowRates, dryGrowRates, 12, 0, 20)

print(myGardenInfo[0])

plt.plot(myGardenInfo[1], myGardenInfo[2], label = "Hostas")
plt.plot(myGardenInfo[1], myGardenInfo[3], label = "Ferns")
plt.plot(myGardenInfo[1], myGardenInfo[4], label = "Sedums")
plt.plot(myGardenInfo[1], myGardenInfo[5], label = "Coneflowers")
plt.legend()
plt.show()

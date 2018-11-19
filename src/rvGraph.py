# Program to read in csv file with radial velocity data from 'RVs.csv' file
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import math


# define orbital function
# V(t) = K sin(2pi (t - t0)/P)
# where K is the amplitude of the sine wave (which is related to the planet mass),
# P is the orbital period of the planet (which should be the same as the period of the sine wave),
# and t0 is a time that sets the phase of the sine wave.
def Vorbit(K, time, time0, P):
    return K * math.sin(2 * math.pi * (time - time0) / P)


def orbitArray(Jmin, Jmax, vMax, K, P, nObservations):
    time0 = Jmin
    JDays = int((Jmax - Jmin))
    JD_resolution = JDays/int(nObservations)
    print(time0, JDays, JD_resolution)
    K = 40.
    P = 1.5
    xJD[0] = Jmin
    for i in range(1, JDays):
        xJD[i] = xJD[i-1] + JD_resolution
        time = xJD[i]
        yVel[i] = Vorbit(K, time, JD_resolution, P)
    return xJD, yVel


# Open file and load into data array
with open('RVs.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

# Creat pandas data frame
df = pd.DataFrame(data, columns=["Name", "JD", "RVel", "e_RVel", "SNR", "Dewar"])

# extract data into arrays
starName = df["Name"].values.astype(str)
starJD = df["JD"].values.astype(float)
starRVel = df["RVel"].values.astype(float)
starERVel = pd.to_numeric(df["e_RVel"])
starSNR = pd.to_numeric(df["SNR"])
starDewar = pd.to_numeric(df["Dewar"])

sLength = len(starName)
sName = starName[0]
nFigure = 1
index = 0
# Extract star data for plotting into numpty arrays
sX = np.empty(sLength, dtype=float)
sY = np.empty(sLength, dtype=float)
xJD = np.empty(sLength, dtype=float)
yVel = np.empty(sLength,dtype=float)
orbitX = np.empty(sLength, dtype=float)
orbitY = np.empty(sLength, dtype=float)

index_start = 0
index_stop = 0
for i in range(0, sLength):

    if (sName == '10700') or (sName == '185144') or (sName == 'GL908'):

        if sName == starName[i]:
            index_stop = index_stop + 1
        else:
            # print(["Star: ", starName[i]])
            # print(["Index: ", index_start, index_stop])

            # fill array for plotting
            sX = 0
            sY = 0
            sX = starJD[index_start:index_stop]
            sY = starRVel[index_start:index_stop]
            # print(["Start values: ", sX[0], sY[0]])
            # print(["Array Size: ", len(sX), len(sY)])
            pMin = min(sX)
            pMax = max(sX)
            pltMax = max(sY)
            pltMin = min(sY)
            # print(["pMin: ", pMin, "pMax: ", pMax,"pltMax: ", pltMax, "pltMin", pltMin ])
            # Set min JD to 2000 and add/subtract 10% for plot size
            pMin = pMin - pMin * .05
            pMax = pMax + pMax * .05
            pltMin = pltMin - pltMin * .1
            pltMax = pltMax + pltMax * .1
            nObs = int(pMax - pMin)
            nObservations = str(index_stop - index_start)
         # Plot star and save image
            plt.figure(nFigure)
            plt.scatter(sX, sY, marker='.')
            # if this is star of interest then plot orbital velocity function
            if (sName == '10700') or (sName == '185144') or (sName == 'GL908'):
                K = 1.0
                Jmin = pMin
                Jmax = pMax
                vMax = pltMax
                P = 0.1
                orbitX = 0
                orbitY = 0
                print(K, len(sX), len(sY), Jmin, Jmax, vMax)

                a, b = orbitArray(Jmin, Jmax, vMax, K, P, nObservations)
                orbitX = a[0:nObs]
                orbitY = b[0:nObs]
                print(orbitX, orbitY)
                plt.plot(orbitX, orbitY, marker='+', c="red")

            plt.axis([pMin, pMax, pltMin, pltMax])

            plt.title("Star: " + sName + " #Observations: " + nObservations)
            plt.xlabel('Julien Date')
            plt.ylabel('Radial Velocity')
            plt.grid()
            # plt.show(nFigure)
            filename = 'Images/Star_' + sName + '.png'
            plt.savefig(filename)
            print("Star: " + starName[i] + " nObservations: " + nObservations)


            # itterate figure and update star name
            nFigure = nFigure + 1
            index_start = index_stop

    sName = starName[i]

# Finished program
#sys.exit()

import numpy as np
#import matplotlib.pyplot as plt
import scipy.linalg as la
import math
import json
import scipy.signal
import sys


def frf(x, f, dt, nseg):
    # Compute the power density spectrums and the cross spectral density
    SXX = scipy.signal.welch(x, 1/dt,nperseg=nseg,noverlap=0)
    #SFF = scipy.signal.welch(f, 1/dt)
    SXF = scipy.signal.csd(x, f, 1/dt,nperseg=nseg,noverlap=0)

    # Extract the frequencies
    freq = SXX[0]

    # Compute the FRF
    FRF = SXX[1]/SXF[1]

    # Extract the magnitude and angle of the FRF
    mag = np.absolute(FRF)
    ang = np.angle(FRF) * 180 / np.pi

    # Extract the real and imaginary part of the FRF
    real = np.real(FRF)
    imag = np.imag(FRF)

    # Compute the coherence
    __, coh = scipy.signal.coherence(x, f, 1/dt,nperseg=nseg,noverlap=0)
    
    return freq, mag, ang, coh, real, imag
# First argument: sampling frequency [Hz]; Second argument: segment width [-]
sampling_frequency=int(sys.argv[1])
segment_width=int(sys.argv[2])
dt=1/sampling_frequency

###Reading force data
#On BBB
forceFilepath = '/home/debian/frfRawData/force.txt'
#forceFilepath='/var/lib/node-red/frfRawData/force.txt'
#forceFilepath='F:\\Clouddienste\\OneDrive - bwedu\\Uni\\Georgia Tech\\GRA\\SoftwareDevelopmentFabian\\Ford FRF\\Messungen\\force.txt'
forceSignal = []
with open(forceFilepath) as f:
    data = json.load(f)
forceSignal = (data['values'])
forceSignal = [float(i) for i in forceSignal]
time=[]
for i in range(0, len(forceSignal), 1):
    time.append(i*dt)
###Reading displacement data
#On BBB
displacementFilepath = '/home/debian/frfRawData/position.txt'
#displacementFilepath='/var/lib/node-red/frfRawData/displacement.txt'
#displacementFilepath='F:\\Clouddienste\\OneDrive - bwedu\\Uni\\Georgia Tech\\GRA\\SoftwareDevelopmentFabian\\Ford FRF\\Messungen\\position.txt'
displacementSignal = []
with open(displacementFilepath) as f:
    data = json.load(f)
displacementSignal = (data['values'])
displacementSignal = [float(i) for i in displacementSignal]
#Find the impact
max_index=forceSignal.index(max(forceSignal))
start_index=round(max_index-0.001/dt)
end_index=round(max_index+0.2/dt)
if end_index>=len(forceSignal):
    end_index=len(forceSignal)-1
if start_index<0:
    start_index=0
print('start: '+ str(start_index))
print('end: '+ str(end_index))
# Computing FRF
freq, mag, ang, coh, real, imag = frf(displacementSignal[start_index:end_index], forceSignal[start_index:end_index], dt,segment_width)

# Converte output to list for creating json file
freq = list(freq)
mag = list(mag)
ang = list(ang)
coh = list(coh)
real = list(real)
imag = list(imag)


# Define output file 
jsonFile = {
    "frequency": freq,
    "magnitude": mag,
    "angle": ang,
    "coh": coh,
    "real": real,
    "imag": imag
}

#Test on laptop
#saveDataFilepath = 'F:\\Clouddienste\\OneDrive - bwedu\\Uni\\Georgia Tech\\GRA\\SoftwareDevelopmentFabian\\Ford FRF\\Messungen\\frf.txt'


#On BBB
saveDataFilepath = '/home/debian/frfRawData/frf.txt'
f = open(saveDataFilepath, "w")
f.write(str(jsonFile))
f.close()
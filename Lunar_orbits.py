import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# Satellite parameters from the table
satellites = {
    'ELFO11': (6540*10**3, 0.6, 63, 0, 90, 0),
    'ELFO12': (6540*10**3, 0.6, 63, 0, 90, 180),
    'ELFO13': (6540*10**3, 0.6, 63, 0, 90, 90),
    'ELFO14': (6540*10**3, 0.6, 63, 0, 90, 270),
    'ELFO21': (6540*10**3, 0.6, 49.4, 180, 90, 0),
    'ELFO22': (6540*10**3, 0.6, 49.4, 180, 90, 180),
    'ELFO23': (6540*10**3, 0.6, 49.4, 180, 90, 90),
    'ELFO24': (6540*10**3, 0.6, 49.4, 180, 90, 270)
}

# # Classical Orbital Elements (COE)
a = 6541.4 *10**3   # [m] Semi-major axis
e = 0.6000  # [--] Eccentricity
i = 56.2   # [deg] Inclination
O = 0.00  # [deg] Right ascension of the ascending node
w = 90.0   # [deg] Argument of perigee
M = 0.00   # [deg] Mean anomaly

# Classical Orbital Elements (radians)
i_rad = np.radians(i)
O_rad = np.radians(O)
w_rad = np.radians(w)
M_rad = np.radians(M)

G = 6.67e-11

# Moon Data
m_moon = 7.34767309 * 10 **22 #kg
R_moon = 1737.4 # km

def orbital_period (a, m):
    
    
    T = 2*np.pi * (np.sqrt(a**3/(G*m)))
    
    return T

sat_period = []

for sat_name, elements in satellites.items():
    
    T = orbital_period(elements[0], m_moon)  # [s] Satellite period
    sat_period.append(T)
    
    
sat_period = np.array(sat_period)
    
print(f"Satellite period {sat_period/3600} h")
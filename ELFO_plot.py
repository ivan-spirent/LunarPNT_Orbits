import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def kep2cart(a, e, i, raan, ap, ma):
    """
    Convert Keplerian elements to Cartesian coordinates using Ely's 2005 reference frame
    
    Parameters:
    a (float): Semi-major axis [km]
    e (float): Eccentricity
    i (float): Inclination [deg]
    raan (float): Right Ascension of Ascending Node [deg]
    ap (float): Argument of Periapsis [deg]
    ma (float): Mean Anomaly [deg]
    
    Returns:
    tuple: (x, y, z) coordinates in km
    """
    # Convert angles to radians
    i_rad = np.radians(i)
    raan_rad = np.radians(raan)
    ap_rad = np.radians(ap)
    ma_rad = np.radians(ma)
    
    # Solve Kepler's equation (simplified)
    ea = ma_rad  # Using mean anomaly as initial guess
    for _ in range(10):  
        ea = ma_rad + e * np.sin(ea)
    
    # Calculate position in orbital plane
    r = a * (1 - e * np.cos(ea)) # Radiovector to any point of the orbit
    x_orb = r * np.cos(ea)
    y_orb = r * np.sin(ea)
  
    
    # Rotation matrices
    rot_ap = R.from_euler('z', ap_rad)
    rot_i = R.from_euler('x', i_rad)
    rot_raan = R.from_euler('z', raan_rad)
    
    # Apply rotations
    pos_orb = np.array([x_orb, y_orb, 0])
    pos = rot_raan.apply(rot_i.apply(rot_ap.apply(pos_orb)))
    
    return pos

# Satellite parameters from the table
satellites = {
    'ELFO11': (6540, 0.6, 63, 0, 90, 0),
    'ELFO12': (6540, 0.6, 63, 0, 90, 180),
    'ELFO13': (6540, 0.6, 63, 0, 90, 90),
    'ELFO14': (6540, 0.6, 63, 0, 90, 270),
    'ELFO21': (6540, 0.6, 49.4, 180, 90, 0),
    'ELFO22': (6540, 0.6, 49.4, 180, 90, 180),
    'ELFO23': (6540, 0.6, 49.4, 180, 90, 90),
    'ELFO24': (6540, 0.6, 49.4, 180, 90, 270)
}

# Create 3D plot
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')

# Plot Moon (simplified as sphere)
r_moon = 1737.4  # Moon radius in km
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = r_moon * np.outer(np.cos(u), np.sin(v))
y = r_moon * np.outer(np.sin(u), np.sin(v))
z = r_moon * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, color='gray', alpha=0.6)

# Plot orbits
for sat_name, elements in satellites.items():
    orbit_points = []
    for ma in np.linspace(0, 360, 100):
        elements_ma = elements[:-1] + (ma,)
        pos = kep2cart(*elements_ma)
        orbit_points.append(pos)
    
    orbit_points = np.array(orbit_points)
    ax.plot(orbit_points[:, 0], orbit_points[:, 1], orbit_points[:, 2], 
            label=sat_name)

# Set plot parameters
ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.set_zlabel('Z (km)')
ax.set_title('Lunar Frozen Orbits')
ax.legend()

# Set equal aspect ratio
ax.set_box_aspect([1,1,1])

plt.show()

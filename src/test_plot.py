import matplotlib.pyplot as plt

# Data: Shoulder x,y coordinates during a lunge
data = [
    {"frame": 0, "x": 0.00, "y": 1.50},
    {"frame": 1, "x": 0.02, "y": 1.49},
    {"frame": 2, "x": 0.05, "y": 1.48},
    {"frame": 3, "x": 0.09, "y": 1.46},
    {"frame": 4, "x": 0.14, "y": 1.44},
    {"frame": 5, "x": 0.20, "y": 1.42},
    {"frame": 6, "x": 0.27, "y": 1.40},
    {"frame": 7, "x": 0.35, "y": 1.38},
    {"frame": 8, "x": 0.44, "y": 1.37},
    {"frame": 9, "x": 0.54, "y": 1.36},
    {"frame": 10, "x": 0.65, "y": 1.36},
    {"frame": 11, "x": 0.77, "y": 1.37},
    {"frame": 12, "x": 0.90, "y": 1.38},
    {"frame": 13, "x": 1.04, "y": 1.40},
    {"frame": 14, "x": 1.19, "y": 1.42},
    {"frame": 15, "x": 1.35, "y": 1.44},
    {"frame": 16, "x": 1.52, "y": 1.47},
    {"frame": 17, "x": 1.70, "y": 1.49},
    {"frame": 18, "x": 1.89, "y": 1.50},
    {"frame": 19, "x": 2.09, "y": 1.51},
    {"frame": 20, "x": 2.30, "y": 1.51},
    {"frame": 21, "x": 2.51, "y": 1.51},
    {"frame": 22, "x": 2.72, "y": 1.51},
    {"frame": 23, "x": 2.93, "y": 1.51},
    {"frame": 24, "x": 3.14, "y": 1.51},
    {"frame": 25, "x": 3.34, "y": 1.51},
    {"frame": 26, "x": 3.53, "y": 1.50},
    {"frame": 27, "x": 3.71, "y": 1.49},
    {"frame": 28, "x": 3.88, "y": 1.48},
    {"frame": 29, "x": 4.03, "y": 1.48},
    {"frame": 30, "x": 4.17, "y": 1.48},
    {"frame": 31, "x": 4.30, "y": 1.48},
    {"frame": 32, "x": 4.42, "y": 1.49},
    {"frame": 33, "x": 4.53, "y": 1.50},
    {"frame": 34, "x": 4.62, "y": 1.50},
    {"frame": 35, "x": 4.70, "y": 1.50}
]

rock_back = [
    {"frame": 0, "x": 0.00, "y": 1.50},
    {"frame": 1, "x": 0.02, "y": 1.49},
    {"frame": 2, "x": 0.05, "y": 1.48},
    {"frame": 3, "x": 0.09, "y": 1.46},
    {"frame": 4, "x": 0.14, "y": 1.44},
    {"frame": 5, "x": 0.20, "y": 1.42},
    {"frame": 6, "x": 0.27, "y": 1.40},
    {"frame": 7, "x": 0.35, "y": 1.38},
    {"frame": 8, "x": 0.44, "y": 1.37},
    {"frame": 9, "x": 0.54, "y": 1.36},
    {"frame": 10, "x": 0.65, "y": 1.36},
    {"frame": 11, "x": 0.77, "y": 1.37},
    {"frame": 12, "x": 0.90, "y": 1.38},
    {"frame": 13, "x": 1.04, "y": 1.40},
    {"frame": 14, "x": 1.19, "y": 1.42},
    {"frame": 15, "x": 1.35, "y": 1.44},
    {"frame": 16, "x": 1.52, "y": 1.47},
    {"frame": 17, "x": 1.70, "y": 1.49},

    # ⚠️ Rock-back begins: slight reverse movement
    {"frame": 18, "x": 1.65, "y": 1.50},
    {"frame": 19, "x": 1.60, "y": 1.49},
    {"frame": 20, "x": 1.58, "y": 1.48},
    {"frame": 21, "x": 1.60, "y": 1.47},
    {"frame": 22, "x": 1.65, "y": 1.47},

    # Resume forward lunge, but less momentum
    {"frame": 23, "x": 1.80, "y": 1.48},
    {"frame": 24, "x": 1.95, "y": 1.49},
    {"frame": 25, "x": 2.10, "y": 1.50},
    {"frame": 26, "x": 2.25, "y": 1.50},
    {"frame": 27, "x": 2.39, "y": 1.49},
    {"frame": 28, "x": 2.52, "y": 1.48},
    {"frame": 29, "x": 2.64, "y": 1.48},
    {"frame": 30, "x": 2.75, "y": 1.48},
    {"frame": 31, "x": 2.85, "y": 1.48},
    {"frame": 32, "x": 2.94, "y": 1.49},
    {"frame": 33, "x": 3.02, "y": 1.50},
    {"frame": 34, "x": 3.09, "y": 1.50},
    {"frame": 35, "x": 3.15, "y": 1.50}
]


# Extract x and y coordinates
x_vals = [point["x"] for point in rock_back]
y_vals = [point["y"] for point in rock_back]

# Plotting
plt.figure(figsize=(10, 4))
plt.plot(x_vals, y_vals, color='royalblue', linestyle='-')
plt.title("Shoulder Trajectory During Fencing Lunge (Side View)")
plt.xlabel("Horizontal Position (meters)")
plt.ylabel("Vertical Position (meters)")
plt.grid(True)
plt.axis('equal')  # Maintain aspect ratio
plt.tight_layout()
plt.show()
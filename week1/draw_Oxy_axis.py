import matplotlib.pyplot as plt
import numpy as np

# Load your image
# Replace 'your_image_path.jpg' with the path to your image file
image = plt.imread('D:/Project/frame/frame172.jpg')

# Flip the image vertically
image = np.flipud(image)

# Create figure and axis
fig, ax = plt.subplots()

# Display the image
ax.imshow(image, origin='lower')

# Get image dimensions
height, width, _ = image.shape

# Set aspect ratio
aspect_ratio = width / height

# Set aspect ratio of the plot
ax.set_aspect(aspect_ratio)

# Draw horizontal line (Ox axis)
ax.axhline(0, color='black')

# Draw vertical line (Oy axis)
ax.axvline(0, color='black')

# Set the limits to show lower left quadrant
ax.set_xlim(left=0, right=width)
ax.set_ylim(bottom=0, top=height)

# # Invert y-axis to make (0,0) the lower left corner
# ax.invert_yaxis()

# Show plot
plt.show()

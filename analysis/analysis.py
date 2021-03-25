import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# Read
img = np.asarray(Image.open('../assets/lego_stud_flat.png'))

# Band split
r = img[:, :, 0]
g = img[:, :, 1]
b = img[:, :, 2]

# Plot
fig, axs = plt.subplots(2, 2)

cax_00 = axs[0, 0].imshow(img)
axs[0, 0].xaxis.set_major_formatter(plt.NullFormatter())
axs[0, 0].yaxis.set_major_formatter(plt.NullFormatter())

cax_01 = axs[0, 1].imshow(r, cmap='Reds')
fig.colorbar(cax_01, ax=axs[0, 1])
axs[0, 1].xaxis.set_major_formatter(plt.NullFormatter())
axs[0, 1].yaxis.set_major_formatter(plt.NullFormatter())

cax_10 = axs[1, 0].imshow(g, cmap='Greens')
fig.colorbar(cax_10, ax=axs[1, 0])
axs[1, 0].xaxis.set_major_formatter(plt.NullFormatter())
axs[1, 0].yaxis.set_major_formatter(plt.NullFormatter())

cax_11 = axs[1, 1].imshow(b, cmap='Blues')
fig.colorbar(cax_11, ax=axs[1, 1])
axs[1, 1].xaxis.set_major_formatter(plt.NullFormatter())
axs[1, 1].yaxis.set_major_formatter(plt.NullFormatter())
plt.show()

# Plot histograms
fig, axs = plt.subplots(3, sharex=True, sharey=True)

axs[0].hist(r.ravel(), bins=25)
axs[0].set_title('Red')
axs[1].hist(g.ravel(), bins=25)
axs[1].set_title('Green')
axs[2].hist(b.ravel(), bins=25)
axs[2].set_title('Blue')

plt.show()

import numpy as np

import matplotlib.pyplot as plt

data_3 = np.loadtxt('./cross-P-3.dat')
data_4 = np.loadtxt('./cross-P-4.dat')
data_5 = np.loadtxt('./cross-P-5.dat')
data_6 = np.loadtxt('./cross-P-6.dat')
res_intensity = data_3[:, 1] *0.02+ data_4[:, 1]*0.25 + data_5[:, 1]*0.54 + data_6[:, 1]*0.18

plt.plot(data_3[:, 0], res_intensity)
plt.xlim(8.51122, 13.48502)
plt.show()

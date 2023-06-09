import scipy.io
import numpy as np
import matplotlib.pyplot as plt

# Data
data = scipy.io.loadmat('data.mat')
u_raw = data['u']
y_raw = data['y']
theta_1 = 0.08  # Infusion rate of cortisol from adrenal glands
theta_2 = 0.0075  # Clearance rate of cortisol by liver
y_estimate = []

k = 1
for val in u_raw:
    a_tk = np.exp(-theta_2*k)
    b_tk = np.array(np.zeros(len(u_raw)))  # Initialize with zeros

    temp = k  # Populate b_tk with nonzero values
    index = 0  # Item index within b_tk
    while temp > 0:
        b_tk[index] = (theta_1/(theta_1-theta_2)*(np.exp(-theta_2*temp)-np.exp(-theta_1*temp)))
        temp -= 1  # k-1, k-2... etc.
        index += 1  # Next index in b_tk

    estimate = a_tk * y_raw[0][0] + b_tk @ u_raw  # Equation 4
    y_estimate.append(estimate)
    k += 1

plt.subplot(2, 1, 1)  # Simulated output
markerline, stemlines, baseline = plt.stem(y_raw,
                                           linefmt='b',
                                           markerfmt='b.')
plt.grid()
plt.ylabel('Magnitude')
plt.xlabel('Sample')
plt.title('Y Output')
plt.tight_layout(pad=1.2)

plt.subplot(2,1,2)  # Estimated output
markerline, stemlines, baseline = plt.stem(y_estimate,
                                           linefmt='g',
                                           markerfmt='g.')
plt.grid()
plt.ylabel('Magnitude')
plt.xlabel('Sample')
plt.title('Y Estimate')
plt.tight_layout(pad=1.2)

plt.show()


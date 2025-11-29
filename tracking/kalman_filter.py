# Louis Do
# 1002072156
# Windows 11
# Python 3.11.3
import numpy as np

# Class kalmanfilter will handle the predicting/updating of the object positions over time using the measuremen an the motions data per frame
class kalmanfilter:
    # the initializer will set the matrice and start tracking with the provided position
    def __init__(self, x0, y0):
        self.x = np.array([[x0], [y0], [0], [0]])

        self.f = np.array([[1,0,1,0],[0,1,0,1], [0,0,1,0],[0,0,0,1]])
        self.h = np.array([[1,0,0,0], [0,1,0,0]])
        self.p = np.eye(4) * 1000
        self.q = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0],[0,0,0,1]])
        self.r = np.array([[10,0],[0,10]])

        self.history = []
        self.history.append((x0, y0))

    # the predict function will predict the step's it takes to get to next position
    def predict(self):
        self.x = np.dot(self.f, self.x)
        self.p = np.dot(np.dot(self.f, self.p), self.f.T) + self.q
        return self.x[0,0], self.x[1,0]

    # the update function will use new measurements to provide a currenttime update on estimate
    def update(self, z):
        z = np.array([[z[0]],[z[1]]])
        y = z - np.dot(self.h, self.x)
        s = np.dot(np.dot(self.h, self.p), self.h.T) + self.r
        k = np.dot(np.dot(self.p, self.h.T), np.linalg.inv(s))
        self.x = self.x + np.dot(k, y)
        self.p = np.dot((np.eye(4) - np.dot(k, self.h)), self.p)
        self.history.append((self.x[0,0], self.x[1,0]))
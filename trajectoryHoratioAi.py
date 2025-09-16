import os
import pandas as pd
import numpy as np
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt

def readData() -> tuple[np.ndarray, np.ndarray]:
    print("Reading data...")
    dataset = pd.read_csv("bbox_light.csv")

    BEV_X = []
    BEV_Y = [] 

    v = (dataset["y1"] + dataset["y2"]) / 2
    u = (dataset["x1"] + dataset["x2"]) / 2
    
    # Load the first frame to define the reference point and axes
    firstXYZ = np.load(os.path.join("xyz", "depth000000.npz"))["xyz"]
    firstV, firstU = int(v[0]), int(u[0])
    xAxis = np.array([firstXYZ[firstV, firstU, 0], firstXYZ[firstV, firstU, 1]])
    yAxis = np.array([xAxis[1], -xAxis[0]]) #perpendicular to x axis


    for i in range(len(dataset)):
        file_name = f"depth{i:06d}.npz"  
        path = os.path.join("xyz", file_name)
        xyz = np.load(path)["xyz"]
        U = int(u[i])
        V = int(v[i])
        if not (np.isnan(xyz[V, U]).any() or np.isinf(xyz[V, U]).any()):
            refVector = np.array([xyz[V, U, 0], xyz[V, U, 1]])
            trafficLightRelative = toWorldFrame(refVector, xAxis, yAxis)
            BEV_X.append(trafficLightRelative[0])
            BEV_Y.append(trafficLightRelative[1])

    print("Data read.")
    return np.array(BEV_X), np.array(BEV_Y)


def toWorldFrame(refVector: np.ndarray, xAxis:np.ndarray, yAxis: np.ndarray) -> np.ndarray:
    correctedX = refVector.dot(xAxis) / np.linalg.norm(xAxis)
    correctedY = refVector.dot(yAxis) / np.linalg.norm(yAxis)
    return np.array([correctedX, correctedY])

def createData(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    print("Creating data...")
    rawTrajectory = Polynomial.fit(x, y, 9)
    xSmoothed = np.linspace(min(x), max(x), 150)
    ySmoothed = rawTrajectory(xSmoothed)
    print("Data created.")
    return xSmoothed, ySmoothed
    

def plotData(x: np.ndarray, y: np.ndarray) -> None:
    print("Plotting data...")
    plt.scatter(x, y, color="blue", label = "Ego trajectory")
    plt.xlabel("Forward (X, m)")
    plt.ylabel("Lateral (Y, m)")
    plt.title("Static Example: Ego Only")
    plt.scatter([0], [0], color="red", label="Traffic Light", marker="x")
    plt.scatter([x[0]], [y[0]], color="green", label="End", marker="o")
    plt.scatter([x[len(x) - 1]], [y[len(y) - 1]], color="orange", label="Start", marker="o")
    plt.legend(loc = "upper right")
    plt.savefig("trajectoryHoratioAi.png", dpi= 300)
    plt.show()
    print("Data plotted.")
    

def main() -> None:
    points = readData()
    data = createData(points[0], points[1])
    x, y = data
    plotData(x, y)
    print("Done")

if __name__ == "__main__":
    main()

import numpy as np
import pandas as pd 

def mape(y, yhat):
    y, yhat = np.array(y), np.array(yhat)
    den = np.maximum(1e-8, np.abs(y))
    return 100 * np.mean(np.abs(yhat - y) / den)

def smape(y, yhat):
    y, yhat = np.array(y), np.array(yhat)
    den = np.maximum(1e-8, (np.abs(y) + np.abs(yhat)) / 2)
    return 100 * np.mean(np.abs(yhat - y) / den)

def wape(y, yhat):
    y, yhat = np.array(y)
    return 100 * np.sum(np.abs(yhat - y)) / np.maximum(1e-8, np.sum(np.abs(y)))


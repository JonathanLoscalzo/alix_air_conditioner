import numpy as np
import pandas as pd
from sklearn.metrics import log_loss

def predict_proba_score(estimators, X, y, score, proba=1):
    """ from a set of models, return mean and std probabilities """
    sc = np.array([ score(y, est.predict_proba(X)[:,proba]) for est in estimators ])
    return sc.mean(), sc.std()

def predict_proba_(estimators, X):
    """ from a set of models, return mean predict_proba result """
    sc = np.array([ est.predict_proba(X)[:,1] for est in estimators ])
    return sc.mean(axis=0)

def plot_feature_importance(fi, cols):
    fi = fi if isinstance(fi, pd.Series) else pd.Series(fi)
    fi.index = cols
    fi.sort_values(ascending=True).tail(35).plot.barh(figsize=(10,10))

def metrics(model, X, y):
    return log_loss(y, model.predict_proba(X))
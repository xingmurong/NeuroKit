# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import scipy.linalg






def loess(y, X=None, alpha=0.75, order=2):
    """Local Polynomial Regression (LOESS)

    Performs a LOWESS (LOcally WEighted Scatter-plot Smoother) regression.


    Parameters
    ----------
    y : list, array or Series
        The response variable (the y axis).
    X : list, array or Series
        Explanatory variable (the x axis). If 'None', will treat y as a continuous signal (useful for smoothing).
    alpha : float
        The parameter which controls the degree of smoothing, which corresponds
        to the proportion of the samples to include in local regression.
    order : int
        Degree of the polynomial to fit. Can be 1 or 2 (default).

    Returns
    -------
    array
        Prediciton of the LOESS algorithm.

    See Also
    ----------
    signal_smooth

    Examples
    ---------
    >>> import pandas as pd
    >>> import neurokit2 as nk
    >>>
    >>> signal = np.cos(np.linspace(start=0, stop=10, num=1000))
    >>> distorted = nk.signal_distord(signal, noise_amplitude=[0.3, 0.2, 0.1], noise_frequency=[5, 10, 50])
    >>>
    >>> pd.DataFrame({
            "Raw": distorted,
            "Loess_1": nk.loess(distorted, order=1),
            "Loess_2": nk.loess(distorted, order=2)}).plot()

    References
    ----------
    - https://simplyor.netlify.com/loess-from-scratch-in-python-animation.en-us/
    """
    if X is None:
        X = np.linspace(0, 1, len(y))


    assert (order == 1) or (order == 2), "Deg has to be 1 or 2"
    assert (alpha > 0) and (alpha <=1), "Alpha has to be between 0 and 1"
    assert len(X) == len(y), "Length of X and y are different"


    X_domain = X

    n = len(X)
    span = int(np.ceil(alpha * n))
    #y_hat = np.zeros(n)
    #x_space = np.zeros_like(X)

    y_hat = np.zeros(len(X_domain))
    x_space = np.zeros_like(X_domain)

    for i, val in enumerate(X_domain):
    #for i, val in enumerate(X):
        distance = abs(X - val)
        sorted_dist = np.sort(distance)
        ind = np.argsort(distance)

        Nx = X[ind[:span]]
        Ny = y[ind[:span]]

        delx0 = sorted_dist[span-1]

        u = distance[ind[:span]] / delx0
        w = (1 - u**3)**3

        W = np.diag(w)
        A = np.vander(Nx, N=1+order)

        V = np.matmul(np.matmul(A.T, W), A)
        Y = np.matmul(np.matmul(A.T, W), Ny)
        Q, R = scipy.linalg.qr(V)
        p = scipy.linalg.solve_triangular(R, np.matmul(Q.T, Y))
        #p = np.matmul(scipy.linalg.pinv(R), np.matmul(Q.T, Y))
        #p = np.matmul(scipy.linalg.pinv(V), Y)
        y_hat[i] = np.polyval(p, val)
        x_space[i] = val

    return y_hat
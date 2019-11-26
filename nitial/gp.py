import numpy as np
import torch
from torch import optim
import pyro
import pyro.contrib.gp as gp
from pyro.contrib.gp.util import conditional
import pyro.distributions as dist

DTYPE = torch.double
torch.set_default_dtype(DTYPE)

def simplex_grid(n=3, buffer=0.1):
    """ construct a regular grid on the ternary simplex """

    xx, yy = np.meshgrid(np.linspace(0.0, 1., n), np.linspace(0.0, 1.0, n))
    s = np.c_[xx.flat,yy.flat]

    sel = np.abs(s).sum(axis=1) <= 1.0
    s = s[sel]
    ss = 1-s.sum(axis=1)
    s = np.hstack((s, ss[:,None]))

    scale = 1-(3*buffer)
    s = buffer + s*scale
    return s

def model_ternary(X, y, drop_last=True, initial_noise_var=1e-4):
    """ set up GP model for single target """

    if drop_last:
        X = X[:,:-1] # ignore the last composition column

    sel = torch.isfinite(y)
    X, y = X[sel], y[sel]
    N, D = X.size()

    # set up ARD Matern 5/2 kernel
    # set an empirical mean function to the median value of observed data...
    kernel = gp.kernels.RBF(input_dim=2, variance=torch.tensor(1.), lengthscale=torch.tensor([1.0, 1.0]))
    # kernel = gp.kernels.Matern52(input_dim=2, variance=torch.tensor(1.), lengthscale=torch.tensor([1.0, 1.0]))
    model = gp.models.GPRegression(X, y, kernel, noise=torch.tensor(initial_noise_var), jitter=1e-8)
    # model.mean_function = lambda x: model.y.median()

    # set a weakly-informative lengthscale prior
    # e.g. half-normal(0, dx/3)
    dx = 1.0
    model.kernel.set_prior("lengthscale", dist.HalfNormal(dx/3))
    model.kernel.set_prior("variance", dist.Gamma(2.0, 1/2.0))

    # set a prior on the likelihood noise based on the variance of the observed data
    model.set_prior('noise', dist.HalfNormal(model.y.var()/2))

    return model

def update_posterior(model, x_new=None, y_new=None, lr=1e-3, num_steps=150, optimize_noise_variance=True):

    if x_new is not None and y_new is not None:
        if x_new.ndimension() == 1:
            x_new = x_new.unsqueeze(0)
        X = torch.cat([model.X, x_new])
        # y = torch.cat([model.y, y_new.squeeze(1)])
        y = torch.cat([model.y, y_new])
        model.set_data(X, y)

    # update model noise prior based on variance of observed data
    model.set_prior('noise', dist.HalfNormal(model.y.var()))

    # reinitialize hyperparameters from prior
    p = model.kernel._priors
    model.kernel.variance = p['variance']()
    model.kernel.lengthscale = p['lengthscale'](model.kernel.lengthscale.size())


    if optimize_noise_variance:
        model.noise = model._priors['noise']()
        optimizer = optim.Adam(model.parameters(), lr=lr)
    else:
        optimizer = optim.Adam([param for name, param in model.named_parameters() if 'noise' not in name], lr=lr)

    losses = gp.util.train(model, optimizer, num_steps=num_steps)
    return losses

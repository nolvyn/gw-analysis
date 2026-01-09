import numpy as np
from pycbc.waveform import td_approximants, fd_approximants

# If the number 1 is seen here, that is simply for quick testing purposes
# 100 - 1000 typically provide good results
DRAW_QUANTITY = 1

THRESH_NUM = 0.001
ALPHA = 0.3
SMALL = 1e-50
DPI = 100

F_HIGHER = 600
F_LOWER = 20
F_REF = 20
DELTA_F = 1 / 128
DELTA_T = 1 / 4096
FREQ_LENGTH = int(1 / (2 * DELTA_F * DELTA_T)) + 1

GWTC_4_HASH = "1a206db3d_721"

F_GRID = np.arange(F_LOWER, F_HIGHER, DELTA_F)
DF_GRID = np.linspace(0, 0.15, 1000)

FD_MODELS = fd_approximants()
TD_MODELS = td_approximants()

MODEL_PAIRS = [
    # ('IMRPhenomXPHM', 'SEOBNRv5HM_ROM'),
    # ('IMRPhenomD', 'SEOBNRv4HM_ROM'),
    # ('IMRPhenomD', 'SEOBNRv5HM_ROM'),
    # ('IMRPhenomXPHM', 'SEOBNRv4HM_ROM'),
    # ('IMRPhenomXPHM', 'SEOBNRv4_ROM'),
    # ('IMRPhenomXPHM', 'IMRPhenomD'),
    # ('IMRPhenomXPHM', 'IMRPhenomPv3HM'),
    # ('IMRPhenomD', 'NRSur4d2s'),
    ('IMRPhenomD', 'IMRPhenomD'),
    # ('IMRPhenomD', 'NRHybSur3dq8'),
    # ('IMRPhenomD', 'NRSur7dq2'),
    # ('IMRPhenomD', 'NRSur7dq4'),
    # ('IMRPhenomD', 'NR_hdf5'),
    # ('SEOBNRv4HM_ROM', 'SEOBNRv4HM'),
    # ('EccentricFD', 'EccentricTD')
]

PRECESSING_MODELS = [
    'IMRPhenomXPHM', 'IMRPhenomPv3HM'
]

RUN_SPREAD_PLOTS = True
RUN_SPREAD_PARAM_PLOTS = False
RUN_MISMATCH_PLOTS = False

USE_PRECESSING = False

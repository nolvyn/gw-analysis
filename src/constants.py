import numpy as np
from pycbc.waveform import td_approximants, fd_approximants

# If the number 1 is seen here, that is simply for quick testing purposes
# 100 - 1000 typically provide good results
DRAW_QUANTITY = 1

THRESH_NUM = 0.0001
ALPHA = 0.3
SMALL = 1e-50
DPI = 100

F_HIGHER = 600
F_LOWER = 20
F_REF = 20
DELTA_F = 1 / 4
# DELTA_F = 1 / 128
DELTA_T = 1 / 4096
FREQ_LENGTH = int(1 / (2 * DELTA_F * DELTA_T)) + 1

GWTC_4_HASH = "1a206db3d_721"

F_GRID = np.arange(F_LOWER, F_HIGHER, DELTA_F)
DF_GRID = np.linspace(0, 0.15, 1000)

VARY_TOTAL_MASS = [10, 20, 40, 60, 80, 100, 150, 200]
VARY_MASS_RATIO = [0.1, 0.2, 0.35, 0.5, 0.65, 0.8, 0.9, 1.0]
VARY_CHI_EFF = [-0.8, -0.5, -0.3, -0.1, 0.0, 0.1, 0.3, 0.5, 0.8]

FD_MODELS = fd_approximants()
TD_MODELS = td_approximants()

MODEL_PAIRS = [
    ("IMRPhenomXPHM", "SEOBNRv5HM_ROM"),
    # ('IMRPhenomD', 'SEOBNRv4HM_ROM'),
    # ('IMRPhenomD', 'SEOBNRv5HM_ROM'),
    # ('IMRPhenomXPHM', 'SEOBNRv4HM_ROM'),
    # ('IMRPhenomXPHM', 'SEOBNRv4_ROM'),
    # ('IMRPhenomXPHM', 'IMRPhenomD'),
    # ('IMRPhenomXPHM', 'IMRPhenomPv3HM'),
    # ('IMRPhenomD', 'NRSur4d2s'),
    # ('IMRPhenomXPHM', 'NRSur4d2s'),
    # ('IMRPhenomD', 'IMRPhenomD'),
    # ('IMRPhenomD', 'NRHybSur3dq8'),
    # ('IMRPhenomD', 'NRSur7dq2'),
    # ('IMRPhenomD', 'NRSur7dq4'),
    # ('IMRPhenomD', 'NR_hdf5'),
    # ('SEOBNRv4HM_ROM', 'SEOBNRv4HM'),
    # ('EccentricFD', 'EccentricTD')
]

PRECESSING_MODELS = ["IMRPhenomXPHM", "IMRPhenomPv3HM"]

RUN_SPREAD_PLOTS = True
RUN_SPREAD_PARAM_PLOTS = True
RUN_MISMATCH_PLOTS = True
RUN_VARY_PLOTS = True

USE_PRECESSING = False

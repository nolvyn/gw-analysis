import numpy as np

# If the number 1 is seen here, that is simply for quick testing purposes
# 100 - 1000 typically provide good results
DRAW_QUANTITY = 1

THRESH_NUM = 0.001
ALPHA = 0.3
SMALL = 1e-50
DPI = 100

F_HIGHER = 600
F_LOWER = 20
DELTA_F = 1 / 4
F_REF = 20

GWTC_4_HASH = "1a206db3d_721"

F_GRID = np.arange(F_LOWER, F_HIGHER, DELTA_F)
DF_GRID = np.linspace(0, 0.15, 1000)

MODEL_PAIRS = [
    # ('IMRPhenomXPHM', 'SEOBNRv5HM_ROM'),
    # ('IMRPhenomD', 'SEOBNRv4HM_ROM'),
    # ('IMRPhenomD', 'SEOBNRv5HM_ROM'),
    # ('IMRPhenomXPHM', 'SEOBNRv4HM_ROM'),
    # ('IMRPhenomXPHM', 'SEOBNRv4_ROM'),
    # ('IMRPhenomXPHM', 'IMRPhenomD'),
    # ('IMRPhenomXPHM', 'IMRPhenomPv3HM'),
    # ('IMRPhenomD', 'NRSur4d2s'),
    # ('IMRPhenomD', 'IMRPhenomD')
    ('IMRPhenomD', 'NRSur7dq2')
]

PRECESSING_MODELS = [
    'IMRPhenomXPHM', 'IMRPhenomPv3HM'
]

RUN_SPREAD_PLOTS = True
RUN_SPREAD_PARAM_PLOTS = False
RUN_MISMATCH_PLOTS = False

USE_PRECESSING = False

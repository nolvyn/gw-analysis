import numpy as np
import matplotlib.pyplot as plt
import pycbc.psd
from pycbc.filter import match
from pycbc.waveform import get_fd_waveform, get_td_waveform, get_fd_waveform_from_td, td_waveform_to_fd_waveform
import h5py

import constants as C
from gwtc import GWTC_2_1, GWTC_3, GWTC_4

def init_plot():
    plt.figure(figsize=(10, 5), dpi=C.DPI)
    plt.grid(True)

def get_parameters(event):
    if event in GWTC_4:
        fn = f'../data/events/IGWN-GWTC4p0-{C.GWTC_4_HASH}-{event}-combined_PEDataRelease.hdf5'
        aprx_list = ['C00:Mixed']
    elif event in GWTC_3:
        fn = f'../data/events/IGWN-GWTC3p0-v2-{event}_PEDataRelease_mixed_cosmo.h5'
        aprx_list = ['C01:Mixed']
    elif event in GWTC_2_1:
        fn = f'../data/events/IGWN-GWTC2p1-v2-{event}_PEDataRelease_mixed_cosmo.h5'
        aprx_list = ['C01:Mixed']
    
    data = h5py.File(fn, 'r')
    return data[aprx_list[0]]['posterior_samples'][:C.DRAW_QUANTITY]

psd_cache = {}
def calculate_psd(n, delta_f, f_low):
    key = (int(n), float(delta_f), float(f_low))
    psd = psd_cache.get(key)
    if psd is None:
        psd = pycbc.psd.aLIGOZeroDetHighPower(*key)
        psd_cache[key] = psd
    return psd

def calculate_amp(h1, h2):
    return (np.abs(h1) - np.abs(h2)) / (np.abs(h1) + C.SMALL)

def calculate_phase(h1, h2):
    return np.unwrap(np.angle(h1)) - np.unwrap(np.angle(h2))

def calculate_r_phase(d_phi, h1):
    psd_obj = calculate_psd(len(h1), C.DELTA_F, C.F_LOWER)
    ref_amplitude = np.abs(h1)
    ref_sigma = np.interp(h1.sample_frequencies, h1.sample_frequencies, psd_obj) + C.SMALL
    align_weights = (ref_amplitude ** 2) / ref_sigma
    fit = np.polynomial.Polynomial.fit(
        h1.sample_frequencies, d_phi, 1, w=align_weights,
        domain=[C.F_LOWER, h1.sample_frequencies[-1]]
    )
    return d_phi - fit(h1.sample_frequencies)

def calculate_mismatch(h1, h2):
    psd_obj = calculate_psd(len(h1), C.DELTA_F, C.F_LOWER)
    match_val, _ = match(h1, h2, psd=psd_obj, low_frequency_cutoff=C.F_LOWER)
    return 1 - match_val

def truncate_waveform(waveforms, wfm_a, wfm_b):
    min_length = min(len(waveforms[wfm_a]), len(waveforms[wfm_b]))
    for model in [wfm_a, wfm_b]:
        waveforms[model] = waveforms[model][:min_length]

    amp_ref = np.abs(waveforms[wfm_a])
    idx_max_amp = int(np.argmax(amp_ref))
    threshold_amp = C.THRESH_NUM * amp_ref[idx_max_amp]

    idx_threshold = len(amp_ref)
    for i in range(idx_max_amp, len(amp_ref)):
        if amp_ref[i] <= threshold_amp:
            idx_threshold = i
            break

    final_len = idx_threshold
    for model in [wfm_a, wfm_b]:
        waveforms[model] = waveforms[model][:final_len]

    h1 = waveforms[wfm_a]
    h2 = waveforms[wfm_b]

    return waveforms, h1, h2

def get_fd_wfm(waveforms, model, params):
    if model in C.FD_MODELS:
    # if model in FD_MODELS:
        params['delta_f'] = C.DELTA_F
        hp_fd, _ = get_fd_waveform(approximant=model, **params)
        waveforms[model] = hp_fd
    elif model in C.TD_MODELS:
        params['delta_t'] = C.DELTA_T
        hp_td, _ = get_td_waveform(approximant=model, **params)
        hp_fd = td_waveform_to_fd_waveform(hp_td, length=C.FREQ_LENGTH)
        waveforms[model] = hp_fd
    else:
        raise ValueError(f"Model '{model}' is not available")
    return waveforms[model]

def generate_waveform(parameter, wfm_a, wfm_b):
    mass1 = parameter['mass_1']
    mass2 = parameter['mass_2']
    distance = parameter['luminosity_distance']
    inclination = parameter['iota']

    spin1x = parameter['spin_1x']
    spin1y = parameter['spin_1y']
    spin1z = parameter['spin_1z']
    spin2x = parameter['spin_2x']
    spin2y = parameter['spin_2y']
    spin2z = parameter['spin_2z']

    if mass1 < mass2:
        mass1, mass2 = mass2, mass1
        spin1x, spin2x = spin2x, spin1x
        spin1y, spin2y = spin2y, spin1y
        spin1z, spin2z = spin2z, spin1z
    
    mass_ratio = mass2 / mass1
    total_mass = mass1 + mass2
    chi_eff = (mass1*spin1z + mass2*spin2z) / total_mass

    waveforms = {}
    for model in [wfm_a, wfm_b]:
        params = {
            'mass1': mass1,
            'mass2': mass2,
            'spin1z': spin1z,
            'spin2z': spin2z,
            'distance': distance,
            'inclination': inclination,
            'f_lower': C.F_LOWER,
            'f_ref': C.F_REF
        }
        
        if C.USE_PRECESSING and model in C.PRECESSING_MODELS:
            params['spin1x'] = spin1x
            params['spin1y'] = spin1y
            params['spin2x'] = spin2x
            params['spin2y'] = spin2y

        waveforms[model] = get_fd_wfm(waveforms, model, params)

    waveforms, h1, h2 = truncate_waveform(waveforms, wfm_a, wfm_b)

    return (waveforms, h1, h2, 
            mass_ratio, total_mass, 
            chi_eff)

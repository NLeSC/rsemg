# helper functions

from scipy import signal
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import FastICA
from scipy.signal import find_peaks
#from scipy.stats import entropy
import collections
import math
from math import log, e


def emg_bandpass_butter(data_emg, low_pass, high_pass):
    """
    The paramemter taken in here is the Poly5 file. Output is the emg after a bandpass as made here.
    """
    sos = signal.butter(3, [low_pass, high_pass], 'bandpass', fs=data_emg.sample_rate, output='sos')
    # sos (output parameter)is second order section  -> "stabilizes" ?
    emg_filtered = signal.sosfiltfilt(sos, data_emg.samples)
    return emg_filtered

def emg_bandpass_butter_sample(data_emg_samp, low_pass, high_pass, sample_rate, output='sos'):
    """
    The paramemter taken in here is the Poly5 file. Output is the emg after a bandpass as made here.
    """
    sos = signal.butter(3, [low_pass, high_pass], 'bandpass', fs = sample_rate, output='sos')
    # sos (output parameter)is second order section  -> "stabilizes" ?
    emg_filtered = signal.sosfiltfilt(sos, data_emg_samp)
    return emg_filtered

def bad_end_cutter(data_emg, percent_to_cut=7, tolerance_percent=10):
    """
    This algorithm takes the end off of EMGs where the end is radically altered, 
    or if not radically altered cuts the last 10 values
    but returns only the array not an altered Poly5.
    """
    sample = data_emg.samples
    len_sample = len(data_emg.samples[0])

    last_half = data_emg.samples[:,int(len_sample/2):]
    percent = abs(int(percent_to_cut))
    cut_number_last = int(((100- percent)/100)*len_sample)

    last_part = data_emg.samples[:,cut_number_last:]
    leads = last_half.shape[0]
    percent_off_list = []
    for l in range(0,leads):
        last_half_means = last_half[l].mean()
        last_part_means = last_part[l].mean()
        difference = abs(last_half_means- last_part_means)/last_half_means
        percent_off_list.append(difference)
    tolerance_list = []
    for element in percent_off_list:
        tolerance = tolerance_percent/100
        
        if element >= tolerance:
            booly= True
            tolerance_list.append(booly)
        else:
            booly = False
            tolerance_list.append(booly)
            
    if True in tolerance_list:
        sample_cut = sample[:,:cut_number_last]
    else:sample_cut = sample[:,:-10]
        
    return sample_cut

def bad_end_cutter_for_samples(data_emg, percent_to_cut=7, tolerance_percent=10):
    """
    This algorithm takes the end off of EMGs where the end is radically altered, 
    or if not radically altered cuts the last 10 values
    but returns only the array not an altered Poly5.
    """
    sample = data_emg
    len_sample = len(data_emg[0])

    last_half = data_emg[:,int(len_sample/2):]
    percent = abs(int(percent_to_cut))
    cut_number_last = int(((100- percent)/100)*len_sample)

    last_part = data_emg[:,cut_number_last:]
    leads = last_half.shape[0]
    percent_off_list = []
    # get rid of for loop, take advange of numpy array- next version
    for l in range(leads):
        last_half_means = last_half[l].mean()
        last_part_means = last_part[l].mean()
        difference = abs(last_half_means- last_part_means)/last_half_means
        percent_off_list.append(difference)
    tolerance = tolerance_percent / 100
    if any(elt >= tolerance for elt in percent_off_list):
        sample_cut = sample[:, :cut_number_last]
    else:sample_cut = sample[:, :-10]
        
    return sample_cut


def bad_end_cutter_better(data_emg, percent_to_cut=7, tolerance_percent=10):
    """
    This algorithm takes the end off of EMGs where the end is radically altered, 
    or if not radically altered cuts the last 10 values
    but returns only the array not an altered Poly5.
    """
    sample = data_emg.samples
    len_sample = len(data_emg.samples[0])

    last_half = data_emg.samples[:,int(len_sample/2):]
    percent = abs(int(percent_to_cut))
    cut_number_last = int(((100- percent)/100)*len_sample)

    last_part = data_emg.samples[:,cut_number_last:]
    leads = last_half.shape[0]
    percent_off_list = []
    # get rid of for loop, take advange of numpy array- next version
    for l in range(leads):
        last_half_means = last_half[l].mean()
        last_part_means = last_part[l].mean()
        difference = abs(last_half_means- last_part_means)/last_half_means
        percent_off_list.append(difference)
    tolerance = tolerance_percent / 100
    if any(elt >= tolerance for elt in percent_off_list):
        sample_cut = sample[:, :cut_number_last]
    else:sample_cut = sample[:, :-10]
        
    return sample_cut


def notch_filter(sample, sample_frequ, freq_to_pull, quality_factor_q):
    # create notch filter
    samp_freq = sample_frequ # Sample frequency (Hz)
    notch_freq = freq_to_pull # Frequency to be removed from signal (Hz)
    quality_factor = quality_factor_q # Quality factor

    # design a notch filter using signal.iirnotch
    b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)

    # compute magnitude response of the designed filter
    freq, h = signal.freqz(b_notch, a_notch, fs=samp_freq)
    # make the output signal
    output_signal = signal.filtfilt(b_notch, a_notch, sample)
    return output_signal


def show_my_power_spectrum(sample, sample_rate, upper_window):
    N = len(sample)
    # for our emg samplerate is 2048

    yf = fft((sample))
    xf = fftfreq(N, 1 / sample_rate)

    plt.plot(xf, np.abs(yf))
    plt.xlim(0, upper_window)
    plt.show()


def emg_highpass_butter(data_emg, cut_above, sample_rate):
    """
    The paramemter taken in here is the Poly5 file's samples or another array.
     Output is the emg after a bandpass as made here.
    """
    sos = signal.butter(3, cut_above, 'highpass', fs=sample_rate, output='sos')
    # sos (output parameter)is second order section  -> "stabilizes" ?
    emg_filtered = signal.sosfiltfilt(sos, data_emg)
    return emg_filtered

def naive_rolling_rms(x, N):
    xc = np.cumsum(abs(x)**2)
    return np.sqrt((xc[N:] - xc[:-N])/N )

def vect_naive_rolling_rms(x, N):
    xc = np.cumsum(np.abs(x)**2)
    return np.sqrt((xc[N:] - xc[:-N])/N )

def zero_one_for_jumps_base(array, cut_off):
    array_list = []
    for i in array:
        if i < cut_off:
            i = 0
        else: i = 1
        array_list.append(i)
    return array_list

def compute_ICA_two_comp(emg_samples):
    """
    Here we have a function that performs an ICA on EMG data.
    Inputs:
        emg_samples: three layer array of the time series EMG data
    
    Output:
        two signals one of which represents ecg components, theother emg
    """
    X = np.c_[emg_samples[0], emg_samples[2]]
    ica = FastICA(n_components=2)
    S = ica.fit_transform(X)
    component_0 = S.T[0]
    component_1 = S.T[1]
    return component_0, component_1

# now write a function to show which array in tuple has more peaks, and choose it
def pick_more_peaks_array(components_tuple):
    """
    Here we have a function that takes a tuple with the two parts of ICA,
    and finds the one with more peaks and anti-peaks. The EMG if without
    a final envelope will have more peaks
    Note: data should not have been finally filtered to envelope level
    """
    c0= components_tuple[0]
    c1 = components_tuple[1]
    low_border_c0 = (c0.max() -c0.mean())/4
    peaks0, _0 = find_peaks(c0, height=low_border_c0, distance = 10)
    antipeaks0, anti_0 = find_peaks((c0*(-1)), height=-low_border_c0, distance = 10)
    low_border_c1 =(c1.max() -c1.mean())/4
    peaks1, _1 = find_peaks(c1, height=low_border_c1, distance = 10)
    antipeaks1, anti_1 = find_peaks((c1*(-1)), height=-low_border_c1, distance = 10)
        
    sum_peaks_0= len(peaks0) + len(antipeaks0)
    sum_peaks_1= len(peaks1) + len(antipeaks1)
        
    if sum_peaks_0 > sum_peaks_1:
        emg_component = components_tuple[0]
    elif sum_peaks_1 > sum_peaks_0:
        emg_component = components_tuple[1]
    else:
        print("this is very strange data, please examine by hand")
    return emg_component


def working_pipeline_exp(our_chosen_file): 
    """
    This function produces a filtered respiraotry EMG signal from a 3 lead sEMG file.
    Inputs:
        our_chosen_file: string of filename
        
    Output:
        processed emg signal filtered and seperated from ecg components
    """
    cut_file_data = bad_end_cutter(our_chosen_file, percent_to_cut=3, tolerance_percent=5)
    bd_filtered_file_data = emg_bandpass_butter_sample(cut_file_data, 5, 450, 2048, output='sos')
    # step 3 end-cutting again to get rid of filtering artifacts
    re_cut_file_data = bad_end_cutter_for_samples(bd_filtered_file_data, percent_to_cut=3, tolerance_percent=5)
    # skip step4 and do step 5 ICA
    components = compute_ICA_two_comp(re_cut_file_data)
    #     the secret hidden step!
    emg= pick_more_peaks_array(components)
    # now process it in final steps
    abs_values = abs(emg)
    final_envelope_d = emg_highpass_butter(abs_values, 150, 2048)
    final_envelope_a = naive_rolling_rms(final_envelope_d, 300)
        
    return final_envelope_a

def slices_slider(array_sample, slice_len):
    """
    This function produces continous sequential slices over an array of a certain legnth.
    Inputs:
        array_sample: signal
        slice_len: the window which you wish to slide with

    Output:
        the function yields, and does not return these slices
    """
    for i in range(len(array_sample) - slice_len + 1):
        yield array_sample[i:i + slice_len]

def entropical(listy):
    """
    This function computes a certain type of entropy of a series signal array.
    Inputs:
        listy: signal

    Output:
        an array of entropy measurements
    """
    probabilities = [n_x/len(s) for x,n_x in collections.Counter(listy).items()]
    e_x = [-p_x*math.log(p_x,2) for p_x in probabilities]
    return sum(e_x)


def compute_power_loss(original_signal, original_signal_sampling_frequency, processed_signal, processed_signal_sampling_frequency):
    """
    This function computes the percentage of power loss after the processing of a signal.
    Inputs:
        original_signal: signal before the processing
        original_signal_sampling_frequency: sampling frequency of the signal before processing
        processed_signal: signal after processing
        processed_signal_sampling_frequency: sampling frequency of the signal after processing

    Output:
        percentage of power loss
    """

    nperseg = 1024
    noverlap = 512
    
    # power spectrum density of the original and processed signals using Welch method
    Pxx_den_orig = signal.welch(original_signal, original_signal_sampling_frequency, nperseg=nperseg, noverlap = noverlap) #as per Lu et al. 2009
    Pxx_den_processed = signal.welch(processed_signal, processed_signal_sampling_frequency, nperseg=nperseg, noverlap = noverlap) 
    
    # compute the percentage of power loss
    power_loss = 100*(1-(np.sum(Pxx_den_processed)/np.sum(Pxx_den_orig)))
    
    return power_loss

def count_decision_array(decision_array):
    ups_and_downs = np.logical_xor(decision_array[1:], decision_array[:-1])
    count = ups_and_downs.sum()/2
    return count

def smooth_for_baseline(single_filtered_array, start=None, end=None, smooth=100):
    """
    This is an adaptive smoothing that overvalues closer numbers.
    """
    
    array = single_filtered_array[start:end]
    dists = np.zeros(len(array))
    # print(len(array), array.max(), array.min())
    wmax, wmin = 0, 0
    nwmax, nwmin = 0, 0
    tail = (smooth - 1) / smooth

    for i, elt in enumerate(array[1:]):
        if elt > 0:
            nwmax = wmax * tail + elt / smooth
        else:
            nwmin = wmin * tail + elt / smooth
        dist = nwmax - nwmin
        dists[i] = dist
        wmax, wmin = nwmax, nwmin
    return array, dists


def smooth_for_baseline_with_overlay(my_own_array, threshold=10, start=None, end=None, smooth=100):
    """
    This is the same as smooth for baseline, but we also get an overlay 0/1 mask tagging the baseline
    """
    array = my_own_array[start:end]
    overlay = np.zeros(len(array)).astype('int8')
    dists = np.zeros(len(array))
    wmax, wmin = 0, 0
    nwmax, nwmin = 0, 0
    count, filler = 0, False
    tail = (smooth - 1) / smooth
    switched = 0

    for i, elt in enumerate(array[1:]):
        if elt > 0:
            nwmax = wmax * tail + elt / smooth
        else:
            nwmin = wmin * tail + elt / smooth
        dist = nwmax - nwmin
        if (i > smooth) and (i - switched > smooth):
            vodist = dists[i - smooth]
            if (vodist / dist > threshold) or (dist / vodist > threshold):
                filler = not filler
                # Now we need to go back and repaing the values in the overlay
                # because the change was detected after `smooth' interval
                overlay[i - smooth:i] = filler
                count += 1
                switched = i
        overlay[i] = filler
        dists[i] = dist
        wmax, wmin = nwmax, nwmin
    return array, overlay, dists
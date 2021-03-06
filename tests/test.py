#sanity tests for the rsemg library


import unittest
import os
import glob
import sys
from tempfile import TemporaryDirectory
# IMPORT Ole's fixed TMSiSDK python interfacwe- may change
sys.path.insert(0,'C:/Projects/tmsi-python-interface')
from TMSiSDK.file_readers import Poly5Reader


sys.path.insert(0, 'C:/Projects/rsemg')

# converter_functions
from rsemg.converter_functions import poly5unpad
from rsemg.converter_functions import hash_it_up_right_all
# helper_functions
from rsemg.helper_functions import bad_end_cutter
from rsemg.helper_functions import bad_end_cutter_better
from rsemg.helper_functions import bad_end_cutter_for_samples
from rsemg.helper_functions import count_decision_array
from rsemg.helper_functions import emg_bandpass_butter
from rsemg.helper_functions import emg_bandpass_butter_sample
from rsemg.helper_functions import notch_filter
from rsemg.helper_functions import show_my_power_spectrum
from rsemg.helper_functions import naive_rolling_rms
from rsemg.helper_functions import vect_naive_rolling_rms

from rsemg.helper_functions import zero_one_for_jumps_base
from rsemg.helper_functions import compute_ICA_two_comp
from rsemg.helper_functions import working_pipeline_exp
from rsemg.helper_functions import entropical
from rsemg.helper_functions import smooth_for_baseline
from rsemg.helper_functions import smooth_for_baseline_with_overlay

sample_emg = os.path.join('not_pushed','Test_lung_data','2022-05-13_11-51-04','002','EMG_recording'+'.Poly5')



class TestDisplayConverterMethods(unittest.TestCase):

    def test_poly5unpad(self):
        reading =Poly5Reader(sample_emg)
        unpadded= poly5unpad(sample_emg)
        unpadded_line = unpadded[0]
        self.assertEqual(len(unpadded_line), reading.num_samples)


class TestHashMethods(unittest.TestCase):

    def test_hash_it_up_right_all(self):
        tempfile1 = 'sample_emg_t.Poly5'
        tempfile2 = 'sample_emg_t.Poly5'
        with TemporaryDirectory() as td:
            with open(os.path.join(td, tempfile1), 'w') as tf:
                tf.write('string')
            with open(os.path.join(td, tempfile2), 'w') as tf:
                tf.write('string')
            self.assertTrue(hash_it_up_right_all(td, '.Poly5').equals(hash_it_up_right_all(td, '.Poly5')))


class TestFilteringMethods(unittest.TestCase):

    def test_emg_band_pass_butter(self):
        sample_read= Poly5Reader(sample_emg)
        sample_emg_filtered = emg_bandpass_butter(sample_read, 1, 10)
        self.assertEqual(
            (len(sample_emg_filtered[0])),
            len(sample_read.samples[0]) ,
        )
    def test_emg_band_pass_butter_sample(self):
        sample_read= Poly5Reader(sample_emg)
        sample_emg_filtered = emg_bandpass_butter_sample(sample_read.samples, 1, 10, 2048)
        self.assertEqual(
            (len(sample_emg_filtered[0])),
            len(sample_read.samples[0]) ,
        )


class TestCuttingingMethods(unittest.TestCase):

    def test_emg_bad_end_cutter(self):
        sample_ready= Poly5Reader(sample_emg)
        sample_emg_cut = bad_end_cutter(sample_ready, 1, 10)
        self.assertNotEqual(
            (len(sample_emg_cut[0])),
            len(sample_ready.samples[0]),
        )
    def test_emg_bad_end_cutter_for_samples(self):
        sample_read= Poly5Reader(sample_emg)
        sample_emg_cut = bad_end_cutter_for_samples(sample_read.samples, 1, 10)
        self.assertNotEqual(
            (len(sample_emg_cut[0])),
            len(sample_read.samples[0]) ,
        )
    def test_emg_bad_end_cutter_better(self):
        sample_read= Poly5Reader(sample_emg)
        sample_emg_cut = bad_end_cutter_better(sample_read, 1, 10)
        self.assertNotEqual(
            (len(sample_emg_cut[0])),
            len(sample_read.samples[0]) ,
        )
    


if __name__ == '__main__':
    unittest.main()

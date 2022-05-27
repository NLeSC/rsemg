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

from rsemg.converter_functions import poly5unpad
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


class TestFilteringMethods(unittest.TestCase):

    def test_emg_band_pass_butter_filter(self):
        sample_read= Poly5Reader(sample_emg)
        sample_emg_filtered = emg_bandpass_butter(sample_read, 1, 10)
        self.assertEqual(
            (len(sample_emg_filtered[0])),
            len(sample_read.samples[0]) ,
        )


# class TestHashMethods(unittest.TestCase):

#     def test_hash_it_up_right_all(self):
#         tempfile1 = 'tempfile1.cnt'
#         tempfile2 = 'tempfile2.cnt'
#         with TemporaryDirectory() as td:
#             with open(os.path.join(td, tempfile1), 'w') as tf:
#                 tf.write('string')
#             with open(os.path.join(td, tempfile2), 'w') as tf:
#                 tf.write('string')
#             self.assertTrue(hash_it_up_right_all(td, '.cnt').equals(hash_it_up_right_all(td, '.cnt')))



if __name__ == '__main__':
    unittest.main()

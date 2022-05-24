#tests for the library


# from posixpath import splitext
# from itertools import islice
import unittest
import os
import glob
import sys
from tempfile import TemporaryDirectory
# IMPORT Ole's fixed TMSiSDK python interfacwe- may change
sys.path.insert(0,'C:/Projects/tmsi-python-interface')
from TMSiSDK.file_readers import Poly5Reader


sys.path.insert(0, 'C:/Projects/rsemg')

from rsemg.rsemg.converter_functions import poly5unpad
from rsemg.rsemg.helper_functions import bad_end_cutter
from rsemg.rsemg.helper_functions import bad_end_cutter_better
from rsemg.rsemg.helper_functions import bad_end_cutter_for_samples
from rsemg.rsemg.helper_functions import count_decision_array
from rsemg.rsemg.helper_functions import emg_bandpass_butter
from rsemg.rsemg.helper_functions import emg_bandpass_butter_sample
from rsemg.rsemg.helper_functions import notch_filter
from rsemg.rsemg.helper_functions import show_my_power_spectrum
from rsemg.rsemg.helper_functions import naive_rolling_rms
from rsemg.rsemg.helper_functions import vect_naive_rolling_rms
from rsemg.rsemg.helper_functions import zero_one_for_jumps_base
from rsemg.rsemg.helper_functions import compute_ICA_two_comp
from rsemg.rsemg.helper_functions import working_pipeline_exp
from rsemg.rsemg.helper_functions import entropical
from rsemg.rsemg.helper_functions import smooth_for_baseline
from rsemg.rsemg.helper_functions import smooth_for_baseline_with_overlay

sample_emg = os.path.join('not_pushed','Test_lung_data','2022-05-13_11-51-04','002','EMG_recording'+'.Poly5')



class TestDisplayConverterMethods(unittest.TestCase):

    def test_poly5unpad(self):
        reading =Poly5Reader(sample_emg)
        unpadded= poly5unpad(sample_emg)
        unpadded_line = unpadded[0]
        self.assertEqual(len(unpadded_line), reading.num_samples)


# class TestFilteringMethods(unittest.TestCase):

#     def test_band_pass_filter(self):
#         sample_eeg_filtered = band_pass_filter(sample_eeg_bdf_read, 0, 10)
#         self.assertEqual(
#             (sample_eeg_filtered.info['lowpass']),
#             10,
#         )


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

# class TestLoadMethods(unittest.TestCase):

   
#     def test_load_metadata(self):
#         filename = os.path.splitext(sample_metadata)[0]
#         loaded_metadata = load_metadata(
#             filename,
#             sys.path[0],
#             sys.path[0],
#             make_excel_files=False,
#             make_csv_files=False,
#         )
#         self.assertEqual(len(loaded_metadata), 143)

#     def test_load_events(self):
#         loaded_event_markers = load_events(event_marker_folder, sample_eeg_list)
#         self.assertEqual(len(loaded_event_markers), 1)
    
#     def test_call_event_markers(self):
#         # temporary directory
#         expected = 10
#         with TemporaryDirectory() as td:
#             caller_save_events(td, islice(generator_load_dataset(path_eeg), 10))
#             actual = sum(1 for txt in glob.glob(os.path.join(td,'*.txt')))
#         # compare number files generated,to expected which we stop at 10 with 
#         self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()

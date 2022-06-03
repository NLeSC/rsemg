# This file contains functions to work with various EMG file types from various hardware/software combinationation,
# and convert them down to an array

# IMPORT Ole's fixed TMSiSDK python interfacwe- may change
import sys

sys.path.insert(0,'../TMSiSDK')
from TMSiSDK.file_readers import Poly5Reader

def poly5unpad(to_be_read):
    """
    This function converts a Poly5 read into an array without padding
    """
    read_object=  Poly5Reader(to_be_read)
    sample_number= read_object.num_samples
    unpadded = read_object.samples[:, :sample_number]
    return unpadded

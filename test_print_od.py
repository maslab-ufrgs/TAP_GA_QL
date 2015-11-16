import pytest
from ExperimentConfig import ExperimentConfig
from Experiment import Experiment
import os

NET_CAPACITY = None

def test_append_header_function():
    e = Experiment(8, ExperimentConfig.ORTUZAR_NETWORK, NET_CAPACITY,
                   ExperimentConfig.ORTUZAR_NETWORK_OD, 1)
    ed1 = ' tt_AB tt_AC tt_AD tt_BD tt_BE tt_CD tt_CF tt_CG tt_DE tt_DG tt_DH tt_EH tt_FG tt_FI'
    ed2 = ' tt_GH tt_GJ tt_GK tt_HK tt_IJ tt_IL tt_JK tt_JL tt_JM tt_KM'
    r = e.appendExtraODPairTimes('basehader')
    assert r == 'basehader tt_AL tt_AM tt_BL tt_BM' + ed1 + ed2


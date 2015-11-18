import pytest
from ExperimentConfig import ExperimentConfig
from Experiment import Experiment
import os

NET_CAPACITY = None

def test_append_header_function():
    e = Experiment(8, ExperimentConfig.ORTUZAR_NETWORK, NET_CAPACITY,
                   ExperimentConfig.ORTUZAR_NETWORK_OD, 1, printPairOD=True)
    r = e.appendExtraODPairTimes('basehader')
    assert r == 'basehader tt_AL tt_AM tt_BL tt_BM'


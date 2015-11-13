import pytest
from ExperimentConfig import ExperimentConfig
from Experiment import Experiment
import os

NET_CAPACITY = None

def test_append_header_function():
    e = Experiment(8, ExperimentConfig.ORTUZAR_NETWORK, NET_CAPACITY,
                   ExperimentConfig.ORTUZAR_NETWORK_OD, 1)
    ed1 = 'AB AC AD BD BE CD CF CG DE DG DH EH FG FI'
    ed2 = ' GH GJ GK HK IJ IL JK JL JM KM'
    r = e.appendExtraODPairTimes('basehader')
    assert r == 'basehader #od_pairs AL AM BL BM #edges ' + ed1 + ed2


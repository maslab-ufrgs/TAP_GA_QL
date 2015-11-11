import pytest
from ExperimentConfig import ExperimentConfig
from Experiment import Experiment
import os

NET_CAPACITY = None

def test_it_does_not_print_unless_flag_supplied():
    e = Experiment(8, ExperimentConfig.network, NET_CAPACITY,
                   ExperimentConfig.network_od, 1)
    e.printODPairs('test.txt')
    assert not os.path.exists('test.txt.odc')

    e = Experiment(8, ExperimentConfig.network, NET_CAPACITY,
                   ExperimentConfig.network_od, 1, outputtype="pairOD")
    e.printODPairs('test.txt')
    assert os.path.exists('test.txt.odc')

def test_experimento_1():
    e = ExperimentConfig(ks=[8], alphas=[0.9], outputype="pairOD")
    e.run()


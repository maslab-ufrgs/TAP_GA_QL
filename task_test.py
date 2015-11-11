import pytest
from ExperimentConfig import ExperimentConfig
import task

def test_it_runs():
    e = ExperimentConfig()
    e.run()
    assert 0 == 0

def test_experimento_11_2015():
    assert task.experimento_11_2015()

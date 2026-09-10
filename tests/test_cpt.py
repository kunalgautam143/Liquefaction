from liquefaction.calculations.cpt import cq, kc_from_ic, soil_behavior_index


def test_cq_cap():
    assert cq(100.0, 1.0, 1.0) <= 1.7


def test_kc_bounds():
    assert kc_from_ic(1.2) == 1.0
    assert kc_from_ic(2.8) == 1.0


def test_soil_behavior_index_positive():
    assert soil_behavior_index(10.0, 1.0) > 0

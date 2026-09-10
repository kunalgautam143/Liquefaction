from liquefaction.calculations.spt import correction_cn, n160cs


def test_cn_cap():
    assert correction_cn(100.0, 5.0) <= 1.7


def test_fines_piecewise():
    assert n160cs(10.0, 0) == 10.0
    assert n160cs(10.0, 35) > 10.0
    mid = n160cs(10.0, 20)
    assert 10.0 < mid < n160cs(10.0, 35)

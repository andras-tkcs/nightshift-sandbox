import pytest

from sandbox_pkg.numbers import clamp, mean


def test_mean():
    assert mean([1, 2, 3]) == 2.0


def test_mean_empty():
    with pytest.raises(ValueError):
        mean([])


def test_clamp_inside():
    assert clamp(5, 0, 10) == 5


def test_clamp_below():
    assert clamp(-3, 0, 10) == 0


def test_clamp_above():
    assert clamp(15, 0, 10) == 10


def test_clamp_on_bounds():
    assert clamp(0, 0, 10) == 0
    assert clamp(10, 0, 10) == 10


def test_clamp_equal_bounds():
    assert clamp(7, 4, 4) == 4


def test_clamp_float():
    assert clamp(2.5, 0.0, 1.0) == 1.0


def test_clamp_int_stays_int():
    assert type(clamp(15, 0, 10)) is int


def test_clamp_infinity():
    assert clamp(float("inf"), 0, 10) == 10
    assert clamp(float("-inf"), 0, 10) == 0


def test_clamp_low_greater_than_high():
    with pytest.raises(ValueError):
        clamp(5, 10, 0)


def test_clamp_nan_value():
    with pytest.raises(ValueError):
        clamp(float("nan"), 0, 10)


def test_clamp_nan_low():
    with pytest.raises(ValueError):
        clamp(5, float("nan"), 10)


def test_clamp_nan_high():
    with pytest.raises(ValueError):
        clamp(5, 0, float("nan"))

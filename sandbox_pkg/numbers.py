"""Number helpers."""


def mean(values):
    """Return the arithmetic mean of a non-empty sequence of numbers."""
    values = list(values)
    if not values:
        raise ValueError("mean() of an empty sequence")
    return sum(values) / len(values)


def clamp(value, low, high):
    """Return value limited to the inclusive range [low, high]."""
    if value != value or low != low or high != high:  # noqa: PLR0124
        raise ValueError("clamp() argument is NaN")
    if low > high:
        raise ValueError("clamp() low is greater than high")
    if value < low:
        return low
    if value > high:
        return high
    return value

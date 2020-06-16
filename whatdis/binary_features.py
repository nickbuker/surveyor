# TODO update docstrings
# standard library imports
from typing import Union
# third party imports
import numpy as np
import pandas as pd
# local imports
from whatdis import utils


def validate_binary_dtype(data: Union[pd.DataFrame, pd.Series]) -> None:
    """Validates if binary data contains only dtype bool or int.

    Args:
        data: Binary data to be type validated.

    Returns:
        None

    Raises:
        TypeError: If `data` contains dtype other than bool or int
    """
    is_df = utils.check_if_df(data)
    err_message = 'Binary feature columns should be of type bool or int64.'
    types = (np.dtype(bool), np.dtype(int))
    if is_df:
        if not data.dtypes.isin(types).all():
            raise TypeError(err_message)
    else:
        if data.dtypes not in types:
            raise TypeError(err_message)
    return


def check_all_same(data: Union[pd.DataFrame, pd.Series]) -> Union[pd.DataFrame]:
    """Checks if binary data contains columns where all values are the same.

    Args:
        data: Binary data to be checked if all values are the same.

    Returns:
        If `data` is a DataFrame, returns a Series with index of column names and values of bools
        indicating if all values are the same. If `data` is a Series, returns a bool indicating
        if all values are the same.
    """
    is_df = utils.check_if_df(data)
    validate_binary_dtype(data)
    title = 'all_same'
    if is_df:
        return utils.result_to_df(data.min(axis=0).eq(data.max(axis=0)), title=title)
    else:
        return utils.result_to_df(data.min() == data.max(), title=title)


def check_mostly_same(
        data: Union[pd.DataFrame, pd.Series],
        thresh: float = 0.95,
) -> pd.DataFrame:
    """Checks if binary data contains columns where almost all values are the same.

    Args:
        data: Binary data to be checked if almost all values are the same.
        thresh: Threshold for what proportion of data must be the same to fail check.

    Returns:
        Series with index of column names and values of bools indicating if almost all values are the same.

        If `data` is a DataFrame, returns a Series with index of column names and values of bools
        indicating if almost all values are the same. If `data` is a Series, returns a bool
        indicating if almost all values are the same.

    Raises:
        ValueError: If `thresh` less than or equal to 0.0 or greater than or equal to 1.0.
    """
    utils.validate_thresh(thresh)
    is_df = utils.check_if_df(data)
    validate_binary_dtype(data)
    title = 'mostly_same'
    if is_df:
        mean = data.mean(axis=0)
        result = (mean >= thresh) | (mean <= 1 - thresh)
    else:
        mean = data.mean()
        result = mean >= thresh or mean <= 1 - thresh
    return utils.result_to_df(data=result, title=title, thresh=thresh, mean=mean)


def check_outside_range(data: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
    """Checks if binary data contains columns where min is less than 0 or max is greater than 1.
    
    Args:
        data: Binary data to be checked if any values are less than 0 or greater than 1.

    Returns:
        If `data` is a DataFrame, returns a Series with index of column names and values of bools
        indicating if the min or max values out of range. If `data` is a Series, returns a bool
        indicating min or max values are out of range.
    """
    is_df = utils.check_if_df(data)
    validate_binary_dtype(data)
    title = 'outside_range'
    if is_df:
        result = (data.min(axis=0) < 0) | (data.max(axis=0) > 1)
    else:
        result = data.min() < 0 or data.max() > 1
    return utils.result_to_df(data=result, title=title)

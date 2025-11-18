import bisect


def find_closest_index(arr, target):
    """
    Find the index of the closest float value in an array of floats with ascending values.

    :param arr: List of floats in ascending order
    :param target: The target float value
    :return: Index of the closest float value
    """
    # Find the position where the target would be inserted to keep the array sorted
    pos = bisect.bisect_left(arr, target)

    # Check the closest value between the position and the previous position
    if pos == 0:
        return 0
    if pos == len(arr):
        return len(arr) - 1

    before = arr[pos - 1]
    after = arr[pos]

    if after - target < target - before:
        return pos
    else:
        return pos - 1


def add_object_column(df, col_name, default_content=None, replace=False):
    """
    Safely adds a column of object dtype to a DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame to modify.
    - col_name (str): The name of the column to add.
    - default_content (any): The default value for each cell (will be deep-copied).
    - replace (bool): If True, replaces the column if it already exists.

    Returns:
    - pd.DataFrame: Modified DataFrame with the object column.
    """
    import copy
    if default_content is None:
        default_content = []

    if replace or col_name not in df.columns:
        df[col_name] = [copy.deepcopy(default_content) for _ in range(len(df))]
        df[col_name] = df[col_name].astype(object)
    return df
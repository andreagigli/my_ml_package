from sklearn.model_selection import train_test_split


def split_data(X, Y, random_seed=None, train_prc=70, val_prc=15, test_prc=15):
    """
    Splits the dataset into training, validation, and test sets based on specified percentages.

    Args:
        X (DataFrame): DataFrame containing the features.
        Y (DataFrame): DataFrame containing the target variable.
        train_prc (int): Percentage of the dataset to include in the training set.
        val_prc (int): Percentage of the dataset to include in the validation set.
        test_prc (int): Percentage of the dataset to include in the test set.
        random_seed (Optional[int]): Seed for random number generator to ensure reproducibility.

    Returns:
        X_train (DataFrame): Training set features.
        Y_train (DataFrame): Training set target variable.
        X_val (DataFrame): Validation set features.
        Y_val (DataFrame): Validation set target variable.
        X_test (DataFrame): Test set features.
        Y_test (DataFrame): Test set target variable.
        cv_indices (None): Placeholder for cross-validation indices, indicating no cross-validation indices are provided in this function.
    """
    assert train_prc + val_prc + test_prc == 100, "Sum of ratios must be 100"

    # Splitting the dataset
    train_size = train_prc / 100
    val_size = val_prc / 100
    test_size = test_prc / 100

    X_train, X_temp, Y_train, Y_temp = train_test_split(X, Y, train_size=train_size, random_state=random_seed, shuffle=True)
    X_val, X_test, Y_val, Y_test = train_test_split(X_temp, Y_temp, test_size=test_size / (test_size + val_size), random_state=random_seed)

    cv_indices = None

    return X_train, Y_train, X_val, Y_val, X_test, Y_test, cv_indices
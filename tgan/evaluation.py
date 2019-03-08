"""This module contains functions to evaluate the training results."""

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier


def _proc_data(df, continuous_cols):
    """Transform dataframe into matrix of features and its labels.

    Args:
        df(pandas.DataFrame): Dataframe to transform.
        continous_cols(list[str]): Name of columns with continous values.

    Returns:
        tuple[numpy.ndarray, numpy.ndarray]: First element is the feature matrix,
        second the labels.

    """
    features = []
    num_cols = len(list(df))

    for i in range(num_cols - 1):

        if i in continuous_cols:
            features.append(df[i].values.reshape([-1, 1]))

        else:
            features.append(pd.get_dummies(df[i]).values)

    features = np.concatenate(features, axis=1)
    labels = df[num_cols - 1].values

    return features, labels


def evaluate_classification(
    train_csv, test_csv, continuous_cols,
    classifier=DecisionTreeClassifier(max_depth=20), metric=accuracy_score
):
    """Score a model with the given data.

    Args:
        train_csv(str): Path to the train csv file.
        test_csv(str): Path to the test csv file.
        continous_cols(list[str]): List of labels of continous columns.
        classifier(object): Classifier to evaluate the classification. It have to implement
           :meth:`fit` and :meth:`predict` methods.
        metric(callable): Metric to score the classifier results.

    Returns:
        float: score for the given data, classifier and metric.

    """
    train_set = pd.read_csv(train_csv, header=-1)
    test_set = pd.read_csv(test_csv, header=-1)

    n_train = len(train_set)
    dataset = pd.concat([train_set, test_set])

    features, labels = _proc_data(dataset, continuous_cols)

    train_set = features[:n_train], labels[:n_train]
    test_set = features[n_train:], labels[n_train:]

    classifier.fit(train_set[0], train_set[1])

    pred = classifier.predict(test_set[0])

    return metric(test_set[1], pred)


if __name__ == "__main__":
    print(
        evaluate_classification('reconstruct.csv', 'census-test.csv', [0, 5, 16, 17, 18, 29, 38]))

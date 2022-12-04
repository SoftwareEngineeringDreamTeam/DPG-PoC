# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=W

class MetricException(Exception):
    pass


class PrecisionException(MetricException):
    # no values above thresholds
    # in other words, no positive predictions
    # useless classifier
    pass


class RecallException(MetricException):
    # no positive ground truths
    # classification task would not exist
    pass


class F1Exception(MetricException):
    # no true positives detected
    # the classifier would be useless
    pass


class AccuracyException(MetricException):
    # no data at all
    pass

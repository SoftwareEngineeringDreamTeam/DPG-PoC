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
    pass


class RecallException(MetricException):
    # no positive ground truths
    pass

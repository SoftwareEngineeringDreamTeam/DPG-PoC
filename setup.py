# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=W

from setuptools import setup

setup(
    name="ROC'n'ROLL",
    packages=['src'],
    author='SoftwareEngineeringDreamTeam',
    version='0.10.2',
    install_requires=[
        'numpy',
        'dearpygui',
        'plotly',
        'kaleido',
        'scikit-learn'
    ],
)

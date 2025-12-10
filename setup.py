# setup.py
from setuptools import setup, find_packages

setup(
    name="watchtime-booster",
    version="0.1.0",
    description="YouTube Watch Time Booster Dashboard",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
        "numpy",
        "google-api-python-client",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "sentence-transformers",
        "scikit-learn",
        "isodate",
        "moviepy"
    ],
    python_requires=">=3.8",
)

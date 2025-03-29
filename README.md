<p align="center">
    <img src="docs/_static/logo.png" alt="RAVEN Logo" width="300"/>
</p>
<h1 align="center">
    RAVEN
</h1>
<h2 align="center">
    Real-time Analysis of Variable Environmental Networks
</h2>

###
[![Documentation Status](https://readthedocs.org/projects/raven-tool/badge/?version=latest)](https://raven-tool.readthedocs.io/en/latest/?badge=latest)
[![GitHub Actions](https://github.com/ajpung/raven/workflows/RAVEN%20CI/badge.svg)](https://github.com/yourusername/raven/actions) 
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ajpung_raven&metric=alert_status)](https://sonarcloud.io/dashboard?id=yourusername_raven)
[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

## Overview
RAVEN is an ML-enhanced platform that integrates real-time environmental physics
data streams like weather, air quality, seismic, oceanic, and electromagnetic data
to detect, analyze, and predict environmental patterns and anomalies, providing
researchers and urban planners with actionable insights through an API.

Although some environment parameters are obtained through models (ex. weather), 
RAVEN is designed to work with real-time data streams of empirical measurements.

## Documentation
Complete documentation is available at [ReadTheDocs](https://raven-tool.readthedocs.io/en/latest/).

## Features
- Real-time multi-source data ingestion
- Data processing and transformation
- Anomaly detection
- Pattern recognition
- Predictive modeling
- API for data access
- Large Language Models (LLM) for data analysis

## Getting Started
Create a virtual environment, install packages, activate, and export the environment
for use in Jupyter notebooks:

```
python -m venv raven-env
.\raven-env\Scripts\activate
python -m pip install -e .
python -m ipykernel install --user --name=raven-env --display-name="RAVEN Environment"
```
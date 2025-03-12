# User Guide

## Installation

### Prerequisites
- Python 3.13 or higher
- Git
- A virtual environment manager (venv, conda, etc.)

### Installation Steps

1. Clone and enter the repository:
   ```bash
   git clone https://github.com/yourusername/raven.git
   cd raven
   ```

2. Create a virtual environment and install packages:
   ```bash
   python -m venv raven-env
   .\raven-env\Scripts\activate
   python -m pip install -e .
   python -m ipykernel install --user --name=raven-env --display-name="RAVEN Environment"
   ```

## Configuration

### API keys
API keys are stored in a JSON file, `raven/config/api_keys.json`. The file contains
two main keys, `Weather` and `CosmosDB`. Key-value pairs in "Weather" correspond to
API keys of different weather data providers, while key-value pairs in "CosmosDB"
contain connection information for the CosmosDB database.

```json
{
  "Weather": {
    "accu-weather": "your-key-here",
    "open-weather": "your-key-here",
    "synoptic-data": "your-key-here"
  },
  "CosmosDB": {
    "host": "https://apung.documents.azure.com:443/",
    "master_key": "master-key-here",
    "database_id": "WeatherDatabase",
    "container_id": "WeatherContainer"
  }
}
```

## Basic Usage

### Getting Started
from raven import Client

## Common Operations
- How to fetch weather data
- How to analyze patterns
- How to access historical data

## Advanced Usage

### Custom configurations
- How to customize data sources
- How to adjust analysis parameters

### Error Handling
- Common errors and their solutions
- Best practices for production use

## API Rate Limits
- Free tier limitations
- Paid tier quotas
- Best practices for staying within limits

## Troubleshooting
### Common Issues
- Installation problems
- Connection issues
- Data retrieval errors

### Getting Help
- How to report issues
- Community resources
- Contact information
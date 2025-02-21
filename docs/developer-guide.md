# Developer Guide

## Project Structure
```
src/raven/
├── core/         # Core functionality
├── modules/      # Feature modules
├── api/          # API integrations
└── ml/          # Machine learning components
```
## Development Setup
1. Clone the repository
2. Set up virtual environment
3. Install development dependencies

## Testing
How to run tests and add new ones...

## Removing unwanted files
To remove unwanted files, exit the IDE and run the following command via
command prompt:
```commandline
cd <repository directory>
rmdir /s /q <environment directory>

git clean -f
```

To count the number of files within the repository, use either of the following
commands:
```commandline
git ls-files | wc -l
```
(Total files)
```commandline
dir /s /a /b | find /c ":"
```
(Total files and directories)
```commandline
for /d %d in (*) do @echo %d & dir /s /a /b "%d" | find /c ":"
```

To aggressively kill all Python and PyCharm processes, use:
```commandline
taskkill /F /IM python.exe
taskkill /F /IM pythonw.exe
taskkill /F /IM python3.exe
taskkill /F /IM code.exe
taskkill /F /IM pycharm64.exe
```
Note that a large number of files will exist when dependencies are reinstalled
or type checking is run! However, the `.gitignore` is properly set up to prevent
those thousands of unnecessary files from being tracked in the future. Using
these commands will also kill all Python and PyCharm processes, so use with caution.

## Testing Documentation
To test the documentation, begin by installing the documentation dependencies:
```commandline
pip install sphinx sphinx-rtd-theme myst-parser
```
Then, navigate to the `docs/` directory and run the following command:
```commandline
sphinx-build -b html . _build/html
```
To view the documentation, open the `index.html` file in the `_build/html/` directory.

## Units

RAVEN uses metric units throughoutRAVEN uses units to ensure consistency and accuracy in data, and are
defined as follows:

|   Parameter   | Unit |
|:-------------:|:----:|
|   Distance    |  km  |
|  Temperature  |  °C  |
|  Wind speed   | m/s  |
| Precipitation |  mm  |
|  Pressure     |  hPa |
|  Humidity     |   %  |

## Weather Codes
|   Value    |  Code   |
|:----------:|:-------:|
|     0      | Unkonwn |
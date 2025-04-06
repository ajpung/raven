# Developer Guide

## Project Structure
```
src/raven/
├── .github/    # Github CI/CD / ReadTheDocs
├── config/     # API keys and configuration
├── docs/       # Documentation
├── examples/   # Example code / Jupyter notebooks
├── src/raven/  # Source code
└── tests/      # Unit tests
```
## Development Setup
1. Clone the repository
2. Set up virtual environment
3. Install development dependencies

## Installing the Environment
```
# Create a virtual environment
python -m venv raven-env
# Activate the virtual environment
.\raven-env\Scripts\activate
# Install the package in editable mode
python -m pip install -e .
# Install the environment in Jupyter
python -m ipykernel install --user --name=raven-env --display-name="RAVEN Environment"
```

## Testing
How to run tests and add new ones...


To aggressively kill all Python and PyCharm processes, use:
```bash
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
```bash
pip install sphinx sphinx-rtd-theme myst-parser
```
Then, navigate to the `docs/` directory and run the following command:
```bash
sphinx-build -b html . _build/html
```
To view the documentation, open the `index.html` file in the `_build/html/` directory.

## Dates / times
RAVEN utilizes the [`dateparser` package](https://dateparser.readthedocs.io/en/latest/.
- If a date/time does not have an associated timezone, it is assumed to be in UTC.
- If a date/time has a non-UTC timezone, it will be converted to UTC.
- Datetime-to-epoch conversions are done in UTC.

## Units
RAVEN uses metric units throughoutRAVEN uses units to ensure consistency and accuracy in data, and are
defined in the {ref}`Units Reference <units>`.


## Codes
Weather codes and HTTP response codes are used to provide more detailed information
about the weather and status of certain API requests. Weather codes can be found in 
the [Weather Codes Guide](./weather-codes.md), and HTTP response codes can be found in
the [HTTP Codes Guide](./http-codes.md).


## Removing unwanted files
To clean up the repository while in the IDE, run the following commands in Powershell (Windows):
```powershell
$repoPath = "G:\Dropbox\AI Projects\raven"
# Count all files in the repository
(Get-ChildItem -Path $repoPath -File -Recurse).Count

# Remove Python cache files
Remove-Item -Path $repoPath\*.pyc -Recurse -Force
Get-ChildItem -Path $repoPath -Filter "__pycache__" -Directory -Recurse | Remove-Item -Recurse -Force
Remove-Item -Path $repoPath\.mypy_cache -Recurse -Force

# Find directories with the most files
Get-ChildItem -Path $repoPath -Directory -Recurse | 
    ForEach-Object { 
        $count = (Get-ChildItem -Path $_.FullName -File -Recurse).Count
        [PSCustomObject]@{
            Path = $_.FullName
            FileCount = $count
        }
    } | 
    Sort-Object -Property FileCount -Descending | 
    Select-Object -First 10

# Git garbage collect (safe)
cd $repoPath
git gc

# Remove files in the virtual environment
# Create an empty directory 
mkdir "$env:TEMP\empty"
# Use robocopy to mirror the empty directory to the virtual environment
robocopy "$env:TEMP\empty" "$repoPath\raven-env" /MIR
# Remove the empty directory in temp
rmdir "$env:TEMP\empty"
# Try to remove the now-empty target directory
Remove-Item -Path "$repoPath\raven-env" -Force -ErrorAction SilentlyContinue -Y
# Re-count all files in the repository
(Get-ChildItem -Path $repoPath -File -Recurse).Count
```

## Data Sources
Note that while many weather APIs have been integrated into RAVEN, not all of them
are available for one reason or another. For instance, NOAA does not provide 
international weather, while other APIs -- though noted in the Issues -- are too 
janky to use in a reliable manner.

Specific APIs that have been developed and *not* included in the analysis include
Ambee, Meteomatics, and Synoptic Data.
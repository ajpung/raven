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
```bash
cd <repository directory>
rmdir /s /q <environment directory>

git clean -f
```

To count the number of files within the repository, use either of the following
commands:
```bash
git ls-files | wc -l
```
(Total files)
```bash
dir /s /a /b | find /c ":"
```
(Total files and directories)
```bash
for /d %d in (*) do @echo %d & dir /s /a /b "%d" | find /c ":"
```

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

## Cleanup
To clean up the repository, run the following commands in Powershell (Windows):
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
```

or in Bash (Linux):
```bash
# Set repository path
repoPath="/path/to/your/repo"  # Replace with your actual path

# Count all files in the repository
find "$repoPath" -type f | wc -l

# Remove Python cache files
find "$repoPath" -name "*.pyc" -type f -delete
find "$repoPath" -name "__pycache__" -type d -exec rm -rf {} +
rm -rf "$repoPath/.mypy_cache"

# Find directories with the most files
find "$repoPath" -type d -print0 | while IFS= read -r -d '' dir; do
  count=$(find "$dir" -type f | wc -l)
  echo "$count $dir"
done | sort -rn | head -10

# Git garbage collect
cd "$repoPath"
git gc
```
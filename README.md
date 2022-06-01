# TogglReports

![Latest Release](https://img.shields.io/github/v/release/ro-56/toggl-api-sgu-csv)
[![Python package](https://github.com/ro-56/toggl-api-sgu-csv/actions/workflows/python-package.yml/badge.svg)](https://github.com/ro-56/toggl-api-sgu-csv/actions/workflows/python-package.yml)
![License, MIT](https://img.shields.io/badge/license-MIT-green)
![Python, 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)

---

TogglReports is a Python library for creating time entry reports from Toggl's detailed report data.

## Prerequisites

- Install [Python](https://www.python.org/downloads/) which includes [pip](https://pip.pypa.io/en/stable/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install TogglReports.

```bash
pip install git+https://github.com/ro-56/toggl-api-sgu-csv
```

## Usage
TogglReports comes by default with only one type of report (sgu). To create a sgu report, run the following script:

```bash
togglReports build sgu
```

The first time you run the script, you will be prompted to configure your installation. Follow each step to configure the core application and each report type installed.

To reset and redo the configuration script, run the script:

```bash
togglReports config
```

## Report: SGU - Expected Toggl Data Structure

- **Time entry:** The name and duration of the sgu task;
- **Project:** The sgu project;
- **Tag:** The sgu category (if multiple, only one is used);

While configuring the report, you can define a specific tag to indicate that a time entry should be ignored while creating a report. 

## FAQ

### 1. How to locate the Toggl API Token?

Your personal Toggl api token can be found following [these instructions](https://support.toggl.com/en/articles/3116844-where-is-my-api-key-located).

### 2. How to create other report types?

Included in this repository is an example report type containing the basic files structure and required configuration for a report type.

The `src\togglreports\plugins\example.py` file is where the report is built: where the data is manipulated from the information extracted from the Toggl API and where the output file is created.

The `data\reports_example.json` file is where you define the report required configuration parameters. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

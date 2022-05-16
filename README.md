# TogglSgu

![Latest Release](https://img.shields.io/github/v/release/ro-56/toggl-api-sgu-csv)
[![Python package](https://github.com/ro-56/toggl-api-sgu-csv/actions/workflows/python-package.yml/badge.svg)](https://github.com/ro-56/toggl-api-sgu-csv/actions/workflows/python-package.yml)

![License, MIT](https://img.shields.io/badge/license-MIT-green)
![Python, 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)

---

TogglSgu is a Python library for exporting Toggl data and exporting it to a csv file in a specific, pre-defined format. The generated csv can later be used on the SGU plataform.

## Prerequisites

- Install [Python](https://www.python.org/downloads/) which includes [pip](https://pip.pypa.io/en/stable/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install ToggleSgu.

```bash
pip install git+https://github.com/ro-56/toggl-api-sgu-csv
```

## Usage
Create a `.yaml` file using the following template:

```yaml
email: email@mail.com
workspace_id: 123456789
api_token: LoremIpsumDolorSitAmetConsecteturAdipiscingElit
sgu_username: LoremIpsum
output_file_name: output_file
```

Run the script:

```bash
getSguToggl build <YAML FILE>
```
## Expected Toggl Data Structure

- **Time entry:** The name and duration of the sgu task;
- **Project:** The sgu project;
- **Tag:** The sgu category (if multiple, only one is used);

## FAQ

### 1. How to locate the Toggl API Token?

Your personal Toggl api token can be found following [these instructions](https://support.toggl.com/en/articles/3116844-where-is-my-api-key-located).

### 2. How can I find my workspace id?

You can find the ids of the workspaces associated with your Toggl account running the following command:

```bash
getSguToggl getIds <YAML FILE>
```

The `.yaml` file for this use only requires your personal API Token. The other fields are ignored.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

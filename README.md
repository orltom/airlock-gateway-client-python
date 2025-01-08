# airlock-gateway-client-python
![](https://github.com/orltom/airlock-gateway-client-python/workflows/CI/badge.svg)
[![License](https://img.shields.io/github/license/orltom/airlock-gateway-client-python)](/LICENSE)

## Module client
Provide for each resource endpoint an rest api client.

## Module workspace
Provide a fluent way to create or update an Airlock Gateway configuration.

## Requirements
- Python 3.8 or higher
- virutalenv

## Prepare development setup
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Run tests
```
python setup.py test
```

## Build from source
```
python setup.py test
python setup.py build_sphinx
python setup.py sdist bdist_wheel
```

## Contributing
Contributions are welcome in any form, be it code, logic, documentation, examples, requests, bug reports, 
ideas or anything else that will help this project move forward.

## Disclaimer
This project is licensed under the MIT License. See the LICENSE file for more details.

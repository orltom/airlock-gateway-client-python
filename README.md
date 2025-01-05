# airlock-gateway-client-python
![](https://github.com/orltom/airlock-gateway-client-python/workflows/CI/badge.svg)
[![License](https://img.shields.io/github/license/orltom/airlock-gateway-client-python)](/LICENSE)

## Module client
Provide for each resource endpoint an rest api client.

## Module workspace
Provide a fluent way to create or update an Airlock Gateway configuration.

## Documentation
For full documentation and tutorials, trigger:
```
python setup.py build_sphinx
```

## Requirements
- Python 3.8 or higher
- virutalenv

## Prepare development setup
```
python3 -m venv env
source env/bin/activate
pip install -r requirement.txt
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
Please use the [GitHub issue tracker](https://github.com/orltom/airlock-gateway-client-python/issues) to submit bugs or request features.

## Disclaimer
Copyright Orlando Tomás.

Distributed under the terms of the MIT license, airlock-gateway-client is free and open source software.

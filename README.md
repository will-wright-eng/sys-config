<div align="center">

# sys-config

[![Build status](https://github.com/william-cass-wright/sys-config/workflows/build/badge.svg?branch=main&event=push)](https://github.com/william-cass-wright/sys-config/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/sys-config.svg)](https://pypi.org/project/sys-config/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/william-cass-wright/sys-config/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/william-cass-wright/sys-config/blob/main/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/william-cass-wright/sys-config/releases)
[![License](https://img.shields.io/github/license/william-cass-wright/sys-config)](https://github.com/william-cass-wright/sys-config/blob/main/LICENSE)
![Coverage Report](assets/images/coverage.svg)

</div>

`sys-config` is a Python package created with [william-cass-wright/cookiecutter-pypackage-slim](https://github.com/william-cass-wright/cookiecutter-pypackage-slim)... kinda

</div>

**PROJECT DEVELOPMENT NOTES**

## Summary

### how to use

- command line tool (component of `smgmt`)
    - transfer AWS Secrets to local (or visversa)
    - crawl `~/.config` & `~` directories for credentials/configs
        - systematically extract and transform for command line
- within CLI project (used to implement `mmgmt`)
    - init new project after binary install
    - explicitly call config file (endpoint usage pattern)
    - function dectorator (on top of command/endpoint)
    - within context???
- other types of projects???

### value to include in config file?

- pypi tokens
- api keys
- dev and prod split
- app specific references within file system

### components

- file crawler
- extractor
- click interface (class inheritance --> factory design pattern?)

## Usage

implementation example within [media-mgmt-cli]:

```python
from .config import ConfigHandler


class AwsStorageMgmt:
    def __init__(self):
        self.s3_resour = boto3.resource("s3")
        self.s3_client = boto3.client("s3")
        self.config = ConfigHandler(project_name="media_mgmt_cli")
        if self.config.check_config_exists():
            self.configs = self.config.get_configs()
            self.bucket = self.configs.get("aws_bucket", None)
            self.object_prefix = self.configs.get("aws_bucket_path", None)
        else:
            echo("config file does not exist, run `mmgmt configure`")

    def upload_file(self, file_name, object_name=None):
        """
        ...
        """
        echo(
            f"uploading: {file_name} \nto S3 bucket: {self.configs.get('aws_bucket')}/{self.configs.get('aws_bucket_path')}/{file_name}"
        )
        ...
```

## Future Work

- setup sys-config

## Project Examples

- [media-mgmt-cli]
- [secret-mgmt-cli]

[media-mgmt-cli]: https://github.com/william-cass-wright/media-mgmt-cli
[secret-mgmt-cli]: https://github.com/william-cass-wright/secrets-mgmt-cli

## Publishing Notes

1. `make install`

```Makefile
#* Installation
.PHONY: install
install:
    poetry lock -n && poetry export --without-hashes > requirements.txt
    poetry install -n
    -poetry run mypy --install-types --non-interactive ./
```

2. bump version

```bash
poetry version [major, minor, bug]
```

> only updates within pyproject.toml

3. publish

```bash
poetry publish --dry-run --build
poetry publish --build
```

4. test

```bash
jupyter lab
python -m pip install sys-config
```

*REPL*

```python
import sys_config
parser = sys_config.ConfigHandler()
parser.__dict__
# results
parser.__dir__()
# results
```

```js
{'project_name': 'tmp',
 'home_path': PosixPath('/Users/willcasswrig'),
 'config_path': PosixPath('/Users/willcasswrig/.config/tmp'),
 'config_file_path': PosixPath('/Users/willcasswrig/.config/tmp/config'),
 'verbose': False,
 'parser': <configparser.ConfigParser at 0x7f8c224ec430>}


['project_name',
 'home_path',
 'config_path',
 'config_file_path',
 'verbose',
 'parser',
 '__module__',
 '__init__',
 'crud_create',
 'create_config_file',
 'crud_update',
 'update_parser',
 'crud_delete_file',
 'crud_read',
 'read_dict',
 'get_config_exists',
 'get_parser_sections',
 'write_config_file',
 'set_config_path',
 'reset_config_path',
 '__dict__',
 '__weakref__',
 '__doc__',
 '__new__',
 '__repr__',
 '__hash__',
 '__str__',
 '__getattribute__',
 '__setattr__',
 '__delattr__',
 '__lt__',
 '__le__',
 '__eq__',
 '__ne__',
 '__gt__',
 '__ge__',
 '__reduce_ex__',
 '__reduce__',
 '__subclasshook__',
 '__init_subclass__',
 '__format__',
 '__sizeof__',
 '__dir__',
 '__class__']
```

*errors*

`parser.crud_read()`

```python
     82 def crud_read(self):
---> 83     self.read_dict(self.__dict__, self.__class__.__name__)
```

> TypeError: Object of type PosixPath is not JSON serializable

`parser.crud_create()`

```
Signature: parser.crud_create()
Docstring: <no docstring>
File:      ~/miniconda/envs/jl2/lib/python3.10/site-packages/sys_config/main.py
Type:      method
```

> add docstring

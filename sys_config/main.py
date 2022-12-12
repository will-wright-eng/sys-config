from typing import Any, Dict

import os
import json
import pathlib
import configparser


class ConfigHandler:
    def __init__(self, project_name="tmp", verbose=False):
        self.project_name = project_name
        self.home_path = pathlib.Path.home()
        self.config_path = self.home_path / ".config" / self.project_name
        self.config_file_path = self.config_path / "config"
        self.verbose = verbose
        self.parser = configparser.ConfigParser()
        if self.get_config_exists():
            print("config file exists, reading contents into parser")
            self.config.read(self.config_file_path)

    # CRUD: create config file
    def crud_create(self):
        """ """
        if self.get_config_exists():
            resp = input("overwrite current config? [Y/n]")
            if resp.lower() in ("yes", "y", "yep", "true"):
                print("overwriting config file")
                self.crud_update()
            else:
                return False
        else:
            self.create_config_file()

    def create_config_file(self):
        if len(self.get_parser_sections()) > 0:
            self.write_config_file(mode="w")
        else:
            print("no contents to write, use update_parser(dict) method to add contents to parser then write")

    # CRUD: update contents
    def crud_update(self, config_dict: Dict[str, Any] = None) -> bool:
        """
        1. update parser with config dict, if used
        2. if file exists, delete it
        3. write new config file from parser
        """
        if config_dict:
            self.update_parser(config_dict)

        try:
            if self.get_config_exists():
                self.crud_delete_file()
            self.create_config_file()
            return True
        except Exception as e:
            print(e)
            return False

    def update_parser(self, config_dict):
        """
        parser = configparser.ConfigParser()
        parser.read_dict({'section1': {'key1': 'value1',
                                       'key2': 'value2',
                                       'key3': 'value3'},
                          'section2': {'keyA': 'valueA',
                                       'keyB': 'valueB',
                                       'keyC': 'valueC'},
                          'section3': {'foo': 'x',
                                       'bar': 'y',
                                       'baz': 'z'}
        })
        """
        self.parser.read_dict(config_dict)

    # CRUD: delete
    def crud_delete_file(self):
        if self.get_config_exists():
            os.remove(self.config_file_path)
        else:
            print("file does not exist")

    # CRUD: read
    def crud_read(self):
        self.read_dict(self.__dict__, self.__class__.__name__)
        self.read_dict(self.parser._sections, self.parser.__class__.__name__)

    def read_dict(self, dict_obj, obj_name: str) -> None:
        print(f"\n# {obj_name} #")
        print(json.dumps(dict_obj, indent=4, sort_keys=True))

    # get
    def get_config_exists(self):
        return os.path.isfile(self.config_file_path)

    def get_parser_sections(self):
        return self.parser.sections()

    # put
    def write_config_file(self, mode: str = "w+"):
        with open(self.config_file_path, mode) as configfile:
            self.parser.write(configfile)

    # set
    def set_config_path(self, local_path: str = "local"):
        if local_path == "local":
            self.config_path = pathlib.Path(".")
        else:
            self.config_path = pathlib.Path(local_path)
        self.config_file_path = self.config_path / "config"

    def reset_config_path(self):
        self.config_path = self.home_path / ".config" / self.project_name
        self.config_file_path = self.config_path / "config"

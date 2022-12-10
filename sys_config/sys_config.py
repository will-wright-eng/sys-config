import os
import pathlib
import configparser


class ConfigHandler:
    def __init__(self, project_name="tmp", verbose=False):
        p = pathlib.Path.home()
        self.home_path = p
        self.config_path = p / ".config" / project_name
        self.config_file_path = self.config_path / "config"
        self.verbose = verbose
        self.config = configparser.ConfigParser()

    def check_exists_print(self):
        if not os.path.isfile(self.config_file_path):
            print(f"config file does not exist for {project_name}")
            return "config file does not exist -- run configure endpoint"
        else:
            self.config.read(self.config_file_path)
            if self.verbose:
                print("-- config file exists --")
                print(self.print_configs())

    def check_config_exists_bool(self):
        return os.path.isfile(self.config_file_path)

    def print_configs(self):
        print(self.config.defaults())
        for key, val in self.config.defaults().items():
            self.print_formatted_configs(key, val)

    def print_formatted_configs(self, key, val, n=20):
        key = str(key)
        val = str(val)
        print(key, (n - int(len(key))) * ".", val)

    def put_file_and_dir(self):
        self.config_path.mkdir(parents=True, exist_ok=True)
        self.config_file_path.touch()

    def put_config_to_file(self):
        # rewrite config file
        with open(self.config_file_path, "w") as configfile:
            self.config.write(configfile)

    def put_config_file_from_dict(self, config_dict: dict):
        self.config_file_input(config_dict)
        self.put_config_to_file()

    def put_project(self, project_name):
        self.project_name = project_name
        self.config_path = self.home_path / ".config" / project_name
        self.config_file_path = self.config_path / "config"
        self.config = configparser.ConfigParser()
        if os.path.isfile(self.config_file_path):
            self.config.read(self.config_file_path)
            print("-- config file exists --")
            print(self.print_configs())

    def put_configs_to_env(self):
        # export configs as environment variables
        for key, val in self.config.defaults().items():
            if key is not None:
                os.environ[key.upper()] = val

    def get_configs_from_file(self):
        if os.path.isfile(self.config_file_path):
            return self.config.defaults()
        else:
            return None

    def get_configs(self, section: str = "DEFAULT"):
        return self.config.defaults()

    def config_file_input(self, config_dict: dict, section: str = "DEFAULT"):
        """
        example:
        config['DEFAULT'] = {'ServerAliveInterval': '45',
                      'Compression': 'yes',
                      'CompressionLevel': '8',}
        """
        self.config[section] = config_dict

    def list_config_dirs(self):
        # list directories
        p = self.home_path / ".config"
        active = []
        other = []
        for x in p.iterdir():
            if x.is_dir():
                tmp = x / "config"
                if os.path.isfile(tmp):
                    active.append(tmp.resolve())
                    resp = "config file exists"
                else:
                    other.append(x.resolve())
                    resp = "no config file"
                self.print_formatted_configs(x, resp, n=45)

        for file_path in active:
            print("\n-- ", file_path, " --")
            tmp = configparser.ConfigParser()
            tmp.read(file_path)
            for key, val in tmp.defaults().items():
                self.formatted_print(key, val)

    def formatted_print(self, key, val, n=20):
        key = str(key)
        val = str(val)
        print(key, (n - int(len(key))) * ".", val)

    def get_configs(self):
        if os.path.isfile(self.config_file_path):
            return self.config.defaults()
        else:
            return None

    def check_config_exists(self):
        return os.path.isfile(self.config_file_path)
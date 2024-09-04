class ConfigParser:
    def __init__(self):
        self.word = '='
        self.config = {}
        return

    def load_config(self, file_path: str, encoding: str = 'utf-8'):
        with open(file=file_path, mode='r', encoding=encoding) as f:
            config_str: str = f.read()
            f.close()

        if config_str == '':
            return False
        config_list = config_str.split('\n')
        config = {}

        for config_tmp in config_list:
            key = ""
            value = ""
            try:
                key = config_tmp.split(self.word)[0].strip()
                value = config_tmp.split(self.word)[1].strip()
            except IndexError:
                pass

            config[key] = value
        self.config = config

        return config

    def add_config(self, key: str, value) -> None:
        self.config[key] = value
        return None

    def delete_config(self, key: str) -> None:
        del self.config[key]
        return None

    def get(self, key: str, default=None):
        return self.config.get(key, default)

    def save_config(self, file_path: str, encoding: str = 'utf-8'):
        config = ''
        for key, value in self.config.items():
            config += f'{key} {self.word} {value}\n'

        with open(file=file_path, mode='w', encoding=encoding) as f:
            f.write(config)
            f.close()
        return None


    def display_config(self):
        for key, value in self.config.items():
            print(f'{key}: {value}')
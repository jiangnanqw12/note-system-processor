class GlobalFlags:
    def __init__(self):
        self.flags = {
            'flag_one_by_one': False,
            'verbose': False,
            'debug': True,
            'TR_MODE': False,
        }

    def set_flag(self, name, value):
        if name in self.flags:
            self.flags[name] = value
        else:
            raise KeyError(f"Flag '{name}' not found.")

    def get_flag(self, name):
        print(f"Getting flag '{name}'")
        print(f"Flags: {self.flags}")
        return self.flags.get(name, None)

    def toggle_flag(self, name):
        if name in self.flags:
            self.flags[name] = not self.flags[name]
        else:
            raise KeyError(f"Flag '{name}' not found.")


if __name__ == '__main__':
    # Usage
    flags = GlobalFlags()
    flags.set_flag('debug', True)
    print(flags.get_flag('debug'))  # Output: True
    flags.toggle_flag('debug')
    print(flags.get_flag('debug'))  # Output: False

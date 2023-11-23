class GlobalFlags:
    def __init__(self):
        self.flags = {
            'flag_one_by_one': False,
            'verbose': False,
            'debug': True,
            'TR_MODE': True,
            'TR_MODE_debug': True,
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


def get_flag_default():
    flags = GlobalFlags()
    flags.set_flag('TR_MODE', True)
    return flags


def get_flag_one_by_one(TR_MODE=0):
    flag_one_by_one = True
    return flag_one_by_one


def get_flag_search_sub_topic1_in_bvids_origin_topic_path(TR_MODE=0):
    flag_search_sub_topic1 = False
    return flag_search_sub_topic1


def main():
    # Usage
    flags = GlobalFlags()
    flags.set_flag('debug', True)
    print(flags.get_flag('debug'))  # Output: True
    flags.toggle_flag('debug')
    print(flags.get_flag('debug'))  # Output: False


if __name__ == '__main__':

    main()

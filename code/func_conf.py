import sys

import toml


def read_conf(file="data/conf/conf1.toml"):
    """
    可以作为中介配置
    """
    try:
        with open(file,encoding='utf-8') as configfile:
            confstr = configfile.read()
        return toml.loads(confstr)
    except Exception as e:
        print('Conf File not found. Check the path variable and filename: ', str(e))
        sys.exit()
def save_conf(data, file="data/conf/conf1.toml"):
    """
    保存配置文件
    """
    try:
        with open(file, "w", encoding="utf-8") as configfile:
            toml.dump(data, configfile)
    except Exception as e:
        print("Failed to save configuration file:", str(e))
        sys.exit()


if __name__ == '__main__':
    conf = read_conf()
    conf['ending']['start']=50000
    # start_duration = conf['data']['start']
    # end_duration = conf['data']['end']
    save_conf(conf)
    print(conf['ending'])
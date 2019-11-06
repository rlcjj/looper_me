from configparser import ConfigParser

from ctpbee import CtpBee

from data_pointer.pointer import DataPointer

if __name__ == '__main__':
    cfg = ConfigParser()
    cfg.read('config.ini')
    remote_ip = cfg.get("client", "remote_ip")
    remote_port = cfg.getint("client", "remote_port")
    key = cfg.get("client", "key")

    """ 简单的基于ctpbee的数据发送端 """
    app = CtpBee("data_pointer", __name__)
    app.config.from_json("data_pointer/config.json")
    pointer = DataPointer("origin_pointer", (remote_ip, remote_port), key)
    app.add_extension(pointer)
    app.start()

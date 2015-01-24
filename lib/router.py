from __future__ import print_function
from jnpr.junos import Device
from lxml import etree


class Router(object):
    @property
    def host(self):
        return self._host

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return None

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def connected(self):
        return self._connected

    @property
    def connection(self):
        return self._connection

    def __init__(self, **kwargs):
        self._host = kwargs.get("host")
        self._user = kwargs.get("user")
        self._password = kwargs.get("password")
        self._gather = kwargs.get("facts", False)
        self._connected = False
        self._connection = self.connect()

    def connect(self):
        connection = Device(host=self._host,
                            user=self._user,
                            password=self._password,
                            gather_facts=self._gather)

        try:
            connection.open()
            self._connected = True
            return connection
        except Exception as e:
            print(e)

    def get_config(self, section=None, structure="text"):
        root = None
        if section is not None:
            root = etree.Element("configuration")
            root.append(etree.Element(section))
        return self._connection.rpc.get_config(root, dict(format=structure))

    def get_interfaces(self, *args, **kwargs):
        structure = kwargs.get("format", "text")
        name = args[0] if len(args) else kwargs.get("name", None)
        options = {"format": structure}
        if name is not None:
            return self.get_interface(options=options, name=name)
        return self._connection.rpc.get_interface_information(options)

    def get_interface(self, *args, **kwargs):
        options = kwargs.get("options")
        name = args[0] if len(args) else kwargs.get("name")
        name = {"interface_name": name}
        return self._connection.rpc.get_interface_information(options, **name)

    def get_bgp(self, *args, **kwargs):
        structure = kwargs.get("format", "text")
        neighbor = args[0] if len(args) else kwargs.get("neighbor", None)
        options = {"format": structure}
        summary = kwargs.get("summary", True)
        if summary:
            return self._connection.rpc.get_bgp_summary_information(options)
        if neighbor is not None:
            return self.get_bgp_neighbor(options=options, neighbor=neighbor)
        return self._connection.rpc.get_bgp_neighbor_information(options)

    def get_bgp_neighbor(self, *args, **kwargs):
        options = kwargs.get("options")
        neighbor = args[0] if len(args) else kwargs.get("neighbor")
        neighbor = {"neighbor_address": neighbor}
        return self._connection.rpc.get_bgp_neighbor_information(options,
                                                                 **neighbor)

    def get_stateful_policies(self, *args, **kwargs):
        detail = args[0] if len(args) else kwargs.get("detail", True)
        structure = kwargs.get("format", "text")
        options = {"format": structure}
        from_zone = kwargs.get("from", None)
        to_zone = kwargs.get("to", None)
        restrictions = {"detail": detail}
        if from_zone is not None:
            restrictions["from_zone"] = from_zone
        if to_zone is not None:
            restrictions["to_zone"] = to_zone
        return self._connection.rpc.get_firewall_policies(options,
                                                          **restrictions)

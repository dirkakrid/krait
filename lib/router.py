"""Router Module

This module implements some abstraction to allow users to interact more
naturally with Junos devices via the Python interpreter.

Most of the methods default to a format of "text" for the RPC calls.  This is
because this is designed primarily for traditional network engineers, and
that's the output format they'll be most comfortable with.

With the above said, although this module is primarily for interacting with
Junos devices via the Python interpreter, it can also be used in a traditional
programming or scripting environment.  For that purpose, it is highly
recommended that you override the default format and set it to "xml".

"""
from __future__ import print_function
from jnpr.junos import Device
from lxml import etree


class Router(object):
    """Router Class

    Implement the Router object.  Routers are the most common network
    elements, and we focus on these and their capabilities.  Most of this
    class's methods have a `format` that defaults to `text`.  It can be
    specified as `xml` for a more programattic interface to the devices.

    """

    @property
    def host(self):
        """
        returns the hostname
        """
        return self._host

    @property
    def user(self):
        """
        returns the user used to login
        """
        return self._user

    @property
    def connected(self):
        """
        returns the state of the connection
        """
        return self._connected

    @property
    def connection(self):
        """
        returns the connection
        """
        return self._connection

    def __init__(self, **kwargs):
        self._host = kwargs.get("host")
        self._user = kwargs.get("user")
        self._password = kwargs.get("password")
        self._gather = kwargs.get("facts", False)
        self._connected = False
        self._connection = self.connect()

    def connect(self):
        """
        Connect to a device.  Uses some settings specified when a Router
        object is instantiated.  Also sets `gather_facts`, which is `False`
        by default (set when the Router object is instantiated).
        """
        connection = Device(host=self._host,
                            user=self._user,
                            password=self._password,
                            gather_facts=self._gather)

        connection.open()
        self._connected = True
        return connection

    def get_config(self, section=None, structure="text"):
        """
        Returns the device configuration in `text` format (the format you
        normally see when typing `show configuration`).  Format can be set to
        `xml`.  Also accepts a `section`, which is the first level of
        configuration hierarchy (such as `show configuration protocols`).
        """
        root = None
        if section is not None:
            root = etree.Element("configuration")
            root.append(etree.Element(section))
        return self._connection.rpc.get_config(root, dict(format=structure))

    def get_interfaces(self, *args, **kwargs):
        """
        Returns the status of all interfaces.  An individual interface can be
        specified via the `name` keyword (or positional argument in position
        `0`).  `format` can also be `xml`.
        """
        structure = kwargs.get("format", "text")
        name = args[0] if len(args) else kwargs.get("name", None)
        options = {"format": structure}
        if name is not None:
            return self.get_interface(options=options, name=name)
        return self._connection.rpc.get_interface_information(options)

    def get_interface(self, *args, **kwargs):
        """
        Returns the status of an individual interface.  Similar to
        `get_interfaces`.  Currently requires `options` to be set to a dict.
        This should (currently) only be used internally by `get_interfaces`,
        but it will later be ready for direct access.
        """
        options = kwargs.get("options")
        name = args[0] if len(args) else kwargs.get("name")
        return self._connection.rpc.get_interface_information(options,
                                                              interface_name=name)

    def get_bgp(self, *args, **kwargs):
        """
        returns the status of BGP.  May return summary information, all
        neighbors, or specific neighbors.  Default `format` is `text`, but may
        be set to `xml` for more programmatic uses.
        """
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
        """
        Returns the status of a specific BGP neighbor.  Currently for use by
        internal methods only.
        """
        options = kwargs.get("options")
        neighbor = args[0] if len(args) else kwargs.get("neighbor")
        return self._connection.rpc.get_bgp_neighbor_information(options,
                                                                 neighbor_address=neighbor)

    def get_stateful_policies(self, *args, **kwargs):
        """
        Returns the stateful policies configured on the device.  This is
        applicable to SRX devices only.  `from` and `to` may be specified as
        zones to filter down the policies you're interested in.  `detail` is
        set to `True` by default (but can be set to `False`) to provide better
        information than just object names.
        """
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

    def get_header(self):
        """
        Returns the device name and software version.  It is the equivalent of
        `show version brief`.
        """
        return self._connection.rpc.get_software_information({"format": "text"},
                                                             brief=True)
    def get_arp(self, *args, **kwargs):
        """
        Returns ARP table.
        """
        hostname = args[0] if len(args) else kwargs.get("hostname", None)
        structure = kwargs.get("format", "text")
        options = {"format": structure}
        if hostname is None:
            return self._connection.rpc.get_arp_table_information(options)
        return self._connection.rpc.get_arp_table_information(options,
                                                              hostname=hostname)

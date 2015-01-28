# krait

An alternative for interfacing with Juniper Networks devices.  All methods
return `text` by default to ease the transition for traditional network
engineers.  That default is easily changed to `xml` for a programmatic interface
to the network elements.

## Installation

You'll need [py-junos-eznc][1].  Once that's done, just clone this repository
(`git clone https://github.com/supertylerc/krait`) and run the script
(`python main.py`).  You can instantiate a device manually from that shell.

Alternatively, you can specify a device to work with initially with the `-d`
option.  This connection will be stored in a variable called `device`.

## Usage

The source code is somewhat self-documenting, but here are some examples.

```lang-python
tyler:krait/ (master✗) > python main.py -d 10.10.1.1                                                                                          [21:24:18]
Krait Power Shell for Junos
Author: Tyler Christiansen <code@tylerc.me>
<output>
node0:
--------------------------------------------------------------------------
Hostname: <redacted>
Model: srx1400
JUNOS Software Release [12.1X44-D25.5]

node1:
--------------------------------------------------------------------------
Hostname: <redacted>
Model: srx1400
JUNOS Software Release [12.1X44-D25.5]
</output>

Python 2.7.8 (default, Oct 20 2014, 15:05:19)
[GCC 4.9.1] on linux2
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> print("User: " + device.user + "\nHostname: " + device.host + "\nConnected: " + str(device.connected))
User: rancid
Hostname: 10.10.1.1
Connected: True
>>> print(etree.tostring(device.get_bgp()))
<output>
Groups: 4 Peers: 9 Down peers: 0
Table          Tot Paths  Act Paths Suppressed    History Damp State    Pending
inet.0               119          9          0          0          0          0
Peer                     AS      InPkt     OutPkt    OutQ   Flaps Last Up/Dwn State|#Active/Received/Accepted/Damped...
111.111.111.11        65001     754159     752103       0       5  6d 8:46:07 3/3/3/0              0/0/0/0
222.222.222.22        65002      91429      97099       0      11      1w3d7h 1/19/1/0             0/0/0/0
</output>

>>> print(etree.tostring(device.get_bgp(format="xml")))
<bgp-information>
<group-count>4</group-count>
<peer-count>9</peer-count>
<down-peer-count>0</down-peer-count>
<bgp-rib style="brief">
<name>inet.0</name>
<total-prefix-count>119</total-prefix-count>
<received-prefix-count>119</received-prefix-count>
<accepted-prefix-count>11</accepted-prefix-count>
<active-prefix-count>9</active-prefix-count>
<suppressed-prefix-count>0</suppressed-prefix-count>
<history-prefix-count>0</history-prefix-count>
<damped-prefix-count>0</damped-prefix-count>
<total-external-prefix-count>119</total-external-prefix-count>
<active-external-prefix-count>9</active-external-prefix-count>
<accepted-external-prefix-count>11</accepted-external-prefix-count>
<suppressed-external-prefix-count>0</suppressed-external-prefix-count>
<total-internal-prefix-count>0</total-internal-prefix-count>
<active-internal-prefix-count>0</active-internal-prefix-count>
<accepted-internal-prefix-count>0</accepted-internal-prefix-count>
<suppressed-internal-prefix-count>0</suppressed-internal-prefix-count>
<pending-prefix-count>0</pending-prefix-count>
<bgp-rib-state>BGP restart is complete</bgp-rib-state>
</bgp-rib>
<bgp-peer style="terse" heading="Peer                     AS      InPkt     OutPkt    OutQ   Flaps Last Up/Dwn State|#Active/Received/Accepted/Damped...">
<peer-address>111.111.111.11</peer-address>
<peer-as>65001</peer-as>
<input-messages>754179</input-messages>
<output-messages>752123</output-messages>
<route-queue-count>0</route-queue-count>
<flap-count>5</flap-count>
<elapsed-time seconds="550153">6d 8:49:13</elapsed-time>
<peer-state format="3/3/3/0              0/0/0/0">Established</peer-state>
<bgp-rib>
<name>inet.0</name>
<active-prefix-count>3</active-prefix-count>
<received-prefix-count>3</received-prefix-count>
<accepted-prefix-count>3</accepted-prefix-count>
<suppressed-prefix-count>0</suppressed-prefix-count>
</bgp-rib>
</bgp-peer>
<bgp-peer style="terse">
<peer-address>222.222.222.22</peer-address>
<peer-as>65002</peer-as>
<input-messages>91448</input-messages>
<output-messages>97120</output-messages>
<route-queue-count>0</route-queue-count>
<flap-count>11</flap-count>
<elapsed-time seconds="890715">1w3d7h</elapsed-time>
<peer-state format="1/19/1/0             0/0/0/0">Established</peer-state>
<bgp-rib>
<name>inet.0</name>
<active-prefix-count>1</active-prefix-count>
<received-prefix-count>19</received-prefix-count>
<accepted-prefix-count>1</accepted-prefix-count>
<suppressed-prefix-count>0</suppressed-prefix-count>
</bgp-rib>
</bgp-peer>
</bgp-information>

>>>
```

> The example above has truncated output for brevity.
> This shell uses the new `print` function
> (`from __future__ import print_function`).

## Contributing

1. Fork it!
2. Create an issue on GitHub
3. Create your feature branch: `git checkout -b feat/gh-#-feature-name`
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin feat/gh-#-feature-name`
6. Submit a pull request :D

## History

2015-02-26: README.md Created

## Credits

Author: [Tyler Christiansen][2] <code@tylerc.me>.

## License

MIT.  See [LICENSE](LICENSE).

[1]: https://github.com/Juniper/py-junos-eznc "py-junos-eznc"
[2]: https://twitter.com/oss_stack "Tyler Christiansen on Twitter"

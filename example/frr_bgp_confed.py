#!/usr/bin/env python

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.log import setLogLevel

import mnextlib


def main():
    # +-----+ .11/24     .21/24 +-----+ .1/24       .2/24 +----+
    # | r11 |-------------------| r21 |-------------------| r2 |
    # +-----+  192.168.12.0/24  +-----+  172.16.12.0/24   +----+
    #    | .11/24                  | .21/24
    #    | 192.168.1.0/24          | 192.168.2.0/24
    #    | .12/24                  | .22/24
    # +-----+                   +-----+
    # | r12 |                   | r22 |
    # +-----+                   +-----+
    net = Mininet(controller=RemoteController, switch=mnextlib.FRRouting)

    r11 = net.addSwitch(
        'r11',
        confDir='~/mnextlib/example/frr/bgp_confed/r11',
    )
    r12 = net.addSwitch(
        'r12',
        confDir='~/mnextlib/example/frr/bgp_confed/r12',
    )
    r21 = net.addSwitch(
        'r21',
        confDir='~/mnextlib/example/frr/bgp_confed/r21',
    )
    r22 = net.addSwitch(
        'r22',
        confDir='~/mnextlib/example/frr/bgp_confed/r22',
    )
    r2 = net.addSwitch(
        'r2',
        confDir='~/mnextlib/example/frr/bgp_confed/r2',
    )

    net.addLink(r11, r21)
    net.addLink(r11, r12)
    net.addLink(r21, r22)
    net.addLink(r21, r2)

    net.start()
    CLI(net)
    net.stop()


if '__main__' == __name__:
    setLogLevel('info')
    main()

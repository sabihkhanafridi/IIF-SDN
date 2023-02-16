#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    cont=net.addController(name='cont',
                      controller=Controller,
                      protocol='tcp',
                      port=6634)

    RYU=net.addController(name='RYU',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    POX=net.addController(name='POX',
                      controller=Controller,
                      protocol='tcp',
                      port=6635)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    MN5 = net.addHost('MN5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    MN1 = net.addHost('MN1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    MN2 = net.addHost('MN2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    MN4 = net.addHost('MN4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    MN3 = net.addHost('MN3', cls=Host, ip='10.0.0.3', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s1, MN1)
    net.addLink(s1, MN2)
    net.addLink(s2, MN3)
    net.addLink(s2, MN4)
    net.addLink(s1, s3)
    net.addLink(s3, s2)
    net.addLink(s3, MN5)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([RYU])
    net.get('s2').start([POX])
    net.get('s3').start([cont])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

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
    c3=net.addController(name='c3',
                      controller=Controller,
                      protocol='tcp',
                      port=6636)

    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    c2=net.addController(name='c2',
                      controller=Controller,
                      protocol='tcp',
                      port=6635)

    c1=net.addController(name='c1',
                      controller=Controller,
                      protocol='tcp',
                      port=6634)

    info( '*** Add switches\n')
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)

    info( '*** Add links\n')
    h1s1 = {'bw':10,'delay':'1'}
    net.addLink(h1, s1, cls=TCLink , **h1s1)
    h5s2 = {'bw':10,'delay':'1'}
    net.addLink(h5, s2, cls=TCLink , **h5s2)
    h4s8 = {'bw':10,'delay':'1'}
    net.addLink(h4, s8, cls=TCLink , **h4s8)
    h6s10 = {'bw':10,'delay':'1'}
    net.addLink(h6, s10, cls=TCLink , **h6s10)
    net.addLink(h3, s5)
    h2s9 = {'bw':10,'delay':'1'}
    net.addLink(h2, s9, cls=TCLink , **h2s9)
    s10s6 = {'bw':10,'delay':'2'}
    net.addLink(s10, s6, cls=TCLink , **s10s6)
    s6s5 = {'bw':30,'delay':'4'}
    net.addLink(s6, s5, cls=TCLink , **s6s5)
    s5s4 = {'bw':30,'delay':'4'}
    net.addLink(s5, s4, cls=TCLink , **s5s4)
    s4s7 = {'bw':40,'delay':'8'}
    net.addLink(s4, s7, cls=TCLink , **s4s7)
    s7s3 = {'bw':30,'delay':'5'}
    net.addLink(s7, s3, cls=TCLink , **s7s3)
    s3s2 = {'bw':50,'delay':'1'}
    net.addLink(s3, s2, cls=TCLink , **s3s2)
    s2s1 = {'bw':15,'delay':'5'}
    net.addLink(s2, s1, cls=TCLink , **s2s1)
    s7s1 = {'bw':20,'delay':'3'}
    net.addLink(s7, s1, cls=TCLink , **s7s1)
    s4s9 = {'bw':20,'delay':'5'}
    net.addLink(s4, s9, cls=TCLink , **s4s9)
    s5s9 = {'bw':20,'delay':'6'}
    net.addLink(s5, s9, cls=TCLink , **s5s9)
    s3s8 = {'bw':10,'delay':'1'}
    net.addLink(s3, s8, cls=TCLink , **s3s8)
    s3s6 = {'bw':40,'delay':'10'}
    net.addLink(s3, s6, cls=TCLink , **s3s6)
    net.addLink(s9, s10)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s9').start([c2])
    net.get('s2').start([c3])
    net.get('s3').start([c3])
    net.get('s10').start([c2])
    net.get('s7').start([c1])
    net.get('s4').start([c1])
    net.get('s8').start([c3])
    net.get('s5').start([c0])
    net.get('s6').start([c0])
    net.get('s1').start([c1])
    for switch in net.switches:
    	switch.cmd("ovs-vsctl set bridge %s stp-enable=true" % (switch.name))
    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()


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
    c2=net.addController(name='c2',
                      controller=Controller,
                      protocol='tcp',
                      port=6635)

    c1=net.addController(name='c1',
                      controller=Controller,
                      protocol='tcp',
                      port=6634)

    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)

    info( '*** Add links\n')
    h7s7 = {'bw':15,'delay':'10','max_queue_size':15}
    net.addLink(h7, s7, cls=TCLink , **h7s7)
    h8s7 = {'bw':10,'delay':'5','max_queue_size':20}
    net.addLink(h8, s7, cls=TCLink , **h8s7)
    s7s5 = {'bw':12,'delay':'10','max_queue_size':40}
    net.addLink(s7, s5, cls=TCLink , **s7s5)
    s6s5 = {'bw':15,'delay':'10','max_queue_size':10}
    net.addLink(s6, s5, cls=TCLink , **s6s5)
    s5s4 = {'bw':30,'delay':'10','max_queue_size':30}
    net.addLink(s5, s4, cls=TCLink , **s5s4)
    s4s3 = {'bw':30,'delay':'10','max_queue_size':30}
    net.addLink(s4, s3, cls=TCLink , **s4s3)
    s3s2 = {'bw':20,'delay':'10','max_queue_size':5}
    net.addLink(s3, s2, cls=TCLink , **s3s2)
    s3s1 = {'bw':15,'delay':'10','max_queue_size':20}
    net.addLink(s3, s1, cls=TCLink , **s3s1)
    h1s1 = {'bw':10,'delay':'2','max_queue_size':20}
    net.addLink(h1, s1, cls=TCLink , **h1s1)
    h2s1 = {'bw':10,'delay':'1','max_queue_size':20}
    net.addLink(h2, s1, cls=TCLink , **h2s1)
    h3s2 = {'bw':10,'delay':'5','max_queue_size':10}
    net.addLink(h3, s2, cls=TCLink , **h3s2)
    h4s2 = {'bw':10,'delay':'10','max_queue_size':20}
    net.addLink(h4, s2, cls=TCLink , **h4s2)
    h5s6 = {'bw':10,'delay':'20','max_queue_size':30}
    net.addLink(h5, s6, cls=TCLink , **h5s6)
    h6s6 = {'bw':15,'delay':'2','max_queue_size':20}
    net.addLink(h6, s6, cls=TCLink , **h6s6)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s4').start([c2])
    net.get('s5').start([c1])
    net.get('s7').start([c1])
    net.get('s6').start([c1])
    net.get('s3').start([c0])

    info( '*** Post configure switches and hosts\n')
    print("Network has been set up successfully.")
    return net


def main():
    net = myNetwork()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    main()
    setLogLevel( 'info' )
    


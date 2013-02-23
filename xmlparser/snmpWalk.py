#!/usr/bin/python

##############
# File: snmpWalk.py
# Name: SNMP Walker
# Creator: D. Tyler Long
# Date: 01 Dec 2012
# Dependents: xmlRemake.py, xml.etree.ElementTree, math, netsnmp
# Running Operating System: Linux x86_64 or i686
# About: SNMP Walker is a closed system tool used to walk across specific MIBs
# inside an SNMP enabled device and grab the returned strings. During this walk
# this script takes the data and organizes the data in XML format.
# Note: xmlRemake is required for this script to run. Code commented out below
# is for testing purposes only. Also the NetSnmp Python bindings are located
# at http://www.net-snmp.org/ or downloaded via RPM using 'yum install net-snmp-*'.
##############

import math
import netsnmp, os
from xml.etree.ElementTree import Element, SubElement, Comment
from xmlRemake import organize

#print("SNMPWalk - All SNMP Devices\n\n")

#SNMP Data from Windows Host Machine
# Create SNMP Session to SNMP Agent
winSession = netsnmp.Session(DestHost='192.168.4.50', Version=1, Community='public')
# Compile SNMP requests to VarList
winVars = netsnmp.VarList(netsnmp.Varbind('sysName', '0'), 
                          netsnmp.Varbind('sysContact', '0'), 
                          netsnmp.Varbind('sysLocation','0'), 
                          netsnmp.Varbind('sysDescr', '0'),
                          netsnmp.Varbind('hrDeviceDescr', '3'), 
                          netsnmp.Varbind('hrStorageDescr', '1'),
                          netsnmp.Varbind('hrStorageSize', '1'), 
                          netsnmp.Varbind('hrMemorySize', '0'), 
                          netsnmp.Varbind('hrSystemUptime', '0'),
                          netsnmp.Varbind('hrSystemProcesses', '0'))
winA = winSession.get(winVars)

#SNMP Data from Linux Virtual Machine
# Create SNMP Session to SNMP Agent
linuxSessionA = netsnmp.Session(DestHost='192.168.4.51', Version=1, Community='public')
# Compile SNMP requests to VarList
linuxVarsA = netsnmp.VarList(netsnmp.Varbind('sysName', '0'), 
                             netsnmp.Varbind('sysContact', '0'), 
                             netsnmp.Varbind('sysLocation','0'), 
                             netsnmp.Varbind('sysDescr', '0'),
                             netsnmp.Varbind('hrDeviceDescr', '768'), 
                             netsnmp.Varbind('hrStorageDescr', '31'),
                             netsnmp.Varbind('hrStorageSize', '10'), 
                             netsnmp.Varbind('hrMemorySize', '0'),
                             netsnmp.Varbind('hrSystemUptime', '0'),
                             netsnmp.Varbind('hrSystemProcesses', '0'))
linuxA = linuxSessionA.get(linuxVarsA)

#SNMP Data from Agent1 Virtual Machine
# Create SNMP Session to SNMP Agent
linuxSessionB = netsnmp.Session(DestHost='192.168.4.52', Version=1, Community='public')
# Compile SNMP requests to VarList
linuxVarsB = netsnmp.VarList(netsnmp.Varbind('sysName', '0'), 
                             netsnmp.Varbind('sysContact', '0'), 
                             netsnmp.Varbind('sysLocation','0'), 
                             netsnmp.Varbind('sysDescr', '0'),
                             netsnmp.Varbind('hrDeviceDescr', '768'),
                             netsnmp.Varbind('hrStorageDescr', '31'),#
                             netsnmp.Varbind('hrStorageSize', '10'),#
                             netsnmp.Varbind('hrMemorySize', '0'),
                             netsnmp.Varbind('hrSystemUptime', '0'),
                             netsnmp.Varbind('hrSystemProcesses', '0'))
linuxB = linuxSessionB.get(linuxVarsB)
# Top element of the created XML document
top = Element('SNMPWalk')
comment = Comment('Generated by Ty Long')

# SNMP Agent # 1
snmpAgent = SubElement(top, 'SNMPAgent', attrb="1")
windowsAgent = SubElement(snmpAgent, 'OperatingSystem')
windowsAgent.text = 'Windows 7'
winSysName = SubElement(snmpAgent, 'SystemName')
winSysName.text = winA[0]
winSysContact = SubElement(snmpAgent, 'SystemContact')
winSysContact.text = winA[1]
winSysType = SubElement(snmpAgent, 'SystemType')
winSysType.text = winA[2]
winSysDesc = SubElement(snmpAgent, 'SystemDesc')
winSysDesc.text = winA[3][10:]
winSysProcessor = SubElement(snmpAgent, 'SystemProcessor')
winSysProcessor.text = winA[4]
winSysDrive = SubElement(snmpAgent, 'SystemDrive')
winSysDrive.text = winA[5][0:-24]
# 1049 MB per GB to be more accurate than 1024 MB when using HDD allocation
sizeInt = int(math.ceil(float(winA[6])/104900))
winSysDriveSize = SubElement(snmpAgent, 'SystemDriveSize')
winSysDriveSize.text = str(sizeInt) + " GB"
sizeInt = int(math.ceil(float(winA[7])/1049000))
winSysMemory = SubElement(snmpAgent, 'SystemMemory')
winSysMemory.text = str(sizeInt) + " GB"
winSysUptime = SubElement(snmpAgent, 'SystemUptime')
winSysUptime.text = winA[8]
winSysProcesses = SubElement(snmpAgent, 'SystemProcesses')
winSysProcesses.text = winA[9]

# SNMP Agent # 2
snmpAgent = SubElement(top, 'SNMPAgent', attrb="2")
linux1Agent = SubElement(snmpAgent, 'OperatingSystem')
linux1Agent.text = 'CentOS 6.3 GNOME x86_64'
linux1SysName = SubElement(snmpAgent, 'SystemName')
linux1SysName.text = linuxA[0]
linux1SysContact = SubElement(snmpAgent, 'SystemContact')
linux1SysContact.text = linuxA[1]
linux1SysType = SubElement(snmpAgent, 'SystemType')
linux1SysType.text = linuxA[2]
linux1SysDesc = SubElement(snmpAgent, 'SystemDesc')
linux1SysDesc.text = linuxA[3][0:-42]
linux1SysProcessor = SubElement(snmpAgent, 'SystemProcessor')
linux1SysProcessor.text = linuxA[4]
linux1SysDrive = SubElement(snmpAgent, 'SystemDrive')
linux1SysDrive.text = linuxA[5]
# 1049 MB per GB to be more accurate than 1024 MB when using HDD allocation
sizeInt = int(math.ceil(float(linuxA[6])/104900))
linux1SysDriveSize = SubElement(snmpAgent, 'SystemDriveSize')
linux1SysDriveSize.text = str(sizeInt) + " GB"
sizeInt = int(math.ceil(float(linuxA[7])/1049000))
linux1SysMemory = SubElement(snmpAgent, 'SystemMemory')
linux1SysMemory.text = str(sizeInt) + " GB"
linux1SysUptime = SubElement(snmpAgent, 'SystemUptime')
linux1SysUptime.text = linuxA[8]
linux1SysProcesses = SubElement(snmpAgent, 'SystemProcesses')
linux1SysProcesses.text = linuxA[9]

# SNMP Agent # 3
snmpAgent = SubElement(top, 'SNMPAgent', attrb="3")
linux2Agent = SubElement(snmpAgent, 'OperatingSystem')
linux2Agent.text = 'Fedora 17 XFCE x86_64'
linux2SysName = SubElement(snmpAgent, 'SystemName')
linux2SysName.text = linuxB[0]
linux2SysContact = SubElement(snmpAgent, 'SystemContact')
linux2SysContact.text = linuxB[1]
linux2SysType = SubElement(snmpAgent, 'SystemType')
linux2SysType.text = linuxB[2]
linux2SysDesc = SubElement(snmpAgent, 'SystemDesc')
linux2SysDesc.text = linuxB[3][0:-43]
linux2SysProcessor = SubElement(snmpAgent, 'SystemProcessor')
linux2SysProcessor.text = linuxB[4]
linux2SysDrive = SubElement(snmpAgent, 'SystemDrive')
linux2SysDrive.text = linuxB[5]
# 1049 MB per GB to be more accurate than 1024 MB when using HDD allocation
sizeInt = int(math.ceil(float(linuxB[6])/104900))
linux2SysDriveSize = SubElement(snmpAgent, 'SystemDriveSize')
linux2SysDriveSize.text = str(sizeInt) + " GB"
sizeInt = int(math.ceil(float(linuxB[7])/1049000))
linux2SysMemory = SubElement(snmpAgent, 'SystemMemory')
linux2SysMemory.text = str(sizeInt) + " GB"
linux2SysUptime = SubElement(snmpAgent, 'SystemUptime')
linux2SysUptime.text = linuxB[8]
linux2SysProcesses = SubElement(snmpAgent, 'SystemProcesses')
linux2SysProcesses.text = linuxB[9]

# Write data and close out the file
f = open('snmpData.xml', 'w')
f.write(organize(top))
f.close()

# Print out code. For testing purposes only.
'''
print os.getcwd()
print("System Name: " + winA[0])
print("System Contact: " + winA[1])
print("System Type: " + winA[2])
#Windows a[3][10:] Removes "Hardware:" tag.
print("System Desc.: " + winA[3][10:])
print("System Processor: " + winA[4])
#Remove "Serial Number" from HDD print out
print("System Drive: " + winA[5][0:-24])
# 1049 MB per GB to be more accurate than 1024 MB when using HDD allocation
sizeInt = int(math.ceil(float(winA[6])/104900))
print("System Size: " + str(sizeInt) + " GB")
sizeInt = int(math.ceil(float(winA[7])/104900))
print("System Used: " + str(sizeInt) + " GB")
sizeInt = int(math.ceil(float(winA[8])/1049000))
print("System Memory: " + str(sizeInt) + " GB")
print("System Uptime in Seconds: " + winA[9])
print("System Processes: " + winA[10])

print

print("System Name: " + linuxA[0])
print("System Contact: " + linuxA[1])
print("System Type: " + linuxA[2])
print("System Desc.: " + linuxA[3][0:-42])
print("System Processor: " + linuxA[4])
#Remove "Serial Number" from HDD print out
print("System Drive: " + linuxA[5])
# 1049e+6 KB per GB to be more accurate than 1024 KB when using HDD allocation
sizeInt = int(math.ceil(float(linuxA[6])/104900))
print("System Size: " + str(sizeInt) + " GB")
sizeInt = int(math.ceil(float(linuxA[7])/1049000))
print("System Memory: " + str(sizeInt) + " GB")
print("System Network Device: " + linuxA[8])
# Device is transmitted as an integer
if linuxA[9] == '2':
    a = "Up"
else:
    a = "Down"
print("Network Device Status: " + a)  
print("System Uptime in Seconds: " + linuxA[10])
print("System Processes: " + linuxA[11])

print 

print("System Name: " + linuxB[0])
print("System Contact: " + linuxB[1])
print("System Type: " + linuxB[2])
print("System Desc.: " + linuxB[3][0:-43])
print("System Processor: " + linuxB[4])
sizeInt = int(math.ceil(float(linuxB[5])/1049000))
print("System Memory: " + str(sizeInt) + " GB")
print("System Network Device: " + linuxB[6])
# Device is transmitted as an integer
if linuxB[7] == '2':
    a = "Up"
else:
    a = "Down"
print("Network Device Status: " + a)
print("System Uptime in Seconds: " + linuxB[8])
print("System Processes: " + linuxB[9])
'''
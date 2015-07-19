import os
import sys
import io
import base64
import subprocess

keylist = [
    'HostName',
    'IP',
    'Score',
    'Ping',
    'Speed',
    'CountryLong',
    'CountryShort',
    'NumVpnSessions',
    'Uptime',
    'TotalUsers',
    'TotalTraffic',
    'LogType',
    'Operator',
    'Message',
    'OpenVPN_ConfigData_Base64',
]
option_list = {1: keylist[1], 6: keylist[6], 7: keylist[7]}


def main():
  if (input("Refresh:") == 'r'):
    subprocess.Popen(
        "wget http://www.vpngate.net/api/iphone/ -O ./temp/vpngate.csv ", shell=True).wait()
  file = open('./temp/vpngate.csv', 'r')

  List = datatoList(file)

  file.close()

  Servers = InterpretList(List)

  generate_files(Servers)

  Theone = Choose_openvpn(Servers)


def datatoList(file):
  List = []
  while (True):
    line = file.readline()
    if not line:
      break
    List.append(line)
  return List
spam = ['*', '*vpn_servers', '#HostName']


def InterpretList(List):
  Servers = []
  for line in List:
    args = line.split(',')
    if len(args) >= 10:
      Server = {}
      for i in range(0, 15):

        Server[keylist[i]] = args[i]
      Servers.append(Server)
  if(Servers):
    Servers.remove(Servers[0])
  return Servers


def generate_files(Servers):
  for Server in Servers:
    file = open(
        './temp/{0}_{1}.ovpn'.format(Server['IP'], Server['CountryShort']), 'w')
    if file:
      data = base64.b64decode(Server['OpenVPN_ConfigData_Base64'])
      data = str(data)
      data = data.replace(r'\'','\'')
      data = data.replace(r'\r','\r')
      data = data.replace(r'\n','\n')
      if data.endswith('\'') and data.startswith('b\''):
        data = data[2:-1]
      file.writelines(data)
      file.close()


def Choose_openvpn(Servers):
  CountryShorts = []
  print('Countrys ',  end=': ')
  for server in Servers:
    try:
      CountryShorts.index(server['CountryShort'])
    except Exception as e:
      CountryShorts.append(server['CountryShort'])
      print(server['CountryShort'],  end=' ')
  limits = ''

  limits = input("\nCountry limits? : ")
  tmp_Servers = []
  for server in Servers:
    CountryShort = server['CountryShort']
    bool_ = False
    for limit in limits.split(','):
      limit = limit.upper()
      if limit == CountryShort:
        bool_ = True
    if (bool_):
      tmp_Servers.append(server)
  Servers = tmp_Servers

  i = 0
  for Server in Servers:
    print(
        str(i) + ' \tIP:{0}   \t Country:{1}\tScore:{2}'.format(Server['IP'], Server['CountryShort'],Server['Score']))
    i += 1
  i = input("Which one:")
  subprocess.Popen('sudo openvpn ./temp/{0}_{1}.ovpn'.format(
      Servers[int(i)]['IP'], Servers[int(i)]['CountryShort']), shell=True)
if __name__ == '__main__':
  main()

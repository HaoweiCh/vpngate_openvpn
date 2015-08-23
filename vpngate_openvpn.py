import os,sys
import base64
import subprocess
import urllib

class vpngate:

	def __init__(self, mirrors=[],proxy='127.0.0.1:8787'):
		self.url = '';self.proxy=''
		url = 'http://www.vpngate.net/'
		if ping_website(url):
			self.url = url
		elif proxy !='' and  ping_website(url,proxy):
			self.url = url
			self.proxy = proxy
		else:

			try:
				i =0
				while self.url=='':
					mirror = mirrors[i]
					if ping_website(mirror):
						self.url = mirror
					elif proxy !='' and  ping_website(mirror,proxy):
						self.url = mirror
						self.proxy = proxy
					i+=1
			except:
				sys.stderr.write('No usable mirror\n')
				sys.exit(-1)




		self.dir_temp = './temp/'
		if not os.path.isdir(self.dir_temp): os.makedirs(self.dir_temp)

		self.keylist = \
		"HostName,IP,Score,Ping,Speed,CountryLong,CountryShort,NumVpnSessions," \
		"Uptime,TotalUsers,TotalTraffic,LogType,Operator,Message,OpenVPN_ConfigData_Base64".split(',')
		self.option_list = {1: self.keylist[1], 6: self.keylist[6], 7: self.keylist[7]}

		self.servers=[];self.servers_ip=[];self.read_servers()
		return
	def read_servers(self):
		pass
	def write_servers(self):
		pass
	def update_CSV(self, url=''):
		if url == '' :url = self.url
		url += 'api/iphone/'
		#todo ...

		if self.proxy!='':
			proxy_support = urllib.request.ProxyHandler({"http":"http://%s"%self.proxy})
			opener = urllib.request.build_opener(proxy_support)
			urllib.request.install_opener(opener)

		response = urllib.request.urlopen(url);
		data = response.read()
		file = open(self.dir_temp + 'vpngate.csv', 'wb')
		file.write(data)
		return not not file
	def update_servers(self):
		file = open(self.dir_temp + 'vpngate.csv', 'rb')
		document = file.read().decode('utf-8')
		List = document.split('\n')
		List.pop(0);List.pop(0);List.pop(-1);List.pop(-1)

		servers=[];servers_ip=[]
		for List_f in List:
			List_f.split(',')
			server={}
			for i in range(0,15):
				server[self.keylist[i]]=List_f[i]
				servers.append(server)
				servers_ip.append(server['IP'])

		if len(self.servers_ip)==0:
			self.servers=servers;self.servers_ip=servers_ip
		else:
			for i in range(0,len(self.servers_ip)):
				try:
					self.servers_ip.index(self.servers_ip[i])
				except :
					self.servers.append(servers[i])
					self.servers_ip.append(servers_ip[i])

		file.close()
		self.write_servers()
		return
	def write_server(self,Server):
		file = open(self.dir_temp+'{0}_{1}.ovpn'.format(Server['IP'], Server['CountryShort']), 'w')
		if file:
			data = base64.b64decode(Server['OpenVPN_ConfigData_Base64'])
			data = str(data).replace(r'\'', '\'').replace(r'\r', '\r').replace(r'\n', '\n')[2:-1]
			file.write(data)
		return
	def generate_files(self):
		for server in self.servers:
			file = open('./temp/{0}_{1}.ovpn'.format(server['IP'], server['CountryShort']), 'w')
			if file:
				self.write_servers(server)

def ping_ip(ip='127.0.0.1'):
	response = subprocess.getoutput('ping ' + ip);  # print( type(response))
	response = response.strip()
	response = response.split('\n')[-1].strip()
	args = response.split(',')
	for arg in args:
		args[0] = (arg.split('=')[-1][:-2])
	if args[0] == '':
		return False
	else:
		return True
def ping_website(url='http://www.baidu.com/',proxy=''):
	if proxy!='':
			proxy_support = urllib.request.ProxyHandler({"http":"http://%s"%proxy})
			opener = urllib.request.build_opener(proxy_support)
			urllib.request.install_opener(opener)
	try:
		response = urllib.request.urlopen(url)
		return response.code == 200
	except:
		return False

def Choose_openvpn(Servers):
	CountryShorts = []
	# print('Countrys ',  end=': ')
	for server in Servers:
		try:
			CountryShorts.index(server['CountryShort'])
		except Exception as e:
			CountryShorts.append(server['CountryShort'])
		# print(server['CountryShort'],  end=' ')
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
			str(i) + ' \tIP:{0}   \t Country:{1}\tScore:{2}'.format(Server['IP'], Server['CountryShort'], Server['Score']))
		i += 1
	i = input("Which one:")
	subprocess.Popen('sudo openvpn ./temp/{0}_{1}.ovpn'.format(
		Servers[int(i)]['IP'], Servers[int(i)]['CountryShort']), shell=True)
def main():
	ping_website()
	v = vpngate()
	v.update_CSV()
	v.servers_ip
	return

if __name__ == '__main__':
	sys.path.append(r'C:\Python34\Lib')
	main()

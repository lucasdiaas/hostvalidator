import sys
import chilkat #Módulo de conexão SSH
import csv     #Módulo para ler e escrever aquivos CSV


#Abrir e ler aquivo.csv
with open('importar.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=';',quotechar='|')

	#Vetores para armazenar os dados necessários
	ips = []
	users = []
	pwds = []
	hostnames = []
	for row in spamreader:

		ip = row[3]
		user = row[4]
		pwd = row[5]
		hostname = row[0]

		ips.append(ip)
		users.append(user)
		pwds.append(pwd)
		hostnames.append(hostname)

#Conexão SSH

ssh = chilkat.CkSsh()

success = ssh.UnlockComponent("Anything for 30-day trial")

if (success != True):
	print(ssh.lastErrorText())
	print("unlock failed")

print(ssh.lastErrorText())
print("unlock successful")

port = 22

i = 0
NotCon = []	
NotAuth = []

for x in range(len(ips)):

	print("----------------------------------------")
	print(hostnames[i])
	print(ips[i])
	print(users[i])


	#Time out de 2s para conexão com o host
	intVal = ssh.get_ConnectTimeoutMs();
	ssh.put_ConnectTimeoutMs(2000);				

	#Conectar ao Host
	success = ssh.Connect(ips[i],port)			
	if (success == True):
		print("Connected")

		#Autenticar com Usuário e Senha
		succs = ssh.AuthenticatePw(users[i],pwds[i])	
		if (succs == True):
			print("Authenticated")
		else:
			print("Wrong Password")
			#Vetor que irá armazenar os hosts que não conseguiu autenticar
			NotAuth.append(hostnames[i])
	else:
		print("Could not Connect")

		#Vetor que irá armazenar os hosts que não conseguiu se conectar
		NotCon.append(hostnames[i])

	i = i+1

# Abre o arquivo que ia conter os hosts que não foi aberta a conexão
resultFyle = open("notCon.csv",'w')

# Cria o objeto e escreve os dados no arquivo
wr = csv.writer(resultFyle, dialect='excel')
for item in NotCon:
    wr.writerow([item,])

# Abre o arquivo que ia conter os hosts que não foi aberta a conexão
resultFyle = open("notAuth.csv",'w')

# Cria o objeto e escreve os dados no arquivo
wr = csv.writer(resultFyle, dialect='excel')
for item in NotAuth:
    wr.writerow([item,])
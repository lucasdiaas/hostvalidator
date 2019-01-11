import sys
import os
import json
import csv
import chilkat

nome_arquivo = 'hosts.csv'


with open(nome_arquivo, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')

    hostnames = []

    for row in spamreader:
        hostname = row[0]

        hostnames.append(hostname)

c = 0

6#Vetor para armazenar os hosts em que a autenticação falhou
notCon = []
notAuth = []

for x in range(len(hostnames)):

    os.system("php api2.php -p" + hostnames[c] + " > res.json")

    fp = open("res.json", "r")

    obj = json.load(fp)

    fp.close()


    i = 0

    print('\n')
    print('---------------------------')

    for x in range(len(obj['result'])):

        idServer = (obj['result'][i]['account_id'])
        hostname = (obj['result'][i]['account_name'])
        user = (obj['result'][i]['account_login'])

        print('\n')
        print(hostname)
        print(user)
        print('\n')

        os.system("php getPwd.php -p" + idServer + " > pwd.json")

        fp = open("pwd.json", "r")

        array = json.load(fp)

        fp.close()

        password = (array['result']['pass'])

        #Conexão SSH

        ssh = chilkat.CkSsh()
        success = ssh.UnlockComponent("Anything for 30-day trial")

        port = 22

        intVal = ssh.get_ConnectTimeoutMs()
        ssh.put_ConnectTimeoutMs(2000)

        success = ssh.Connect(hostname, port)

        if (success == True):
            print("Connected")

            #Autenticar usuário e senha
            succs = ssh.AuthenticatePw(user, password)

            if(succs == True):
                print("Authenticated")
            else:
                print("Wrong Password")

                #Adicionar esse hostname ao vetor
                notAuth.append(hostname)
        else:
            print("Could not Connect")

            #Adicionar esse hostname ao vetor
            notCon.append(hostname)

        i = i + 1

    print('---------------------------')

    c = c + 1

os.system("rm res.json")

os.system("rm pwd.json")

#Remove nomes duplicados no vetor
notCon = list(set(notCon))

#Remove nomes duplicados no vetor
notAuth = list(set(notAuth))

#Abre o arquivo que irá conter os hosts em que a conexão falhou
resultFyle = open("notCon.csv", 'w')

#Cria o objeto e escreve os dados no arquivo

wr = csv.writer(resultFyle, dialect='excel')
for item in notCon:
    wr.writerow([item,])

#Abre o arquivo que irá conter os hosts em que a autenticação falhou
resultFyle = open("notAuth.csv", 'w')

#Cria o objeto e escreve os dados no arquivo

wr = csv.writer(resultFyle, dialect='excel')
for item in notAuth:
    wr.writerow([item,])

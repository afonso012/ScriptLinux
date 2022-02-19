from os import system as s

apti = "apt install -y "
Ans = "null"

s("cd /")
#s("cd /LinuxServices/")

while (Ans != "s"):
    s("clear")
    IpMaquina = input("Introduzir ip da maquina: ")
    s("clear")
    DefGateway = input("Introduzir ip Default Gateway: ")
    s("clear")
    Dns = input("Introduzir ip DNS: ")
    s("clear")
    Dominio = input("Introduzir nome Dominio: ")
    s("clear")
    Range = input("Introduzir Range de ip's  \n  Exemplo: <192.168.50.5 192.168.50.35>")
    s("clear")
    NomeMaquina = input("Introduzir Nome da maquina (root@<nome_aqui>): ")
    s("clear")
    print("IP da maquina: " + IpMaquina)
    print("Default Gateway: " + DefGateway)
    print("DNS: " + Dns)
    print("Dominio: " + Dominio)
    print("Range: " + Range)
    print("Nome da maquina: " + NomeMaquina)
    print()
    print("Esta informacao está correta?      s/n")
    Ans = input()

s("ip link set enp0s3 up")
s("ip link set enp0s8 down")
s("apt update && apt upgrade -y")
for i in ["isc-dhcp-server", "bind9", ]: #services to install
    s(apti + i)

Ip = IpMaquina.split(".")
IpRede = ""
for i in Ip:
    if i == Ip[3]:
        IpRede += "0"
    else:
        IpRede += i + "."

IpRedeArpa = ""
for i in [Ip[2], Ip[1], Ip[0], "in-addr.arpa"]:
    IpRedeArpa += i
    if i != "in-addr.arpa":
        IpRedeArpa += "."

file = "00-installer-config.yaml"
fin = open(file, "rt")
data = fin.read()
data = data.replace("ipmaquina", IpMaquina)
data = data.replace("defgate", DefGateway)
fin.close()
fin = open(file, "wt")
fin.write(data)
fin.close()

s("mv 00-installer-config.yaml /etc/netplan/")
s("netplan apply")

file = "dhcpd.conf"
fin = open(file, "rt")
data = fin.read()
data = data.replace("dominio", Dominio)
data = data.replace("defgate", DefGateway)
data = data.replace("iprede", IpRede)
data = data.replace("rangedeips", Range)
fin.close()
fin = open(file, "wt")
fin.write(data)
fin.close()

s("mv dhcpd.conf /etc/dhcp/")
s("mv isc-dhcp-server /etc/default/")

s("service isc-dhcp-server restart")



#bind9
file = "named.conf.local"
fin = open(file, "rt")
data = fin.read()
data = data.replace("dominio", Dominio)
data = data.replace("ipdaarpa", IpRedeArpa)
fin.close()
fin = open(file, "wt")
fin.write(data)
fin.close()

s("mv named.conf.local /etc/bind/")

file = "forward.terceiradose.pt"
fin = open(file, "rt")
data = fin.read()
data = data.replace("dominio", Dominio)
data = data.replace("nomedamaquina", NomeMaquina)
data = data.replace("defgate", DefGateway)
fin.close()
fin = open(file, "wt")
fin.write(data)
fin.close()

s("mv forward.terceiradose.pt forward." + Dominio)
s("mv forward." + Dominio + " /etc/bind/")

file = "reverse.terceiradose.pt"
fin = open(file, "rt")
data = fin.read()
data = data.replace("dominio", Dominio)
data = data.replace("nomedamaquina", NomeMaquina)
data = data.replace("defgate", DefGateway)
fin.close()
fin = open(file, "wt")
fin.write(data)
fin.close()

s("mv reverse.terceiradose.pt reverse." + Dominio)
s("mv reverse." + Dominio + " /etc/bind/")

s("service bind9 restart")

s("ip link set enp0s3 down")
s("ip link set enp0s8 up")


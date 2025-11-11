import os
import shutil
import subprocess


def main():
    tekst = ""
    tekst += operativtSystemet() + "\n"
    tekst += lagringsplass() + "\n"
    tekst += bruker() + "\n"
    tekst += ipFinder() + "\n"
    tekst += instalertProgramvare() 
    
    skrivTilTekstFil(tekst)
  


def operativtSystemet():
    match os.name:
        case "nt":
            operativsystem = "Windows"
        case "posix":
            operativsystem = "Linux"
        case "java":
            operativsystem = "Java"

    try:
        versjon = os.popen("ver").read().strip()
    except:
        versjon = "ikke tilgjengelig"
    fullTekst = f"operativ systemet er {operativsystem}\nversjonen er {versjon}"
    print(fullTekst)
    return fullTekst

def lagringsplass():
    total, brukt, ledig = shutil.disk_usage("/")
    fullTeskt = f"Total lagringsplass: {total/1_000_000_000:.2f} GB\nBrukte lagringsplass: {brukt/1_000_000_000:.2f} GB\nLedig lagringsplass: {ledig/1_000_000_000:.2f} GB"
    print(fullTeskt)
    return fullTeskt


def bruker():
    brukerNavn = os.getlogin()
    print("Brukeren pa maskinen er:",brukerNavn)
    return "Brukeren pa maskinen er:" + brukerNavn

def ipFinder():
    if os.name == "nt":
        os.system("ipconfig > ipconfig.txt")
        ip = open("ipconfig.txt","r").read()
        ip = ip.split("\n")
        for a in ip:
            if a.strip().startswith("IPv4"):
                print(a.strip())
                return a.strip()
    elif os.name == "posix":
        ip = subprocess.getoutput("ip a").split("\n")
        for a in ip:
            if a.strip().startswith("inet"):
                print(a.split(" ")[1])
                return a.split(" ")[1]
            



def instalertProgramvare():
    print("Instalerte programmer på systemet:")
    if os.name == "nt":
        cmd='winget list product get name'
        resultat= subprocess.getoutput(cmd)
        print(resultat)
    else:
        cmd = 'dpkg --list'
        resultat = subprocess.getoutput(cmd)
        print(resultat)
    
    return resultat



def skrivTilTekstFil(data):
    with open("c:\\maskin\\maskinvareConf.txt","w") as maskinvareSkriver:
        maskinvareSkriver.write(data)
    print("alt er nå i en tekst fil")
    return
        

    


main()
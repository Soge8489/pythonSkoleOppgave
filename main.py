import os
import shutil

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
    print ("operativ systemet er", operativsystem)
    print ("versjonen er", versjon)
    return

def lagringsplass():
    total, brukt, ledig = shutil.disk_usage("/")
    print(f"Total lagringsplass: {total/1_000_000_000:.2f} GB")
    print(f"Brukte lagringsplass: {brukt/1_000_000_000:.2f} GB")
    print(f"Ledig lagringsplass: {ledig/1_000_000_000:.2f} GB")
    return


def bruker():
    brukerNavn = os.getlogin()
    print ("Brukeren på maskinen er:",brukerNavn)
    return

def ipFinder():
    ip = os.popen

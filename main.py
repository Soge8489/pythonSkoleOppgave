import os as operativsystem
#def listAvFilerOgMapper():
    #standardMappe = operativsystem.getcwd()
    #List = operativsystem.listdir() 
    #return List
#print(listAvFilerOgMapper())

#def lagMappeogslett(fillnavn):
    #operativsystem.mkdir(fillnavn)
    #if fillnavn in operativsystem.listdir():
        #print("fill finnes")
   # operativsystem.rmdir(fillnavn)

#lagMappeogslett("Test mappe")

#def underMappeFinner():
    #for i in operativsystem.listdir():
        #fillMapppe =  f"{operativsystem.getcwd()}/{i}"
        #if operativsystem.path.isdir(fillMapppe):
            #print (f"{fillMapppe} {operativsystem.listdir(fillMapppe)}")

#underMappeFinner()

def fillMedtxtTeller():
    antall =0
    for i in operativsystem.listdir():
        if i.endswith(".txt"):
            print (i)
            antall += 1
    print ("det finnes",antall,"filler")
fillMedtxtTeller()

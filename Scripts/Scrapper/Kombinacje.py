from random import randint

index =545
atribute = "Czas trwania:select:1"
combination = ["1h:1", "2h:2", "5h:3", "10h:5", "tygodniowy:4"]
with open('combinations.csv', mode='a+', newline='', encoding='utf-8') as combinationsFile:
    for i in range(index):
        if randint(0, 10) < 3:
            combinationsFile.write(str(i)+";"+atribute+";"+combination[0]+";"+str(1)+";"+"9999999"+'\n')
            combinationsFile.write(str(i)+";"+atribute+";"+combination[randint(1,len(combination)-1)]+";"+str(1)+";"+"9999999"+'\n')
        else:
            combinationsFile.write(str(i)+";"+atribute+";"+combination[0]+";"+str(1)+";"+"9999999"+'\n')

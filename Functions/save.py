from BDD.models import Personne


def save():
    
    personnes=Personne.objects.all()
    file = open("C:/Users/kentin/Desktop/Projet/test2.txt", "w")
    for p in personnes:
        p.user.last_name
        p.user.first_name
        p.user.email
        p.sexe
        p.adresse
        file.write(str(p.user.last_name) + ";;;" + str(p.user.first_name) + ";;;" + str(p.user.email) + ";;;" + str(p.sexe) + ";;;" + p.adresse + "!!!\n")
    file.close()
import pandas as pd
import numpy as np

data = pd.read_csv('logs.csv')

def long_plsc(l1,l2):
    """Renvoie un tableau permettant de trouver la plus longue sous-séquence commune aux listes de mots l1 et l2"""
    m,n = len(l1),len(l2)
    c = np.zeros((m+1,n+1)) # c[i, j] : longueur de la plus longue sous-séquence commune à l1[:i] et l2[:j]
    b = np.zeros((m+1,n+1)) # b[i,j] : permet de se souvenir d'où on est venu dans le tableau pour trouver la valeur c[i,j]
    #avec '1' : vient d'en haut à gauche, '2' : vient du haut, '3' : vient de la gauche
    for i in range(1,m+1):
        for j in range(1,n+1):
            if l1[i-1]==l2[j-1]:
                c[i,j] = c[i-1, j-1] + 1
                b[i,j] = 1
            elif c[i-1, j] >= c[i, j-1]:
                c[i,j] = c[i-1, j]
                b[i,j] = 2
            else:
                c[i,j] = c[i,j-1]
                b[i,j] = 3
    return b

def plsc(memo, l1, i, j):
    "Renvoie la liste des indices de la plus longue sous-séquence commune à l1 et l2"
    if i ==0 or j == 0 :
        return []
    if memo[i,j] == 1:
        return(plsc(memo, l1, i-1, j-1)+[(i-1,j-1)])
    elif memo[i,j]== 2:
        return(plsc (memo, l1, i-1,j))
    else:
        return(plsc(memo,l1,i,j-1))

def differences(s1,s2):
    """Renvoie la liste des couples (mistake, correction)  des chaines de caractères s1 et s2"""
    l1, l2 = [" "] + s1.split() + [" "],[" "] + s2.split() + [" "]
    b = long_plsc(l1,l2)
    indices = plsc(b,l1,len(l1),len(l2))
    derivee = [(indices[i+1][0]-indices[i][0],indices[i+1][1]-indices[i][1]) for i in range (len(indices) - 1) ] #dérivée discrète, permet de savoir de combien on avance pour avoir la plus longue sous-séquence commune
    res = []
    j1,j2 = indices[0]
    k = 0
    j1+=1
    j2+=1
    while j1 < len(l1) and j2 < len(l2) and k < len(indices) -1:
        if (j1,j2) == indices[k+1]:
            j1 += 1
            j2 += 1
            k += 1
        else:
            if derivee[k] == (2,2): #cas d'une substitution de mots
                k += 1
                res.append((l1[j1], l2[j2]))
                j1 +=2
                j2 +=2
            elif derivee[k] == (2,1): #un mot supprimé dans l1
                erreur = l1[j1-1] + " " + l1[j1]+ " " + l1[j1+1]
                corr = l2[j2 -1] + " " + l2[j2]
                res.append((erreur, corr))
                k += 1 
                j1 += 2
                j2 += 1
            elif derivee[k] == (1,2): # un mot ajouté dans l2
                erreur = l1[j1 -1] + " " + l1[j1]
                corr = l2[j2-1] + " " + l2[j2]+ " " + l2[j2+1]
                res.append((erreur, corr))
                k += 1 
                j1 += 1
                j2 += 2
            else: #si jamais il y a une suppression/trou de plus d'un mot  on généralise cette approche
                erreur =""
                j1 -= 1
                while j1 <= indices[k+1][0]:
                    erreur += " " + l1[j1]
                    j1 += 1
                corr = ""
                j2 -= 1
                while j2 <= indices[k+1][1]:
                    corr += " " + l2[j2]
                    j2 += 1
                    
                k += 1
                res.append((erreur.strip(), corr.strip()))
    return res

lin, col = data.shape
dico = {"input_id" : [], "mistake" : [], "correction":[]}


for i in range(1, lin):
    s1, s2 = data['initial_text'][i], data['corrected_text'][i]
    id_i = data['id'][i]
    res = differences(s1,s2)
    for couple in res:
        dico['input_id'].append(id_i)
        dico['mistake'].append(couple[0])
        dico['correction'].append(couple[1])
df = pd.DataFrame(dico)

df.to_csv('mistakes.csv')
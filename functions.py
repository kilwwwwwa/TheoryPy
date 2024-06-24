
class Graph:
    def __init__(self, n):
        self.matAdj = [[0] * n for _ in range(n)]
        self.nbrSommets = n

    def ajouterArrete(self, u, v,poids):
        self.matAdj[u][v] = poids
        self.matAdj[v][u] = poids
    def EnleverArrete(self, u, v):
        self.matAdj[u][v] = 0
        self.matAdj[v][u] = 0

    def ajouterSommet(self):
        for row in self.matAdj:
            row.append(0)
        self.nbrSommets += 1
        self.matAdj.append([0] * self.nbrSommets)

    def EnleverSommet(self, v):
        del self.matAdj[v]
        for row in self.matAdj:
            del row[v]
        self.nbrSommets -= 1

    def afficherAdjMat(self):
        if self.nbrSommets == 0:
            print("Matrice est vide")
        else:
            for rowNbr in range(self.nbrSommets):
                print(" ",rowNbr, end=" ")
            print()    
            for i in range(self.nbrSommets):
                print(i, end=" ")
                for j in range(self.nbrSommets):
                    print(self.matAdj[i][j], end=" ")
                print() 

    def ordre(self):
        return self.nbrSommets

    def degree(self, v):
        return sum(self.matAdj[v])

    def voisins(self, v):
        return [i for i in range(self.nbrSommets) if self.matAdj[v][i] == 1]

    def verifyChemin(self, u, v, length):
        visited = [False] * self.nbrSommets
        return self.helpVerifyChemin(u, v, length, visited)

    def helpVerifyChemin(self, u, v, length, visited):
        if length == 0:
            return u == v
        visited[u] = True
        for i in range(self.nbrSommets):
            if self.matAdj[u][i] != 0 and not visited[i]:
                if self.helpVerifyChemin(i, v, length - 1, visited):
                    return True
        visited[u] = False
        return False


    def cheminEleurien(self):
        degreeImpair = sum(self.degree(v) % 2 != 0 for v in range(self.nbrSommets))
        if degreeImpair == 0:
            return "Cycle Euleurien"
        elif degreeImpair == 2:
            return "Chemin Euleurien"
        else:
            return "ni cycle ni chemin Eulerien"
        
        
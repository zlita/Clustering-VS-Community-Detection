import math
from igraph import *


# ------------------------ distance
def euclidianDistance(coordinate1, coordinate2):
	# each coordinate should be of the same dimension
	if(len(coordinate1) != len(coordinate2)):
		raise ValueError('error : the coordinate of the two points should be of the same dimension')

	sumOfSquare = 0
	for i,j in zip(coordinate1,coordinate2):
		sumOfSquare = sumOfSquare + ((abs(i) - abs(j)) ** 2)

	distance = math.sqrt(sumOfSquare)
	return distance


class netMethods:
	# ------------------------ loading
	# -- Type de données:
	# --
	# -- sommets demarre a 0
	# --
	# -- [
	# -- ...
	# -- (sommet1, sommet2[, poid])
	# -- (sommet2, sommet7[, poid])
	# -- ...
	# -- ]
	# --
	# --------------------------------
	def loadData(filename):
		graph=Graph.Read_GML(filename)
		return graph.get_edgelist()


	# ------------------------ transfrom
	class transform:

		#k nearest neightboors
		def naiveTransform(netData,**kwargs):
			k = kwargs.get('k', None)	# valeur par défault à definir, None ne peut pas permettre de construire un graphe
			nbrPoint = len(netData)
			distance = [dict() for x in range(nbrPoint)]	#create one dictionary for each point.
			graph = []

			#calcul of all the distance
			for i, vector in enumerate(netData) :
				j = i + 1
				while j < nbrPoint :#if j < i the entry is already in the dictionnary so it's useless to calculate it again.
					distance[i][j] = euclidianDistance(netData[i], netData[j])
					distance[j][i] = distance[i][j]
					j += 1

				#construction of the graph.
				j = 0
				while j < k :
					nearest = min(distance[i], key=distance[i].get)
					del distance[i][nearest]
					if([nearest, i] not in graph) :	#as the graph is non-oriented we don't want to add 2 time the same edge.
						graph.append([i, nearest])
					j += 1

			return graph



	# ------------------------ clustering
	class clustering:
		def infomap(netObject, clusterCount=None,**kwargs):
			graph = Graph(0, netObject)
			partition = graph.community_infomap()
#			modularity = graph.modularity(partition)
			return partition


		def louvain(netObject, clusterCount=None,**kwargs):
			graph = Graph(0, netObject)
			partition = graph.community_multilevel()
#			modularity = graph.modularity(partition)
			return partition


		def labelPropagation(netObject, clusterCount=None,**kwargs):
			graph = Graph(0, netObject)
			partition = graph.community_label_propagation()
#			modularity = graph.modularity(partition)
			return partition

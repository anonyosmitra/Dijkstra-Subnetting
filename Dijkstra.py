from tabulate import tabulate
nodes=["Z","C","Y","M","G","W","H","Q","F","R","I","L"]
edges=[("Z","C",1),("Z","Y",8),("C","G",9),("C","M",5),("Y","H",6),("Y","W",4),("M","Q",11),("G","F",2),("G","Q",9),("W","R",8),("W","H",6),("H","I",2),("H","L",10),("Q","I",2),("F","I",6),("R","L",10)]


finished=[]
pending=[]
route={}
CN=None
RevOrder=False
nodes.sort(reverse=RevOrder)
tabHist=[]
rowCount=1
def makeRow():
	ana=""
	global tabHist,finished,rowCount
	pending.sort()
	finished.sort()
	rw=[rowCount,", ".join(pending),", ".join(finished),CN]
	rowCount+=1
	for i in route.keys():
		rw+=[route[i]["Dist"]]
	tabHist+=[rw]
def printTable():
	header=["No","Analysis","Finished","Current"]
	for i in nodes:
		header+=[i]
	print(tabulate(tabHist,headers=header))
def popMinPending():
	if len(pending)==0:
		return None
	min=pending[0]
	for i in pending:
		if route[i]["Dist"]<route[min]["Dist"]:
			min=i
		elif route[i]["Dist"]==route[min]["Dist"]:
			if min<i and RevOrder:
				min = i
	pending.remove(min)
	return min
def visitNode(n):
	global pending
	neigh=getNeighbours(n)
	d=route[n]["Dist"]
	for i in neigh:
		if i["node"] not in finished:
			i["dist"]+=d
			if route[i["node"]]["Dist"]=="INF":
				route[i["node"]]["Dist"]=i["dist"]
				pending+=[i["node"]]
			elif route[i["node"]]["Dist"]>i["dist"]:
				route[i["node"]]["Dist"] = i["dist"]

def setup():
	for i in nodes:
		route[i]={"parent":None,"Dist":"INF"}
def getNeighbours(n):
	neg=[]
	for i in edges:
		if i[0]==n:
			neg+=[{"node":i[1],"dist":i[2]}]
		if i[1]==n:
			neg+=[{"node":i[0],"dist":i[2]}]
	return neg

def routeFrom(hn):
	global CN,pending,finished
	setup()
	CN=hn
	route[CN]["Parent"] = "HOME"
	route[CN]["Dist"]=0
	pending+=[CN]
	makeRow()
	while len(pending)>0:
		CN=popMinPending()
		finished+=[CN]
		visitNode(CN)
		makeRow()
	printTable()

print("Nodes: "+str(len(nodes)))
print("Edges: "+str(len(edges)))
routeFrom("C")
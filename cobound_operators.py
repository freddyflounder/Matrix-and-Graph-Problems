#Please reference https://www.stat.uchicago.edu/~lekheng/work/psapm.pdf
#for formulas and context.
#These are meant to work as a template for any undirected graphs with a weights matrix and can be adjusted to work for directed graphs

##Functions defined on graphs:

#All of the following may be redefined as long as they following the 
#alternating property: f(i,j)=-f(j,i), f(i,j,k)=-f(k,j,i)
#Given functions require a weight matrix. Adjust code if you
#Wish to use functions without such pre-condition

def get_neighbors(i, G):
  N=[]
  for vertex in G[i]:
    if vertex!=0 and G[i].index(vertex)!=i:
      N.append(G[i].index(vertex))
  return N

#vertex function
#input: vertex index i, weights matrix W
#output: value at vertex i
def vertex_function(i, W):
  return W[i][i]

#edge function
#input: two vertices i and j, weight matrix W, adj matrix G
#output: weight of edge (i,j)
def edge_function(i,j,G,W):
  if(G[i][j]!=0):
    if W[i][i]<W[j][j]:
      return vertex_function(j, W) + vertex_function(i ,W)
    else:
      return -(vertex_function(j, W) - vertex_function(i ,W))
  else:
    return 0

#triangle function
#input: vertices on a triangle i, j, k, adj matrix G, weight matrix W
#output: value of triangle (i,j,k)
def triangle_function(i,j,k,G,W):
  if(G[i][j]!=0 and G[j][k]!=0 and G[k][i]!=0):
    if W[i][i]<W[j][j] and W[j][j]<W[k][k]:
      return W[i][i]+W[j][j]+W[k][k]
    else:
      return -(W[i][i]+W[j][j]+W[k][k])
  else:
    return 0

##Graph function operators:

#Graph Gradient Operator
#input: vertex function and adj matrix G
#output: matrix of gradients of G according to above functions defined on weights matrix W
def grad(G, W):
  grad_matrix=[]
  iterate=0
  for i in G:
    grad_row = []
    for j in range(len(i)):
      if j!=iterate:
        if(i[j]!=0):
          grad_row.append(vertex_function(j, W) - vertex_function(iterate ,W))
        else: 
          grad_row.append(0)
      else:
        grad_row.append(0)
    grad_matrix.append(grad_row)
    iterate+=1
  return grad_matrix

#Graph Curl Operator
#input: adj matrix G, 
#output: tensor space of curl of G
def curl(G, W):
  curl_tensor=[]
  i_iterate=0
  for i in G:
    curl_matrix=[]
    for j in range(len(i)):
      curl_row=[]
      for k in range(len(i)):
        if (i[j]!=0 and i[k]!=0 and G[k][j]!=0 and i_iterate!=k and i_iterate!=j and j!=k):
          curl_row.append(edge_function(i_iterate, j, G, W) + edge_function(j, k, G, W) + edge_function(k, i_iterate, G, W))
        else:
          curl_row.append(0)
      curl_matrix.append(curl_row)
    curl_tensor.append(curl_matrix)
    i_iterate+=1
  return curl_tensor

#Graph Divergence Operator
#input: adj matrix G, edge function (pre-defined in program)
#output: array of output flow of edge function through each vertex
def div(G,W):
  divergence=[]
  for i in range(len(G)):
    N=get_neighbors(i, G)
    sum=0
    for neighbor in N:
      sum=sum + (W[i][neighbor]/2)*edge_function(i, neighbor, G, W)
    divergence.append(sum)
  return divergence

#Graph Laplacian Operator
def Laplacian(G,W):
  del_0=(div(grad(G,W), W))
  for i in range(len(del_0)):
    del_0[i]*=(-1)
  return del_0


##Test Cases##

P_2=[]
Weight_1=[]
row_one=[0, 1]
row_two=[1, 0]
w_1=[10,1]
w_2=[1,9]
P_2.append(row_one)
P_2.append(row_two)
Weight_1.append(w_1)
Weight_1.append(w_2)

#print(grad(P_2, Weight_1))
#print(Laplacian(P_2, Weight_1))

C_3=[]
Weight_2=[]
row_one=[0,1,1]
row_two=[1,0,1]
row_three=[1,1,0]
w_1=[10,1,1]
w_2=[1,3,1]
w_3=[1,1,4]
Weight_2.append(w_1)
Weight_2.append(w_2)
Weight_2.append(w_3)
C_3.append(row_one)
C_3.append(row_two)
C_3.append(row_three)

print(grad(C_3, Weight_2))
print(Laplacian(C_3, Weight_2))


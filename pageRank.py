__author__ = 'akshaykulkarni'

import Web
import numpy
import random

'''
generateRandomNumber generates a random number between 0 to n-1 following zipf Distribution
'''
def generateRandomNumber(n):
    m = n+1
    while m > n:
        m   = numpy.random.zipf(4.0)
    return m-1


'''
This function initializes the WebObject class
 - in_edges[i] -> is a list which contains nodes pointed to node i
 - out_edges[i] -> is a number denoting number of out-going edges from i
 - dangling_pages[i] -> is a boolean denotes whether current node is dangling or not. A node is dangling if it does not have any out-edge
'''
def init_random_web(pages):

    webObject   = Web.Web(pages)
    for page in xrange(pages):
        number_inlinks  = generateRandomNumber(pages+1)
        inlinks_values  = random.sample(xrange(pages),number_inlinks)

        '''
        inlinks_values is a list of nodes from which there is incoming edge to current node
        '''

        webObject.in_edges[page]    = inlinks_values
        for edge in inlinks_values:
            if 0 == webObject.out_edges[edge]:
                webObject.dangling_pages.pop(edge)
            webObject.out_edges[edge]   = webObject.out_edges[edge]+1


    return webObject

'''
PageRank is computed by repeatedly refinning the initial probability(rank) assigned to each node
P(i+1) = M*P(i)

P(i)   -> PageRank in ith Step
P(i+1) -> PageRank in (i+1)th Step
M -> is n*n matrix whose structure reflect link structure of the web

M can be written as,M = sA + sD + tE
- sA representing the crazy websurfer randomly picking links to follow
- sD due to the fact that the websurfer can’t randomly pick a link when they hit a dangling page
- tE representing the websurfer getting bored and “teleporting” to a random webpage.

s -> is the probability of websurfer taking doing action A or D
t = 1-s -> is the probability of websurfer taking doing action E

Initial PageRank will not matter if the algorithm is ran sufficient and allowed to converge
'''

def nextStep(webObject,p,s):

    pageCount   = webObject.pageCount
    prob        = numpy.matrix(numpy.zeros((pageCount,1)))

    '''
    Computing matrix D
    '''
    sum_dangling= sum(p[j] for j in webObject.dangling_pages.keys())


    for i in xrange(pageCount):
        csum    = 0;

        for edge in webObject.in_edges[i]:
            csum    = csum + ((p[edge]*1.0)/(webObject.out_edges[edge]*1.0))

        csum        = csum*s
        csum        = csum + (sum_dangling*s*1.0)/(pageCount*1.0)
        csum        = csum + ((1.0-s)/(pageCount*1.0))
        prob[i]     = csum

    return prob/numpy.sum(prob)

def page_rank(webObject,s=0.85,tol=0.000001):

    init_p      = numpy.matrix(numpy.ones((webObject.pageCount,1)))/webObject.pageCount
    init_change = 1.0
    iteration   = 0

    while init_change > tol:

        p           = nextStep(webObject,init_p,s)
        init_change = numpy.sum(numpy.abs(init_p-p))
        init_p      = p
        iteration   = iteration+1

    return init_p


webObject   = init_random_web(100)
print page_rank(webObject)

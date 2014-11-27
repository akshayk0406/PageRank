__author__ = 'akshaykulkarni'

class Web:

    def __init__(self,pages):
        self.pageCount          = pages
        self.in_edges           = {}
        self.out_edges          = {}
        self.dangling_pages     = {}

        for i in xrange(pages):
            self.in_edges[i]        = []
            self.out_edges[i]       = 0
            self.dangling_pages[i]  = True


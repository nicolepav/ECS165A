# from blist import blist

"""
A data strucutre holding indices for various columns of a table. Key column should be indexd by default, other columns can be indexed through this object. Indices are usually B-Trees, but other data structures can be used as well.
"""

class Index:

    def __init__(self, table):
        # One index for each table. All our empty initially.
        self.indices = [None] *  table.num_columns



    """
    # returns the location of all records with the given value on column "column"
    """
    #TODO Finish this
    def locate(self, column, value):
        self.indices[column-1].clearReturningData()
        self.indices[column-1].returnRangeData(self.indices[column-1].root, value, value)
        returningRecords = self.indices[column-1].returnData
        #return the location
        pass

    """
    # Returns the RIDs of all records with values in column "column" between "begin" and "end"
    """

    def locate_range(self, begin, end, column):
        self.indices[column-1].clearReturnData()
        self.indices[column-1].returnRangeData(self.indices[column-1].root, begin, end)
        returningRecords = self.indices[column-1].returnData
        return returningRecords

    """
    # optional: Create index on specific column
    """
    #record data = array of pageranges
    #column_number assumes the user passes the number of the table column from their view
    def create_index(self, column_number, pageRanges):
        self.indices[column_number-1] = BST()
        for pageRange in pageRanges:
            for basePages in pageRange.basePages:
                basePageRecords = basePages.getAllRecords()
                for record in basePageRecords:
                    # if record has not been invalidated
                    # TODO: Update this to whatever the invalidation signifier is when issue resolved
                    if record[0] != 0:

                        # if schema says record has tail pages
                        if record[3] == 1:      
                            # tail logic using indirection column to access tail page
                            tailRecord = pageRange.getPreviousTailRecord(record[0])
                            self.indices[column_number-1].insert(tailRecord[column_number + 3], tailRecord)
                            print("Tail record used") 
                        else:
                            # use data that is here in base page
                            self.indices[column_number-1].insert(record[column_number + 3], record)
                            print("Base record used")
            
                    else: 
                        pass
                        # the record was invalidated
                        
        # M M M M X X X X
        # 0 1 2 3 4 5 6 7
        #         1 2 3 4


    """
    # optional: Drop index of specific column
    """

    def drop_index(self, column_number):
        self.indices[column_number-1] = None
        pass



class Node:
    def __init__(self, data = None, record = None):
        self.data = data
        self.record = record #pointer
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None
        self.returnData = []

    def insert(self, data, record):
        # check if root node is none
        if self.root is None:
            self.root = Node(data, record)
        #tree has at least one node in it and find appro location to put the new node
        #create a helper method _insert
        else:
            self._insert(data, record, self.root)

    def _insert(self, data, record, cur_node):
        #data is less than cur_node data
        if data < cur_node.data:
            #left node is avaliable for insert
            if cur_node.left is None:
                cur_node.left = Node(data, record)
            #else traverse down
            else:
                self._insert(data, record, cur_node.left)
        elif data >= cur_node.data:
            if cur_node.right is None:
                cur_node.right = Node(data , record)
            else:
                self._insert(data, record, cur_node.right)

    # TODO change append data to record when data insertion is figured out
    def returnRangeData(self, cur_node, begin, end):
        
    # Base Case Start at root
        
        if cur_node is None:
            return
 
    # Since the desired o/p is sorted, recurse for left
    # subtree first. If root.data is greater than k1, then
    # only we can get o/p keys in left subtree
        if begin < cur_node.data :
            self.returnRangeData(cur_node.left, begin, end)
 
    # If root's data lies in range, then prints root's data
        if begin <= cur_node.data and end >= cur_node.data:
            self.returnData.append(cur_node.record[0])
 
    # If root.data is smaller than k2, then only we can get
    # o/p keys in right subtree
        if end >= cur_node.data:
            self.returnRangeData(cur_node.right, begin, end)

    def clearReturnData(self):
        self.returnData = []




    def print_tree(self, traversal_type):
        if traversal_type == "preorder":
            return self.preorder_print(self.root, "")

    def preorder_print(self,start,traversal):
        if start:
            traversal += (str(start.data) + "-")
            traversal = self.preorder_print(start.left, traversal)
            traversal = self.preorder_print(start.right, traversal)
        return traversal



#

class Node(object):
    '''节点类'''

    def __init__(self,data, pnext=None):
        '''
        	data: 节点保存的数据
        	_next: 保存下一个节点对象
        '''
        self.data = data
        self._next = pnext

    def __repr__(self):
        return str(self.data)

class ListNode(object):
    '''链表类'''
    def __init__(self):
    	self.head=None
    	self.lenght=0

    def isEmpty(self):
    	'''判断是否为空'''
    	return (self.length==0)

    def append(self,data):
        '''增加一个节点'''
        item=None
        if isinstance(data,Node):
            item = data
        else:
            item = Node(data)

        #如果头不存在
        if not self.head:
            self.head = item
            self.length = 1
        else:
            # 如果存在找到末尾然后添加节点
            node = self.head
            while node._next:
                node = node._next
            node._next=item
            self.length+=1

    def delete(self,index):
        '''删除一个节点'''
        if self.isEmpty():
            print("listNode is empty")
            return False

        # 删除头节点
        if index == 0:
            self.head=self.head._next
            self.length-=1
            return True

        j=0
        node = self.head
        prev = self.head
        while node._next and j<index:
            prev=node
            node=node._next
            j+=1

        if j==index:
            prev._next = node._next
            self.length-=1

    def getNode(self,index,data=None,update=False):
        '''查找节点'''
        if self.isEmpty():
            print("listNode is empty")
            return False
        j=0
        node=self.head
        while node._next and j<index:
            node = node._next
            j+=1

        # 更新
        if update:
            if j==index:
                node.data=data
            return   

        return node.data
        

    def update(self,index,data):
        '''更新节点'''
        self.getNode(index,data,True)

    def getIndex(self,data):
        '''查找索引'''
        if self.isEmpty():
            print("listNode is empty")
            return False
        
        # 索引列表
        index=[]

        j=0
        node=self.head
        while node:
            if node.data == data:
                index.append(j)
            node=node._next
            j+=1

        indexLen=len(index)
        if indexLen==0:
            return False
        elif indexLen==1:
            return index[0]
        else:
            print(" index not only , is list. ")
            return index

    def insert(self,index,data):
        '''插入节点'''
        if self.isEmpty():
            print("listNode is empty, so append data")
            index=0
            self.head=None
            self.append(data)
            return True

        item = None
        if isinstance(data,Node):
            item = data
        else:
            item = Node(data)

        if index==0:
            item._next = self.head
            self.head = item
            self.length += 1

        j = 0
        node = self.head
        prev = self.head
        while node._next and j<index:
            prev=node
            node=node._next
            j+=1

        if j == index :
            item._next = node
            prev._next = item
            return True 

    def clear(self):
        self.head = None
        self.length = 0


    def __repr__(self):
        '''字符串'''
        if not self.head:
            return ' empty listNode '

        s=[]
        node = self.head
        while node:
            s.append(str(node.data))
            node = node._next
            
        return " -> ".join(s)

    def __getitem__(self,index):
        '''索引取值'''
        return self.getNode(index)

    def __setitem__(self,index,value):
        '''设置值'''
        print(index)
        self.update(index,value)

if __name__ == '__main__':

    # 创建链表
    chain=ListNode()

    # 添加数据
    print("add 10 numbers")
    for i in range(10,20):
        chain.append(i)
    
    print(chain)    

    # 查找索引
    print("value eq 12 is index = ",end=" ")
    print(chain.getIndex(12))

    # 更新上面查找的索引
    print("update  ")
    index=chain.getIndex(12)
    if isinstance(index,int):
        chain.update(index,99)

    # 再次查找索引
    print("again, value eq 12 is index = ",end=" ")
    print(chain.getIndex(12))


    print(" because listNode is : ")
    print(chain)

    # 删除一个索引
    print("delete index 0")
    chain.delete(0)
    print(chain)

    # insert
    print("insert data")
    chain.insert(1,9)
    print(chain)
     
    # 直接索引获取值
    print("use [] get data")
    print(chain[3])

    # 直接设置值
    print("append same value")
    chain.append(90)
    chain.append(90)
    print(chain)
    
    # 查找相同值索引
    print("search 90 index")
    print(chain.getIndex(90))





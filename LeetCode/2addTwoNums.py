# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

############## start ##############
        
def listNodeToInt(listN):
    '''链表转整数'''
    result=0
    i=0
    node=listN
    while True:
 
        if not isinstance(node,ListNode):
            break
        result += node.val*10**i
        node=node.next
        i+=1

    return result

def intToListNode(num):
    '''整数转链表，抄袭stringToListNode '''
    dummyRoot = ListNode(0)
    ptr = dummyRoot
    number=-1
    while True:
        if num == 0:
            if number==-1:
                ptr.next=ListNode(0)
            break
        number=num%10
        num=num//10

        ptr.next = ListNode(number)
        ptr = ptr.next

    ptr = dummyRoot.next
    return ptr
    

class Solution:
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        #list1=listNodeToString(l1)
        #print(list1)


        i1=listNodeToInt(l1)
        i2=listNodeToInt(l2)
        i3=i1+i2
        #print(i1,i2)
        #print(i3)
        l3=intToListNode(i3)
        
        #print(listNodeToString(l3))

        return l3

##############  end  ##############   

def stringToListNode(input):
    numbers=input
    # Now convert that list into linked list
    dummyRoot = ListNode(0)
    ptr = dummyRoot
    for number in numbers:
        ptr.next = ListNode(number)
        ptr = ptr.next

    ptr = dummyRoot.next
    return ptr

def listNodeToString(node):
    if not node:
        return "[]"

    result = ""
    while node:
        result += str(node.val) + ", "
        node = node.next
    return "[" + result[:-2] + "]"

def main():

    while True:
        try:

            line = [0]
            l1 = stringToListNode(line);
            line = [0]
            l2 = stringToListNode(line);
            
            ret = Solution().addTwoNumbers(l1, l2)

            out = listNodeToString(ret);
            print(out)

            #throw
            raise StopIteration
        except StopIteration:
            break

if __name__ == '__main__':
    main()

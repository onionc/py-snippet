# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def middleNode(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        head2=head
        l=1

        while head.next!=None:
            head=head.next
            
            l+=1
        
        w=l//2+1
        

        l=1
        while head2.next!=None:
            if w==l:
                break
            head2=head2.next
            
            l+=1  
        return head2
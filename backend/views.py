from django.shortcuts import render
from django.http import JsonResponse, request, response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from multiprocessing import Manager, Process
import time


# Create your views here.
class Queue:
    #Constructor creates a list
    def __init__(self):
        self.queue = list()
        self.start_time = 0
        self.start_time2 = 0
        self.counter = 1

    #Adding elements to queue
    def enqueue(self,data):
      #Checking to avoid duplicate entry (not mandatory)
        if data not in self.queue:
            self.queue.insert(0,data)
            if self.start_time != 0:
                self.start_time2 = time.time()
                self.start_time += self.start_time2

            self.start_time = time.time()
            return True
        else:
            self.counter += 1
            return self.counter
        # return False


    #Removing the last element from the queue
    def dequeue(self):
        if len(self.queue)>0:
            elapsed_time = time.time() - self.start_time
            self.start_time = self.start_time - elapsed_time
            self.queue.pop()
            return self.start_time * self.counter
        return ("Counter Empty!")

    #Getting the size of the counter queue
    def size(self):
        return len(self.queue)

    #printing the elements of the queue
    def printQueue(self):
        return self.queue

    def time(self):
        start_time = time.time()
        elapsed_time = time.time() - start_time
        time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

@api_view(['GET'])
def CounterTicket(request):
    customerQueue = Queue()
    p1 = customerQueue.enqueue('P1')
    p2 = customerQueue.enqueue('P2')
    p3 = customerQueue.enqueue('P3')
    d1 = customerQueue.dequeue()
    d2 = customerQueue.dequeue()
    # d3 = customerQueue.dequeue()
    q = {}
    q['time taken for p1'] = d1
    q['time taken for p2'] = d2
    q['time taken for p3'] = d2
    return JsonResponse({'timetaken':q})

def preprocess(mat):
    (M, N) = (len(mat), len(mat[0]))
    s = [[0 for x in range(len(mat[0]))] for y in range(len(mat))]
    s[0][0] = mat[0][0]
 
    for j in range(1, len(mat[0])):
        s[0][j] = mat[0][j] + s[0][j - 1]
 
    for i in range(1, len(mat)):
        s[i][0] = mat[i][0] + s[i - 1][0]
 
    for i in range(1, len(mat)):
        for j in range(1, len(mat[0])):
            s[i][j] = mat[i][j] + s[i - 1][j] + s[i][j - 1] - s[i - 1][j - 1]
 
    return s
 
# Calculate the sum of all elements in a submatrix in constant time
@api_view(['POST'])
def findSubmatrixSum(request):
    try:
        data = JSONParser().parse(request)
        mat = data['mat']
        p = q = 1
        r = s = 3
        if not mat or not len(mat):
            return 0
        mat = preprocess(mat) 
        total = mat[r][s]
        if q - 1 >= 0:
            total -= mat[r][q - 1]
    
        if p - 1 >= 0:
            total -= mat[p - 1][s]
    
        if p - 1 >= 0 and q - 1 >= 0:
            total += mat[p - 1][q - 1]
    
        return JsonResponse({
            'total': total
        })
    except Exception as ex:
        return JsonResponse({
            "status": str(ex)
        })
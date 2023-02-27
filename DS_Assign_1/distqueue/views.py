from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .queue_funcs import *

# from distQueue import distQueue
#Temporary queue implemented for Part A
# mesgQ = distQueue()

def Topics(request):
    # print("Heeyyy thereee")
    if request.method == 'GET':
        final_resp = listTopics()
        # final_resp = {'status':'success'}
        # final_resp['number'] = len(list_topics)
        print(final_resp)
        return JsonResponse(final_resp)

    elif request.method == 'POST':
        final_resp = {'status':'message'}
        if request.POST.get('topic_name') == None:
            # print(request.POST)
            final_resp['status'] = "failure"
            final_resp['message'] = "No key 'topic_name' found in the POST method"
            return JsonResponse(final_resp)
        else:
            final_resp = createTopic(request.POST.get('topic_name'))
            return JsonResponse(final_resp)

def registerConsumer(request):
    final_resp = {'status':'failure'}
    if request.method == 'POST':
        # print("Hey")
        # Check if valid parameters
        if request.POST.get('topic_name') == None:
            final_resp['message'] = "No key 'topic_name' found in the POST method"
            return JsonResponse(final_resp)
        #register the consumer
        final_resp = qregisterConsumer(request.POST.get('topic_name'))
        return JsonResponse(final_resp)

    final_resp['status'] = 'failure'
    final_resp['message'] = 'GET method not supported for this endpoint'
    return JsonResponse(final_resp)


def registerProducer(request):
    final_resp = {'status':'failure'}
    if request.method == 'POST':
        # Check if valid parameters
        if request.POST.get('topic_name') == None:
            final_resp['message'] = "No key 'topic_name' found in the POST method"
            return JsonResponse(final_resp)
        #register the producer
        final_resp = qregisterProducer(request.POST.get('topic_name'))
        return JsonResponse(final_resp)

    final_resp['message'] = 'GET method not supported for this endpoint'
    return JsonResponse(final_resp)

def enqueue(request):
    final_resp = {'status':'failure'}
    if request.method == 'POST':
        # Check if valid parameters
        if request.POST.get('message',None) == None:
            final_resp["message"] = "No key 'message' found in the POST method"
            return JsonResponse(final_resp)
        if request.POST.get('topic_name') == None:
            final_resp["message"] = "No key 'topic_name' found in the POST method"
            return JsonResponse(final_resp)
        if request.POST.get('producer_id') == None:
            final_resp["message"] = "No key 'producer_id' found in the POST method"
            return JsonResponse(final_resp)

        #Add the log message to the queue
        # print(request.POST.get('topic_name'),request.POST.get('producer_id'))
        final_resp = qenqueue(request.POST.get('topic_name'),request.POST.get('producer_id'),request.POST.get('message'))
        return JsonResponse(final_resp)

    final_resp['message'] = 'GET method not supported for this endpoint'
    return JsonResponse(final_resp)

def dequeue(request):
    final_resp = {'status':'failure'}
    if request.method == 'GET':
        # Check if valid parameters
        if request.GET.get('topic_name') == None:
            final_resp["message"] = "No key 'topic_name' found in the GET method"
            return JsonResponse(final_resp)
        if request.GET.get('consumer_id') == None:
            final_resp["message"] = "No key 'consumer_id' found in the GET method"
            return JsonResponse(final_resp)
        #Remove and return the log message from the queue
        final_resp = qdequeue(request.GET.get('topic_name'),request.GET.get('consumer_id'))
        return JsonResponse(final_resp)

    final_resp['message'] = 'POST method not supported for this endpoint'
    return JsonResponse(final_resp)

def size(request):
    final_resp = {'status':'failure'}
    if request.method == 'GET':
        # print(request.GET.get('topic_name'))
        # Check if valid parameters
        if request.GET.get('topic_name') == None:
            final_resp["message"] = "No key 'topic_name' found in the GET method"
            return JsonResponse(final_resp)
        if request.GET.get('consumer_id') == None:
            final_resp["message"] = "No key 'consumer_id' found in the GET method"
            return JsonResponse(final_resp)
        #Return the number of log messages in the requested topic for the consumer
        final_resp = qsize(request.GET.get('topic_name'),request.GET.get('consumer_id'))
        return JsonResponse(final_resp)

    final_resp['message'] = 'POST method not supported for this endpoint'
    return JsonResponse(final_resp)
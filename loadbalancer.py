import asyncio, requests
from flask import Flask, make_response, jsonify
from flask import request
import aiohttp

write_ports = [5001]
read_ports = [5002,5003]

app = Flask(__name__)

lock = asyncio.Lock()
round_index = 0
serverLink = "http://127.0.0.1:"

# session = aiohttp.ClientSession()

async def get_link(reroute):
    global round_index
    async with lock:
        newLink = (serverLink + str(read_ports[round_index]))
        round_index = (round_index + 1)%(len(read_ports))
        newLink += reroute
        return newLink
    
async def get_requests(params, link):
    #Redirect the get requests to the read managers 
    print("Heyyy")
    # session = aiohttp.ClientSession()
    final_link = await get_link(link)
    print("Sending get requests to ", final_link)
    try:
        return requests.get(final_link, json = params.get_json())
    except:
        return requests.get(final_link)

async def post_requests(params, link):
    # session = aiohttp.ClientSession()
    final_link = (serverLink + str(write_ports[0])) + link
    print("Sending post requests to ", final_link)
    try:
        return requests.post(final_link, json = params.get_json())
    except:
        return requests.post(final_link)

@app.route(rule = '/<link>', methods = ["GET", "POST"])
async def reroute(link):
    print(link)
    if request.method == 'POST':
        resp = await post_requests(request,"/"+link)
        return make_response(resp.json(),resp.status_code)
    elif request.method == 'GET':
        # print(request)
        resp = await get_requests(request,"/"+link)
        return make_response(resp.json(),resp.status_code)

@app.route(rule = '/<link1>/<link2>', methods = ["GET","POST"])
async def reroute2(link1, link2):
    print(link1, link2)
    if request.method == 'POST':
        resp = await post_requests(request,"/"+link1 +"/"+link2)
        # print(resp)
        return make_response(resp.json(),resp.status_code)
    elif request.method == 'GET':
        # print(request)
        resp = await get_requests(request,"/"+link1+"/"+link2)
        # print(resp)
        return make_response(resp.json(),resp.status_code)

if __name__ == '__main__':
    app.run(debug = True)
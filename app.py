import asyncio, requests
from flask import Flask

write_ports = [5001]
read_ports = [5002,5003]

lock = asyncio.Lock()
round_index = 0
serverLink = "http://127.0.0.1:"

async def get_link():
    async with lock:
        newLink = (serverLink + str(read_ports[round_index]))
        round_index = (round_index + 1)%(len(read_ports))
        return newLink

async def get_requests(params, link):
    #Redirect the get requests to the read managers 
    final_link = await get_link() + link
    resp = requests.get(final)

async def post_requests(params, link):
    final_link = (serverLink + str(write_ports[0])) + link
    resp = requests.post(final_link, params = params, data = params, json = params)
    return resp

@app.route('/<link>')
def reroute(link):
    if request.method == 'POST':
        return post_requests(request.get_json(),"/"+link)
    elif request.method == 'GET':
        return get_requests(request.get_json(), "/"+link)

async def main():
    


app = Flask(__name__)

if __name__ == '__main__':
    app.run()
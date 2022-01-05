import socket
import asyncio

async def main():
    #default host and port: localhost:5555
    HOST = "localhost"
    PORT = 5555

    with socket.socket() as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        #infinite looping the request and response handling
        while (1 == 1):
            await ens_connections(sock)
            #decodeing the request and splitting it into the requested page
            req = connection.recv(1024).decode('utf-8')
            print(req)
            string_list = req.split(' ')
            #method = string_list[0]
            requested_page =  string_list[1]
            print(f"client requested: {requested_page}")

            page = requested_page.lstrip('/')
            # setting the header according to the type of the asked content
            if(page == ''):
                type = 'text/html'
                page = 'index.html'
            elif(page == 'shutdown'):
                #shutting down the server on call via breaking the loop
                type = 'text/html'
                page = 'shutdown.html'
                await page_response(type, page)
                break
            elif(page == 'favicon.ico'):
                type = 'image/x-icon'
            
            #response
            await page_response(type, page)


async def ens_connections(sock):
    #enstablist the connection
    global connection, address
    connection, address = sock.accept()
    return connection, address

async def responsing(response, header):
    #response to the request with the given content and header
    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()

async def page_response(file_type, page):
    try:
        #read the content of the requested file and setting the header
        with open(page, 'rb') as f:
            response = f.read()
            f.close()
        type = file_type
        header = (f"HTTP/1.1 200 OK\nContent-Type:{file_type}\n\n")
    except Exception as e:
        #on exception sending a 404 code and the not found page
        f = open("notfound.html", "rb")
        response = f.read()
        f.close()
        header = (f"HTTP/1.1 404 Not Found\nContent-Type:text/html\n\n")

    await responsing(response, header)

asyncio.run(main())

import socket
import json
import machine


from enums.pins import Pins

class RequestHandler():
    def __init__(self):
        pass



    # Function to handle client requests
    def handle_request(self,client):
        request = client.recv(1024).decode()
        method = request.split()[0]
        path = request.split()[1]
        
        if method == 'GET':
            self.GET(path)
        
        elif method == 'POST':
            self.POST(path)
        else:
            client.send('HTTP/1.0 404 Not Found\r\n\r\n')
        client.close()
        


    # Function to handle client requests
    def handle_requestcp(self,client):
        request = client.recv(1024).decode()
        method = request.split()[0]
        path = request.split()[1]
        
        if method == 'GET' and path == '/api/temperature':
            adc = machine.ADC(4)
            conversion_factor = 3.3 / 65535
            sensor_value = adc.read_u16() * conversion_factor
            temperature = 27 - (sensor_value - 0.706) / 0.001721
            response = json.dumps({"temperature": temperature})
            client.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
            client.send(response)
        elif method == 'POST' and path == '/api/control-led':
            content_length = int(request.split('Content-Length: ')[-1].split()[0])
            body = request.split('\r\n\r\n')[-1][:content_length]
            data = json.loads(body)
            # led_red.value(data.get("ledRed", 0))
            # led_green.value(data.get("ledGreen", 0))
            response = json.dumps({"message": "Command sent successfully!"})
            client.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
            client.send(response)
        else:
            client.send('HTTP/1.0 404 Not Found\r\n\r\n')
        client.close()

    def GET(self,path):
        return 1
    
    def POST(self,path):
        return 1



class APRequestHandler(RequestHandler):
    def __init__(self):
        pass

    def ReceiveData(self,client):
        request = client.recv(1024).decode()
        method = request.split()[0]
        path = request.split()[1]
        if method == "POST" and path == "/api/data":
            print("Correct POST Command Receieved")
            content_length = int(request.split('Content-Length: ')[-1].split()[0])
            body = request.split('\r\n\r\n')[-1][:content_length]
            print(f"Content Body Received: {body}")
            if type(body) is not str:
                data = json.load(body)
            else:
                data = json.loads(body)
            try:
                hash = data["hash"]
                client.close()
                return hash
            except:
                client.send('HTTP/1.0 404 Not Found\r\n\r\n')
                client.close()
                return False
        else:
            client.send('HTTP/1.0 404 Not Found\r\n\r\n')

        client.close()

        return False

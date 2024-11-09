import network
import socket
from time import sleep


from src.requestHandler import APRequestHandler
class WAPSetup():
    def __init__(self,s,p):
        """
        desc:
            Init class for Picoscope Access Point
        args:
            s: str, Pico Access Point SSID
            P: str, Password fro Pico Access Point

        """
        self.ssid = s  
        self.password = p
        self.ap = self.StartAP()


    def GetIF(self):
        return self.ap.ifconfig()
    
    # def GetIP(self):
    #     return self.ap.ifconfig()

        

    def StartAP(self):
        """
        desc:
            Create the Access point
        returns:
            ap: object network.WLAN returns the access point object so it can be closed after setup is complete
        """
        ap = network.WLAN(network.AP_IF)
        ap.config(essid=self.ssid, password=self.password)
        ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
        ap.active(True)

        # Wait for AP to be active
        while not ap.active():
            pass

        print("Access point active")
        print(ap.ifconfig())
        self.IP = ap.ifconfig()
        return ap
    
    def KillAP(self):
        """
        desc:
            Disable the access point once WAP Setup is complete

        
        """
        try:
            self.ap.active(False)
            return True
        except Exception as e:
            raise Exception(f"Failed to close Access Point exception: {e}")


    def WaitForPost(self, port = 80, timeout = 1800):
        onlyPost = APRequestHandler()
        addr = socket.getaddrinfo(self.GetIF()[0], port)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        print('listening Started')
        counter = 0
    
        while timeout != counter:
            
            try:
                client, addr = s.accept()
                response = onlyPost.ReceiveData(client)
                
                if response is not False:
                    client.close()
                    return response
            except OSError as e:
                client.close()
                print(f'connection closed, exception: {e}')

            client.close()
            counter += 1
            sleep(1)


            

            


            


         





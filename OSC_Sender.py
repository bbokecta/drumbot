from pythonosc.udp_client import SimpleUDPClient

def send_talkmode():
    
    ip = "172.20.10.8"
    port = 8001

    client = SimpleUDPClient(ip, port)


    client.send_message("/TALKMODE", "200")

def send_dancemode():
    ip = "172.20.10.8"
    port = 8001

    client = SimpleUDPClient(ip, port)

    client.send_message("/DANCEMODE", "100")
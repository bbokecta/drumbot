from pythonosc.udp_client import SimpleUDPClient

def send_talkmode():
    
    ip = "192.168.1.108"
    port = 8001

    client = SimpleUDPClient(ip, port)


    client.send_message("/TALKMODE", "200")

def send_dancemode():
    ip = "192.168.1.108"
    port = 8001

    client = SimpleUDPClient(ip, port)

    client.send_message("/DANCEMODE", "100")
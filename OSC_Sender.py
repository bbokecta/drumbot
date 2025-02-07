from pythonosc.udp_client import SimpleUDPClient

def send_keyword(keyword):
    ip = "192.168.0.51"
    port = 8000

    client = SimpleUDPClient(ip, port)

    client.send_message("/your/address", keyword)
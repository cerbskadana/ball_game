import socket
import threading
import pickle

from random import randint

HOST = "localhost"
PORT = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(13)

clients = {}
next_id ={}
players = {}

def handle_client(conn,player_id):
    conn.sendall(pickle.dumps({"type": "id","id": player_id}))
    players[player_id] = (randint(-300,300),randint(-300,300),20)
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            x,y,r = pickle.loads(data)
            players[player_id] = (x,y,r)

            for c in clients.values():
                c.sendall(pickle.dumps({"type":"state","players": players}))
    except Exception as e:
        print("server error:",e)

    finally:
        del players[player_id]
        del clients[player_id]
        conn.close()
print("Server starting")
while True:
    conn,addr = server.accept()
    player_id = next_id
    next_id += 1

    clients[player_id] = conn
    print("conected:",addr,", ID:",player_id)
    threading.Thread(target=handle_client,args=(conn,player_id),daemon=True).start()
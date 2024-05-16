
import socket
from _thread import *
import sys

server = "192.168.1.68"
port = 5557

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def make_data_str(pos, health, mana, action,frame_index):
    return f"{pos[0]},{pos[1]},{health},{mana},{action},{frame_index}"

def read_data_str(data_str):
    data = data_str.split(",")
    return int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5])

pos = [(200, 310), (700, 310)]
health = [100, 100]
mana = [0, 0]
action = [0, 0]
frame_index = [0, 0]

def threaded_client(conn, player):
    conn.send(str.encode(make_data_str(pos[player], health[player], mana[player], action[player],frame_index[player])))
    while True:
        try:
            data = conn.recv(2048).decode()
            if not data:
                print("Disconnected")
                break

            x, y, h, m, act, frame = read_data_str(data)
            pos[player] = (x, y)
            health[player] = h
            mana[player] = m
            action[player] = act
            frame_index[player] = frame
            if player == 1:
                reply = make_data_str(pos[0], health[0], mana[0],action[0], frame_index[0])
            else:
                reply = make_data_str(pos[1], health[1], mana[1],action[1],frame_index[1])

            print(data)
            print(reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
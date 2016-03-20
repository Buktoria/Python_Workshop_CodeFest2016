# chat_client.py

import sys
import socket
import select

##### YOUR CODE GOES HERE #####
class ChatProfile(object):
    def __init__(self):
        self.name = 'Vicky'
        self.nickname = 'Buktroia'
        self.area_of_study = 'CS'
chat_profile = ChatProfile()
###############################

def chat_client():
    if(len(sys.argv) < 3) :
        print('Usage : python chat_client.py hostname port')
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print('Unable to connect')
        sys.exit()

    print('Connected to remote host. You can start sending messages')
    sys.stdout.write('[{}] '.format(chat_profile.name)); sys.stdout.flush()
    s.send('{} who is studying {} has entered the chat room.\n'.format(
        chat_profile.nickname, chat_profile.area_of_study
    ).encode())

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])

        for sock in ready_to_read:
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data :
                    print('\nDisconnected from chat server')
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data.decode("utf-8", "strict") )
                    sys.stdout.write('[{}] '.format(chat_profile.name)); sys.stdout.flush()

            else :
                # user entered a message
                msg = '[{}] {}'.format(chat_profile.nickname, sys.stdin.readline())
                s.send(msg.encode())
                sys.stdout.write('[{}] '.format(chat_profile.name)); sys.stdout.flush()

if __name__ == "__main__":

    sys.exit(chat_client())

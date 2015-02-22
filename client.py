import sys
import zmq
import time
import random


def main(args):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://localhost:%d' % 12000)
    message = ''
    for request in range (1,100):
        print "Sending request ", request,"..."
        socket.send(message)
        #  Get the reply.
        message = socket.recv()
        if not message:
            break
        print "Received reply ", request, "[", message, "]"
        time.sleep(random.randint(1, 3))



if __name__ == '__main__':
    sys.exit(main(sys.argv))

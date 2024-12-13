'''
Pham Minh Thien
Assignment 4
Prof. Palak Mejpara
'''

from client import client_Side
from server import server
import threading


serverStarter = threading.Thread(target=server)

c1 = threading.Thread(target=client_Side, args=("Client 1",))
c2 = threading.Thread(target=client_Side, args=("Client 2",))


serverStarter.start()
c1.start()
c2.start()


serverStarter.join()
c1.join()
c2.join()

'''
server-side code to receive images from raspberry pi

Author: Jeong Sangjun
'''
import io
import socket
import struct
from PIL import Image

from os import path
from configparser import ConfigParser
from datetime import date
 
# read config file and get initialization info
try:
    current_dir = path.dirname(path.abspath(__file__))
    config = ConfigParser()
    config.read(path.join(current_dir,'config.ini'))
    # assign network for check if access is valid
    network = config['NETWORK'] 
except:
    # exit if error arise
    print("Error while reading config...")
    exit()
else:
    client = network['client']
    port = network['port']

# Start a socket listening for connections on (client, port) (0.0.0.0 means all interfaces)
server_socket = socket.socket()

server_socket.bind((client, port))
server_socket.listen(0)
 
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')

try:
    num = 200
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some processing on it
        image_stream.seek(0)
        
        image = Image.open(image_stream)
        print('Image is %dx%d' % image.size)
                
        image.verify()
        print('Image is verified')

        # Save image
        numstr = "%04d"%num
        image.save(path.join(current_dir,'smpllane',f'ln{numstr} {str(date.today())}.jpg'))

        num += 1
finally:
    connection.close()
    server_socket.close()
# activate on Raspberry Pi with picamera
from img_receiver import CONFIG_INI
import io
import socket
import struct
import time
import picamera
from os import path
from configparser import ConfigParser

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
    server = network['server']
    port = network['port']

# Connect a client socket
client_socket = socket.socket()

client_socket.connect((server, port))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 320)
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)
        
        # Note the start time and construct a stream to hold image date temporarily
        # (we could write it directly to connection but in this case
        # we want to find out the size of each capture first to keep
        # our protocol simple)
        
        start = time.time()
        capturingfor = 30           # time for capturing.

        stream = io.BytesIO()
        for img in camera.capture_continuous(stream, 'jpeg'):

            # Write the length of the capture to the stream and flush to ensure it actually gets sent
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            
            # Rewind the stream and send the image data over the wire
            stream.seek(0)
            connection.write(stream.read())
            
            #If we've been capturing for more than 30 seconds, quit
            if time.time() - start > capturingfor:
                break

            # Reset the stream for the next capture
            stream.seek(0)
            stream.truncate()

    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L',0))
finally:
    connection.close()
    client_socket.close()
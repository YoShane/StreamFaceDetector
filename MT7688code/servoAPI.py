import serial  
import time  
from flask import Flask   
from flask import Response  
from flask import request  
from flask import jsonify
from flask_cors import CORS
import os
 
#f = os.popen('ifconfig br-lan | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1') # AP model
f = os.popen('ifconfig apcli0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1') # Station model  
inet_addr = f.read()  
print(inet_addr)
app = Flask(__name__)
CORS(app)

# ****************************************************
# open serial COM port to /dev/ttyS0, which maps to UART0(D0/D1)
# the baudrate is set to 57600 and should be the same as the one
# specified in the Arduino sketch uploaded to ATMega32U4.
# ****************************************************

def setup():  
  global s 
  s = serial.Serial("/dev/ttyS0", 57600) 

# ****************************************************
# GET http://mylinkit.local:5000/api/status
# ****************************************************
@app.route("/api/status", methods=['GET'])
def getPos():  
    fp = open("/root/storePos.txt", "r")
    pos = int(fp.read())
    fp.close()
    return jsonify({'status':200,'pos':pos,'result':'Done'})

# ****************************************************
# POST http://mylinkit.local:5000/api/action
# ****************************************************
@app.route("/api/action", methods=['POST'])
def setPos():  
    # open file
    fp = open("/root/storePos.txt", "r+")
    value = request.form['value']

    pos = int(fp.read())
    
    if value == 'pull':
        if(pos-1 < 1):
            return jsonify({'status':204,'pos':pos,'result':'This is max right step'})
        s.write("0")
        fp.seek(0)
        fp.write(str(pos-1))
        return jsonify({'status':200,'pos':pos-1,'result':'Done'})
    elif value == 'push':
        if(pos+1 > 5):
            return jsonify({'status':204,'pos':pos,'result':'This is max left step'})
        s.write("1")
        fp.seek(0)
        fp.write(str(pos+1))   
        return jsonify({'status':200,'pos':pos+1,'result':'Done'}) 
    
    # close file
    fp.close()


if __name__ == '__main__':  
    setup() 
    app.debug = True
    app.run(
        host = inet_addr,
        port = 5000
    )

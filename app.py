from flask import * 
import http.server
import socket
import socketserver
import webbrowser
import pyqrcode
import os

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/submit',methods=['POST','GET'])
def p2p():
    input_string = request.form['inputString']
    PORT = 8010


    folder_path = input_string

# If the user presses Enter, default to the Desktop
    if not folder_path:
        folder_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

# Change the working directory to the specified folder
    try:
        os.chdir(folder_path)
    except Exception as e:
        print("Error changing directory:", e)
        exit(1)

# Creating an HTTP request handler
    Handler = http.server.SimpleHTTPRequestHandler

# Finding the IP address of the PC
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        IP = f"http://{s.getsockname()[0]}:{PORT}"
        link = IP
    except Exception as e:
        print("Error getting IP address:", e)
        exit(1)

# Converting the IP address into the form of a QR code
    url = pyqrcode.create(link)
    url.svg("myqr.svg", scale=8)

# Open the QR code image in the web browser
    webbrowser.open('myqr.svg')

# Creating the HTTP server and serving files
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("Serving at port", PORT)
            print("Type this in your browser:", IP)
            print("Or use the QR Code")
            httpd.serve_forever()
    except Exception as e:
        print("Error starting server:", e)
    return render_template('index.html')
    

# main driver function
if __name__ == '__main__':
    app.run(debug=True)
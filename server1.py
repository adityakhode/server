import http.server
import socketserver
import socket
import threading
import os
import cgi

UPLOAD_DIRECTORY = "C:/Users/Aditya/Documents/Aditya/Coading/Pythonfiles/upload/"  # Replace with the directory to save uploaded files

def get_laptop_ip():
    # Get the IP address of the laptop
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        laptop_ip = s.getsockname()[0]
        s.close()
        return laptop_ip
    except socket.error as e:
        print(f"Error getting laptop IP address: {e}")
        return None

class UploadHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle GET requests
        if self.path == '/':
            # Display a simple HTML form for file upload
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = """
            <html><body>
            <h2>Upload a file:</h2>
            <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" multiple><br>
            <input type="submit" value="Upload">
            </form>
            </body></html>
            """
            self.wfile.write(html.encode('utf-8'))
        else:
            # Return 404 for other paths
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        # Handle POST requests (file upload)
        if self.path == '/upload':
            content_type = self.headers.get('Content-Type')
            if content_type and content_type.startswith('multipart/form-data'):
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                if 'file' in form:
                    uploaded_file = form['file']
                    filename = os.path.join(UPLOAD_DIRECTORY, uploaded_file.filename)
                    with open(filename, 'wb') as f:
                        f.write(uploaded_file.file.read())

                    # Respond with a success message
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'File uploaded successfully!')
                else:
                    # No file uploaded
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Please upload a file.')
            else:
                # Invalid content type
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid request. Please upload a file.')
        else:
            # Return 404 for other paths
            self.send_response(404)
            self.end_headers()

def start_http_server(port):
    # Start the HTTP server on the specified port with the custom request handler
    with socketserver.TCPServer(("", port), UploadHandler) as httpd:
        print(f"Serving at: http://{get_laptop_ip()}:{port}/")
        httpd.serve_forever()

if __name__ == "__main__":
    # Replace the 'port' as needed
    port_number = 8000

    # Start the HTTP server in a separate thread
    server_thread = threading.Thread(target=start_http_server, args=(port_number,))
    server_thread.daemon = True
    server_thread.start()

    # Print the web address for the phone
    print(f"Web address to be pasted in mobile browser: http://{get_laptop_ip()}:{port_number}/")
    print("Press Ctrl+C to stop the server.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nServer stopped.")

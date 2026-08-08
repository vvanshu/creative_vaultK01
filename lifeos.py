import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8502
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iris-quest")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def main():
    print(f"Starting IRIS QUEST HTTP Server...")
    print(f"Directory: {DIRECTORY}")
    print(f"Local URL: http://localhost:{PORT}")
    
    # Open default web browser to the app
    webbrowser.open(f"http://localhost:{PORT}")
    
    try:
        with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer shut down.")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

import webbrowser
import threading
from .app import create_app

def main():
    app = create_app()
    port = 5000
    url = f"http://localhost:{port}"
    
    # Open browser after short delay
    threading.Timer(1.5, lambda: webbrowser.open(url)).start()
    
    print(f"Starting Leaderbird at {url}")
    app.run(host='localhost', port=port, debug=False)

if __name__ == '__main__':
    main()
import socket
import threading

def createPackage(data, sendtoip, *ip_addresses):
    local_ip = socket.gethostbyname(socket.gethostname())
    ipaddrsfto = ','.join(ip_addresses)
    package = f"(DAT:{data},IPADDRFROM:{local_ip},IPADDRTO:{sendtoip},IPADDRSFORWARDTO:{ipaddrsfto})"
    return package

def sendPackage(package):
    # Extract the IP address from the package
    parts = package.split(",")
    ip = parts[2].split(":")[1]  # Get the sendtoip value
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, 65535))
            s.sendall(package.encode('utf-8'))
            print("Package sent.")
    except Exception as e:
        print(f"Error sending package: {e}")

def start_server(host='0.0.0.0', port=65535):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                data = receivePackage(conn)
                print(f"Received package: {data}")

def receivePackage(conn):
    try:
        response = conn.recv(65535)
        return response.decode('utf-8')
    except Exception as e:
        print(f"Error receiving package: {e}")
        return None

if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Prepare to send a package
    data = "example_data"
    sendtoip = "127.10.1.1"  # Replace with the target IP address
    ip_addresses = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]

    # Check if the sendtoip is 127.10.1.1 and send the package
    if sendtoip == "127.10.1.1":
        package = createPackage(data, sendtoip, *ip_addresses)
        print("Sending package:", package)
        sendPackage(package)

    # Keep the main thread alive to allow the server to run
    while True:
        pass  # Infinite loop to keep the script running

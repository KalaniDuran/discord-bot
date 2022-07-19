from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import json
import cgi
import sqlite3

hostName = 'localhost'
serverPort = 7080
connection = sqlite3.connect("/Users/Kalani/discord.db")
connection.row_factory = sqlite3.Row

class MyHandler(BaseHTTPRequestHandler):
    """
    Handles all requests that want to create data within the database.
    All cases are based on the URL path of the request.
    """
    def do_POST(self):
        match self.path:
            case "/createuser":
                self.createUser()
            case "/creategame":
                self.createGame()
            case "/assigngame":
                pass
            case _:
                self.default()

    """
    Handles all requests that want to retrieve data, mainly from within the database.
    All cases are based on the URL path of the request.
    """
    def do_GET(self):
        match self.path:
            case "/ping":
                self.ping()
            case "/getuser":
                self.getUser()
            case "/getgame":
                pass
            case "/getgamesplayed":
                pass
            case _:
                self.default()

    """
    Aceepts JSON input with new user information in order to create a user within the database.
    New user information is accepted in this format:
    {
        "username" : "Discord username"
    }
    """
    def createUser(self):
        ctype, _ = cgi.parse_header(self.headers.get('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        connection.execute("""
        INSERT into users(username) 
        VALUES (:username)""", message)

        connection.commit()

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes("User created", "utf-8"))

    """
    Aceepts JSON input with new user information in order to create a user within the database.
    New user information is accepted in this format:
    {
        "username" : "Discord username"
    }
    """
    def createGame(self):
        ctype, _ = cgi.parse_header(self.headers.get('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        connection.execute("""
        INSERT into games(title) 
        VALUES (:title)""", message)

        connection.commit()

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes("Game created", "utf-8"))


    """
    Aceepts JSON input user information to retrieve full user info.
    Information is accepted in this format:
    {
        "username" : "Discord username"
    }
    """
    def getUser(self):
        ctype, _ = cgi.parse_header(self.headers.get('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        result = connection.execute("""
            SELECT user_id, username
            FROM users 
            WHERE username=:username""", message).fetchall()

        connection.commit()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        for row in result:
            self.wfile.write(json.dumps(dict(row)).encode('utf-8'))


    """
    Simple ping request to check if server is up and functional.
    Returns "pong"
    """
    def ping(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("pong", "utf-8"))
    
    """
    Default case for any URL paths that aren't specifically covered.
    Returns "Request: /URLpath"
    """
    def default(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Request: %s" % self.path, "utf-8"))


if __name__ == '__main__':
    webServer = HTTPServer((hostName, serverPort), MyHandler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try: 
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
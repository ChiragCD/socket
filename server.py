import socket, time, threading, tkinter

class acceptor(object):

    buffer = ""
    
    def __init__(self, program):

        self.program = program

    def run(self):

        while(True):
            self.buffer = input()
            self.program.acceptor_handler(self.buffer)

class sender(socket.socket):

    def __init__(self, connection, program):

        print("sst")
        socket.socket.__init__(self)
        self.program = program
        self.host = "192.168.0.101"
        self.port = 2000
        self.bind((self.host, self.port))
        self.connect(connection)
        print("sender")

    def run(self, msg):
        
        self.send(msg.encode("utf-8"))
                
    def end(self):

        self.close()

class receiver(socket.socket):

    buffer = ""

    def __init__(self, program):

        print("rst")
        socket.socket.__init__(self)
        self.program = program
        self.host = "192.168.0.101"
        self.port = 2001
        self.bind((self.host, self.port))
        self.listen(1)
        print("wefjfi")
        connection, self.program.connection = self.accept()
        print("receiver")

    def run(self):

        while(True):
            self.buffer = self.recv(1024).decode("utf-8")
            self.program.receiver_handler(self.buffer)

    def end(self):

        self.close()

class output(object):

    def __init__(self, program):

        self.program = program
        self.window = tkinter.Tk()
        self.var = tkinter.StringVar()
        self.var.set("Start")
        box = tkinter.Message(self.window, textvariable = self.var)
        box.pack()

    def manage(self, msg, alignment):

        if(alignment == LEFT):
            adjusted_message = msg.ljust(100)
        elif(alignment == RIGHT):
            adjusted_message = msg.rjust(100)
        self.text += '\n' + adjusted_message
        self.var.set(self.text)
    
class node(object):

    end = False

    def __init__(self):

        self.connection = ""
        self.receiver = receiver(self)
        self.sender = sender(connection, self)
        self.acceptor = acceptor(self)
        self.output = output(self)

        self.control()

    def control(self):

        self.acceptor_thread = threading.Thread(target = self.acceptor.run)
        self.receiver_thread = threading.Thread(target = self.receiver.run)
        self.output_thread = threading.Thread(target = self.output.window.mainloop)

        self.acceptor_thread.start()
        self.receiver_thread.start()
        self.output_thread.start()

    def acceptor_handler(self, msg):

        self.sender.run(msg)
        self.output.manage(msg, RIGHT)
        if(msg == "close"):
            self.end()

    def receiver_handler(self, msg):

        self.output.manage(msg, LEFT)
        if(msg == "close"):
            self.end()
        
    def end(self):

        self.acceptor_thread.exit()
        self.receiver_thread.exit()
        self.receiver.end()
        self.sender.end()

node()

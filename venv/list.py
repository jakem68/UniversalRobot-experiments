class List:

    def __init__(self, name):
        self.name = name
        self.items = []

    def store_item(self, this_item):
        self.items.append(this_item)
        pass

    def send_item(self, socket):
        try:
            this_item = self.items.pop()
            socket.sendall(this_item.encode('utf-8'))
            print("item {0} sent to socket".format(this_item.encode('utf-8')))
        except:
            print("List is empty")
            socket.sendall("EOF".encode('utf-8'))
            pass
        pass

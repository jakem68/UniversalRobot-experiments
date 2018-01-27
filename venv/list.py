class List:

    def __init__(self, name):
        self.name = name
        self.items = []

    def store_item(self, this_item):
        self.items.append(this_item)
        pass

    def send_item(self, socket):
        this_pose = self.poses.pop()
        if this_pose != '':
            socket.sendall(this_pose.encode('utf-8'))
            print("item sent to socket")
        else:
            print("List is empty")
        pass

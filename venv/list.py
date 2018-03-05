import tempfile, time, os
import json

class List():

    def __init__(self, name):
        self.name = name
        self.items = []

    def store_item(self, this_item):
        self.items.append(this_item)
        pass

    def send_item(self, socket):
        try:
            this_item = self.items.pop(0)
            socket.sendall(this_item.encode('utf-8'))
            print("item {0} sent to socket".format(this_item.encode('utf-8')))
        except:
            print("List is empty")
            socket.sendall("EOF".encode('utf-8'))
            pass
        pass

    def send_nr_leaks(self, socket):
        # create json format of list
        json_list = json.dumps(self.items)

        # create filename
        ts = time.strftime("%Y%m%d-%H%M%S")
        filename = 'leakRecording'+ts+'.txt'
        tempdir = tempfile.gettempdir()
        file = os.path.join(os.path.sep, tempdir, filename)
        print(file)

        # write json format list to file
        f = open('%s' % file, 'w')
        f.write(json_list)
        f.close()

        # start counting the leaks
        nr_leaks = 0
        try:
            for item in self.items:
                this_valuelist_str = item.split(",")
                this_value_leakstatus = this_valuelist_str[6][:-1]
                if this_value_leakstatus == "1":
                    print("leak found")
                    nr_leaks += 1
            print("just before sending")
            str_nr_leaks = "("+str(nr_leaks)+")"
            print(str_nr_leaks)
            socket.sendall(str_nr_leaks.encode('utf-8'))
            print("nr_leaks found is {0}".format(str(nr_leaks).encode('utf-8')))
        except:
            print("List is empty")
            socket.sendall("EOF".encode('utf-8'))
            pass
        pass

#test

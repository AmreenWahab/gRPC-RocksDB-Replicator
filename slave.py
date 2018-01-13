'''
################################## slave.py #############################
# 
################################## slave.py #############################
'''
import grpc
import replicator_pb2
import argparse
import rocksdb 

PORT = 3000

slavedb = rocksdb.DB("slavedb1.db", rocksdb.Options(create_if_missing=True))

class Slave():
    
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = replicator_pb2.ReplicatorStub(self.channel)
        
    def run(self):
        
        action = self.stub.slaveConnector(replicator_pb2.SlaveRequest())
        for a in action:
            if a.action == 'put':
                print("# Put {} : {} to slave db".format(a.key, a.value))
                #inserting data into slave db
                slavedb.put(a.key.encode(), a.value.encode())
                print ("# Successfulyy added data to slavedb")
                
                #fetch value from slave db to check
                v = (slavedb.get(a.key.encode())).decode()
                print ("# Key in slave db : "+a.key+"     Value in slavedb : " + v)
                print("")

            elif a.action == 'delete':
                print ("# Delete {} from slave db".format(a.key))
                #deleting data from slave db
                slavedb.delete(a.key.encode())
                print ("# Successfully deleted")
                print("")

    
if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("host", help="ip")
        args = parser.parse_args()
        print("Slave is connecting to Server at {} : {}...".format(args.host, PORT))
        slave = Slave(host=args.host)
        slave.run()

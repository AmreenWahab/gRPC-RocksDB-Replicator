'''
################################## client.py #############################
# 
################################## client.py #############################
'''
import grpc
import replicator_pb2
import argparse

PORT = 3000

class MainClient():
    
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = replicator_pb2.ReplicatorStub(self.channel)

    def put(self, key, value):
        return self.stub.put(replicator_pb2.Request(key=key ,value=value))

    def delete(self, key):
        return self.stub.delete(replicator_pb2.GetAndDeleteRequest(key=key))

    def get(self, key):
        return self.stub.get(replicator_pb2.GetAndDeleteRequest(key=key))

def main():
   
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="display a square of a given number")
    args = parser.parse_args()
    print("Client is connecting to Server at {}:{}...".format(args.host, PORT))
    client = MainClient(host=args.host)
    print(" ")
    print("---------------------------------------------------------------")
    print("")
    print ("# PUT Request 1 :  key = a   value = foo ")
    resp = client.put('a','foo')
    print ("# PUT Response 1 : key = " +resp.key + "value = "+resp.value)
    print(" ")
    print("---------------------------------------------------------------")
    print("")
    print ("# PUT Request 2 :  key = b   value = bar ")
    resp1 = client.put('b','bar')
    print ("# PUT Response 2 : key = " +resp1.key + "   value = "+resp1.value)
    print("")
    print("---------------------------------------------------------------")
    print("")
    print("# DELETE Request  1 :  key =  " + resp.key)
    resp2 = client.delete(resp.key)
    print("# DELETE Response 1 : key deleted = " +resp2.key+"  value deleted = " +resp2.value) 
    print("")
    print("---------------------------------------------------------------")
    print("")
    print("# GET Request 1 : key = "+resp1.key)
    resp3 = client.get(resp1.key)
    print("# GET Response 1 : key  = " +resp3.key+"  value  = " +resp3.value) 
    
if __name__ == "__main__":
    main()

'''
################################## server.py #############################
# Lab1 gRPC RocksDB Server 
################################## server.py #############################
'''
import time
import grpc
import replicator_pb2
import replicator_pb2_grpc
import rocksdb
import queue
#import Queue
from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class ReplicatorServicer(replicator_pb2.ReplicatorServicer):
    def __init__(self):
        self.db = rocksdb.DB("masterdb.db", rocksdb.Options(create_if_missing=True))
        self.queue= queue.Queue()

    def replicate(db_action):
        #decorator to replicate db operations
        def wrapper(self, request, context): 
            #delete request contains only key , so fetch value from db to meet SlaveResponse format
            if(db_action.__name__=="delete"):
                value = (self.db.get(request.key.encode()))
                action = replicator_pb2.SlaveResponse(action = db_action.__name__, key=request.key.encode(), value=value)
            else:
                #put request contains both key and value which encoded to be put into db
                action = replicator_pb2.SlaveResponse(action = db_action.__name__, key=request.key.encode(), value=request.value.encode())
            #add db operations to a queue in the form of a response
            self.queue.put(action)
            return db_action(self, request, context)
        return wrapper


    def slaveConnector(self, request, context):
        '''
        slave connects with master and master sends db_actions from queue to slave
        busy-wait loop
        '''
        #add counter to keep track of requests
        counter = 1 
        print ("Slave Connected")
        while True:
            while not self.queue.empty():
                    #send each request to slave from the operations queue
                    print("Replicating request :  "+ str(counter) +"  to slave")
                    #increment counter with each request replicated at slave side
                    counter = counter + 1
                    yield self.queue.get() 
                    

    @replicate
    def put(self, request, context):
        print ("## PUT REQUEST")
        #add data into client db
        self.db.put(request.key.encode(), request.value.encode())
        return replicator_pb2.Response(key=request.key,value=request.value)
    
    @replicate
    def delete(self, request, context):
        print ("## DELETE REQUEST")
        value = (self.db.get(request.key.encode())).decode()
        #delete data from client db
        self.db.delete(request.key.encode())
        return replicator_pb2.Response(key=request.key, value=value)

    def get(self, request, context):
        print ("## GET REQUEST")
        #fetch data from client db
        value = (self.db.get(request.key.encode())).decode()
        return replicator_pb2.Response(key=request.key, value=value)


def run(host, port):
    '''
        Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    replicator_pb2_grpc.add_ReplicatorServicer_to_server(ReplicatorServicer(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print ("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 3000)

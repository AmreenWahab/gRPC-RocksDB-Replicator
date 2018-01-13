# gRPC-RocksDB-Replicator
Implementing a RocksDB replication in Python using the design from this [C++ replicator.](https://medium.com/@Pinterest_Engineering/open-sourcing-rocksplicator-a-real-time-rocksdb-data-replicator-558cd3847a9d)  Differences form the replicator are: Use GRPC Python server instead of Thrift server. Exploring GRPC sync, async, and streaming.


## Create stub for client and server
```sh
docker run -it --rm --name grpc-tools -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. replicator.proto
```
## Server - master.py
```sh
docker run -p 3000:3000 -it --rm --name lab1-server -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 master.py
```
## Client - client.py
```sh
docker run -it --rm --name lab1-client -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 client.py 192.168.0.1
```
        
**Expected Output on Client**
```sh
Client is connecting to Server at 192.168.0.1:3000...
 
---------------------------------------------------------------

# PUT Request 1 :  key = a   value = foo 
# PUT Response 1 : key = avalue = foo
 
---------------------------------------------------------------

# PUT Request 2 :  key = b   value = bar 
# PUT Response 2 : key = b   value = bar

---------------------------------------------------------------

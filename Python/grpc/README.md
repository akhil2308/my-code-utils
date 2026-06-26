# Minimal gRPC (Python)

Plain server + client for [greeter.proto](greeter.proto). The Locust gRPC load-test scripts
live in `Locust/locust_grpc_scripts/`.

## 1. Install
```bash
pip install grpcio grpcio-tools
```

## 2. Generate stubs from the proto
Run this whenever the `.proto` changes — it writes `greeter_pb2.py` and `greeter_pb2_grpc.py`:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. greeter.proto
```

## 3. Run
```bash
python server.py          # terminal 1
python client.py          # terminal 2  -> "server said: Hello, akhil!"
```

> The generated `*_pb2*.py` files are build artifacts — regenerate rather than commit them.

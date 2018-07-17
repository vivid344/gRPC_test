from __future__ import print_function

import grpc

import gateway_pb2
import gateway_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50000')
    stub = gateway_pb2_grpc.AVRGatewayStub(channel)
    print('Input Number\n')
    print('1.SignUp\n2.SignIn\n3.Transaction\n4.Balance\n5.History\n')
    i = int(input())
    response = 'none'

    if i == 1:
        print('student_id:')
        student_id = input()
        print('password:')
        password = input()
        response = stub.SignUp(gateway_pb2.SignUpRequest(student_id=student_id, password=password))
        print(response.message)
    elif i == 2:
        print('student_id:')
        student_id = input()
        print('password:')
        password = input()
        response = stub.SignIn(gateway_pb2.SignInRequest(student_id=student_id, password=password))
        print(response.message)
        print('Your address:' + response.address)
    elif i == 3:
        response = stub.Transaction(
            gateway_pb2.TransactionRequest(student_id='g2118041', address='g2118023', transfer=100))
        print(response.message)
    elif i == 4:
        response = stub.Balance(gateway_pb2.BalanceRequest(student_id='g2118041'))
        print(response.message)
    elif i == 5:
        response = stub.History(gateway_pb2.HistoryRequest(student_id='g2118041'))
        print(response.message)
    else:
        pass


if __name__ == '__main__':
    run()

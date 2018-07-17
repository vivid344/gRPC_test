import sqlite3
import time
from concurrent import futures

import grpc

from gateway_pb2 import SignUpResponse, SignInResponse, TransactionResponse, BalanceResponse, HistoryResponse
from gateway_pb2_grpc import AVRGatewayServicer, add_AVRGatewayServicer_to_server

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class RouteGuideServicer(AVRGatewayServicer):
    # SignUpに関する関数
    def SignUp(self, request, context):
        print('Call SignUp')
        conn = sqlite3.connect('FinTechFront.db')
        c = conn.cursor()

        # 既にその会員idが登録されているかの確認
        count_sql = 'SELECT count(*) from USER_DATA where student_id=?'
        count = c.execute(count_sql, (request.student_id,))  # ,ないとエラー出た

        # なかった場合　
        if count.fetchone()[0] == 0:

            # TODO:公開鍵，秘密鍵，アドレスを生成する機能の追加

            sign_up_sql = 'insert into USER_DATA (student_id, password, open_key, secret_key, address) values(?, ?, ?, ?, ?)'
            data = (request.student_id, request.password, request.student_id, request.student_id, request.student_id)
            c.execute(sign_up_sql, data)
            conn.commit()
            return SignUpResponse(message='Success')
        # 既に登録されていた場合
        else:
            return SignUpResponse(message='Already')

    # SignInに関する関数
    def SignIn(self, request, context):
        print('Call SignIn')
        conn = sqlite3.connect('FinTechFront.db')
        c = conn.cursor()

        signIn_sql = 'SELECT * from USER_DATA where student_id=? AND password=?'
        signIn = c.execute(signIn_sql, (request.student_id, request.password))

        try:
            address = signIn.fetchone()[5]
        except:
            address = ''

        if address:
            return SignInResponse(message='Success', address=address)
        else:
            return SignInResponse(message='false', address='')

    def Transaction(self, request, context):
        print('Call Transaction')

        # TODO:トランザクション生成する機能の追加

        return TransactionResponse(message='Transaction')

    def Balance(self, request, context):
        print('Call Balance')

        # TODO:idからアドレス参照，上にアドレスを投げて，残高を確認する機能の追加

        return BalanceResponse(message='Balance', transfer='150.35')

    def History(self, request, context):
        print('Call History')

        # TODO:idからアドレス参照，上にアドレスを投げて，取引履歴を確認する機能の追加

        return HistoryResponse(message='History')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_AVRGatewayServicer_to_server(RouteGuideServicer(), server)
    server.add_insecure_port('[::]:50000')
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

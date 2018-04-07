import os
import httplib

import tornado.ioloop
import tornado.web
import json


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, it's works!")


class LoanHandler(tornado.web.RequestHandler):

    UNDECIDED = 'Undecided'
    DECLINED = 'Declined'
    APPROVED = 'Approved'

    AMOUNT_TO_LOAN = 50000

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def __validate_amount_loan(self, amount):
        if self.AMOUNT_TO_LOAN == amount:
            return self.UNDECIDED
        return self.DECLINED if amount > self.AMOUNT_TO_LOAN else self.APPROVED

    def post(self):
        try:
            data = json.loads(self.request.body)
            if 'amount' in data:
                amount = float(data['amount'])
                message = self.__validate_amount_loan(amount)
                status = httplib.OK
            else:
                message = 'Amount is required.'
                status = httplib.BAD_REQUEST

            response = {'message': message}
            self.set_status(status)
            self.write(response)

        except Exception as e:
            self.set_status(httplib.INTERNAL_SERVER_ERROR)
            message = {'message': e.message}
            self.write(message)
 
    def options(self):
        self.set_status(httplib.OK)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/loan", LoanHandler),
    ], debug=True, autoreload=False)


if __name__ == "__main__":
    app = make_app()
    app.listen(int(os.environ.get('PORT', 8888)))
    tornado.ioloop.IOLoop.current().start()

import os
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, it's works!")


class LoanHandler(tornado.web.RequestHandler):

    UNDECIDED = 'Undecided'
    DECLINED = 'Declined'
    APPROVED = 'Approved'

    AMOUNT_TO_LOAN = 50000

    def __validate_amount_loan(self, amount):
        if self.AMOUNT_TO_LOAN == amount:
            return self.UNDECIDED
        return self.DECLINED if amount > 50000 else self.APPROVED

    def post(self):
        try:
            data = self.request.arguments
            if 'amount' in data:
                amount = float(data['amount'][0])
                message = self.__validate_amount_loan(amount)
                status = 200
            else:
                message = 'Amount is required.'
                status = 400

            response = {'message': message}
            self.set_status(status)
            self.write(response)

        except Exception as e:
            self.set_status(500)
            message = {'message': e.message}
            self.write(message)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/loan", LoanHandler),
    ], debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(int(os.environ.get('PORT', 8888)))
    tornado.ioloop.IOLoop.current().start()

from tornado.testing import AsyncHTTPTestCase

import app
import json
import httplib


class TestTornadoTestApp(AsyncHTTPTestCase):

    def get_app(self):
        return app.make_app()

    def test_homepage(self):
        response = self.fetch('/')
        self.assertEqual(response.code, httplib.OK)
        self.assertEqual(response.body, "Hello, it's works!")

    def test_loan_approved(self):
        response = self.fetch('/loan', body=json.dumps({'amount': app.LoanHandler.AMOUNT_TO_LOAN - 1}), method="POST")
        self.assertEqual(response.code, httplib.OK)
        response_body = json.loads(response.body)
        self.assertEqual(response_body['message'], app.LoanHandler.APPROVED)

    def test_loan_declined(self):
        response = self.fetch('/loan', body=json.dumps({'amount': app.LoanHandler.AMOUNT_TO_LOAN + 1}), method="POST")
        self.assertEqual(response.code, httplib.OK)
        response_body = json.loads(response.body)
        self.assertEqual(response_body['message'], app.LoanHandler.DECLINED)

    def test_loan_undecided(self):
        response = self.fetch('/loan', body=json.dumps({'amount': app.LoanHandler.AMOUNT_TO_LOAN}), method="POST")
        self.assertEqual(response.code, httplib.OK)
        response_body = json.loads(response.body)
        self.assertEqual(response_body['message'], app.LoanHandler.UNDECIDED)

    def test_bad_request(self):
        response = self.fetch('/loan', body=json.dumps({}), method="POST")
        self.assertEqual(response.code, httplib.BAD_REQUEST)

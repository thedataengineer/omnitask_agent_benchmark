
import unittest
from shared.database import DatabaseConnection
from services.auth_service.auth_handler import AuthService
from services.billing_service.billing_handler import BillingService
from services.task_engine.task_dispatcher import TaskDispatcher
from services.gateway.gateway_router import ApiGateway

class TestMicroservicesSuite(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseConnection()
        self.auth = AuthService()
        self.billing = BillingService()
        self.task = TaskDispatcher()
        self.gateway = ApiGateway(self.auth, self.billing, self.task)

    def test_end_to_end_flow(self):
        # 1. Auth
        auth_res = self.gateway.handle_auth({'id': 'u101', 'email': 'dev@omnitask.io', 'password': 'Secr3tPassword!'})
        self.assertEqual(auth_res['status'], 200)
        self.assertTrue(self.auth.verify_token(auth_res['token']))

        # 2. Billing
        bill_res = self.gateway.handle_charge({'invoice_id': 'inv_99', 'user_id': 'u101', 'amount_cents': 5000, 'token': 'tok_visa_4242'})
        self.assertEqual(bill_res['status'], 200)
        self.assertTrue(bill_res['paid'])

        # 3. Task
        task_res = self.gateway.handle_dispatch({'job_id': 'job_01', 'user_id': 'u101', 'payload': {'action': 'sync'}})
        self.assertEqual(task_res['status'], 202)
        self.assertEqual(self.task.process_batch(1), 1)

if __name__ == '__main__':
    unittest.main()

from typing import Dict, Any

class ApiGateway:
    def __init__(self, auth_svc, billing_svc, task_svc):
        self.auth_svc = auth_svc
        self.billing_svc = billing_svc
        self.task_svc = task_svc
        self.routes = {
            '/api/v1/auth/token': self.handle_auth,
            '/api/v1/billing/charge': self.handle_charge,
            '/api/v1/tasks/dispatch': self.handle_dispatch
        }

    def handle_auth(self, body: Dict[str, Any]) -> Dict[str, Any]:
        user = self.auth_svc.register(body['id'], body['email'], body['password'])
        token = self.auth_svc.generate_token(user)
        return {'status': 200, 'token': token, 'user_id': user.id}

    def handle_charge(self, body: Dict[str, Any]) -> Dict[str, Any]:
        inv = self.billing_svc.create_invoice(body['invoice_id'], body['user_id'], body['amount_cents'])
        success = self.billing_svc.process_payment(inv.id, body['token'])
        return {'status': 200 if success else 400, 'paid': success}

    def handle_dispatch(self, body: Dict[str, Any]) -> Dict[str, Any]:
        job = self.task_svc.enqueue_job(body['job_id'], body['user_id'], body['payload'])
        return {'status': 202, 'job_id': job.id, 'state': job.status}

# OpenCode Native Direct TUI Streamed Patch

    def cors_headers(self): return True

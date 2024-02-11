from django.db import transaction


class TransactionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        transaction.set_autocommit(False)
        response = self.get_response(request)

        if response.status_code >= 500:
            transaction.rollback()
        else:
            transaction.commit()
        transaction.set_autocommit(True)
        return response

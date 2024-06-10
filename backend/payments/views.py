import json
import requests
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

stripe.api_key = settings.STRIPE_SECRET_KEY


@require_http_methods(["POST"])
@csrf_exempt
def charge_view(request):

    print('charge_view, request', request)
    try:
        # truemed_payment_session_redirect_url = 'https://bing.com'
        # Create a Truemed PaymentSession here

        url = "https://dev-api.truemed.com/payments/v1/create_payment_session"

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-truemed-api-key": settings.TRUEMED_API_KEY
        }

        idempotency_key = '0123456789' # Should be tied to current user session or something

        request_body = {
            "total_amount": 100,
            "order_items": [
                {
                    "name": "Truemed test item",
                    "amount": 100,
                    "quantity": 1,
                    "sku": "1"
                }
            ],
            "success_url": "http://localhost:3000/success_call?id={{payment_session_id}}",
            "failure_url": "http://localhost:3000/failure_call?id={{payment_session_id}}",
            "idempotency_key": idempotency_key,
            "customer_email": "conner@connerpro.com",
            "customer_name": "Conner Lambden",
            "customer_state": "CO",
            "metadata": "truemed_test"
        } # Just demo data

        response = requests.post(url, headers=headers, json=request_body)

        if response.status_code == 200:
            response_json = response.json()
            
            truemed_payment_session_redirect_url = response_json['redirect_url']
            return HttpResponse({
            json.dumps({"redirect_url": truemed_payment_session_redirect_url})
        })

        else:
            return HttpResponse(
                json.dumps({"message": f"Unable to process payment, try again."})
            )



        
    # Something else happened, completely unrelated to Stripe
    except Exception as e:
        return HttpResponse(
            json.dumps({"message": f"Unable to process payment, try again."})
        )

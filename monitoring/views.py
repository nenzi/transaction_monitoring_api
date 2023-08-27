from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .webhook import process_transaction

@csrf_exempt
@require_POST
def webhook(request):
    transaction_id = request.POST.get("transaction_id")
    if transaction_id:
        process_transaction(int(transaction_id))
        return JsonResponse({"status": "Webhook processed"})
    return JsonResponse({"status": "No action taken"})

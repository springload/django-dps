from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from .decorators import dps_result_view
from .models import Transaction


@dps_result_view
def process_transaction(request, token, result):
    """Process a pxpay transaction using the result retrieved from dps, and
       redirect to the appropriate "success" or "failure" page. """

    # once a transaction is completed, it can't be processed again, so only
    # retrieve PROCESSING transactions
    transaction = get_object_or_404(Transaction, secret=token,
                                    status=Transaction.PROCESSING)

    # save transaction result in all cases
    transaction.result_dict = result
    transaction.save()

    success = result['Success'] == '1'

    # update transaction status according to success
    if success:
        status_updated = transaction.set_status(Transaction.SUCCESSFUL)

        # if recurring payments are required, save the billing token
        content_object = transaction.content_object
        if content_object.is_recurring():
            content_object.set_billing_token(result["DpsBillingId"] or None)
    else:
        status_updated = transaction.set_status(Transaction.FAILED)

    # call the callback if it exists
    callback_name = 'transaction_succeeded' if success else \
                    'transaction_failed'
    callback = getattr(transaction.content_object, callback_name, None)
    if callback:
        redirect_url = callback(transaction, True, status_updated)
    else:
        redirect_url = None

    return HttpResponseRedirect(
        redirect_url or reverse('transaction_result', (transaction.secret, )))


def transaction_result(request, token):
    transaction = get_object_or_404(Transaction, secret=token,
                                    status__in=[Transaction.SUCCESSFUL,
                                                Transaction.FAILED])
    return render_to_response("dps/transaction_success.html", {
        "request": request,
        "transaction": transaction,
        "success": (transaction.status == Transaction.SUCCESSFUL),
    })

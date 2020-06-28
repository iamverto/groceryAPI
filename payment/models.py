from django.db import models

class Payment(models.Model):
    # order
    # mode
    # driver
    # store
    # amount
    # date
    # is_settled_by_driver
    # is_settled_to_store
    """
    create Receipt each time the admin made a settlement. calculate the all payments with order id and dates and
    details and display the 96% to payable to the store.
    TRANSACTION
        receipt pdf
        date
        total amount
        total payable
        commission
    after transaction make pending amount of stores 0. and also these payments is_settled_to_store=True

    **take the pending amount from driver and mark as settle then their all payments becomes is_settled_by_driver=True
    """
    pass
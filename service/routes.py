######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Payment Store Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Payments from the inventory of payments in the PaymentShop
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import PaymentMethod
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# DELETE A PET
######################################################################
@app.route("/payments/<int:payment_type_id>", methods=["DELETE"])
def delete_payments(payment_type_id):
    """
    Delete a Payment

    This endpoint will delete a Payment based the id specified in the path
    """
    app.logger.info("Request to delete payment with id: %d", payment_type_id)

    payment = PaymentMethod.find(payment_type_id)
    if payment:
        payment.delete()

    app.logger.info("Payment with ID: %d delete complete.", payment_type_id)
    return "", status.HTTP_204_NO_CONTENT
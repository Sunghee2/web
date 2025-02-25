# -*- coding: utf-8 -*-
"""Define the Grant subminer management command.

Copyright (C) 2018 Gitcoin Core

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

from django.conf import settings
from django.core.management.base import BaseCommand

from dashboard.utils import get_tx_status, has_tx_mined
from grants.clr import predict_clr
from grants.models import Contribution, Grant
from marketing.mails import warn_subscription_failed


class Command(BaseCommand):

    help = 'calculate CLR estimates for all grants'

    def handle(self, *args, **options):
        clr_prediction_curves = predict_clr(random_data=False, save_to_db=True)

        # Uncomment these for debugging and sanity checking
        # for grant in clr_prediction_curves:
            #print("CLR predictions for grant {}".format(grant['grant']))
            #print("All grants: {}".format(grant['grants_clr']))
            #print("prediction curve: {}\n\n".format(grant['clr_prediction_curve']))

        # sanity check: sum all the estimated clr distributions - should be close to CLR_DISTRIBUTION_AMOUNT
        clr_data = [g['grants_clr'] for g in clr_prediction_curves]

        # print(clr_data)

        total_clr_funds = sum([each_grant['clr_amount'] for each_grant in clr_data[0]])
        print("allocated CLR funds:{}".format(total_clr_funds))

        print("finished CLR estimates")

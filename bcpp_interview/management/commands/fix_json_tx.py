import json
import sys
import re

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from edc_sync.models import OutgoingTransaction

from bcpp_interview.models import (
    FocusGroupItem, GroupDiscussion, InterviewRecording,
    GroupDiscussionRecording, SubjectConsent, SubjectLocator, Interview, SubjectLoss, PotentialSubject)
from call_manager.models import Call
from edc_sync.constants import SERVER


class Command(BaseCommand):

    help = ('Fix outgoing transactions on the client where natural key fields returned a string instead of '
            'list (run once on the client before transferring transactions to server)')

    def handle(self, *args, **options):

        if settings.EDC_SYNC_ROLE == SERVER:
            raise CommandError('Command may not be run on a server.')

        affected_models = {
            'focus_group': [FocusGroupItem, GroupDiscussion],
            'interview': [InterviewRecording],
            'group_discussion': [GroupDiscussionRecording],
            'group_discussion_label': [GroupDiscussion],
            'focus_group': [FocusGroupItem, GroupDiscussion],
            'group_discussion_label': [GroupDiscussion],
            'potential_subject': [Call, SubjectConsent, SubjectLocator, FocusGroupItem, Interview, SubjectLoss],
        }
        self.fix_outgoing_transactions(affected_models)

    def fix_outgoing_transactions(self, affected_models):

        sys.stdout.write('\nFixing JSON for affected outgoing transactions\n')

        for field, models in affected_models.items():
            for model in models:
                transactions = self.get_outgoing_transactions(model)
                if transactions.count() > 0:
                    saved = 0
                    for index, outgoing_transaction in enumerate(self.get_outgoing_transactions(model)):
                        json_string = outgoing_transaction.aes_decrypt(outgoing_transaction.tx)
                        json_parsed = json.loads(json_string)
                        if isinstance(json_parsed[0]['fields'][field], str):
                            json_parsed[0]['fields'][field] = self.to_natural_key(json_parsed[0]['fields'][field])
                            json_string = json.dumps(json_parsed)
                            outgoing_transaction.tx = outgoing_transaction.aes_encrypt(json_string)
                            saved += 1
                            outgoing_transaction.save()
                            sys.stdout.write('  [X] {}   {}  saved={}        \r'.format(self.get_old_tx_name(model), index, saved))
                        sys.stdout.write('  [X] {}   {}  saved={}          \r'.format(self.get_old_tx_name(model), index, saved))
                    sys.stdout.write('\n')
                else:
                    sys.stdout.write('  [ ] {}   {}\n'.format(self.get_old_tx_name(model), 0))
        sys.stdout.write('Done\n\n')

    def to_natural_key(self, value):
        """Return natural key either by lookup with value if value is a 'pk' or just return value as a list."""
        if re.match('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', value):
            obj = PotentialSubject.objects.get(id=value)
            to_natural_key = obj.natural_key()
        else:
            to_natural_key = [value]
        return to_natural_key

    def get_outgoing_transactions(self, model):
        return OutgoingTransaction.objects.filter(tx_name=self.get_old_tx_name(model), is_consumed_server=False)

    def get_tx_name(self, model):
        return '{}.{}'.format(model._meta.app_label, model._meta.model_name.lower())

    def get_old_tx_name(self, model):
        return model._meta.object_name

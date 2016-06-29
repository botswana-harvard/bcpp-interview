import json
import sys

from django.core.management.base import BaseCommand
from edc_sync.models.incoming_transaction import IncomingTransaction

from bcpp_interview.models import (
    FocusGroupItem, GroupDiscussion, InterviewRecording,
    GroupDiscussionRecording, SubjectConsent, SubjectLocator, Interview, SubjectLoss)


class Command(BaseCommand):

    help = 'Fix incoming transactions where natural key fields returned a string instead of list (run once before deserialization)'

    def handle(self, *args, **options):

        affected_models = {
            'focus_group': [FocusGroupItem, GroupDiscussion],
            'interview': [InterviewRecording],
            'group_discussion': [GroupDiscussionRecording],
            'group_discussion_label': [GroupDiscussion],
            'potential_subject': [SubjectConsent, SubjectLocator, FocusGroupItem, Interview, SubjectLoss],
            'focus_group': [FocusGroupItem, GroupDiscussion],
            'group_discussion_label': [GroupDiscussion],
        }

        sys.stdout.write('\nFixing JSON for affected incoming transactions\n')

        for field, models in affected_models.items():
            for model in models:
                transactions = self.get_incoming_transactions(model)
                if transactions.count() > 0:
                    saved = 0
                    for index, incoming_transaction in enumerate(self.get_incoming_transactions(model)):
                        json_string = incoming_transaction.aes_decrypt(incoming_transaction.tx)
                        json_parsed = json.loads(json_string)
                        if isinstance(json_parsed[0]['fields'][field], str):
                            json_parsed[0]['fields'][field] = [json_parsed[0]['fields'][field]]
                            json_string = json.dumps(json_parsed)
                            incoming_transaction.tx = incoming_transaction.aes_encrypt(json_string)
                            saved += 1
                            incoming_transaction.save()
                            sys.stdout.write('  [X] {}   {}  saved={}        \r'.format(self.get_old_tx_name(model), index, saved))
                        sys.stdout.write('  [X] {}   {}  saved={}          \r'.format(self.get_old_tx_name(model), index, saved))
                    sys.stdout.write('\n')
                else:
                    sys.stdout.write('  [ ] {}   {}\n'.format(self.get_old_tx_name(model), 0))
        sys.stdout.write('Done\n\n')

    def get_incoming_transactions(self, model):
        return IncomingTransaction.objects.filter(tx_name=self.get_old_tx_name(model), is_consumed=False)

    def get_tx_name(self, model):
        return '{}.{}'.format(model._meta.app_label, model._meta.model_name.lower())

    def get_old_tx_name(self, model):
        return model._meta.object_name

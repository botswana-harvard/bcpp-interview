from edc_sync.models import SyncHistoricalRecords

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_registration.models import RegisteredSubjectModelMixin


class RegisteredSubject(RegisteredSubjectModelMixin, BaseUuidModel):

    history = SyncHistoricalRecords()

    class Meta:
        app_label = 'registration'

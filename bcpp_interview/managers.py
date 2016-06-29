from django.db import models


class SubjectLocationManager(models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(potential_subject__subject_identifier=subject_identifier)


class SubjectLocatorManager(models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(potential_subject__subject_identifier=subject_identifier)


class NurseConsentManager(models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class SubjectConsentManager(models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class PotentialSubjectManager(models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class InterviewManager(models.Manager):
    def get_by_natural_key(self, reference):
        return self.get(reference=reference)


class FocusGroupManager(models.Manager):

    def get_by_natural_key(self, reference):
        return self.get(reference=reference)


class FocusGroupItemManager(models.Manager):

    def get_by_natural_key(self, reference, subject_identifier):
        return self.get(focus_group__reference=reference, potential_subject__subject_identifier=subject_identifier)


class SubjectLossManager(models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class GroupDiscussionLabelManager(models.Manager):

    def get_by_natural_key(self, discussion_label):
        return self.get(discussion_label=discussion_label)

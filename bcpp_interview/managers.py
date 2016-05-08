from django.db import models


class InterviewManager(models.Manager):
    def get_by_natural_key(self, interview_identifier):
        return self.get(interview_identifier=interview_identifier)


class SubjectGroupManager(models.Manager):

    def get_by_natural_key(self, group_name):
        return self.get(group_name=group_name)


class SubjectGroupItemManager(models.Manager):

    def get_by_natural_key(self, subject_group, subject_consent):
        return self.get(subject_group=subject_group, subject_consent=subject_consent)


class RecordingManager(models.Manager):

    def get_by_natural_key(self, sound_filename):
        return self.get(sound_filename=sound_filename)

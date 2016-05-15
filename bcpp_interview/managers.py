from django.db import models


class InterviewManager(models.Manager):
    def get_by_natural_key(self, interview_identifier):
        return self.get(interview_identifier=interview_identifier)


class SubjectGroupManager(models.Manager):

    def get_by_natural_key(self, group_name):
        return self.get(group_name=group_name)


class SubjectGroupItemManager(models.Manager):

    def get_by_natural_key(self, subject_group, subject_identifier):
        return self.get(subject_group=subject_group, potential_subject__subject_identifier=subject_identifier)


class RecordingManager(models.Manager):

    def get_by_natural_key(self, sound_filename):
        return self.get(sound_filename=sound_filename)


class SubjectLossManager(models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class GroupDiscussionLabelManager(models.Manager):

    def get_by_natural_key(self, discussion_label):
        return self.get(discussion_label=discussion_label)

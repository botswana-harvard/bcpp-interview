"""
Working script

Update RawData with 35 recs from KW where 30 are new and 4 are updates to existing data.

1?

"""

import csv
from dateutil import parser

from django.db import IntegrityError

from bcpp_interview.models import RawData, PotentialSubject, SubjectLocation, SubjectLocator
from edc_map.exceptions import MapperError
from datetime import date

csv_filename = '/Users/erikvw/Documents/bcpp/bcpp_interview/pairs1to10_subjects_pims_final_erik2.csv'
added = 0
updated = 0

with open(csv_filename, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    header = None
    for recs, row in enumerate(reader):
        if not header:
            header = row
        else:
            try:
                obj = RawData.objects.create(**row)
                obj.source = 'kathleen'
                obj.save()
                added += 1
            except IntegrityError:
                # update the existing record
                obj = RawData.objects.get(subject_identifier=row.get('subject_identifier'))
                obj.category = row['category']
                obj.sub_category = row['sub_category']
                obj.issue = row['issue']
                obj.elig_cat = row['elig_cat']
                obj.source = 'updated kw'
                obj.save()
                updated += 1


""" Update existing Potential Subjects with data from KW."""

for obj in PotentialSubject.objects.filter(pair__gt=5):
    raw_data = RawData.objects.get(subject_identifier=obj.subject_identifier)
    if obj.category != raw_data.category or obj.sub_category != raw_data.sub_category:
        obj.category = raw_data.category
        obj.sub_category = raw_data.sub_category
        obj.source = 'updated_kw'
        obj.save()

""" Add new Potential Subjects. """
added = 0
for obj in RawData.objects.filter(pair__gt=5):
    try:
        PotentialSubject.objects.create(
            first_name=obj.first_name,
            last_name=obj.last_name,
            subject_identifier=obj.subject_identifier,
            identity=obj.identity,
            dob=parser.parse(obj.dob),
            gender=obj.gender,
            category=obj.category,
            sub_category=obj.sub_category,
            community=obj.community,
            pair=obj.pair,
            source='kathleen'
        )
        added += 1
    except IntegrityError:
        pass


""" Update subject location. """
for obj in PotentialSubject.objects.filter(source='kathleen'):
    try:
        obj = RawData.objects.get(subject_identifier=obj.subject_identifier)
        try:
            SubjectLocation.objects.create(
                subject_identifier=obj.subject_identifier,
                gps_confirm_latitude=obj.latitude,
                gps_confirm_longitude=obj.longitude,
                community=obj.community,
            )
        except MapperError as e:
            print(str(e))
        except IntegrityError:
            print(str(e))
    except RawData.DoesNotExist:
        pass


""" Update subject locator """
csv_filename = '/Users/erikvw/Documents/bcpp/bcpp_interview/locator20160811.csv'
field_list = [field.name for field in SubjectLocator._meta.fields]
added = 0
with open(csv_filename, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    header = None
    for recs, row in enumerate(reader):
        if not header:
            header = row
            columns_to_remove = [f for f in header if f not in field_list]
        else:
            subject_identifier = row.get('subject_identifier')
            try:
                potential_subject = PotentialSubject.objects.get(
                    subject_identifier=subject_identifier)
                for k in columns_to_remove:
                    row.pop(k, None)
                row['date_signed'] = parser.parse(row['date_signed'])
                # row['report_datetime'] = parser.parse(row['report_datetime'])
                SubjectLocator.objects.create(potential_subject=potential_subject, **row)
                added += 1
            except IntegrityError:
                pass
            except PotentialSubject.DoesNotExist:
                pass


""" Call manager """

from edc_call_manager.caller_site import site_model_callers

model_caller = site_model_callers._registry['model_callers']['subjects']
scheduled = None

for obj in PotentialSubject.objects.filter(source='kathleen'):
    options = model_caller.personal_details_from_subject(obj)
    options['potential_subject'] = obj
    call = model_caller.call_model.objects.create(
        scheduled=scheduled or date.today(),
        label=model_caller.label,
        repeats=model_caller.repeats,
        **options)
    model_caller.log_model.objects.create(
        call=call,
        locator_information=model_caller.get_locator(obj))

"""
A few methods to help extract data from bcpp.

either you are on the bcpp server console or have a bcpp virtualenv and tunnel to bcpp mysql

To get locator data from bcpp:

    from bcpp_interview import get_locator_dataframe, identity, decrypt_locator, get_consent_dataframe, decrypt_consent
    df_locator = get_locator_dataframe()
    decrypt_locator(df_locator)  # takes a long time
    df_consent = get_consent_dataframe()
    decrypt_consent(df_consent)  # takes a long time

"""

import pandas as pd
import numpy as np
from django.core.exceptions import ImproperlyConfigured
from edc.core.crypto_fields.classes import FieldCryptor
from bhp066.apps.bcpp_subject.models import SubjectConsent, SubjectLocator
from M2Crypto.RSA import RSAError

consent_columns = {
    'subject_identifier': 'subject_identifier',
    'first_name': 'first_name',
    'last_name': 'last_name',
    'identity': 'identity',
    'gender': 'gender',
    'dob': 'dob',
    'household_member__household_structure__household__plot__plot_identifier': 'plot_identifier',
    'household_member__household_structure__household__plot__gps_target_lat': 'gps_target_lat',
    'household_member__household_structure__household__plot__gps_target_lon': 'gps_target_lon',
}

locator_columns = {
    'subject_visit__household_member__registered_subject__subject_identifier': 'subject_identifier',
    'alt_contact_cell': 'alt_contact_cell',
    'alt_contact_cell_number': 'alt_contact_cell_number',
    'alt_contact_name': 'alt_contact_name',
    'alt_contact_rel': 'alt_contact_rel',
    'alt_contact_tel': 'alt_contact_tel',
    'consent_version': 'consent_version',
    'contact_cell': 'contact_cell',
    'contact_name': 'contact_name',
    'contact_phone': 'contact_phone',
    'contact_physical_address': 'contact_physical_address',
    'contact_rel': 'contact_rel',
    'date_signed': 'date_signed',
    'has_alt_contact': 'has_alt_contact',
    'home_visit_permission': 'home_visit_permission',
    'mail_address': 'mail_address',
    'may_call_work': 'may_call_work',
    'may_contact_someone': 'may_contact_someone',
    'may_follow_up': 'may_follow_up',
    'may_sms_follow_up': 'may_sms_follow_up',
    'other_alt_contact_cell': 'other_alt_contact_cell',
    'physical_address': 'physical_address',
    'report_datetime': 'report_datetime',
    'subject_cell': 'subject_cell',
    'subject_cell_alt': 'subject_cell_alt',
    'subject_phone': 'subject_phone',
    'subject_phone_alt': 'subject_phone_alt',
    'subject_visit': 'subject_visit',
    'subject_work_phone': 'subject_work_phone',
    'subject_work_place': 'subject_work_place'}

consent_encrypted_columns = {
    'first_name': ['rsa', 'local'],
    'last_name': ['rsa', 'restricted'],
    'identity': ['rsa', 'restricted'],
    'gps_target_lat': ['rsa', 'local'],
    'gps_target_lon': ['rsa', 'local'],
}

locator_encrypted_columns = {
    'alt_contact_cell_number': ['rsa', 'local'],
    'alt_contact_name': ['rsa', 'local'],
    'alt_contact_rel': ['rsa', 'local'],
    'alt_contact_cell': ['rsa', 'local'],
    'other_alt_contact_cell': ['rsa', 'local'],
    'alt_contact_tel': ['rsa', 'local'],
    'mail_address': ['aes', 'local'],
    'physical_address': ['aes', 'local'],
    'subject_cell': ['rsa', 'local'],
    'subject_cell_alt': ['rsa', 'local'],
    'subject_phone': ['rsa', 'local'],
    'subject_phone_alt': ['rsa', 'local'],
    'subject_work_place': ['aes', 'local'],
    'subject_work_phone': ['rsa', 'local'],
    'contact_name': ['rsa', 'local'],
    'contact_rel': ['rsa', 'local'],
    'contact_physical_address': ['aes', 'local'],
    'contact_cell': ['rsa', 'local'],
    'contact_phone': ['rsa', 'local'],
}


def get_consent_dataframe():
    """Return the SubjectConsent data as a dataframe (encrypted fields still encrypted)."""
    qs = SubjectConsent.objects.all()
    qs = qs.values_list(*consent_columns.keys())
    dataframe = pd.DataFrame(list(qs), columns=consent_columns.keys())
    dataframe.rename(columns=consent_columns, inplace=True)
    dataframe.fillna(value=np.nan, inplace=True)
    for column in list(dataframe.select_dtypes(include=['datetime64[ns, UTC]']).columns):
        dataframe[column] = dataframe[column].astype('datetime64[ns]')
    return dataframe


def get_locator_dataframe():
    """Return the SubjectLocator data as a dataframe (encrypted fields still encrypted)."""
    qs = SubjectLocator.objects.all()
    qs = qs.values_list(*locator_columns.keys())
    dataframe = pd.DataFrame(list(qs), columns=locator_columns.keys())
    dataframe.rename(columns=locator_columns, inplace=True)
    dataframe.fillna(value=np.nan, inplace=True)
    for column in list(dataframe.select_dtypes(include=['datetime64[ns, UTC]']).columns):
        dataframe[column] = dataframe[column].astype('datetime64[ns]')
    return dataframe


def decrypt_by_column(df, columns):
    """Return the dataframe with columns decrypted."""
    for column, algorithm in columns.items():
        df[column] = df.apply(lambda row: decrypt(row, algorithm, column_name=column), axis=1)
    return df


def decrypt_locator(df):
    """Return the locator dataframe with columns decrypted."""
    return decrypt_by_column(df, locator_encrypted_columns)


def decrypt_consent(df):
    """Return the locator dataframe with columns decrypted."""
    return decrypt_by_column(df, consent_encrypted_columns)


def decrypt(row, algorithm, column_name):
    value = np.nan
    if pd.notnull(row[column_name]):
        field_cryptor = FieldCryptor(*algorithm)
        try:
            value = field_cryptor.decrypt(row[column_name])
            if value.startswith('enc1::'):
                raise ImproperlyConfigured(
                    'Cannot decrypt identity, specify path to the encryption keys in settings.KEYPATH')
        except RSAError:
            value = row[column_name]
            print('RSAError', column_name, algorithm)
    return value

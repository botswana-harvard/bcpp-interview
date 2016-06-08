import pandas as pd
import numpy as np


class EdcModelToDataFrame(object):
    """
        e = EdcModelToDataFrame(ClinicVlResult, add_columns_for='clinic_visit')
        my_df = e.dataframe
    """

    def __init__(self, model=None, queryset=None, query_filter=None, add_columns_for=None):
        self._columns = []
        self.dataframe = pd.DataFrame()
        query_filter = query_filter or {}
        self.queryset = queryset or model.objects.all()
        self.model = model or self.queryset.model
        if self.queryset.count() > 0:
            self.model = model or self.queryset.model
            self.values_list = self.queryset.values_list(*self.columns.keys()).filter(**query_filter)
            self.dataframe = pd.DataFrame(list(self.values_list), columns=self.columns.keys())
            self.dataframe.rename(columns=self.columns, inplace=True)
            self.dataframe.fillna(value=np.nan, inplace=True)
            for column in list(self.dataframe.select_dtypes(include=['datetime64[ns, UTC]']).columns):
                self.dataframe[column] = self.dataframe[column].astype('datetime64[ns]')

    def __repr__(self):
        return '{}({}.{})'.format(
            self.__class__.__name__, self.model._meta.app_label, self.model._meta.model_name)

    def __str__(self):
        return '{}.{}'.format(self.model._meta.app_label, self.model._meta.model_name)

    @property
    def columns(self):
        if not self._columns:
            columns = self.remove_sys_columns(list(self.queryset[0].__dict__.keys()))
            self._columns = dict(zip(columns, columns))
        return self._columns

    def remove_sys_columns(self, columns):
        names = ['_state', '_user_container_instance', 'using']
        for name in names:
            try:
                columns.remove(name)
            except ValueError:
                pass
        return columns

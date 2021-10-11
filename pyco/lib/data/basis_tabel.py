from typing import Union

import pyco.model as pycom
import pandas as pd

class BasisTabel(object):

    KOLOMMEN = None  # should be a list
    DATA = None     # should be a list

    def __init__(self):
        pass

    def _check_data_KOLOMMEN(self):
        if not isinstance(self.KOLOMMEN, list) and not isinstance(self.KOLOMMEN, tuple):
            raise ValueError('tabel heeft geen KOLOM gegevens')
        if not isinstance(self.DATA, list) and not isinstance(self.DATA, tuple):
            raise ValueError('tabel heeft geen DATA gegevens')
        if len(self.DATA) <= 1:
            raise ValueError('data heeft niet genoeg rijen (minimaal 2)')
        len_kolommen = len(self.KOLOMMEN)
        if len_kolommen == 0:
            raise ValueError('data heeft geen KOLOM gegevens')
        for rij in self.DATA:
            if not isinstance(rij, list) and not isinstance(rij, tuple):
                raise ValueError('een rij in DATA is geen lijst')
            if len(rij) != len_kolommen:
                raise ValueError('een rij in DATA heeft niet juiste aantal kolommen')

    def interpoleer(self,
                    input_kolom: Union[str, pycom.Waarde],
                    input_waarde: Union[float, int, pycom.Waarde],
                    output_kolom: Union[str, pycom.Waarde]):
        self._check_data_KOLOMMEN()
        if isinstance(input_kolom, pycom.Waarde):
            input_kolom = input_kolom._export_waarde(None)
        if isinstance(input_waarde, pycom.Waarde):
            input_waarde = input_waarde._export_waarde(None)
        if isinstance(output_kolom, pycom.Waarde):
            output_kolom = output_kolom._export_waarde(None)

        index_input_kolom = self.KOLOMMEN.index(input_kolom)
        index_output_kolom = self.KOLOMMEN.index(output_kolom)

        vorige_input_waarde = self.DATA[0][index_input_kolom]
        vorige_output_waarde = self.DATA[0][index_output_kolom]

        if input_waarde <= vorige_input_waarde:
            return vorige_output_waarde

        for data_rij in self.DATA[1:]:
            rij_input_waarde = data_rij[index_input_kolom]
            rij_output_waarde = data_rij[index_output_kolom]

            if input_waarde <= vorige_input_waarde:
                interpol_waarde = vorige_output_waarde + (input_waarde - vorige_input_waarde) / (rij_input_waarde - vorige_input_waarde) * (rij_output_waarde - vorige_output_waarde)
                return interpol_waarde

            vorige_input_waarde = rij_input_waarde
            vorige_output_waarde = rij_output_waarde

        return vorige_output_waarde

    @property
    def pd_dataframe(self):
        return pd.DataFrame(self.DATA, columns=self.KOLOMMEN)

    def plot(self):
        self.pd_dataframe.plot.line()

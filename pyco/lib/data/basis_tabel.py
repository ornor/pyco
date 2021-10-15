from typing import Union

import pyco.model as pycom
import pandas as pd

class BasisTabel(object):

    KOLOMMEN = None  # should be a list
    DATA = None     # should be a list

    def __init__(self):
        self._check_data_KOLOMMEN()
        self.data = pd.DataFrame(self.DATA, columns=self.KOLOMMEN)

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

    def figuur(self, x_kolom:str=None, y_kolommen:Union[list, tuple]=None,
             titel:str=None, x_titel:str=None, y_titel:str=None,
             snijpunt:Union[list, tuple]=None, snijpunt_x_format:str='{:.2f}',
             snijpunt_y_format:str='{:.2f}', venster:bool=False):
        x_kolom = self.KOLOMMEN[0] if x_kolom is None else x_kolom
        y_kolommen = self.KOLOMMEN[1:] if y_kolommen is None else y_kolommen

        fig = pycom.Figuur(
            breedte=12,
            hoogte=12,
            raster=True,
            legenda=True,
            titel=titel,
            x_as_titel=x_titel,
            y_as_titel=y_titel,
        )

        if x_kolom not in self.KOLOMMEN:
            raise KeyError('kolomnaam niet beschikbaar:', x_kolom)
        x_kolom_data = self.data[x_kolom].to_list()

        for y_kolom in y_kolommen:
            if y_kolom not in self.KOLOMMEN:
                raise KeyError('kolomnaam niet beschikbaar:', y_kolom)
            y_kolom_data = self.data[y_kolom].to_list()
            coordinaten = list(zip(x_kolom_data, y_kolom_data))
            fig = fig.lijn(
                coordinaten=coordinaten,
                kleur=fig.volgende_kleur,
                naam=y_kolom,
            )

        if snijpunt is not None:
            if not len(snijpunt) == 2:
                raise ValueError('snijpunt is geen lijst of tuple met twee elementen')
            x_waarde = snijpunt[0]._export_waarde(None) if isinstance(snijpunt[0], pycom.Waarde) else snijpunt[0]
            y_waarde = snijpunt[1]._export_waarde(None) if isinstance(snijpunt[1], pycom.Waarde) else snijpunt[1]
            fig = fig.lijn(
                coordinaten=((x_waarde, 0), (x_waarde, y_waarde), (0, y_waarde)),
                kleur='darkgrey',
            ).tekst(
                coordinaten=((x_waarde, 0),),
                teksten=(snijpunt_x_format.format(x_waarde),),
                hor_uitlijnen='center',
                vert_uitlijnen='top',
            ).tekst(
                coordinaten=((0, y_waarde),),
                teksten=(snijpunt_y_format.format(y_waarde),),
                hor_uitlijnen='right',
                vert_uitlijnen='center',
            )

        return fig

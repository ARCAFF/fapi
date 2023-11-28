from datetime import datetime
from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.time import Time
from sunpy.io.special import read_srs
from sunpy.net import Fido, attrs as a


def download_srs(time: datetime):
    r"""
    Download SRS file for given time.

    Parameters
    ----------
    time
        Time to search for SRS file

    Returns
    -------

    """
    time = Time(time)
    tstart = time - 12 * u.hour
    tend = time + 12 * u.hour
    srs_query = Fido.search(a.Time(tstart, tend), a.Instrument.soon)
    if 'srs' not in srs_query.keys():
        raise SRSNotFoundError(f'No SRS file found for {time.isot}')
    closest_idx = np.argmin(srs_query['srs']['Start Time'] - time)
    srs_file = Fido.fetch(srs_query['srs'][closest_idx])
    if len(srs_file.errors) != 0:
        raise SRSDownloadError(f"Error downloading file {srs_query['srs']['url']}")
    return srs_file


def classify(time: datetime, hgs_latitude: float, hgs_longitude: float):
    r"""
    Create and classify an AR cutout from time and position.

    Parameters
    ----------
    time
        Date and time to use for classification.
    hgs_latitude
        Cutout centre latitude.
    hgs_longitude
        Cutout centre longitude.
    Returns
    -------
    Classification result

    """
    srs_file = download_srs(time)

    srs_path = Path(srs_file[0])
    if srs_path.exists():
        hgs_latitude = hgs_latitude << u.deg
        hgs_longitude = hgs_longitude << u.deg
        result = {
            'time': time,
            'hale_class': 'QS',
            'mcintosh_class': 'QS',
            'hgs_latitude': hgs_latitude.to_value(u.deg),
            'hgs_longitude': hgs_longitude.to_value(u.deg)
        }
        srs_table = read_srs(srs_path)
        ar_indices = srs_table['ID'] == 'I'
        ars = srs_table[ar_indices]
        if len(ars) > 0:
            # TODO diffrot the coordinate the time of the SRS file or vice versa.
            distance = np.sqrt((ars['Latitude'] - hgs_latitude)**2 + (ars['Longitude'] - hgs_longitude)**2)
            min_distance_index = np.argmin(distance)
            if distance[min_distance_index] <= 10 * u.deg:  # Arbitrary distance threshold
                result = {
                    'time': time,
                    'hale_class': ars[min_distance_index]['Mag Type'],
                    'mcintosh_class': ars[min_distance_index]['Z'],
                    'hgs_latitude': hgs_latitude.to_value(u.deg),
                    'hgs_longitude': hgs_longitude.to_value(u.deg)
                }
        return result


def detect_ars(time: datetime):
    srs_file = download_srs(time)

    srs_path = Path(srs_file[0])
    if srs_path.exists():
        detections = []
        srs_table = read_srs(srs_path)
        ar_indices = srs_table['ID'] == 'I'
        ars = srs_table[ar_indices]
        if len(ars) > 0:
            for ar in ars:
                center_lat = ar['Latitude']
                center_lon = ar['Longitude']

                bl_lat = (center_lat - 5*u.deg).to_value(u.deg)
                bl_lon = (center_lon - 5*u.deg).to_value(u.deg)
                tr_lat = (center_lat + 5*u.deg).to_value(u.deg)
                tr_lon = (center_lon + 5*u.deg).to_value(u.deg)

                detection = {'time': time,
                             "bbox": {"bottom_left": {"latitude": bl_lat, "longitude": bl_lon},
                                      "top_right": {"latitude": tr_lat, "longitude": tr_lon}},
                             "hale_class": ar['Mag Type'], "mcintosh_class": ar['Z']}
                detections.append(detection)

        return detections


class SRSNotFoundError(Exception):
    r"""No SRS file found"""
    pass


class SRSDownloadError(Exception):
    r"""Error downloading SRS file"""
    pass

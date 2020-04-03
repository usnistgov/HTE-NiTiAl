""" older version of db stores e-chem data directly as a json string.

this script extracts that json data to csv files, and removes autoranging artifacts in the process.
"""
import os
import json
import cycvolt
import dataset
import numpy as np
import pandas as pd

def load_cv(jsondata):
    cvdata = json.loads(jsondata)
    del cvdata['error_codes']
    del cvdata['current_range']
    return pd.DataFrame(cvdata)

def remove_autorange_artifacts(data):
    I = data['current']
    V = data['potential']
    segment = data['segment']

    log_I = np.zeros_like(I)
    for s in segment.unique():
        mask = segment == s
        absval = np.abs(I[mask])
        _log_current = np.log10(np.clip(absval, absval[absval > 0].min(), np.inf))
        a = cycvolt.analyze.model_autorange_artifacts(V[mask], I[mask])
        _log_current = _log_current - a
        log_I[mask] = _log_current

    return np.power(10, log_I)

if __name__ == '__main__':

    db = dataset.connect('sqlite:///data/k20-NiTiAl-v2.db')
    expt = db['experiment']

    os.makedirs('data/k20-v2-cvs', exist_ok=True)

    for row in expt.all():

        cvdata = load_cv(row['results'])
        cvdata['corrected_current'] = remove_autorange_artifacts(cvdata)
        cvdata.to_csv(f"data/k20-v2-cvs/cv_{row['id']:04d}.csv")

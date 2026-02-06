#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2025 KAPPA.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by KAPPA. Access to and use of this information is
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import pathlib

import toolz.curried as toolz


def _stem_names():
    """Returns the sequence of example stem names."""
    example_stems = ['completion_analysis', 'plot_time_series', 'plot_trajectories',
                     'plot_treatment', 'search_data_frames', 'volume_2_first_response',
                     'add_stages', 'stage_qc_results', 'change_stage_times', ]
    return example_stems


def notebook_names():
    """Returns the sequence of example notebook names."""
    result = toolz.pipe(
        _stem_names(),
        toolz.filter(lambda sn: sn not in {'add_stages', 'stage_qc_results', 'change_stage_times'}),
        toolz.map(lambda sn: str(pathlib.Path(sn).with_suffix('.ipynb'))),
    )
    return result


def ordered_script_names():
    script_name_pairs = [
        ('plot_trajectories.py', 0),
        ('plot_treatment.py', 1),
        ('plot_time_series.py', 2),
        ('completion_analysis.py', 3),
        ('volume_2_first_response.py', 4),
        ('search_data_frames.py', 5),
        ('add_stages.py', 6),
        ('stage_qc_results.py', 7),
        ('change_stage_times.py', 8),
    ]
    ordered_pairs = sorted(script_name_pairs, key=lambda op: op[1])
    ordered_names = [op[0] for op in ordered_pairs]
    difference = set(script_names()).difference(set(ordered_names))
    assert len(difference) == 0, f'Ordered set, {ordered_names},' \
                                 f' differs from, set {script_names()}' \
                                 f' by, {difference}.'
    return ordered_names


def script_names():
    """Returns the sequence of example script names."""
    result = [str(pathlib.Path(s).with_suffix('.py')) for s in _stem_names()]
    return result

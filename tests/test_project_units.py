#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2020 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import unittest.mock

from hamcrest import assert_that, equal_to

from orchid.project import Project
from orchid.project_loader import ProjectLoader
from tests.stub_net import create_stub_net_project


class TestProjectUnits(unittest.TestCase):

    def test_returns_meter_project_unit_from_net_project_length_units(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'],
                                                   project_length_unit_abbreviation='m')
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('length'), equal_to('m'))

    def test_returns_feet_project_unit_from_net_project_length_units(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'],
                                                   project_length_unit_abbreviation='ft')
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('length'), equal_to('ft'))

    def test_returns_kPa_project_unit_from_net_project_pressure_units(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'],
                                                   project_pressure_unit_abbreviation='kPa')
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('pressure'), equal_to('kPa'))

    def test_returns_psi_project_unit_from_net_project_pressure_units(self):
        stub_net_project = create_stub_net_project(well_names=['dont-care-well'],
                                                   project_pressure_unit_abbreviation='psi')
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('pressure'), equal_to('psi'))

    def test_returns_bpm_project_unit_from_net_slurry_rate_units(self):
        stub_net_project = create_stub_net_project(slurry_rate_unit_abbreviation='bbl/min',
                                                   well_names=['dont-care-well'])
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('slurry rate'), equal_to('bbl/min'))

    def test_returns_lb_per_gal_project_unit_from_net_proppant_concentration_units(self):
        stub_net_project = create_stub_net_project(
            proppant_concentration_unit_abbreviation='lb/gal (U.S.)', well_names=['dont-care-well'])
        sut = create_sut(stub_net_project)

        assert_that(sut.unit('proppant concentration'), equal_to('lb/gal (U.S.)'))


def create_sut(stub_net_project):
    patched_loader = ProjectLoader('dont_care')
    patched_loader.native_project = unittest.mock.MagicMock(name='stub_project', return_value=stub_net_project)

    sut = Project(patched_loader)
    return sut


if __name__ == '__main__':
    unittest.main()

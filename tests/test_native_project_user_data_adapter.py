#  Copyright 2017-2023 Reveal Energy Services, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#
#      http://www.apache.org/licenses/LICENSE-2.0 
#
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 
#
# This file is part of Orchid and related technologies.
#


import re
import unittest
import unittest.mock
import uuid

from hamcrest import assert_that, equal_to, calling, raises
import option
import toolz.curried as toolz

from orchid import (
    native_project_user_data_adapter as uda,
    net_stage_qc as nqc,
)

from tests import stub_net as tsn


# Test ideas
# - Set QC notes for stage ID calls `SetValue` with correct values
# - Set start stop confirmation for stage ID calls `SetValue` with correct values
class TestNativeProjectUserDataAdapter(unittest.TestCase):
    def test_canary(self):
        self.assertEqual(2 + 2, 4)

    def test_stage_qc_notes_if_qc_notes_available_for_stage(self):
        stage_id = 'b64521bf-56a2-4e9c-abca-d466670c75a1'
        expected_qc_notes = 'lucrum nugatorium provenivit'
        sut = create_sut(stage_id, qc_notes=expected_qc_notes)

        assert_that(sut.stage_qc_notes(uuid.UUID(stage_id)), equal_to(expected_qc_notes))

    def test_stage_qc_notes_empty_if_qc_notes_not_available_for_stage(self):
        stage_id = '412e5a99-7040-4972-8b27-3ff0d1ab4d94'
        sut = create_sut(stage_id)

        assert_that(sut.stage_qc_notes(uuid.UUID(stage_id)), equal_to(''))

    def test_stage_qc_notes_raises_error_if_value_has_unexpected_net_type(self):
        stage_id = tsn.DONT_CARE_ID_A
        sut = create_sut(stage_id, to_json={nqc.make_qc_notes_key(stage_id): {'Type': 'System.Int32',
                                                                              'Value': -84}})

        assert_that(calling(sut.stage_qc_notes).with_args(uuid.UUID(stage_id)),
                    raises(AssertionError,
                           pattern=re.compile('Expected, "System.String", but found ".*".')))

    def test_stage_start_stop_confirmation_if_start_stop_confirmation_available_for_stage(self):
        stage_id = '15fd59d7-da16-40bd-809b-56f9680a0773'
        expected_start_stop_confirmation = nqc.CorrectionStatus.UNCONFIRMED
        sut = create_sut(stage_id, start_stop_confirmation=expected_start_stop_confirmation)

        assert_that(sut.stage_start_stop_confirmation(uuid.UUID(stage_id)),
                    equal_to(expected_start_stop_confirmation))

    def test_stage_start_stop_confirmation_empty_if_start_stop_confirmation_not_available_for_stage(self):
        stage_id = 'f4511635-b0c1-488e-b978-e55a82c40109'
        sut = create_sut(stage_id)

        assert_that(sut.stage_start_stop_confirmation(uuid.UUID(stage_id)),
                    equal_to(nqc.CorrectionStatus.NEW))

    def test_stage_start_stop_confirmation_raises_error_if_value_has_unexpected_net_type(self):
        stage_id = tsn.DONT_CARE_ID_B
        sut = create_sut(stage_id, to_json={
            nqc.make_start_stop_confirmation_key(stage_id): {
                'Type': 'System.Double',
                'Value': 129.847},
        })

        assert_that(calling(sut.stage_start_stop_confirmation).with_args(uuid.UUID(stage_id)),
                    raises(AssertionError,
                           pattern=re.compile('Expected, "System.String", but found ".*".')))

    def test_stage_start_stop_confirmation_raises_error_if_value_not_stage_correction_status(self):
        stage_id = tsn.DONT_CARE_ID_C
        sut = create_sut(stage_id, to_json={
            nqc.make_start_stop_confirmation_key(stage_id): {
                'Type': 'System.String',
                'Value': 'Newt'},
        })

        assert_that(calling(sut.stage_start_stop_confirmation).with_args(uuid.UUID(stage_id)),
                    raises(ValueError))

    def test_set_stage_qc_notes_if_already_set_invokes_correct_calls(self):
        stage_id = '35e4a85b-7b4e-44f6-9484-7286d575d22a'
        existing_qc_notes = 'animus meus aedificio repudiat'
        sut = create_sut(stage_id, qc_notes=existing_qc_notes)
        stub_net_mutable_project_user_data = tsn.MutableProjectUserDat().create_net_stub()
        sut.dom_object.ToMutable = unittest.mock.MagicMock(return_value=stub_net_mutable_project_user_data)

        sut.set_stage_qc_notes(uuid.UUID(stage_id), 'vertet paci')

        assert_single_call_to_mutable(sut)
        assert_call_to_set_value(stub_net_mutable_project_user_data,
                                 '35e4a85b-7b4e-44f6-9484-7286d575d22a',
                                 'vertet paci', nqc.make_qc_notes_key, toolz.identity)

    def test_set_stage_qc_notes_if_not_set_invokes_correct_calls(self):
        sut = create_sut('299536d2-736c-4052-8c53-b76615552c09')
        stub_net_mutable_project_user_data = tsn.MutableProjectUserDat().create_net_stub()
        sut.dom_object.ToMutable = unittest.mock.MagicMock(return_value=stub_net_mutable_project_user_data)

        sut.set_stage_qc_notes(uuid.UUID('299536d2-736c-4052-8c53-b76615552c09'), 'lucatori dissimulant')

        assert_single_call_to_mutable(sut)
        assert_call_to_set_value(stub_net_mutable_project_user_data,
                                 '299536d2-736c-4052-8c53-b76615552c09',
                                 'lucatori dissimulant',
                                 nqc.make_qc_notes_key, toolz.identity)

    def test_set_stage_start_stop_confirmation_if_already_set_invokes_correct_calls(self):
        ante_start_stop_confirmation = nqc.CorrectionStatus.NEW
        sut = create_sut('2bb41603-a246-421a-8d77-c79ebfac8cb7', start_stop_confirmation=ante_start_stop_confirmation)
        stub_net_mutable_project_user_data = tsn.MutableProjectUserDat().create_net_stub()
        sut.dom_object.ToMutable = unittest.mock.MagicMock(return_value=stub_net_mutable_project_user_data)

        sut.set_stage_start_stop_confirmation(uuid.UUID('2bb41603-a246-421a-8d77-c79ebfac8cb7'),
                                              nqc.CorrectionStatus.CONFIRMED)

        assert_single_call_to_mutable(sut)
        assert_call_to_set_value(stub_net_mutable_project_user_data,
                                 '2bb41603-a246-421a-8d77-c79ebfac8cb7', nqc.CorrectionStatus.CONFIRMED,
                                 nqc.make_start_stop_confirmation_key, lambda v: v.value)

    def test_set_stage_start_stop_confirmation_if_not_set_invokes_correct_calls(self):
        sut = create_sut('29ee6679-6499-496c-9027-c018013640d6')
        stub_net_mutable_project_user_data = tsn.MutableProjectUserDat().create_net_stub()
        sut.dom_object.ToMutable = unittest.mock.MagicMock(return_value=stub_net_mutable_project_user_data)

        sut.set_stage_start_stop_confirmation(uuid.UUID('29ee6679-6499-496c-9027-c018013640d6'),
                                              nqc.CorrectionStatus.CONFIRMED)

        assert_single_call_to_mutable(sut)
        assert_call_to_set_value(stub_net_mutable_project_user_data,
                                 '29ee6679-6499-496c-9027-c018013640d6', nqc.CorrectionStatus.CONFIRMED,
                                 nqc.make_start_stop_confirmation_key, lambda v: v.value)


def create_sut(stage_id_text: str, qc_notes=None, start_stop_confirmation=None, to_json=None):
    stage_id = uuid.UUID(stage_id_text)
    maybe_qc_notes = option.maybe(qc_notes)
    maybe_confirmation = option.maybe(start_stop_confirmation)
    maybe_to_json = option.maybe(to_json)

    notes_stage_qc = maybe_qc_notes.map_or(lambda notes: {stage_id: {'stage_qc_notes': notes}}, {})
    confirmation_stage_qc = maybe_confirmation.map_or(
        lambda confirmation: {stage_id: {'stage_start_stop_confirmation': confirmation}}, {})
    stages_qc = toolz.merge_with(toolz.merge, [notes_stage_qc, confirmation_stage_qc])

    stub_project_user_data = tsn.ProjectUserDataDto()
    to_json = maybe_to_json.map_or(lambda json: json, {})
    if stages_qc and to_json:
        stub_project_user_data = tsn.ProjectUserDataDto(stages_qc=stages_qc, to_json=to_json)
    elif stages_qc and not to_json:
        stub_project_user_data = tsn.ProjectUserDataDto(stages_qc=stages_qc)
    elif not stages_qc and to_json:
        stub_project_user_data = tsn.ProjectUserDataDto(to_json=to_json)

    result = uda.NativeProjectUserDataAdapter(stub_project_user_data.create_net_stub())
    return result


def assert_single_call_to_mutable(sut):
    # Expect single call with no arguments
    sut.dom_object.ToMutable.assert_called_once_with()


def assert_call_to_set_value(stub_net_mutable_project_user_data, stage_id, expected_to_value, key_func,
                             transform_func):
    # Expect single call with specified arguments
    stub_net_mutable_project_user_data.SetValue.assert_called_once()
    actual_key, actual_variant = stub_net_mutable_project_user_data.SetValue.call_args_list[0].args
    assert_that(actual_key, equal_to(key_func(stage_id)))
    assert_that(actual_variant.GetValue[str](), equal_to(transform_func(expected_to_value)))


if __name__ == '__main__':
    unittest.main()

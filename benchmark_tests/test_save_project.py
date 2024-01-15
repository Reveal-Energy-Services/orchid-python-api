#  Copyright 2017-2024 KAPPA
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


import pytest

import orchid


@pytest.mark.slow
def test_save_project(benchmark):
    load_path = orchid.training_data_path().joinpath('Project_frankNstein_Permian_UTM13_FEET.ifrac')
    loaded_project = orchid.load_project(str(load_path))
    save_path = orchid.training_data_path().joinpath('Project_frankNstein_Permian_UTM13_FEET.benchmark.ifrac')
    save_path.unlink(missing_ok=True)
    benchmark(orchid.save_project, loaded_project, str(save_path))
    assert save_path.exists()
    save_path.unlink()

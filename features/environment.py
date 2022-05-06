#  Copyright (c) 2017-2022 Reveal Energy Services, Inc 
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

import pathlib


def before_all(context):
    context.loaded_projects = {}


def after_all(context):
    context.loaded_projects = {}


def after_feature(context, feature):
    if feature.name == 'Low-level example scripts':
        repository_root = pathlib.Path()
        for script_file_name in ['auto_pick.py',
                                 'auto_pick_iterate_example.py ',
                                 'auto_pick_and_create_stage_attribute.py ']:
            script_path = repository_root.joinpath(script_file_name)
            script_path.unlink(missing_ok=False)

#
#   Copyright 2023 The Foundry Visionmongers Ltd
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

# pylint: disable=no-self-use
# pylint: disable=invalid-name,redefined-outer-name
# pylint: disable=missing-class-docstring,missing-function-docstring

import pytest
import os

# This environment var must be set before the usd imports.
os.environ["TF_DEBUG"] = "OAIO_RESOLVER"
from pxr import Plug, Usd


@pytest.fixture(autouse=True)
def register_plugin():
    # plugInfo.json file for the example resolver should be installed
    # in the resources folder under the test directory.
    Plug.Registry().RegisterPlugins(os.path.join(os.getcwd(), "resources"))


def test_open_stage_and_logging(capfd):
    stage = Usd.Stage.Open("resources/empty_shot.usda")
    captured = capfd.readouterr()
    assert "_CreateIdentifier" in captured.out
    assert "_Resolve" in captured.out
    assert "_GetExtension" in captured.out
    assert "_GetAssetInfo" in captured.out
    assert "_OpenAsset" in captured.out
    assert "_GetModificationTimestamp" in captured.out
    assert "_GetExtension" in captured.out

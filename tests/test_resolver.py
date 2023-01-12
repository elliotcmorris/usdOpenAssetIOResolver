# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 The Foundry Visionmongers Ltd

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

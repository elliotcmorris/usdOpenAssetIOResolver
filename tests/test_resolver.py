# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 The Foundry Visionmongers Ltd

# pylint: disable=no-self-use
# pylint: disable=invalid-name,redefined-outer-name
# pylint: disable=missing-class-docstring,missing-function-docstring

import pytest
import os

# This environment var must be set before the usd imports.
os.environ["TF_DEBUG"] = "OPENASSETIO_RESOLVER"
from pxr import Plug, Usd, Ar


# Assume OpenAssetIO is configured as the custom primary resolver for
# all tests. If you're wondering where this is configured, it may
# just be set via the `PXR_PLUGINPATH_NAME` environment variable.

# Verify OpenAssetIO configured as the AR resolver.
@pytest.fixture(autouse=True)
def openassetio_configured():
    pr = Plug.Registry()
    plugin = pr.GetPluginWithName("usdOpenAssetIOResolver")

    assert (
        plugin is not None
    ), "OpenAssetIO is not configured as a resolver. Set `PXR_PLUGINPATH_NAME` to `plugInfo.json`"


# Set the default resolver search path to a subdirectory
def build_search_path_context(path_relative_from_file):
    script_dir = os.path.realpath(os.path.dirname(__file__))
    full_path = os.path.join(script_dir, path_relative_from_file)
    return Ar.DefaultResolverContext([path_relative_from_file])


# This test can be removed once the logging transforms, alchemy like,
# into real functionality.
def test_open_stage_and_logging(capfd):
    stage = Usd.Stage.Open("resources/empty_shot.usda")
    captured = capfd.readouterr()

    outputs = captured.out.split(os.environ["TF_DEBUG"])
    assert "UsdOpenAssetIOResolver::UsdOpenAssetIOResolver" in outputs[1]
    assert "_CreateIdentifier" in outputs[2]
    assert "_Resolve" in outputs[3]
    assert "_GetExtension" in outputs[4]
    assert "_GetAssetInfo" in outputs[5]
    assert "_OpenAsset" in outputs[6]
    assert "_GetModificationTimestamp" in outputs[7]
    assert "_GetExtension" in outputs[8]


# As all the data tends to follow the same form, convenience method
# to avoid repeating myself
def assert_parking_lot_structure(usd_stage):
    floor = usd_stage.GetPrimAtPath("/ParkingLot/ParkingLot_Floor_1")
    car1 = usd_stage.GetPrimAtPath("/ParkingLot/ParkingLot_Floor_1/Car1")
    car2 = floor.GetChild("Car2")

    assert car1.GetPropertyNames() == ["color", "spec_color"]
    assert car2.GetPropertyNames() == ["color", "spec_color"]


# Given a USD document that references an asset via a direct relative
# file path, then the asset is resolved to the file path as expected.
def test_openassetio_resolver_has_no_effect_with_no_search_path():

    stage = Usd.Stage.Open(
        "resources/integration_test_data/resolver_has_no_effect_with_no_search_path/parking_lot.usd"
    )

    assert_parking_lot_structure(stage)


# Given a USD document that references an asset via a relative search-path
# based file path, then the asset is resolved the the file path as expected.
def test_openassetio_resolver_has_no_effect_with_search_path():

    context = build_search_path_context(
        "resources/integration_test_data/resolver_has_no_effect_with_search_path/search_path_root"
    )
    stage = Usd.Stage.Open(
        "resources/integration_test_data/resolver_has_no_effect_with_no_search_path/parking_lot.usd",
        context,
    )

    assert_parking_lot_structure(stage)


# Given a USD document that recursively references multiple other USD
# documents, and expects the resolve output structured in the form of
# adjacent relative file paths, then each document can be resolved via
# OpenAssetIO.
@pytest.mark.xfail(reason="OpenAssetIO not integrated yet")
def test_recursive_resolve_to_adjacent_file_path():
    stage = Usd.Stage.Open(
        "resources/integration_test_data/recursive_resolve_to_adjacent_file_path/parking_lot.usd"
    )

    assert_parking_lot_structure(stage)


# Given a USD document that recursively references multiple other USD
# documents, and expects the resolve output structured in the form of
# search-path based file paths, then each document can be resolved via
# OpenAssetIO.
@pytest.mark.xfail(reason="OpenAssetIO not integrated yet")
def test_recursive_resolve_to_search_path():
    context = build_search_path_context(
        "resources/integration_test_data/recursive_resolve_to_search_path/search_path_root"
    )

    stage = Usd.Stage.Open(
        "resources/integration_test_data/recursive_resolve_to_search_path/parking_lot.usd",
        context,
    )

    assert_parking_lot_structure(stage)


# Given a USD document that references a second level document via an
# assetized reference resolvable by OpenAssetIO, and that second level
# document containing a non-assetized, adjacent relative file path
# reference to a third level document, then the document can be fully
# resolved.
@pytest.mark.xfail(reason="OpenAssetIO not integrated yet")
def test_assetized_child_ref_non_assetized_grandchild():
    stage = Usd.Stage.Open(
        "resources/integration_test_data/assetized_child_ref_non_assetized_grandchild/parking_lot.usd"
    )

    assert_parking_lot_structure(stage)


# Given a USD document that references a second level document via an
# non-assetized, adjacent relative file path reference, and that second
# level document containing an assetized reference resolvable by
# OpenAssetIO to a third level document, then the document can be fully
# resolved.
@pytest.mark.xfail(reason="OpenAssetIO not integrated yet")
def test_non_assetized_child_ref_assetized_grandchild():
    stage = Usd.Stage.Open(
        "resources/integration_test_data/non_assetized_child_ref_assetized_grandchild/parking_lot.usd"
    )

    assert_parking_lot_structure(stage)

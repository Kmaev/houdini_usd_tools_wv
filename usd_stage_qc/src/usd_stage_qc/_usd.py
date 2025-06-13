from pxr import Usd, UsdGeom, UsdShade
from typing import Tuple
import hou
import os


def is_usd_file(path: str) -> bool:
    """
    Checks if a given path points to an existing USD file.
    """
    if not isinstance(path, str):
        raise TypeError("Expected path to be a string")

    if not path:
        raise ValueError("Path cannot be an empty string or whitespace.")

    path = path.strip()

    usd_extensions = ('.usd', '.usda', '.usdc', '.usdz')
    return path.lower().endswith(usd_extensions) and os.path.isfile(path)


def collect_prims_without_material(stage: Usd.Stage) -> list[str]:
    """
    Traverses usd stage and collect all primitives without bound material.
    """

    start_prim = stage.GetPseudoRoot()
    iterator = iter(Usd.PrimRange(start_prim))
    no_material = []
    for prim in iterator:
        if not iterator.IsPostVisit() and prim.IsA(UsdGeom.Imageable):

            bound_material, _ = check_prim_material_binding(prim)
            if prim.IsA(UsdGeom.Mesh):
                if not bound_material or not bound_material.GetPrim().IsActive():
                    no_material.append(prim)
    return no_material


def check_prim_material_binding(prim: Usd.Prim) -> Tuple[Usd.Prim, UsdShade.Tokens]:
    """
    Checks if a primitive has material binding
    """
    mat_bind_api = UsdShade.MaterialBindingAPI(prim)
    bound_material, strength = mat_bind_api.ComputeBoundMaterial()
    return bound_material, strength


def check_live_houdini_stage(stage):
    """
    Gets a list of primitives without properly bound material in a live houdini session
    """
    mat_binds = collect_prims_without_material(stage)

    return mat_binds


def check_usd_file(stage_path: str) -> bool:
    """
    Gets a list of primitives without properly bound material
    """
    if is_usd_file(stage_path):
        stage = Usd.Stage.Open(stage_path)

        if stage is None:
            raise ValueError(f"Failed to open USD stage from file: {stage_path}")
        return collect_prims_without_material(stage)
    return None


def find_all_materials(stage: Usd.Stage) -> list[Usd.Prim]:
    """
    Collects all materials from the stage and returns the list of Usd.Prim
    """
    start_prim = stage.GetPseudoRoot()
    iterator = iter(Usd.PrimRange(start_prim))
    materials = []
    for prim in iterator:

        if prim.IsA(UsdShade.Material):
            material = UsdShade.Material(prim)
            materials.append(material)
    return materials

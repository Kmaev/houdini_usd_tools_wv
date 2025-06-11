import hou
from pxr import Usd
import os
from usd_stage_qc import _status_messages


def get_single_selected_node():
    """
    Returns a single selected Houdini node.
    """
    selected = hou.selectedNodes()

    if not selected:
        _status_messages.handle_error('No nodes were selected. Please select one node.')

    if len(selected) > 1:
        _status_messages.handle_error('More than one node was selected. Please select only one node.')

    return selected[0]


def create_and_insert_hou_node(parent_node: hou.node, type: str, name: str):
    """
    Creates and inserts a node as an output of the parent_node into a current nodes stream,
    Returns: created and inserted node
    """
    parent_pos = parent_node.position()
    context = parent_node.parent()

    inserted_node = context.createNode(type, name)
    inserted_node.setPosition(hou.Vector2(parent_pos[0], parent_pos[1] - 1))

    old_outputs = parent_node.outputs()
    for idx, output_node in enumerate(old_outputs):
        output_node.setInput(0, inserted_node)

    inserted_node.setInput(0, parent_node)

    inserted_node.setDisplayFlag(True)
    parent_node.setSelected(False)
    inserted_node.setSelected(True)
    offset_outputs_position(inserted_node)
    return inserted_node


def offset_outputs_position(root):
    """
    Runs over all the nodes connected to the selected root node and
    offset their position in Y accordingly.
    """
    queue = [root]
    while len(queue) > 0:
        current = queue.pop(0)
        if current is not root:
            pos = current.position()
            current.setPosition(hou.Vector2(pos[0], pos[1] - 1))

        for node in current.outputs():
            queue.append(node)


def compute_mat_assign_index(material_assign_node: hou.node):
    """
    Computes the next material assignment index.
    If there is only one material and its path is empty, returns the current index.
    Otherwise, increments the current material count by 1 and returns it.
    """
    mat_num = material_assign_node.parm("nummaterials").eval()

    if mat_num <= 1 and material_assign_node.parm(f"matspecpath{mat_num}").eval() == '':
        new_mat_index = mat_num
    else:
        new_mat_index = mat_num + 1
    return new_mat_index


def populate_mat_assign_parms(material_assign_node: hou.node, mat_index: int, usd_prim: Usd.Prim,
                              material_prim: Usd.Prim):
    """
    Populates the material assignment parameters for a new material entry.
    """
    material_assign_node.parm("nummaterials").set(mat_index)
    material_assign_node.parm(f"primpattern{mat_index}").set(str(usd_prim.GetPath()))
    material_assign_node.parm(f"matspecpath{mat_index}").set(str(material_prim.GetPath()))

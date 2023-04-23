
import math
import bpy
from .node_layout import NodeLayout
from bpy.types import NodeSocket


def redraw():
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)


def is_instance(node, node_type_name):
    return node.bl_idname == node_type_name


def new_node(type, context=None):
    if isinstance(context, bpy.types.Material):
        return context.node_tree.nodes.new(type=type)
    if isinstance(context, bpy.types.NodeTree):
        return context.nodes.new(type=type)
    if isinstance(context, bpy.types.bpy_prop_collection):
        return context.new(type=type)

    return bpy.ops.node.add_node(type=type)


def get_input_socket_object(node, socket):
    if isinstance(socket, NodeSocket):
        return socket
    return node.inputs[socket]


def get_output_socket(node, socket):
    if isinstance(socket, NodeSocket):
        return socket
    return node.outputs[socket]


def get_root_parent_nodes(nodes):
    root_parent_nodes = list()
    for n in nodes:
        if n.parent is None:
            root_parent_nodes.append(n)
    return root_parent_nodes


def filter_children(nodes):
    pass


def get_nodes_in_hierarchy_depth(nodes, node_tree, depth):
    if depth < 1:
        return list(nodes)

    current_depth = 1
    current_nodes_list = list(nodes)

    while current_depth <= depth:
        children_list = list()
        for n in current_nodes_list:
            children_list += get_children(n, node_tree.nodes)
        current_nodes_list = children_list
        current_depth += 1

    return current_nodes_list


def get_children(parent, nodes):
    children = list()
    for n in nodes:
        if n.parent == parent:
            children.append(n)
    return children


def get_nodes_with_image(nodes, image):
    result_nodes = list()
    for n in nodes:
        if n.image == image:
            result_nodes.append(n)
    return result_nodes


def has_children(node, nodes):
    for n in nodes:
        if n.parent == node:
            return True
    return False


def get_node_with_type(nodes, type):
    for n in nodes:
        if n.bl_idname == type:
            return n
    return None

def has_children_with_children(node, nodes):
    children = get_children(node, nodes)
    for c in children:
        if has_children(c, nodes):
            return True
    return False


def get_nodes_links(context):
    tree = context.space_data.node_tree

    # Get nodes from currently edited tree.
    # If user is editing a group, space_data.node_tree is still the base level (outside group).
    # context.active_node is in the group though, so if space_data.node_tree.nodes.active is not
    # the same as context.active_node, the user is in a group.
    # Check recursively until we find the real active node_tree:
    if tree.nodes.active:
        while tree.nodes.active != context.active_node:
            tree = tree.nodes.active.node_tree

    return tree.nodes, tree.links


def get_selected(nodes):
    selected_nodes = set()

    for node in nodes:
        if node.select:
            selected_nodes.add(node)

    return list(selected_nodes)


def select_nodes(nodes, select=True):
    for n in nodes:
        n.select = select


def get_width(node):
    return node.width


def get_height(node):
    if node.bl_idname == 'ShaderNodeTexImage':
        return 30.0 if node.hide else 251.0

    if node.hide:
        return node.height_hidden
    return node.height


def get_dimensions_fallback(node):
    dimensions = [node.dimensions[0], node.dimensions[1]]
    if dimensions[0] < 0.5:
        dimensions[0] = 240.0
    if dimensions[1] < 0.5:
        dimensions[1] = 30.0 if node.hide else 251.0
    return dimensions


def layout_nodes(nodes, layout, padding_x=60.0, padding_y=20.0, center=None):
    if layout == NodeLayout.SQUARE:
        square_layout_nodes(nodes, padding_x, padding_y, center)
    elif layout == NodeLayout.SINGLE_COLUMN:
        single_column_layout_nodes(nodes, padding_y, center)
    elif layout == NodeLayout.DUAL_STEP:
        dual_step_layout_nodes(nodes, padding_x, padding_y, center)


def get_bounds(nodes):
    first_node = nodes[0]
    w = get_width(first_node)
    h = get_height(first_node)

    left = first_node.location[0]
    up = first_node.location[1]
    right = left + w
    down = up - h

    for n in nodes:
        w = get_width(n)
        h = get_height(n)

        if left > n.location[0]:
            left = n.location[0]
        if down > n.location[1] - h:
            down = n.location[1] - h

        if right < n.location[0] + w:
            right = n.location[0] + w
        if up < n.location[1]:
            up = n.location[1]

    return left, up, right, down


def get_location_center_from_bounds(bounds):
    left = bounds[0]
    up = bounds[1]
    right = bounds[2]
    down = bounds[3]
    return [left + ((right - left) * 0.5), down + ((up - down) * 0.5)]


def get_location_center(nodes):
    bounds = get_bounds(nodes)
    return get_location_center_from_bounds(bounds)


def square_layout_nodes(nodes, padding_x=60.0, padding_y=20.0, center=None):
    node_count = len(nodes)
    if node_count <= 1:
        return
    if center is None:
        center = get_location_center(nodes)

    per_side_count = int(math.ceil(math.sqrt(node_count)))
    current_index = 0

    summed_height = 0.0
    current_max_height = 0.0
    row_heights = list()

    summed_width = 0.0
    current_summed_width = 0.0
    col_widths = list()

    for col in range(0, per_side_count):
        if current_index >= node_count:
            break
        for row in range(0, per_side_count):
            if current_index >= node_count:
                break

            current_height = get_height(nodes[current_index])
            current_width = get_width(nodes[current_index]) + padding_x
            current_summed_width += current_width

            current_index += 1

            if current_height > current_max_height:
                current_max_height = current_height

            if len(col_widths) > row:
                if current_width > col_widths[row]:
                    col_widths[row] = current_width
            else:
                col_widths.append(current_width)

        summed_height += current_max_height + padding_y
        row_heights.append(current_max_height)
        current_max_height = 0.0

        if current_summed_width > summed_width:
            summed_width = current_summed_width
        current_summed_width = 0.0

    summed_width -= padding_x
    summed_height -= padding_y

    start_loc = [center[0] - (summed_width*0.5), center[1] + (summed_height * 0.5)]
    current_loc = [start_loc[0], start_loc[1]]
    current_index = 0

    for col in range(0, per_side_count):
        current_loc[0] = start_loc[0]
        for row in range(0, per_side_count):
            if current_index >= node_count:
                return
            nodes[current_index].location = current_loc[0], current_loc[1]
            current_loc[0] += col_widths[row]
            current_index += 1

        current_loc[1] -= row_heights[col] + padding_y

def hide_nodes(nodes, hide=True, reposition=False):
    highest_node = nodes[0]
    biggest_y = nodes[0].location[1]
    second_biggest_y = nodes[0].location[1] - 1000000.0
    biggest_h = get_height(nodes[0])

    if reposition:
        for n in nodes:
            y = n.location[1]
            if biggest_y < y:
                highest_node = n
                biggest_y = y
                biggest_h = get_height(n)
        for n in nodes:
            y = n.location[1]
            if n != highest_node:
                if y != biggest_y and second_biggest_y < y:
                    second_biggest_y = y

    for n in nodes:
        old_h = get_height(n)
        n.hide = hide
        if reposition:
            y = n.location[1]
            if y < biggest_y:
                new_h = get_height(n)

                # old method for reference, do not delete
                #ratio = new_h / old_h
                #new_y = biggest_y - ((ratio * (biggest_y - y)))

                padding_diff_second = ((biggest_y - biggest_h) - second_biggest_y)
                padding_diff_current = (biggest_y - biggest_h) - y
                padding_diff_ratio = padding_diff_current / padding_diff_second

                y_diff_second = biggest_y - second_biggest_y
                y_diff_current = biggest_y - y
                y_diff_ratio = y_diff_current / y_diff_second

                new_y = biggest_y - new_h - padding_diff_second - (padding_diff_second*(padding_diff_ratio-1.0))
                new_y -= (new_h - old_h) * (y_diff_ratio-1.0)

                n.location = n.location[0], new_y


def get_summed_height(nodes, padding_y=0.0):
    summed_height = 0.0
    for node in nodes:
        summed_height += get_height(node) + padding_y
    summed_height -= padding_y
    return summed_height


def get_biggest_height(nodes):
    biggest_height = 0.0
    for node in nodes:
        current_height = get_height(node)
        if current_height > biggest_height:
            biggest_height = current_height
    return biggest_height


def get_biggest_width(nodes):
    biggest_width = 0.0
    for node in nodes:
        current_width = get_width(node)
        if current_width > biggest_width:
            biggest_width = current_width
    return biggest_width


def single_column_layout_nodes(nodes, padding_y=20.0, center=None):
    node_count = len(nodes)
    if node_count <= 1:
        return
    if center is None:
        center = get_location_center(nodes)

    summed_height = get_summed_height(nodes, padding_y)
    biggest_width = get_biggest_width(nodes)

    start_loc = [center[0] - biggest_width*0.5, center[1] + summed_height*0.5]
    current_loc = [start_loc[0], start_loc[1]]

    for node in nodes:
        height = get_height(node)
        node.location = current_loc[0], current_loc[1]
        current_loc[1] = current_loc[1] - height - padding_y


def dual_step_layout_nodes(nodes, padding_x=60.0, padding_y=20.0, center=None):
    node_count = len(nodes)
    if node_count <= 1:
        return
    if center is None:
        center = get_location_center(nodes)

    left_width = get_width(nodes[0])
    for i in range(2, node_count, 2):
        current_width = get_width(nodes[i])
        if current_width > left_width:
            left_width = current_width

    summed_height = get_summed_height(nodes, padding_y)

    start_loc = [center[0] - (padding_x*0.5) - left_width, center[1] + (summed_height*0.5)]
    current_loc = [start_loc[0], start_loc[1]]
    index = 0
    w = 0.0
    for node in nodes:
        if index % 2 == 0:
            w = get_width(node)

        h = get_height(node)
        node.location = current_loc[0], current_loc[1]

        if index % 2 != 0:
            current_loc[0] = current_loc[0] - w - padding_x
        else:
            current_loc[0] = current_loc[0] + w + padding_x

        current_loc[1] = current_loc[1] - h - padding_y
        index += 1


def group_nodes(group_name, nodes, node_context, name=None, label=None, color=None):
    group = bpy.data.node_groups.new(group_name, 'ShaderNodeTree')
    input_node = group.nodes.new('NodeGroupInput')
    group.inputs.new('NodeSocketVector', 'Vector')

    for node in nodes:
        group.nodes.add(node)
        group.links.new(node.inputs[0], input_node.outputs[0])

    group_node = new_node(group.name, node_context)

    if name is not None:
        group_node.name = name

    if label is not None:
        group_node.label = label

    if color is not None:
        group_node.use_custom_color = True
        group_node.color = color


def layout_input_output_nodes(group, distance=500):
    other_nodes = list()
    input_nodes = list()
    output_nodes = list()

    for n in group.nodes:
        if n.bl_idname == 'NodeGroupInput':
            input_nodes.append(n)
        elif n.bl_idname == 'NodeGroupOutput':
            output_nodes.append(n)
        else:
            other_nodes.append(n)

    other_bounds = get_bounds(other_nodes)
    other_center = get_location_center_from_bounds(other_bounds)
    other_center_offset = (other_bounds[2] - other_bounds[0]) * 0.5

    for input_node in input_nodes:
        loc = input_node.location
        input_width = get_width(input_node)
        loc[0] = other_center[0] - other_center_offset - distance - input_width
        input_node.location = loc

    for output_node in output_nodes:
        loc = output_node.location
        loc[0] = other_center[0] + other_center_offset + distance
        output_node.location = loc


def generate_group_outputs(group, characterizations):
    output_node = group.nodes.new('NodeGroupOutput')
    input_index = len(group.outputs)

    for characterization in characterizations:
        for tex_node in characterization.shader_texture_nodes:
            if characterization.characteristic_group is None or characterization.characteristic_group.channels > 1:
                group.outputs.new('NodeSocketColor', characterization.characteristic_group.first_name)
                group.links.new(output_node.inputs[input_index], tex_node.outputs['Color'])
            else:
                group.outputs.new('NodeSocketFloat', characterization.characteristic_group.first_name)
                group.links.new(output_node.inputs[input_index], tex_node.outputs['Color'])
            input_index += 1


def frame_nodes(nodes, node_context, name=None, label=None, color=None):
    node_frame = new_node('NodeFrame', node_context)

    if name is not None:
        node_frame.name = name

    if label is not None:
        node_frame.label = label

    if color is not None:
        node_frame.use_custom_color = True
        node_frame.color = color

    for node in nodes:
        node.parent = node_frame

    return node_frame

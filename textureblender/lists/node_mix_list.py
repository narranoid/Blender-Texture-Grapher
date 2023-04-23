
import bpy
from bpy.types import UIList, PropertyGroup, NodeTree
from bpy.props import BoolProperty, CollectionProperty, StringProperty
from dataclasses import dataclass
from typing import List, Set, Dict, Tuple, Optional


class MATERIAL_UL_node_mix_list(UIList):

    # The draw_item function is called for each item of the collection that is visible in the list.
    #   data is the RNA object containing the collection,
    #   item is the current drawn item of the collection,
    #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
    #   have custom icons ID, which are not available as enum items).
    #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
    #   active item of the collection).
    #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
    #   index is index of the current item in the collection.
    #   flt_flag is the result of the filtering process for this item.
    #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
    #         need them.
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        socket_list = data
        socket_entry = item

        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # You should always start your row layout by a label (icon + text), or a non-embossed text field,
            # this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
            # We use icon_value of label, as our given icon is an integer value, not an enum ID.
            # Note "data" names should never be translated!
            if socket_entry:
                layout.prop(socket_entry, "create_sockets", text="", emboss=False)
                self.draw_entry_prop(layout, socket_entry, "input_socket_first")
                if socket_list.use_custom_input_names:
                    self.draw_entry_prop(layout, socket_entry, "input_socket_first_name")
                self.draw_entry_prop(layout, socket_entry, "input_socket_second")
                if socket_list.use_custom_input_names:
                    self.draw_entry_prop(layout, socket_entry, "input_socket_second_name")
            else:
                layout.label(text="", translate=False, icon_value=icon)
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

    def draw_entry_prop(self, layout, socket_entry, prop_name):
        sub_layout = layout.column()
        sub_layout.enabled = socket_entry.create_sockets
        layout.prop(socket_entry, prop_name, text="", emboss=False)


import bpy

from .textureblender.ops import ImageNodeFileImporter, LayoutNodesOperator, HideNodesOperator, UnhideNodesOperator, \
    FrameImageSetOperator, GroupImageSetOperator, ConnectActiveToSelectedOperator, ConnectSelectedToActiveOperator, \
    ShaderTexImageMultiEditOperator

from .textureblender.panels import TextureSetSetupPanel, LayoutNodesFileBrowserPanel, LayoutNodesPanel, \
    DynamicFormatPanel, ConnectNodesPanel


bl_info = {
    'version': (0, 1),
    'blender': (2, 80, 0),
    'author': 'Florian Friedrich (@narranoid)',
    'name': 'Texture Grapher',
    'location': 'Node Editor > Sidebar > Texture Grapher',
    'description': 'Texturing workflow utilities',
    'warning': 'This is a Beta release! Use at your own risk!',
    'category': 'Material',
}


classes = [
    # Operators
    ImageNodeFileImporter,
    LayoutNodesOperator,
    HideNodesOperator,
    UnhideNodesOperator,
    FrameImageSetOperator,
    GroupImageSetOperator,
    ConnectActiveToSelectedOperator,
    ConnectSelectedToActiveOperator,
    ShaderTexImageMultiEditOperator,

    # Panels
    TextureSetSetupPanel,
    LayoutNodesPanel,
    LayoutNodesFileBrowserPanel,
    DynamicFormatPanel,
    ConnectNodesPanel
]


addon_keymaps = []


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
        kmi = km.keymap_items.new("texture_grapher.shader_tex_image_multi_edit", type='I', value='PRESS')
        addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.itmes.remove(kmi)
    addon_keymaps.clear()

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()

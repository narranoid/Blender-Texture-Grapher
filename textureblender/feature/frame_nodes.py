

class FrameNodesFeature:

    def frame_nodes(self, texture_set_characterization, node_tree):
        return texture_set_characterization.frame_nodes_in_tree(node_tree, set_label=True, set_name=True)

    def create_framed_nodes(self, texture_set_characterization, node_tree):
        pass

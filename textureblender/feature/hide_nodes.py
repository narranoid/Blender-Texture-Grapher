
from .. import node_util as nu


class HideNodesFeature:

    def hide_nodes(self, nodes, hide):
        nu.hide_nodes(nodes, hide=hide, reposition=True)

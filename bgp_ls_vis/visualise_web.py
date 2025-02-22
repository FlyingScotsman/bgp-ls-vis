import yaml
from proto import GoBGPQueryWrapper
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import plotly.express as px
from pprint import pprint
import graphing
import plotly.graph_objects as go


def main():
    """First method called when ran as script"""
    rpc = GoBGPQueryWrapper("192.168.242.132", "50051")

    lsdb = rpc.get_lsdb()

    nx_graph = graphing.build_nx_from_lsdb(lsdb)

    elements = []

    for node in nx_graph.nodes():
        elements.append(
            {
                "data": {"id": node, "label": node},
            },
        )
    for source_edge, target_edge in nx_graph.edges():
        elements.append(
            {
                "data": {
                    "source": source_edge,
                    "target": target_edge,
                    "cost": nx_graph[source_edge][target_edge][0]["cost"],
                }
            }
        )

    app = dash.Dash(__name__)
    app.layout = html.Div(
        [
            html.P("Mad topology:"),
            cyto.Cytoscape(
                id="cytoscape",
                elements=elements,
                layout={"name": "cose"},
                style={
                    "width": "100%",
                    "height": "700px",
                },
                stylesheet=[
                    {
                        "selector": "node",
                        "style": {"label": "data(id)"},
                    },
                    {
                        "selector": "edge",
                        "style": {
                            "source-label": "data(cost)",
                            "source-text-offset": 40,
                        },
                    },
                ],
            ),
        ]
    )

    app.run_server(debug=True)


if __name__ == "__main__":
    main()

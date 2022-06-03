from dash import Dash, html, dcc, Input, Output, callback
import dash_uploader as du
from app import app
import utils
import base64
import sys, os

sys.path.append(os.path.dirname(sys.path[0]))
from rsemg import converter_functions

du.configure_upload(app, r"C:\tmp\Uploads", use_upload_id=True)


@du.callback(
    output=Output('emg-graphs-container', 'children'),
    id='upload-emg-data',
)
def parse_vent(status):
    vent_data = converter_functions.poly5unpad(status[0])
    children = utils.add_emg_graphs(vent_data)

    return children


@du.callback(
    output=Output('ventilator-graphs-container', 'children'),
    id='upload-ventilator-data',
)
def parse_emg(status):
    emg_data = converter_functions.poly5unpad(status[0])
    children = utils.add_ventilator_graphs(emg_data)

    return children

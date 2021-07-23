import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction

import numpy as np
import pandas as pd
import datetime
from datetime import datetime as dt
import pathlib

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Clinical Analytics Dashboard"

server = app.server
app.config.suppress_callback_exceptions = True

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

df = pd.read_csv(DATA_PATH.joinpath("operational resultsmeta1.csv"))
pdf = pd.read_csv(DATA_PATH.joinpath("all_patients_breast.csv"))

scenario_list = df["scenario"].unique()
scenario_chair_list = df["scenario_chairs"].unique()
scenario_nurse_list = df["scenario_nurses"].unique()
scenario_doc_list = df["scenario_docs"].unique()
clinic_list = df["Clinic Name"].unique()
group_list = df["Group"].unique().tolist()

df["Time"] = df["datetime"].apply(lambda x: dt.strptime(x, "%Y-%m-%d %H:%M:%S"))  # String -> Datetime
#df["Time"] = df["datetime"].apply(lambda x: dt.strptime(x, "%d/%m/%Y %H:%M"))  # String -> Datetime
#df["Time"] = df["datetime"].apply(lambda x: dt.strptime(x, "%d/%m/%Y %H:%M:%S"))  # String -> Datetime

# Insert weekday and hour of checkin time
df["Days of Wk"] = df["Time Hour"] = df["Time"]
df["Days of Wk"] = df["Days of Wk"].apply(lambda x: dt.strftime(x, "%A"))  # Datetime -> weekday string

df["Time Hour"] = df["Time Hour"].apply(lambda x: dt.strftime(x, "%I %p"))  # Datetime -> int(hour) + AM/PM

day_list = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

#check_in_duration = df["Time"].describe()
# Register all departments for callbacks
all_departments = df["Group"].unique().tolist()
wait_time_inputs = [Input((i + "_wait_time_graph"), "selectedData") for i in all_departments]
score_inputs = [Input((i + "_score_graph"), "selectedData") for i in all_departments]


def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Clinical Analytics"),
            html.H3("Welcome to the Clinical Analytics Dashboard"),
            html.Div(
                id="intro",
                children="Explore clinic patient volume by time of day, waiting time, and care score. Click on the heatmap to visualize patient experience at different time points.",
            ),
        ],
    )


def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.P("Select Clinic"),
            dcc.Dropdown(
                id="clinic-select",
                options=[{"label": i, "value": i} for i in clinic_list],
                value=clinic_list[0],
            ),
            html.Br(),
            html.P("Select Check-In Time"),
            dcc.DatePickerRange(
                id="date-picker-select",
                start_date=dt(2020, 1, 1),
                end_date=dt(2020, 1, 30),
                min_date_allowed=dt(2020, 1, 1),
                max_date_allowed=dt(2020, 1, 30),
                initial_visible_month=dt(2020, 1, 1),
            ),
            html.Br(),
            html.Br(),
            html.P("Select Group"),
            dcc.Dropdown(
                id="group-select",
                options=[{"label": i, "value": i} for i in group_list],
                value=group_list[:],
                multi=True,
            ),
            html.Br(),

            html.P("Select Scenario Chairs"),
            dcc.Dropdown(
                id="scenario-chair-select",
                options=[{"label": i, "value": i} for i in scenario_chair_list],
                value=scenario_chair_list[:],
                multi=True,
            ),
            html.Br(),
            html.P("Select Scenario Nurses"),
            dcc.Dropdown(
                id="scenario-nurse-select",
                options=[{"label": i, "value": i} for i in scenario_nurse_list],
                value=scenario_nurse_list[:],
                multi=True,
            ),
            html.Br(),
            html.P("Select Scenario Doctors"),
            dcc.Dropdown(
                id="scenario-doc-select",
                options=[{"label": i, "value": i} for i in scenario_doc_list],
                value=scenario_doc_list[:],
                multi=True,
            ),
            html.Br(),

            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
            ),
         ],
    )

def generate_patient_volume_heatmap(start, end, clinic, hm_click, group_type, scenario_chair_num,
                                    scenario_nurse_num,scenario_doc_num, reset):
    """
    :param: start: start date from selection.
    :param: end: end date from selection.
    :param: clinic: clinic from selection.
    :param: hm_click: clickData from heatmap.
    :param: group_type: admission type from selection.
    :param: reset (boolean): reset heatmap graph if True.

    :return: Patient volume annotated heatmap.
    """
    #filtered_df = df[(df["Clinic Name"] == clinic) & (df["Admit Source"].isin(admit_type))]
    filtered_df = df[(df["Clinic Name"] == clinic) & (df["scenario_chairs"].isin(scenario_chair_num)) & (df["scenario_docs"].isin(scenario_doc_num))
                     & (df["scenario_nurses"].isin(scenario_nurse_num)) & (df["Group"].isin(group_type))]
    filtered_df = filtered_df.sort_values("Time").set_index("Time")[start:end]


    x_axis = [datetime.time(i).strftime("%I %p") for i in range(8,19)]  # 24hr time list
    y_axis = day_list

    hour_of_day = ""
    weekday = ""
    shapes = []

    if hm_click is not None:
        hour_of_day = hm_click["points"][0]["x"]
        weekday = hm_click["points"][0]["y"]

        # Add shapes
        x0 = x_axis.index(hour_of_day) / 24
        x1 = x0 + 1 / 24
        y0 = y_axis.index(weekday) / 7
        y1 = y0 + 1 / 7

        shapes = [
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=x0,
                x1=x1,
                y0=y0,
                y1=y1,
                line=dict(color="#ff6347"),
            )
        ]

    # Get z value : sum(number of records) based on x, y,

    z = np.zeros((7, 24))
    annotations = []

    for ind_y, day in enumerate(y_axis):
        filtered_day = filtered_df[filtered_df["Days of Wk"] == day]
        for ind_x, x_val in enumerate(x_axis):
            #sum_of_record = filtered_day[filtered_day["Time Hour"] == x_val]["Number of Records"].sum()
            #columns
            # all patients waiting
            #  all patients treated
            # patients at admin
            # patients between treatment cycles
            # patients at consultation
            # patients at treatment
            # patients at pharmacy
            # patients in between treatments
            # patients at cashier
            # patients total ADR

            puncm = int(filtered_day[filtered_day["Time Hour"] == x_val]["uncompleted patients"].mean())
            pwait = int(filtered_day[filtered_day["Time Hour"] == x_val]["all patients waiting"].mean())
            padmin = int(filtered_day[filtered_day["Time Hour"] == x_val]["patients at admin"].mean())
            pbtwn_c = int(filtered_day[filtered_day["Time Hour"] == x_val]["patients between treatment cycles"].mean())
            pcons = int(filtered_day[filtered_day["Time Hour"] == x_val]["patients at consultation"].mean())
            ptreat = int(filtered_day[filtered_day["Time Hour"] == x_val]["patients at treatment"].mean())
            ppharm = int(filtered_day[filtered_day["Time Hour"] == x_val]["patients at pharmacy"].mean())
            pbtwn_t = int(filtered_day[filtered_day["Time Hour"] == x_val]["patients in between treatments"].mean())
            pcash = int(filtered_day[filtered_day["Time Hour"] == x_val]["patients at cashier"].mean())
            padr = int(filtered_day[filtered_day["Time Hour"] == x_val]["patients total ADR"].mean())
            pflow = int(filtered_day[filtered_day["Time Hour"] == x_val]["all patients flow"].sum())


            sum_of_record = pflow # puncm - pbtwn_c#pwait+padmin+pcons+ptreat+ppharm+pcash
            #print('Time Hour:'+str(x_val)+' '+str(sum_of_record))
            z[ind_y][ind_x] = sum_of_record

            annotation_dict = dict(
                showarrow=False,
                text="<b>" + str(sum_of_record) + "<b>",
                xref="x",
                yref="y",
                x=x_val,
                y=day,
                font=dict(family="sans-serif"),
            )
            # Highlight annotation text by self-click
            if x_val == hour_of_day and day == weekday:
                if not reset:
                    annotation_dict.update(size=15, font=dict(color="#ff6347"))

            annotations.append(annotation_dict)

    # Heatmap
    hovertemplate = "<b> %{y}  %{x} <br><br> %{z} Patient Records"

    data = [
        dict(
            x=x_axis,
            y=y_axis,
            z=z,
            type="heatmap",
            name="",
            hovertemplate=hovertemplate,
            showscale=False,
            colorscale=[[0, "#caf3ff"], [1, "#2c82ff"]],
        )
    ]

    layout = dict(
        margin=dict(l=70, b=50, t=50, r=50),
        modebar={"orientation": "v"},
        font=dict(family="Open Sans"),
        annotations=annotations,
        shapes=shapes,
        xaxis=dict(
            side="top",
            ticks="",
            ticklen=2,
            tickfont=dict(family="sans-serif"),
            tickcolor="#ffffff",
        ),
        yaxis=dict(
            side="left", ticks="", tickfont=dict(family="sans-serif"), ticksuffix=" "
        ),
        hovermode="closest",
        showlegend=False,
    )
    return {"data": data, "layout": layout}


#



app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],
        ),
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # Patient Volume Heatmap
                html.Div(
                    id="patient_volume_card",
                    children=[
                        html.B("Patients Seen"),
                        html.Hr(),
                        dcc.Graph(id="patient_volume_hm"),
                    ],
                ),
                # Patient Wait time by Department
            ],
        ),
    ],
)

'''html.Div(
    id="distribution",
    children=[
        html.B("Patient Wait Time Distributions"),
        html.Hr(),
        html.Div(id="wait_time_dist", children=None),
    ],
),'''


@app.callback(
    Output("patient_volume_hm", "figure"),
    [
        Input("date-picker-select", "start_date"),
        Input("date-picker-select", "end_date"),
        Input("clinic-select", "value"),
        Input("patient_volume_hm", "clickData"),
        Input("group-select", "value"),
        Input("scenario-chair-select", "value"),
        Input("scenario-nurse-select", "value"),
        Input("scenario-doc-select", "value"),
        Input("reset-btn", "n_clicks"),
    ],
)
def update_heatmap(start, end, clinic, hm_click, group_type, scenario_chair_num, scenario_nurse_num, scenario_doc_num, reset_click):
    start = start + " 00:00:00"
    end = end + " 00:00:00"

    reset = False
    # Find which one has been triggered
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "reset-btn":
            reset = True

    # Return to original hm(no colored annotation) by resetting
    return generate_patient_volume_heatmap(
        start, end, clinic, hm_click, group_type, scenario_chair_num, scenario_nurse_num, scenario_doc_num, reset
    )


#app.clientside_callback(
#    ClientsideFunction(namespace="clientside", function_name="resize"),
#    Output("output-clientside", "children"),
#    [Input("wait_time_table", "children")] + wait_time_inputs + score_inputs,
#)


'''
@app.callback(
    Output("wait_time_table", "children"),
    [
        Input("date-picker-select", "start_date"),
        Input("date-picker-select", "end_date"),
        Input("clinic-select", "value"),
        Input("admit-select", "value"),
        Input("patient_volume_hm", "clickData"),
        Input("reset-btn", "n_clicks"),
    ]
    + wait_time_inputs
    + score_inputs,
)

def update_table(start, end, clinic, admit_type, heatmap_click, reset_click, *args):
    start = start + " 00:00:00"
    end = end + " 00:00:00"

    # Find which one has been triggered
    ctx = dash.callback_context

    prop_id = ""
    prop_type = ""
    triggered_value = None
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        prop_type = ctx.triggered[0]["prop_id"].split(".")[1]
        triggered_value = ctx.triggered[0]["value"]

    # filter data
    filtered_df = df[
        (df["Clinic Name"] == clinic) & (df["Admit Source"].isin(admit_type))
    ]
    filtered_df = filtered_df.sort_values("Check-In Time").set_index("Check-In Time")[
        start:end
    ]
    departments = filtered_df["Department"].unique()

    # Highlight click data's patients in this table
    if heatmap_click is not None and prop_id != "reset-btn":
        hour_of_day = heatmap_click["points"][0]["x"]
        weekday = heatmap_click["points"][0]["y"]
        clicked_df = filtered_df[
            (filtered_df["Days of Wk"] == weekday)
            & (filtered_df["Check-In Hour"] == hour_of_day)
        ]  # slice based on clicked weekday and hour
        departments = clicked_df["Department"].unique()
        filtered_df = clicked_df

    # range_x for all plots
    wait_time_xrange = [
        filtered_df["Wait Time Min"].min() - 2,
        filtered_df["Wait Time Min"].max() + 2,
    ]
    score_xrange = [
        filtered_df["Care Score"].min() - 0.5,
        filtered_df["Care Score"].max() + 0.5,
    ]

    figure_list = []

    if prop_type != "selectedData" or (
        prop_type == "selectedData" and triggered_value is None
    ):  # Default condition, all ""

        for department in departments:
            department_wait_time_figure = create_table_figure(
                department, filtered_df, "Wait Time Min", wait_time_xrange, ""
            )
            figure_list.append(department_wait_time_figure)

        for department in departments:
            department_score_figure = create_table_figure(
                department, filtered_df, "Care Score", score_xrange, ""
            )
            figure_list.append(department_score_figure)

    elif prop_type == "selectedData":
        selected_patient = ctx.triggered[0]["value"]["points"][0]["customdata"]
        selected_index = [ctx.triggered[0]["value"]["points"][0]["pointIndex"]]

        # [] turn on un-selection for all other plots, [index] for this department
        for department in departments:
            wait_selected_index = []
            if prop_id.split("_")[0] == department:
                wait_selected_index = selected_index

            department_wait_time_figure = create_table_figure(
                department,
                filtered_df,
                "Wait Time Min",
                wait_time_xrange,
                wait_selected_index,
            )
            figure_list.append(department_wait_time_figure)

        for department in departments:
            score_selected_index = []
            if department == prop_id.split("_")[0]:
                score_selected_index = selected_index

            department_score_figure = create_table_figure(
                department,
                filtered_df,
                "Care Score",
                score_xrange,
                score_selected_index,
            )
            figure_list.append(department_score_figure)

    # Put figures in table
    table = generate_patient_table(
        figure_list, departments, wait_time_xrange, score_xrange
    )
    return table

'''

# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)

import base64
import io
import sys
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

# Initialize Dash app
def create_app():
    app = dash.Dash(__name__)
    app.title = "Baja Shock Data GUI"

    # Layout
    app.layout = html.Div([
        html.H1("Baja Shock Data Analysis"),
        dcc.Upload(
            id='upload-data',
            children=html.Div(['Drag and Drop or ', html.A('Select a .txt File')]),
            style={
                'width': '60%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                'textAlign': 'center', 'margin': '10px'
            },
            multiple=False
        ),
        html.Div([
            html.Label("Start Time (s):"),
            dcc.Input(id='start-time', type='number', value=0, min=0, step=0.001),
            html.Label("End Time (s):"),
            dcc.Input(id='end-time', type='number', value=10, min=0, step=0.001),
            html.Button('Process', id='process-btn', n_clicks=0)
        ], style={'margin': '10px'}),
        dcc.Graph(id='pos-graph'),
        dcc.Graph(id='vel-hist-graph')
    ])

    # Callback registration
    @app.callback(
        [Output('pos-graph', 'figure'), Output('vel-hist-graph', 'figure')],
        [Input('process-btn', 'n_clicks')],
        [State('upload-data', 'contents'), State('start-time', 'value'), State('end-time', 'value')]
    )
    def update_graph(n_clicks, contents, start_time, end_time):
        if not n_clicks or not contents:
            return dash.no_update, dash.no_update
        try:
            df = parse_contents(contents)
        except ValueError as e:
            print(f"Parsing error: {e}")
            return {}, {}

        # Filter timeframe
        df_filtered = df[(df['Time'] >= start_time) & (df['Time'] <= end_time)]

        # Position vs Time
        pos_fig = px.line(
            df_filtered,
            x='Time',
            y=[col for col in df_filtered.columns if 'pos' in col],
            labels={'value': 'Position', 'variable': 'Shock'},
            title=f'Shock Position ({start_time}s–{end_time}s)'
        )

        # Velocity histograms
        vel_df = df_filtered.melt(
            id_vars='Time',
            value_vars=[col for col in df_filtered.columns if 'vel' in col],
            var_name='Shock',
            value_name='Velocity'
        )
        vel_fig = px.histogram(
            vel_df,
            x='Velocity',
            color='Shock',
            barmode='overlay',
            nbins=30,
            opacity=0.75,
            title=f'Histogram of Shock Velocities ({start_time}s–{end_time}s)'
        )
        vel_fig.update_layout(xaxis_title='Velocity', yaxis_title='Frequency')
        return pos_fig, vel_fig

    return app

# Data parsing utility
def parse_contents(contents):
    """
    Decode base64 contents and parse whitespace-delimited ASCII into DataFrame.
    Adds Time and Shock velocity columns.
    """
    try:
        header, b64 = contents.split(',', 1)
        raw = base64.b64decode(b64).decode('utf-8')
        df = pd.read_csv(io.StringIO(raw), delim_whitespace=True, header=None)
    except Exception as e:
        raise ValueError(f"Failed to parse upload: {e}")

    # Insert Time and rename position columns
    dt = 0.001
    df.insert(0, 'Time', df.index * dt)
    pos_cols = [f'Shk{i} pos' for i in range(1, df.shape[1])]
    if len(pos_cols) != df.shape[1] - 1:
        # Data has unexpected number of columns
        raise ValueError(f"Expected 4 position columns, found {df.shape[1]-1}")
    df.columns = ['Time'] + pos_cols

    # Compute velocities
    for i, col in enumerate(pos_cols, start=1):
        df[f'Shk{i} vel'] = df[col].diff() / dt
    return df

# Test suite
def run_tests():
    import base64 as _b64
    # Test 1: correct columns
    sample = "1 2 3 4 5\n6 7 8 9 10"
    content = "data:text/plain;base64," + _b64.b64encode(sample.encode()).decode()
    df = parse_contents(content)
    expected_cols = ['Time', 'Shk1 pos', 'Shk2 pos', 'Shk3 pos', 'Shk4 pos',
                     'Shk1 vel', 'Shk2 vel', 'Shk3 vel', 'Shk4 vel']
    assert list(df.columns) == expected_cols, f"Cols mismatch: {df.columns}"

    # Test 2: velocity correctness
    sample2 = "0 0 0 0 0\n0.001 1 2 3 4"
    content2 = "data:text/plain;base64," + _b64.b64encode(sample2.encode()).decode()
    df2 = parse_contents(content2)
    assert round(df2.loc[1, 'Shk1 vel'], 6) == 1000.0, f"Vel error: {df2.loc[1, 'Shk1 vel']}"

    # Test 3: malformed input raises
    try:
        parse_contents("not,base64")
        raise AssertionError("Expected ValueError for bad input")
    except ValueError:
        pass

    print("All tests passed.")

# Entry point
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        run_tests()
    else:
        app = create_app()
        try:
            app.run(host='127.0.0.1', port=8050, debug=False)
        except OSError as e:
            print(f"Failed to start server: {e}")
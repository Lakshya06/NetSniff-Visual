import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import os

# Initialize the Dash app
app = dash.Dash(__name__)

# Path to the CSV file
csv_file_path = "network_data.csv"

# Define a dictionary mapping ports to protocols
PORT_TO_PROTOCOL = {
    80: 'HTTP',
    443: 'HTTPS',
    53: 'DNS',
    22: 'SSH',
    21: 'FTP',
    110: 'POP3',
    25: 'SMTP',
    3306: 'MySQL',
    8080: 'HTTP-Alt',
    53: 'DNS',
    69: 'TFTP',
    161: 'SNMP',
    4433: 'RDP',  # Added for example
}

# Function to read the CSV file and get the latest data
def read_latest_data():
    # Check if the CSV file exists
    if not os.path.exists(csv_file_path):
        return pd.DataFrame()

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    return df

# Function to create a pie chart for packet types (TCP/UDP)
def create_pie_chart(df):
    # Count the protocol occurrences (TCP/UDP)
    protocol_counts = df['Protocol'].value_counts()

    # Create pie chart with custom colors
    pie_chart = go.Figure(data=[go.Pie(labels=protocol_counts.index, values=protocol_counts.values, marker=dict(colors=['#FF9999', '#66b3ff']))])

    pie_chart.update_layout(title="Packet Type Distribution (TCP vs UDP)")

    return pie_chart

# Function to create a pie chart for protocols based on port numbers
def create_protocol_pie_chart(df):
    # Map the ports to protocols for both Source and Destination Ports
    src_protocol_counts = df['Source Port'].map(PORT_TO_PROTOCOL)
    dst_protocol_counts = df['Destination Port'].map(PORT_TO_PROTOCOL)

    # Concatenate the two series (source and destination port protocols)
    protocol_counts = pd.concat([src_protocol_counts, dst_protocol_counts])

    # Remove NaN values if any
    protocol_counts = protocol_counts.dropna()

    # Count the occurrences of each protocol
    protocol_dist = protocol_counts.value_counts()

    # Create pie chart for protocol distribution based on port numbers with custom colors
    protocol_pie_chart = go.Figure(data=[go.Pie(labels=protocol_dist.index, values=protocol_dist.values, marker=dict(colors=['#ffcc99', '#99ff99', '#ffb3e6', '#c2c2f0']))])

    protocol_pie_chart.update_layout(title="Protocol Distribution by Ports")

    return protocol_pie_chart


# Function to create bar charts for IP addresses (horizontal bars)
def create_ip_address_bar_chart(df):
    # Count occurrences of Source and Destination IPs
    src_ip_counts = df['Source IP'].value_counts().head(10)  # Top 10 Source IPs
    dst_ip_counts = df['Destination IP'].value_counts().head(10)  # Top 10 Destination IPs

    # Create horizontal bar chart for Source IPs
    src_ip_bar = go.Figure(data=[go.Bar(x=src_ip_counts.values, y=src_ip_counts.index, orientation='h', name="Source IP", marker=dict(color='blue'))])
    dst_ip_bar = go.Figure(data=[go.Bar(x=dst_ip_counts.values, y=dst_ip_counts.index, orientation='h', name="Destination IP", marker=dict(color='green'))])

    src_ip_bar.update_layout(title="Top Source IPs", xaxis_title="Count", yaxis_title="IP Address")
    dst_ip_bar.update_layout(title="Top Destination IPs", xaxis_title="Count", yaxis_title="IP Address")

    return src_ip_bar, dst_ip_bar

# Function to create bar charts for Ports with specific port numbers
def create_port_bar_chart(df):
    # Count occurrences of Source and Destination Ports
    src_port_counts = df['Source Port'].value_counts().head(10)  # Top 10 Source Ports
    dst_port_counts = df['Destination Port'].value_counts().head(10)  # Top 10 Destination Ports

    # Create bar chart for Source Ports with explicit labels
    src_port_bar = go.Figure(data=[go.Bar(x=src_port_counts.index.astype(str), y=src_port_counts.values, name="Source Port", marker=dict(color='purple'))])
    dst_port_bar = go.Figure(data=[go.Bar(x=dst_port_counts.index.astype(str), y=dst_port_counts.values, name="Destination Port", marker=dict(color='orange'))])

    src_port_bar.update_layout(title="Top Source Ports", xaxis_title="Port", yaxis_title="Count")
    dst_port_bar.update_layout(title="Top Destination Ports", xaxis_title="Port", yaxis_title="Count")

    return src_port_bar, dst_port_bar

# Function to create a line chart for packet lengths over time
def create_packet_length_chart(df):
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')  # Convert Timestamp to datetime
    packet_length_chart = go.Figure(data=[go.Scatter(x=df['Timestamp'], y=df['Packet Length'], mode='lines', name='Packet Length')])

    packet_length_chart.update_layout(title="Packet Length Over Time", xaxis_title="Timestamp", yaxis_title="Packet Length")

    return packet_length_chart

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Network Traffic Dashboard"),
    html.Div([
        dcc.Graph(id="pie-chart", style={'display': 'inline-block', 'width': '45%'}),
        dcc.Graph(id="protocol-pie-chart", style={'display': 'inline-block', 'width': '45%'}),
    ]),
    html.Div([
        dcc.Graph(id="src-ip-bar-chart", style={'display': 'inline-block', 'width': '45%'}),
        dcc.Graph(id="dst-ip-bar-chart", style={'display': 'inline-block', 'width': '45%'}),
    ]),
    html.Div([
        dcc.Graph(id="src-port-bar-chart", style={'display': 'inline-block', 'width': '45%'}),
        dcc.Graph(id="dst-port-bar-chart", style={'display': 'inline-block', 'width': '45%'}),
    ]),
    html.Div([
        dcc.Graph(id="packet-length-chart", style={'display': 'inline-block', 'width': '45%'}),
    ]),
    dcc.Interval(id="interval-update", interval=5000, n_intervals=0)  # Update every 5 seconds
])

# Define the callback to update the dashboard
@app.callback(
    [Output("pie-chart", "figure"),
     Output("protocol-pie-chart", "figure"),
     Output("src-ip-bar-chart", "figure"),
     Output("dst-ip-bar-chart", "figure"),
     Output("src-port-bar-chart", "figure"),
     Output("dst-port-bar-chart", "figure"),
     Output("packet-length-chart", "figure")],
    [Input("interval-update", "n_intervals")]
)
def update_dashboard(n):
    # Read the latest data from the CSV file
    df = read_latest_data()

    if df.empty:
        return [{} for _ in range(7)]  # Return empty figures if no data is available

    # Generate and return updated charts
    pie_chart = create_pie_chart(df)
    protocol_pie_chart = create_protocol_pie_chart(df)
    src_ip_bar, dst_ip_bar = create_ip_address_bar_chart(df)
    src_port_bar, dst_port_bar = create_port_bar_chart(df)
    packet_length_chart = create_packet_length_chart(df)

    return pie_chart, protocol_pie_chart, src_ip_bar, dst_ip_bar, src_port_bar, dst_port_bar, packet_length_chart

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)  # Run the Dash app

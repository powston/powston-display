import argparse
from datetime import datetime
from zoneinfo import ZoneInfo
from paho.mqtt import client as mqtt_client
from paho.mqtt.enums import CallbackAPIVersion
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
client = mqtt_client.Client(callback_api_version=CallbackAPIVersion.VERSION2)

# Utility functions
def number_to_currency(value):
    if abs(value) >= 1000:
        return f"${value / 1000:.2f}k"
    return f"${value:.2f}" if abs(value) >= 1 else f"{value * 100:.2f}c"

def number_to_percentage(value):
    return f"{value:.1f}%"

def number_to_power(value):
    if abs(value) >= 1000:
        return f"{value / 1000:.1f}kW"
    return f"{value:.1f}W"

def process_client_loops(client):
    while client.want_write():
        client.loop_write()

# Display functions for each line
def display_inverter_time(client, mqtt_username, display_id, data):
    try:
        inverter_time = datetime.fromisoformat(data['last_inverter_time']).astimezone(ZoneInfo('Australia/Brisbane'))
        client.publish(f"{mqtt_username}/cmnd/{display_id}/displaytext", f"[s1y0] {inverter_time}: {data['action']}")
    except KeyError:
        logger.warning("Missing 'last_inverter_time' in data")

def display_house_power(client, mqtt_username, display_id, data):
    try:
        client.publish(f"{mqtt_username}/cmnd/{display_id}/displaytext", f"[s2y15] House: {number_to_power(data['house_power'])}/{number_to_power(data['grid_power'])}")
    except KeyError:
        logger.warning("Missing 'house_power' or 'grid_power' in data")

def display_battery_status(client, mqtt_username, display_id, data):
    try:
        client.publish(f"{mqtt_username}/cmnd/{display_id}/displaytext", f"[s2y40] Battery: {data['battery_soc']:.1f}%/{data['battery_voltage']:.1f}V")
    except KeyError:
        logger.warning("Missing 'battery_soc' or 'battery_voltage' in data")

def display_prices(client, mqtt_username, display_id, data):
    try:
        sell_price = number_to_currency(data['sell_price'] / 100)
        client.publish(f"{mqtt_username}/cmnd/{display_id}/displaytext", f"[s2y80] Sell: {sell_price}/kWh")
        buy_price = number_to_currency(data['buy_price'] / 100)
        client.publish(f"{mqtt_username}/cmnd/{display_id}/displaytext", f"[s2y100] Buy: {buy_price}/kWh")
        logger.info(f"Published buy price '{buy_price}/kWh'")
    except KeyError:
        logger.warning("Missing 'buy_price' or 'sell_price' in data")

def display_forecast(client, mqtt_username, display_id, data):
    if 'forecast' in data and len(data['forecast']) > 10:
        forecast_line1 = ', '.join([number_to_currency(data['forecast'][i]) for i in range(0, 4)])
        forecast_line2 = ', '.join([number_to_currency(data['forecast'][i]) for i in range(4, 10)])
        forecast_line3 = ', '.join([number_to_currency(data['forecast'][i]) for i in range(11, 16)])
        client.publish(f"{mqtt_username}/cmnd/{display_id}/displaytext", f"[s1y120] Fcst: {forecast_line1}")
        process_client_loops(client)
        client.publish(f"{mqtt_username}/cmnd/{display_id}/displaytext", f"[s1y130] {forecast_line2}")
        process_client_loops(client)
        client.publish(f"{mqtt_username}/cmnd/{display_id}/displaytext", f"[s1y140] {forecast_line3}")
        process_client_loops(client)

# Main message handler
def on_message(client, userdata, message):
    logger.info(f"Received message on topic '{message.topic}'")
    data = json.loads(message.payload.decode())
    mqtt_username = message.topic.split('/')[0]
    display_id = userdata['display_id']

    # Clear display before updating
    client.publish(f"{mqtt_username}/cmnd/{display_id}/displayclear", "")
    process_client_loops(client)

    # Update each display section
    display_inverter_time(client, mqtt_username, display_id, data)
    display_house_power(client, mqtt_username, display_id, data)
    display_battery_status(client, mqtt_username, display_id, data)
    display_prices(client, mqtt_username, display_id, data)
    display_forecast(client, mqtt_username, display_id, data)

# Main entry point for the script
def main():
    argparser = argparse.ArgumentParser(description='Replay inverter data to display.')
    argparser.add_argument('--server', type=str, default='mqtt.powston.com', help='MQTT server to connect to.')
    argparser.add_argument('--port', type=int, default=1883, help='MQTT port to connect to.')
    argparser.add_argument('--username', type=str, default='', help='MQTT username.')
    argparser.add_argument('--password', type=str, default='', help='MQTT password.')
    argparser.add_argument('--inverter', type=str, default='inverter_1', help='Inverter to replay data for.')
    argparser.add_argument('--display', type=str, default='tasmota_EAB2A0', help='Display to send data to.')
    args = argparser.parse_args()

    mqtt_server = args.server
    mqtt_port = args.port
    mqtt_username = args.username
    mqtt_password = args.password
    inverter = args.inverter

    client.user_data_set({'display_id': args.display})
    client.on_message = on_message
    client.username_pw_set(mqtt_username, mqtt_password)
    client.connect(mqtt_server, mqtt_port)
    client.subscribe(f"{mqtt_username}/powston/{inverter}/state")
    client.loop_forever()


if __name__ == '__main__':
    main()

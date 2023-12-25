from flask import Flask, request, jsonify
import pywifi

app = Flask(__name__)


def connect_to_wifi(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Assuming you have one Wi-Fi interface

    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = pywifi.const.AUTH_ALG_OPEN
    profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
    profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    profile = iface.add_network_profile(profile)
    iface.connect(profile)


@app.route('/connect_wifi', methods=['POST'])
def connect_wifi():
    data = request.get_json()
    new_wifi_ssid = data.connect_wifiget('ssid')
    new_wifi_password = data.get('password')

    if not new_wifi_ssid or not new_wifi_password:
        return jsonify({"message": "SSID and password are required."}), 400

    try:
        connect_to_wifi(new_wifi_ssid, new_wifi_password)
        return jsonify({"message": "Connected to the new Wi-Fi network."})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
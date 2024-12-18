from flask import Flask, request, jsonify
from flask_cors import CORS
from zeroconf import ServiceInfo, Zeroconf
import socket
from cri_lib import CRIController  # Ensure this is the correct library for your robot
import traceback
from time import sleep

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app)

# Initialize the CRI Controller
controller = CRIController()


def register_mdns_service():
    zeroconf = Zeroconf()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    service_info = ServiceInfo(
        "_http._tcp.local.",
        "FlaskServer._http._tcp.local.",
        addresses=[socket.inet_aton(ip_address)],
        port=5000,
        properties={},
        server=f"{hostname}.local.",
    )
    zeroconf.register_service(service_info)
    print(f"Broadcasting Flask server on {ip_address}:5000")

@app.route('/connect_robot', methods=['POST'])
def connect_robot():
    try:
        print("Attempting to connect to the robot...")
        if not controller.connect("127.0.0.1", 3921):  # Adjust IP and port as necessary
            raise Exception("Unable to connect to the robot")
        controller.set_active_control(True)
        controller.enable()
        controller.wait_for_kinematics_ready(10)
        print("Robot successfully connected and initialized")
        return jsonify({"status": "Connected"})
    except Exception as e:
        print(f"Error connecting to robot: {e}")
        return jsonify({"status": "Error", "message": str(e)}), 500

@app.route('/disconnect_robot', methods=['POST'])
def disconnect_robot():
    """
    Disconnect the robot from the controller.
    """
    try:
        if controller.connected:
            controller.close()
            print("Robot disconnected successfully.")
            return jsonify({"status": "Disconnected"})
        else:
                return jsonify({"status": "Error", "message": "Robot is not connected."}), 400
    except Exception as e:
        print(f"Error disconnecting the robot: {e}")
        return jsonify({"status": "Error", "message": str(e)}), 500

@app.route('/command', methods=['POST'])
def command():
    try:
        # Parse the JSON request
        data = request.json
        if not data or 'command' not in data:
            return jsonify({"status": "Error", "message": "Invalid JSON or missing 'command' field"}), 400

        command = data.get('command')
        if command == "pick_apple":
            pick_apple()
            return jsonify({"status": "Success", "message": "Pick-apple and-put sequence completed"})
        elif command == "pick_orange":
            pick_orange()
            return jsonify({"status": "Success", "message": "Pick-orange and-put sequence completed"})
        else:
            return jsonify({"status": "Error", "message": "Unknown command"}), 400
    except Exception as e:
        # Log the full traceback for debugging
        traceback.print_exc()
        return jsonify({"status": "Error", "message": str(e)}), 500

def pick_apple():
    try:
        if not controller.connected:
            raise Exception("Robot is not connected. Call /connect_robot first.")
        print("Executing pick-apple and-put sequence")
        controller.move_joints(
            7.5, 56.1, 75.69, 8.38, -31.49, -18.15, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_cartesian(
            # 572.3, 62.1, 163.4, -128.14, 74.22, -132.29, 0.0, 0.0, 0.0, 100.0,
            572.3, 62.1, 163.4, -128.14, 74.22, -132.29, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            7.08, 60.91, 66.6, 9.19, -37.22, -18.8, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            32.29, 43.39, 66.6, 9.19, -37.22, -18.8, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_cartesian(
            # 483.8, 275.1, 333.7, -4.31, 70.64, -29.36, 0.0, 0.0, 0.0, 100.0,
             483.8, 275.1, 333.7, -4.31, 70.64, -29.36, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            30.52, 42.85, 73.43, 5.62, -43.25, -106.49, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            30.52, 42.85, 73.43, 5.62, -43.25, -26.11, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            17.93, 42.34, 73.43, 5.62, -43.25, -26.11, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_cartesian(
            531.4, 162.8, 144.7, -38.05, 63.18, -48.75, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            17.92, 71.96, 65.41, 4.02, -52.55, -23.82, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_cartesian(
            404.6, 166.0, 117.7, -62.29, 68.33, -76.06, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            67.8, 56.44, 102.22, 11.11, -74.14, -25.12, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        sleep(2.5)
        controller.move_cartesian(
            184.4, 415.2, 117.8, -19.93, 68.34, -76.06, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            69.56, 58.08, 97.72, 13.52, -75.14, -26.45, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_cartesian(
            185.2, 342.9, 194.4, -12.03, 67.45, -66.77, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            -85.41, 35.54, 120.33, 8.04, -74.8, -24.2, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_cartesian(
            13.8, -431.9, 160.9, -161.63, 67.45, -66.77, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            -86.05, 48.02, 107.19, 7.44, -64.64, -24.02, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_cartesian(
            30.4, -365.0, 195.6, 175.25, 69.08, -92.12, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        print("Pick-apple and-put sequence completed")
    except Exception as e:
        print(f"Error in move_to_zero: {e}")
        raise

def pick_orange():
    try:
        if not controller.connected:
            raise Exception("Robot is not connected. Call /connect_robot first.")
        print("Executing pick-orange and-put sequence")
        controller.move_joints(
            2.45, 56.1, 75.69, 8.38, -31.49, -18.15, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_cartesian(
            568.2, 13.7, 163.4, -133.19, 74.22, -132.29, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            2.35, 59.45, 69.34, 8.97, -40.61, -18.91, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_cartesian(
            411.4, 10.3, 190.3, -86.58, 77.98, -82.95, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_cartesian(
            411.4, 164.3, 190.3, -86.58, 77.98, -82.95, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            32.29, 43.39, 66.6, 9.19, -37.22, -18.8, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            30.52, 42.85, 73.43, 5.62, -43.25, -26.11, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            17.93, 42.34, 73.43, 5.62, -43.25, -26.11, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_cartesian(
            531.4, 162.8, 144.7, -38.05, 63.18, -48.75, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            17.92, 71.96, 65.41, 4.02, -52.55, -23.82, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_cartesian(
            404.6, 166.0, 117.7, -62.29, 68.33, -76.06, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            67.8, 56.44, 102.22, 11.11, -74.14, -25.12, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        sleep(2.5)
        controller.move_cartesian(
            184.4, 415.2, 117.8, -19.93, 68.34, -76.06, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            69.56, 58.08, 97.72, 13.52, -75.14, -26.45, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_cartesian(
            185.2, 342.9, 194.4, -12.03, 67.45, -66.77, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            -85.41, 35.54, 120.33, 8.04, -74.8, -24.2, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_cartesian(
            13.8, -431.9, 160.9, -161.63, 67.45, -66.77, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_joints(
            -86.05, 48.02, 107.19, 7.44, -64.64, -24.02, 0.0, 0.0, 0.0, 40.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        controller.move_cartesian(
            30.4, -365.0, 195.6, 175.25, 69.08, -92.12, 0.0, 0.0, 0.0, 100.0,
            wait_move_finished=True,
            move_finished_timeout=1000
        )
        # controller.load_programm("C:\iRC-igusRobotControl-V14\Data\Programs\pick_orange.xml")
        # controller.start_programm()
        print("Pick-orange and-put sequence completed")
    except Exception as e:
        print(f"Error in pick_and_put: {e}")
        raise

if __name__ == '__main__':
    register_mdns_service()
    app.run(host='0.0.0.0', port=5000)  # Bind to all network interfaces on port 5000

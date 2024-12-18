import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: RobotControlScreen(),
    );
  }
}

class RobotControlScreen extends StatefulWidget {
  @override
  _RobotControlScreenState createState() => _RobotControlScreenState();
}

class _RobotControlScreenState extends State<RobotControlScreen> {
  final String serverUrl =
      "http://10.0.2.2:5000"; // Replace with your Flask server's IP and port

  String responseMessage = "No action taken yet";

  // Function to send a POST request to the Flask server
  Future<void> sendPostRequest(
      String endpoint, Map<String, dynamic> body) async {
    final url = Uri.parse('$serverUrl/$endpoint');
    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(body),
      );

      if (response.statusCode == 200) {
        final jsonResponse = jsonDecode(response.body);
        setState(() {
          responseMessage = jsonResponse['message'] ?? "Action successful";
        });
      } else {
        setState(() {
          responseMessage = "Error: ${response.body}";
        });
      }
    } catch (e) {
      setState(() {
        responseMessage = "Error: $e";
      });
    }
  }

  // Functions for each button's action
  void connectToRobot() {
    sendPostRequest('connect_robot', {});
  }

  void Apple() {
    sendPostRequest('command', {"command": "pick_apple"});
  }

  void Orange() {
    sendPostRequest('command', {"command": "pick_orange"});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Robot Control"),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: connectToRobot,
              child: Text("Connect to Robot"),
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: Apple,
              style: ElevatedButton.styleFrom(
                foregroundColor: Colors.white,
                backgroundColor: Colors.red, // Text color
              ),
              child: Text("Apple Juice"),
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: Orange,
              style: ElevatedButton.styleFrom(
                foregroundColor: Colors.white,
                backgroundColor: Colors.orange, // Text color
              ),
              child: Text("Orange Juice"),
            ),
            SizedBox(height: 32),
            Text(
              "Response: $responseMessage",
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }
}

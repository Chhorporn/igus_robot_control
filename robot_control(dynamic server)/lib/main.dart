import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:multicast_dns/multicast_dns.dart';

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
  String? serverUrl;
  String responseMessage = "Searching for server...";
  bool isServerDiscovered = false;

  @override
  void initState() {
    super.initState();
    discoverServer();
  }

  Future<void> discoverServer() async {
    final MDnsClient mdns = MDnsClient();
    try {
      await mdns.start();

      await for (final PtrResourceRecord ptr in mdns.lookup<PtrResourceRecord>(
          ResourceRecordQuery.serverPointer('_http._tcp.local'))) {
        await for (final SrvResourceRecord srv
            in mdns.lookup<SrvResourceRecord>(
                ResourceRecordQuery.service(ptr.domainName))) {
          await for (final IPAddressResourceRecord ip
              in mdns.lookup<IPAddressResourceRecord>(
                  ResourceRecordQuery.addressIPv4(srv.target))) {
            final sanitizedIp = ip.address.address; // Clean IP
            final discoveredUrl = 'http://$sanitizedIp:${srv.port}';

            setState(() {
              serverUrl = discoveredUrl;
              responseMessage = "Discovered server: $discoveredUrl";
            });
            print("Discovered server: $discoveredUrl");
            return; // Stop further discovery after finding the server
          }
        }
      }
    } catch (e) {
      // Fallback to a hardcoded IP for debugging
      setState(() {
        serverUrl =
            "http://192.168.1.28:5000"; // Replace with your Flask server's IP
        responseMessage =
            "Failed to discover server. Using fallback: $serverUrl";
      });
      print("Error discovering server: $e");
    } finally {
      mdns.stop();
    }
  }

  Future<void> sendPostRequest(
      String endpoint, Map<String, dynamic> body) async {
    if (serverUrl == null) {
      setState(() {
        responseMessage = "Server not discovered yet.";
      });
      return;
    }

    // Construct and validate the full URL
    final url = Uri.parse('$serverUrl/$endpoint');
    if (!url.hasScheme || !url.host.isNotEmpty) {
      setState(() {
        responseMessage = "Invalid server URL.";
      });
      return;
    }

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(body),
      );

      if (response.statusCode == 200) {
        final jsonResponse = jsonDecode(response.body);
        setState(() {
          responseMessage = jsonResponse['status'] ?? "Request successful";
        });
      } else {
        setState(() {
          responseMessage =
              "Error: ${response.statusCode} - ${response.reasonPhrase}";
        });
      }
    } catch (e) {
      setState(() {
        responseMessage = "Connection failed: $e";
      });
    }
  }

  void connectToRobot() {
    sendPostRequest('connect_robot', {});
  }

  void pickApple() {
    sendPostRequest('command', {"command": "pick_apple"});
  }

  void pickOrange() {
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
              onPressed: serverUrl == null ? null : connectToRobot,
              child: Text("Connect to Robot"),
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: serverUrl == null ? null : pickApple,
              style: ElevatedButton.styleFrom(
                foregroundColor: Colors.white,
                backgroundColor: Colors.red,
              ),
              child: Text("Apple Juice"),
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: serverUrl == null ? null : pickOrange,
              style: ElevatedButton.styleFrom(
                foregroundColor: Colors.white,
                backgroundColor: Colors.orange,
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

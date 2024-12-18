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
  String responseMessage = "Server not discovered yet";

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
            final rawIp = ip.address.toString();
            final sanitizedIp = rawIp.split(';').first.trim();
            final discoveredUrl = 'http://$sanitizedIp:${srv.port}';

            setState(() {
              serverUrl = discoveredUrl;
              responseMessage = "Discovered server: $serverUrl";
            });
            print("Discovered server: $serverUrl");
            return;
          }
        }
      }
    } catch (e) {
      // Fallback to a hardcoded IP for debugging
      setState(() {
        serverUrl =
            "http://192.168.56.1:5000"; // Replace with your Flask server's IP
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

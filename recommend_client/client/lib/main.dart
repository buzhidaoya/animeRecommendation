import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert' show json;
import 'dart:convert' show jsonEncode;
import 'package:flutter_linkify/flutter_linkify.dart';
import 'package:url_launcher/url_launcher.dart';


void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Recommendation Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // Try running your application with "flutter run". You'll see the
        // application has a blue toolbar. Then, without quitting the app, try
        // changing the primarySwatch below to Colors.green and then invoke
        // "hot reload" (press "r" in the console where you ran "flutter run",
        // or simply save your changes to "hot reload" in a Flutter IDE).
        // Notice that the counter didn't reset back to zero; the application
        // is not restarted.
        primaryColor: Color(0xff4D8669),
      ),
      home: MyHomePage(
        title: 'MOVIE RECOMMENDATION SYSTEM', 
        ),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String _result = '';
  String _username = '';
  var _coverURLs = ["", "", "", "", "", "", "", "", "", "", "", ""];
  var _URLs = ["", "", "", "", "", "", "", "", "", "", "", ""];

  void _getRecommendation() async {
      final http.Response response = await http.post(
        'http://127.0.0.1:5000/recommendation/' + _username,
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{
          'title': 'title',
        }),
      );
      // print(response);
      if (response.statusCode == 200) {
        var result = json.decode(response.body);  // parse result into Map<String, dynamic>
        // print(result);
        setState(() {
          _result = result.toString();
          // print(json.decode('{a:"a"}'));
          // var j = json.decode(_result);
          // var j = json.decode(_result);
          // print(j);
          // print(j["movieIds"]);
          print(result["movieIds"]);
          // for (final k in result["movieIds"]){
          //   final value = result["movieIds"][k];
          //   print(value);
          // }
          final movie0 = result["movieIds"]['0'];
          print(movie0);
          print("*****************************************");
          print(movie0[3]);
          _coverURLs[0] = result["movieIds"]['0'][3];
          _coverURLs[1] = result["movieIds"]['1'][3];
          _coverURLs[2] = result["movieIds"]['2'][3];
          _coverURLs[3] = result["movieIds"]['3'][3];
          _coverURLs[4] = result["movieIds"]['4'][3];
          _coverURLs[5] = result["movieIds"]['5'][3];
          _coverURLs[6] = result["movieIds"]['6'][3];
          _coverURLs[7] = result["movieIds"]['7'][3];
          _coverURLs[8] = result["movieIds"]['8'][3];
          _coverURLs[9] = result["movieIds"]['9'][3];
          _URLs[0] = result["movieIds"]['0'][2];
          _URLs[1] = result["movieIds"]['1'][2];
          _URLs[2] = result["movieIds"]['2'][2];
          _URLs[3] = result["movieIds"]['3'][2];
          _URLs[4] = result["movieIds"]['4'][2];
          _URLs[5] = result["movieIds"]['5'][2];
          _URLs[6] = result["movieIds"]['6'][2];
          _URLs[7] = result["movieIds"]['7'][2];
          _URLs[8] = result["movieIds"]['8'][2];
          _URLs[9] = result["movieIds"]['9'][2];
        });
      }
 
  }

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: SingleChildScrollView(
        child: 
        Center(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        // 要加的：
        // 1. 用户提示：输入用户名
        // 2. Button：Submit
        // 3. 显示推荐出来的电影。
        child: Column(
          // Column is also a layout widget. It takes a list of children and
          // arranges them vertically. By default, it sizes itself to fit its
          // children horizontally, and tries to be as tall as its parent.
          //
          // Invoke "debug painting" (press "p" in the console, choose the
          // "Toggle Debug Paint" action from the Flutter Inspector in Android
          // Studio, or the "Toggle Debug Paint" command in Visual Studio Code)
          // to see the wireframe for each widget.
          //
          // Column has various properties to control how it sizes itself and
          // how it positions its children. Here we use mainAxisAlignment to
          // center the children vertically; the main axis here is the vertical
          // axis because Columns are vertical (the cross axis would be
          // horizontal).
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Container(
              padding: const EdgeInsets.all(20.0),
              child: Text(
                'PLEASE INPUT YOUR USERNAME: ',
                style: TextStyle(color: Colors.grey, fontSize: 12),
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 200.0),
              child: TextField(
              // obscureText: true,
              onChanged: (text) {
                _username = text;
              },
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                // labelText: 'UserName',
              ),
            ),
            ),
            
            Container(
              padding: const EdgeInsets.all(20.0),
              width: 300.0,
              height: 80.0,
              child: RaisedButton(
                child: Text('SUBMIT', style: TextStyle(color: Colors.white, fontSize: 14)),
                onPressed: () {
                  _getRecommendation();
                },
                color: Color(0xff4D8669),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.all(Radius.circular(8)),
                ),
              ),
            ),
            // Linkify(
            //   onOpen: (link) async {
            //     if (await canLaunch(link.url)) {
            //         await launch(link.url);
            //       } else {
            //         throw 'Could not launch $link';
            //       }
            //   },
            //   text: "$_result",
            //   style: TextStyle(color: Color(0xff4A5C50)),
            //   linkStyle: TextStyle(color: Color(0xffBBBBAD)),
            // ),

            GestureDetector(
              onTap: () { 
                  print("Tapped a Container"); 
                  launch(_URLs[0]);
              },
              child: Image.network(_coverURLs[0]),
            ),
            GestureDetector(
              onTap: () { 
                  print("Tapped a Container"); 
                  launch(_URLs[1]);
              },
              child: Image.network(_coverURLs[1]),
            ),
            GestureDetector(
              onTap: () { 
                  print("Tapped a Container"); 
                  launch(_URLs[2]);
              },
              child: Image.network(_coverURLs[2]),
            ),
            GestureDetector(
              onTap: () { 
                  print("Tapped a Container"); 
                  launch(_URLs[3]);
              },
              child: Image.network(_coverURLs[3]),
            ),
            GestureDetector(
              onTap: () { 
                  print("Tapped a Container"); 
                  launch(_URLs[4]);
              },
              child: Image.network(_coverURLs[4]),
            ),
            GestureDetector(
              onTap: () { 
                  print("Tapped a Container"); 
                  launch(_URLs[5]);
              },
              child: Image.network(_coverURLs[5]),
            ),
            GestureDetector(
              onTap: () { 
                  print("Tapped a Container"); 
                  launch(_URLs[6]);
              },
              child: Image.network(_coverURLs[6]),
            ),
            GestureDetector(
              onTap: () { 
                  print("Tapped a Container"); 
                  launch(_URLs[7]);
              },
              child: Image.network(_coverURLs[7]),
            ),
            GestureDetector(
              onTap: () { 
                  print("Tapped a Container"); 
                  launch(_URLs[8]);
              },
              child: Image.network(_coverURLs[8]),
            ),
            GestureDetector(
              onTap: () { 
                  print("Tapped a Container"); 
                  launch(_URLs[9]);
              },
              child: Image.network(_coverURLs[9]),
            ),
            // Text(
            //   '$_result',
            //   style: Theme.of(context).textTheme.headline4,
            // ),
          ],
        ),
      ),
      ),
    );
  }
}

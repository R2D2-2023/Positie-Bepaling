#include <SFML/Graphics.hpp>
#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/objdetect.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include "./lib/SimpleSerial.h"
#include "rectangle.hpp"
#include "text.hpp"
#include "picture.hpp"
#include "math.h"
using namespace cv;
using namespace std;

int main() {
    char com_port[] = "\\\\.\\COM6";
    DWORD COM_BAUD_RATE = CBR_9600;
    SimpleSerial Serial(com_port, COM_BAUD_RATE);
    int reply = 0;

    Mat frame;
    VideoCapture cap;
    int deviceID = 0;
    int apiID = cv::CAP_ANY; 

    QRCodeDetector qrDecoder = QRCodeDetector();

    int x = 0;
    int y = 0;
    int angle = 0;

    sf::RenderWindow window{ sf::VideoMode{ 640, 480 }, "SFML window" };

    // rectangle p1( sf::Vector2f( 320, 240 ), sf::Vector2f( 50, 100 ) );
    sprite a1( sf::Vector2f( 320, 240 ), sf::Vector2f( 0.5, 0.5 ), "ArrowUp.png" );
    sprite m1( sf::Vector2f( 0, 0 ), sf::Vector2f( 1.0, 1.0 ), "testMap.png" );
    text t1( sf::Vector2f( 10, 10 ), 60 );
    drawable * objects[] = { &m1, &a1, &t1 }; // Drawable * array en geen Drawable want reference is natuurlijk address en geen object.
    
    cap.open(deviceID, apiID);
    if (!cap.isOpened()) {
        cerr << "ERROR! Unable to open camera\n";
        return -1;
    }

    if( Serial.connected_ ) {
        // Main window loop.
        while (window.isOpen()) {
            // wait for a new frame from camera and store it into 'frame'
            cap.read(frame);
            // check if we succeeded
            if (frame.empty()) {
                cerr << "ERROR! blank frame grabbed\n";
            }

            string qrReply = "1";
            std::string data = qrDecoder.detectAndDecode(frame);
            if(data.length()>0) {
                cout << data << endl;
                if(data == "1"){
                    Serial.WriteSerialPort(&qrReply[0]);
                }
            }

            // Read incoming serial data.
            string incoming = Serial.ReadSerialPort();
            if( incoming != "" ) {
                // char* coord = strtok( &incoming[0], "," );
                // x = atoi(coord);
                // coord = strtok( NULL, "," );
                // y = atoi(coord);
                // coord = strtok( NULL, "," );
                // angle = atoi(coord);
                std::string token;
                std::string delimiter = ",";
                token = incoming.substr(0, incoming.find(delimiter));
                x = atoi(&token[0]);
                incoming.erase(0, incoming.find(delimiter) + delimiter.length());
                token = incoming.substr(0, incoming.find(delimiter));
                y = atoi(&token[0]);
                incoming.erase(0, incoming.find(delimiter) + delimiter.length());
                token = incoming.substr(0, incoming.find(delimiter));
                angle = atoi(&token[0]);

                std::cout<<x<<','<<y<<','<<angle<<'\n';
            }

            if (angle > 348.75 || angle < 11.25) {
                t1.setDirection("N");
            }
            else if (angle > 11.25 && angle < 33.75) {
                t1.setDirection("NNE");
            }
            else if (angle > 33.75 && angle < 56.25) {
                t1.setDirection("NE");
            }
            else if (angle > 56.25 && angle < 78.75) {
                t1.setDirection("ENE");
            }
            else if (angle > 78.75 && angle < 101.25) {
                t1.setDirection("E");
            }
            else if (angle > 101.25 && angle < 123.75) {
                t1.setDirection("ESE");
            }
            else if (angle > 123.75 && angle < 146.25) {
                t1.setDirection("E");
            }
            else if (angle > 146.25 && angle < 168.75) {
                t1.setDirection("SSE");
            }
            else if (angle > 168.75 && angle < 191.25) {
                t1.setDirection("S");
            }
            else if (angle > 191.25 && angle < 213.75) {
                t1.setDirection("SSW");
            }
            else if (angle > 213.75 && angle < 236.25) {
                t1.setDirection("SW");
            }
            else if (angle > 236.25 && angle < 258.75) {
                t1.setDirection("WSW");
            }
            else if (angle > 258.75 && angle < 281.25) {
                t1.setDirection("W");
            }
            else if (angle > 281.25 && angle < 303.75) {
                t1.setDirection("WNW");
            }
            else if (angle > 303.75 && angle < 326.25) {
                t1.setDirection("NW");
            }
            else if (angle > 326.25 && angle < 348.75) {
                t1.setDirection("NWN");
            }

            a1.setRotation((float)angle);
            a1.jump(sf::Vector2f(x, y));
            // if( sf::Keyboard::isKeyPressed(sf::Keyboard::Space) ) {
            //     float speed = 0.1;
            //     float y_Offset = cos(reply * 3.14159265359 / 180) * speed;
            //     float x_Offset = sin(reply * 3.14159265359 / 180) * speed;
            //     a1.move(sf::Vector2f(x_Offset, -y_Offset));
            // }

            string resetReply = "r";
            if( sf::Keyboard::isKeyPressed(sf::Keyboard::R) ) {
                Serial.WriteSerialPort(&resetReply[0]);
                a1.jump(sf::Vector2f(320.0, 240.0));
            }

            string moveReply = "m";
            if( sf::Keyboard::isKeyPressed(sf::Keyboard::M) ) {
                Serial.WriteSerialPort(&moveReply[0]);
            }

            // Update window.
            window.clear();
            for( drawable * object : objects ){
			    object->draw( window );
		    }
            window.display();
            
            // Display Webcam Image.
            imshow("Live", frame);

            // Handle window.
            sf::Event event;
            if( window.pollEvent(event) ){
                if (event.type == sf::Event::Closed) {
                    window.close();
                }
            }
        }
    }
}
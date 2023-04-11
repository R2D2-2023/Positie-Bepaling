#include <SFML/Graphics.hpp>
#include "./lib/SimpleSerial.h"
#include "rectangle.hpp"
#include "text.hpp"
#include "picture.hpp"
#include "math.h"

int main() {
    char com_port[] = "\\\\.\\COM6";
    DWORD COM_BAUD_RATE = CBR_9600;
    SimpleSerial Serial(com_port, COM_BAUD_RATE);
    int reply = 0;

    sf::RenderWindow window{ sf::VideoMode{ 640, 480 }, "SFML window" };

    // rectangle p1( sf::Vector2f( 320, 240 ), sf::Vector2f( 50, 100 ) );
    sprite a1( sf::Vector2f( 320, 240 ), sf::Vector2f( 0.5, 0.5 ), "ArrowUp.png" );
    sprite m1( sf::Vector2f( 0, 0 ), sf::Vector2f( 1.0, 1.0 ), "testMap.png" );
    text t1( sf::Vector2f( 10, 10 ), 60 );
    drawable * objects[] = { &m1, &a1, &t1 }; // Drawable * array en geen Drawable want reference is natuurlijk address en geen object.
    
    if( Serial.connected_ ) {
        // Main window loop.
        while (window.isOpen()) {
            // Read incoming serial data.
            string incoming = Serial.ReadSerialPort();
            if( incoming != "" ) {
                reply = atoi(&incoming[0]);
                std::cout<<reply<<'\n';
            }

            if (reply > 348.75 || reply < 11.25) {
                t1.setDirection("N");
            }
            else if (reply > 11.25 && reply < 33.75) {
                t1.setDirection("NNE");
            }
            else if (reply > 33.75 && reply < 56.25) {
                t1.setDirection("NE");
            }
            else if (reply > 56.25 && reply < 78.75) {
                t1.setDirection("ENE");
            }
            else if (reply > 78.75 && reply < 101.25) {
                t1.setDirection("E");
            }
            else if (reply > 101.25 && reply < 123.75) {
                t1.setDirection("ESE");
            }
            else if (reply > 123.75 && reply < 146.25) {
                t1.setDirection("E");
            }
            else if (reply > 146.25 && reply < 168.75) {
                t1.setDirection("SSE");
            }
            else if (reply > 168.75 && reply < 191.25) {
                t1.setDirection("S");
            }
            else if (reply > 191.25 && reply < 213.75) {
                t1.setDirection("SSW");
            }
            else if (reply > 213.75 && reply < 236.25) {
                t1.setDirection("SW");
            }
            else if (reply > 236.25 && reply < 258.75) {
                t1.setDirection("WSW");
            }
            else if (reply > 258.75 && reply < 281.25) {
                t1.setDirection("W");
            }
            else if (reply > 281.25 && reply < 303.75) {
                t1.setDirection("WNW");
            }
            else if (reply > 303.75 && reply < 326.25) {
                t1.setDirection("NW");
            }
            else if (reply > 326.25 && reply < 348.75) {
                t1.setDirection("NWN");
            }

            a1.setRotation((float)reply);
            if( sf::Keyboard::isKeyPressed(sf::Keyboard::Space) ) {
                float speed = 0.1;
                float y_Offset = cos(reply * 3.14159265359 / 180) * 0.1;
                float x_Offset = sin(reply * 3.14159265359 / 180) * 0.1;
                a1.move(sf::Vector2f(x_Offset, -y_Offset));
            }

            string reply = "r";
            if( sf::Keyboard::isKeyPressed(sf::Keyboard::R) ) {
                Serial.WriteSerialPort(&reply[0]);
                a1.jump(sf::Vector2f(320.0, 240.0 ));
            }

            // Update window.
            window.clear();
            for( drawable * object : objects ){
			    object->draw( window );
		    }
            window.display();

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
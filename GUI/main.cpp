#include <SFML/Graphics.HPP>
#include "./lib/SimpleSerial.h"
#include "rectangle.hpp"
#include "text.hpp"
#include "math.h"

int main() {
    char com_port[] = "\\\\.\\COM6";
    DWORD COM_BAUD_RATE = CBR_9600;
    SimpleSerial Serial(com_port, COM_BAUD_RATE);
    int reply = 0;

    sf::RenderWindow window{ sf::VideoMode{ 640, 480 }, "SFML window" };

    rectangle p1( sf::Vector2f( 320, 240 ), sf::Vector2f( 100, 50 ) );
    text t1( sf::Vector2f( 10, 10 ), 60 );
    drawable * objects[] = { &p1, &t1 }; // Drawable * array en geen Drawable want reference is natuurlijk address en geen object.
    
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

            p1.setRotation((float)reply);
            if( sf::Keyboard::isKeyPressed(sf::Keyboard::Space) ) {
                float y_Offset = tan( reply * 3.14159265359 / 180.0 ) * 1.0;
                if( reply > 180 ) {
                    float y_Offset = tan( reply * 3.14159265359 / 180 ) * 1;
                    p1.move(sf::Vector2f( ( -0.01 ), ( -y_Offset * 0.01 ) ));
                }
                else {
                    float y_Offset = tan( reply * 3.14159265359 / 180 ) * 1;
                    p1.move(sf::Vector2f( ( +0.01 ), ( y_Offset * 0.01 ) ));
                }
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
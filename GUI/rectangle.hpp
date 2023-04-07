#ifndef RECTANGLE_HPP
#define RECTANGLE_HPP

#include <SFML/Graphics.hpp>
#include "object.hpp"

class rectangle : public drawable {
    private:
        sf::Vector2f position;
        sf::Vector2f size;
        sf::Color color;
        float angle;

    public:
        void draw( sf::RenderWindow & window ) override {
            sf::RectangleShape rectangle;
            rectangle.setSize(size);
            rectangle.setPosition(position);
            rectangle.setFillColor( color );
            rectangle.setRotation(angle);
            rectangle.setOrigin(rectangle.getSize().x * 0.5f, rectangle.getSize().y * 0.5f);
            rectangle.setPosition(rectangle.getPosition().x + rectangle.getOrigin().x, rectangle.getPosition().y + rectangle.getOrigin().y);
            window.draw(rectangle);
        }

        sf::FloatRect returnRect(){
            sf::RectangleShape rectangle;
            rectangle.setSize(size);
            rectangle.setPosition(position);
            return rectangle.getGlobalBounds();
        }

        void setRotation( float targetAngle ){
	        angle = targetAngle;
        }

        void jump( sf::Vector2f target ){
	        position = target;
        }

        void jump( sf::Vector2i target ){
            jump( sf::Vector2f( 
                static_cast< float >( target.x ), 
                static_cast< float >( target.y )
            ));
        }

        void move( sf::Vector2f delta ){
            position += delta;
        }

        void setColor( int red, int green, int blue ) {
            color = sf::Color( red, green, blue );
        }

        rectangle( sf::Vector2f position, sf::Vector2f size ):
        position(position),
        size(size),
        color( sf::Color( 0, 255, 0 ) )
        {}
};

#endif
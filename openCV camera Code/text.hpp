#ifndef TEXT_HPP
#define TEXT_HPP

#include <SFML/Graphics.hpp>
#include "object.hpp"

class text : public drawable {
    private:
        sf::Vector2f position;
        float size;
        sf::Font font;
        std::string str;

    public:
        void draw( sf::RenderWindow & window ) override {
            sf::Text text(str, font);
            text.setCharacterSize(size);
            text.setStyle(sf::Text::Bold);
            text.setFillColor(sf::Color::White);
            window.draw(text);
        }

        void setDirection( std::string direction ) {
            str = direction;
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

        text( sf::Vector2f position, float size ):
        position(position),
        size(size)
        {
            font.loadFromFile("font.ttf");
        }
};

#endif
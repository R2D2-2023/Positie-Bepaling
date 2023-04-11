#ifndef PICTURE_HPP
#define PICTURE_HPP

#include <SFML/Graphics.hpp>
#include "object.hpp"

class sprite : public drawable {
    protected:
        sf::Vector2f position;
        sf::Vector2f scale;
        float angle;

    private:
        sf::Texture texture;

    public:
        void draw( sf::RenderWindow & window ) override {
            sf::Sprite sprite;
            sprite.setTexture(texture);
            sprite.setPosition(position);
            sprite.setRotation(angle);
            sprite.setScale(scale);
            sprite.setOrigin(64 * 0.5f, 64 * 0.5f);
            sprite.setPosition(sprite.getPosition().x + sprite.getOrigin().x, sprite.getPosition().y + sprite.getOrigin().y);
            window.draw(sprite);
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

        sprite( sf::Vector2f position, sf::Vector2f scale, std::string filePath ):
            position(position),
            scale(scale)
        {
            texture.loadFromFile(filePath);
        }
};

#endif
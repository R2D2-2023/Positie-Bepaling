#ifndef DRAWABLE_HPP
#define DRAWABLE_HPP

#include <SFML/Graphics.hpp>

class drawable {
public:
    virtual void draw( sf::RenderWindow & window ){}
};

#endif
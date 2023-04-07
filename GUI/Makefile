main.exe : Main.o SimpleSerial.o
	g++ build/Main.o build/SimpleSerial.o -o ".\build\main.exe" -LC:\SFML-2.5.1\lib -lsfml-graphics -lsfml-window -lsfml-system -lsfml-audio
	".\build\main.exe"

Main.o: main.cpp
	g++ -c main.cpp -IC:\SFML-2.5.1\include -o ".\build\Main.o"

SimpleSerial.o: lib/SimpleSerial.cpp lib/SimpleSerial.h
	g++ -c lib/SimpleSerial.cpp -o ".\build\SimpleSerial.o"
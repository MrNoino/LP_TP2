# LP - PW 2 - Reuse of code produce by others

## 1. Introduction
Code reuse is a programming technique that reduces time and resources to develop software. The concept
code reuse is typically applied in two different ways: (1) proprietary code, or (2) produced code
by third parties (e.g., libraries, frameworks, APIs – Application Programming Interface). This practical work (TP) aims to
objective to understand the main advantages and advantages of reusing code produced by third parties, through the
development of an autonomous irrigation planning system using the Flask framework.
Flask is a software development framework that simplifies the process of building a web application.
Unlike other frameworks, Flask allows you to easily scale the size/complexity of the application you develop. This framework, which emerged in 2010 as a simple wrapper around Wekzeug and Jinga, is today a
one of the most popular Python frameworks for developing web applications, with a large and well-endowed community ([link](https://flask.palletsprojects.com/en/2.2.x/)).

## 2. Description
This TP pretends to develop an autonomous irrigation system. Simply put, the system must be flat
watering based on data collected by a soil moisture sensor, weather forecast, and humidity conditions
only make recommendations (ideal value and range of variation). Furthermore, the system must have a web management dashboard
either for data presentation (namely, last value collected by the soil moisture sensor and historical
over time, performance status of the irrigation system, weather forecast and the next irrigation), or to configure the
operating conditions of the irrigation system and location.
In addition to using the Flask framework, we recommend that students use other frameworks or libraries to
accelerate/facilitate web application development, such as:
• Bootstrap ([link](https://getbootstrap.com/)) for user interface development.
• SQLAlchemy ([link](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)) for interaction with the database.
• SocketIO ([link](https://flask-socketio.readthedocs.io/en/latest/ -server side; https://socket.io/ - client side)) for near real-time presentation of data collected by the soil moisture sensor , actuator status and other
information that is considered relevant.
• AccuWeather API ([link](https://rapidapi.com/stefan.skliarov/api/AccuWeather/details)) for maximum theoretical understanding.
• ChartJS ([link](https://www.chartjs.org/)) for creating charts.

# LP - TP 2 - Reutilização de código produzido por terceiros

## 1. Introdução 
A reutilização de código é uma técnica de programação que reduz o tempo e os recursos para desenvolver software. O conceito 
de reutilização de código é, normalmente, aplicado de duas formas diferentes: (1) código proprietário, ou (2) código produzido 
por terceiros (p. ex., bibliotecas, frameworks, APIs – Application Programming Interface). Este trabalho prático (TP) tem como 
objetivo compreender as principais vantagens e desvantagens da reutilização de código produzido por terceiros, através do 
desenvolvimento de um sistema autónomo de planeamento de regas recorrendo à framework Flask.
Flask é uma framework de desenvolvimento de software que simplifica o processo de construção de uma aplicação web. 
Contrariamente a outras frameworks, o Flask possibilita escalar facilmente a dimensão / complexidade da aplicação desenvolvida. Esta framework que surgiu, em 2010, como um simples wrapper (invólucro) em torno de Wekzeug e Jinga, é hoje uma 
das frameworks Python mais populares para o desenvolvimento de aplicações web, com uma ampla comunidade e bem documentada ([link](https://flask.palletsprojects.com/en/2.2.x/)). 

## 2. Descrição 
Pretende-se com este TP o desenvolvimento de um sistema autónomo de rega. De forma simples, o sistema deverá ser planear
as regas baseado nos dados coletados por um sensor de humidade do solo, previsão meteorológica, e condições de humidade 
do solo recomendadas (valor ideal e intervalo de variação). Além disso, o sistema deverá ter uma dashboard web de gestão 
quer para apresentação dos dados (nomeadamente, último valor coletado pelo sensor de humidade do solo e histórico ao 
longo do tempo, estado de atuação do sistema de rega, previsão meteorológica e da próxima rega), quer para configurar as 
condições de atuação do sistema de rega e local.
Para além da utilização da framework Flask, recomenda-se que os alunos utilizem outras frameworks ou bibliotecas para 
acelerar / facilitar o desenvolvimento da aplicação web, tais como:
• Bootstrap ([link](https://getbootstrap.com/)) para o desenvolvimento da interface com o utilizador.
• SQLAlchemy ([link](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)) para interação com a base de dados.
• SocketIO ([link](https://flask-socketio.readthedocs.io/en/latest/ -server side; https://socket.io/ - client side)) para apresentação em near real-time dos dados coletados pelo sensor de humidade do solo, estado do atuador e outras 
informações que forem consideradas pertinentes.
• AccuWeather API ([link](https://rapidapi.com/stefan.skliarov/api/AccuWeather/details)) para a obter as previsões meteorológicas.
• ChartJS ([link](https://www.chartjs.org/)) para criação de gráficos.

**Nuno Lopes | Afonso Fonseca | Karine Florencio**
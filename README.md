[![Build Status](https://travis-ci.com/ParnThanatibordee/KUIZ.svg?branch=master)](https://travis-ci.com/ParnThanatibordee/KUIZ)
[![codecov](https://codecov.io/gh/ParnThanatibordee/KUIZ/branch/master/graph/badge.svg?token=0XLOULBQ02)](https://codecov.io/gh/ParnThanatibordee/KUIZ)

# <img src="logo/KUIZ logo.png" width="150" height="80">

KUIZ is a web application quiz where you can create/take a quiz for learning and sharing knowledge from various subjects, questions and answers. The target of KUIZ is to help educational personnel (Teachers, Professors, Students) or people who want to enhance the knowledge both general and non at [Kasetsart University](https://www.ku.ac.th).

## Background

As the era changes, Technology keeps developing themself little bit per second that make our daily life integrate with technology much more, plus today virus pandemic make our life hard struggle with business, working and studying. Most students right now are having an online course instead of an offline course that causes several problems for both teachers and students  that didn’t prepare/familiar with materials and technology(Application). This is why we choose this topic to help students learn from the quiz like [Quizlet](https://quizlet.com/) instead of reading the whole book.

## Table of content:
| Content |
| ------------------------------ |
| [Wiki Home](../../wiki/Home) |
| [Vision Statement](../../wiki/Vision%20Statement) |
| [Features list](../../wiki/Requirements) |
| [Installation Instruction](../../wiki/Installation%20Instruction) |


## Requirement before starting KUIZ

| Name | Required version(s) |
|------|---------------------|
| Python | 3.7 or Higher |
| Django | 3.2.7 or Higher |

### Getting Start

1. Clone the respository to your machine or PC.

    ```
   git clone https://github.com/ParnThanatibordee/KUIZ.git
    ```
2. Change directory to the local repository by typing this command.

    ```
   cd KUIZ
    ```
3. Install virtualenv to your machine or PC by this command.

    ```
   py -m pip install virtualenv
    ```
4. Create virtual environment for KUIZ directory.

    ```
   py -m venv venv
    ```
5. Activate virtual environment.


    For Mac OS / Linux
    ```
   source venv\Scripts\activate
    ```
    
    For Window
    ```
   venv\Scripts\activate
    ```
6. Install all require packages by this command.

    ```
   pip install -r requirements.txt
    ```
7. Create .env file inside KUIZ (same level as settings.py) and change the debug=True.

    ```
   SECRET_KEY=YOUR_SECRET_KEY
   DEBUG=True
   GOOGLE_OAUTH2_KEY=YOUR_GOOGLE_OAUTH2_KEY
   GOOGLE_OAUTH2_SECRET=YOUR_GOOGLE_OAUTH2_SECRET
    ```
8. Type this command to migrate the KUIZ database.

    ```
   py manage.py migrate
    ```
9. Running the server by this command.
    ```
   py manage.py runserver
    ```
    
## Iterations


[Iteration1](../../wiki/Iteration-1)

[Iteration2](../../wiki/Iteration-2)

[Iteration3](../../wiki/Iteration-3)

[Iteration4](../../wiki/Iteration-4)

[Iteration5](../../wiki/Iteration-5)

[Iteration6](../../wiki/Iteration-6)

[Iteration7](../../wiki/Iteration-7)

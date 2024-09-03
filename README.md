
<h1>Aux Cord - socializing music recommendation </h1>
<table>
<tr>
<td>
  A Django website using the Spotify Web API to <b>create connection and belonging with music</b>! By using machine learning (particularly decision tree classification) to output an independent playlist based on the shared musical qualities of two inputted playlists, this program lets people with distinct musical tastes bond over new music they can both enjoy! <br>
  <b>Try it out with a friend here: https://aux-cord.onrender.com/</b> <br>
</td>
</tr>
</table>

![](http://ForTheBadge.com/images/badges/made-with-python.svg) <br>
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Django CI](https://github.com/ftrichardson/aux-cord/actions/workflows/django.yml/badge.svg)](https://github.com/ftrichardson/aux-cord/actions/workflows/django.yml)

<img width="1346" alt="Screen Shot 2024-02-07 at 4 41 08 AM" src="https://github.com/ftrichardson/aux-cord/assets/141296571/f802aff0-b08d-4b93-a47b-0eeda7aba996">

## Table of Contents
 [Demo](#demo)&nbsp;&#8226;&nbsp;[Built With](#built-with)&nbsp;&#8226;&nbsp;[About This App/User Story](#about)&nbsp;&#8226;&nbsp;[Usage](#usage)


## Demo

https://github.com/user-attachments/assets/cb6f3e78-2e31-45a1-bd1b-cc4a0eab5704


## Built With
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Spotify](https://img.shields.io/badge/Spotify-1ED760?style=for-the-badge&logo=spotify&logoColor=white)


## Usage

**1.** Clone the repository and navigate to aux-cord/ui directory
```python
git clone https://github.com/ftrichardson/aux-cord

cd aux-cord/ui
```

**2.** Create and activate a virtual environment
```python
virtualenv env

source env/bin/activate
```

**3.** Install dependencies
```python
pip install -r requirements.txt
```

**4.** Set up migrations
```python
python manage.py migrate
```

**5.** Start project's development server
```python
python manage.py runserver
```

**6.** Open your web browser and visit <a href="http://127.0.0.1:8000/" target="_blank">http://127.0.0.1:8000/</a> to access the application.

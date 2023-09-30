![aux-cord-banner-updated](https://github.com/ftrichardson/aux-cord/assets/141296571/ba00f7bd-da3d-48f3-8a29-d2c75a70cc95)
<p align="center">
  <a href="#description">Description</a> •
  <a href="#third-party-libraries-used">Third-Party Libraries Used</a> •
  <a href="#demo">Demo</a> •
  <a href="#installation">Installation</a>
</p>

## Description
This program socializes Spotify’s music recommendation system by using machine learning to output an independent playlist based on the shared musical qualities of two inputted playlists, enabling Spotify users with distinct musical tastes to algorithmically discover musical commonalities (i.e. sharing the aux cord).

## Third-Party Libraries Used
* pandas
* scikit-learn
* requests
* spotipy

## Demo
https://github.com/ftrichardson/aux-cord/assets/141296571/1a4598e4-10fb-47b4-ab1f-e516036f7fe5



## Installation

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
python manage.pr migrate
```

**5.** Start project's development server
```python
python manage.py runserver
```

**6.** Open your web browser and visit <a href="http://127.0.0.1:8000/" target="_blank">http://127.0.0.1:8000/</a> to access the application.


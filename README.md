![aux-cord-banner-updated](https://github.com/ftrichardson/aux-cord/assets/141296571/ba00f7bd-da3d-48f3-8a29-d2c75a70cc95)

**Now live! Try it out with a friend here: https://aux-cord.onrender.com/
## Table of Contents
<p>
  <a href="#description">Description</a>
</p>
<p>
  <a href="#third-party-libraries-used">Third-Party Libraries Used</a>
</p>
<p>
  <a href="#demo">Demo</a>
</p>
<p>
  <a href="#installation">Installation</a>
</p>

## Description
This program socializes Spotify’s music recommendation system by using machine learning (particularly decision tree classification) to output an independent playlist based on the shared musical qualities of two inputted playlists, enabling Spotify users with distinct musical tastes to algorithmically discover musical commonalities (i.e. sharing the aux cord).

## Third-Party Libraries Used
* pandas
* scikit-learn
* requests
* spotipy
* matplotlib

## Demo

https://github.com/ftrichardson/aux-cord/assets/141296571/deda1565-3119-47c6-8b73-e72ab9633f1d


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
python manage.py migrate
```

**5.** Start project's development server
```python
python manage.py runserver
```

**6.** Open your web browser and visit <a href="http://127.0.0.1:8000/" target="_blank">http://127.0.0.1:8000/</a> to access the application.

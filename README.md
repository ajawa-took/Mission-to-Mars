# Mission-to-Mars
splinter, beautysoup; flask, mongdb; and a tiny bit of bootstrap html.

### Deliverable 3 extra bootstrap components
1. article paragraph is now centered
2. button is now yellow ( btn-warning )
3. "Mars" in the jumbotron title is italicized

### What's where

- All the scraping happens in `scraping.py`. You can play with it in a python terminal by starting with `import scraping`. If you want to alter the code, play with the `Mission_to_Mars_Challenge.ipynb` jupyter notebook instead.

- All the mongoing and flasking happens in `app.py`. The `/scrape` route is not meant to be displayed ever, it's just the secret place where the scraping backend does its work.

- The webpage is laid out in `index.html`. Flask gives it a dictionary named `mars` (which flask pulls from the mongo database), and the html can get at stuff in that distionary like so.
  - If the value associated with a key (e.g. `news_title`) is simple, like a string, `{{ mars.news_title }}` inserts it into html.
  - One more complicated thing you can do is iterate a list. In our case, pythonic `mars['hemispheres']` also known as `mars.hemispheres` in this setting, is a list. We can iterate through it with 
  ```
  {% for hemisphere in mars.hemispheres %}
  lines of html you want to be executed for each thingy in the list
  {% endfor %}
  ```


### Problems

 - Sometimes, the scraping code throws "stale" "not attached to document" errors. I cannot tell what makes the difference: different runs of same code sometimes throw it and somtimes don't. Closing and opening the automated browser a lot seems to help. This may have something to do with old versions of everything: at the start of the course, on the advice of TAs, I set my environment to be python3.7 while lots of latest versions of packages want 3.8.

 - I was not able to cleanly scrape the 4 urls to click for the hemispheres scrape. My best efforts yeild 9 objects on the webpage being scraped, of which [1], [3], [5], and [7] are the ones we want. My code extracts those.


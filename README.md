Go-links
----------

Very simple internal short-linking system.

The home for this project is https://gitlab.com/daniellawrence/go-links

screenshots
-------------

![https://gitlab.com/daniellawrence/go-links/raw/master/screenshots/index.png](https://gitlab.com/daniellawrence/go-links/raw/master/screenshots/index.png)
![https://gitlab.com/daniellawrence/go-links/raw/master/screenshots/edit.png](https://gitlab.com/daniellawrence/go-links/raw/master/screenshots/edit.png)


Examples
----------

```python
DEMO_RECORDS = [
    ('mail', 'https://mail.google.com'),
    ('git', 'https://gitlab.com{/search?terms=^}'),
    ('github', 'https://github.com{/search?terms=^}'),
    ('in', 'https://linkedin.com'),
    ('fb', 'https://www.facebook.com')
]
```

If you visit http://go/git you would be redirect to https://gitlab.com

However if you visit `http:/go/git go-links`, you would be redirected to search, for "go-links" 


TODO
-----

* ~Save GoRecords into a database~
* ~Push lots of things into a `settings.py` file~
* Add OAuth2
* Show "your" go-links
* Pretty up the index of links
* Optional "hits" into the database

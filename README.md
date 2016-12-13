Go-links
----------

Very simple internal short-linking system.

The home for this project is https://gitlab.com/daniellawrence/go-links

Example short link

```yaml
---
name: git
link: https://gitlab.com{/search?terms=^}
```

If you visit http://go/git you would be redirect to https://gitlab.com

However if you visit `http:/go/git go-links`, you would be redirected to search, for "go-links" 


TODO
-----

* -Save GoRecords into a database-
* Add OAuth2
** Show "your" go-links
* Push lots of things into a `settings.py` file
* Pretty up the index of links
* Optional "hits" into the database

# insta2reddit

Python script to post an Instagram picture into a target subreddit.

You do not need an Instagram account, as the script does not rely on any API to fetch pictures but  
uses *Selenium* instead to parse the content of a given post and download the image from there.

However: you will need a reddit account as well as the access to a reddit app to post the image
there, this is done using *PRAW: The Python Reddit API Wrapper*.

## Create a Reddit App 

Once you are logged-in to reddit, an app can be created by accessing this page: https://www.reddit.com/prefs/apps/  
Do not forget to update both the *praw_client_id* and *praw_client_secret* variables in the *config.py* file so the
script can actually use your app for posting.

Your actual reddit account username and password are not stored in any file and will instead be prompted when
running the script.

## Usage

You can post one or more pictures from reddit to Instagram.

```
$ ./main.py https://www.instagram.com/p/SomePost r/subreddit1 post-title1 [https://www.instagram.com/p/Some0therPost r/subreddit2 post-title2 ...]
```

## It's not theft

The purpose of this script is not to steal content from Instagram creators by not crediting them or aknowledging
the source material, in fact: the script immediatly posts a comment under the post after its creation, this comment
links directly to the source Instagram post.
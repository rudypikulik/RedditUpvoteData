# RedditUpvoteData
A quick study on the effect of post timing on upvote amounts


  As a redditor, I was interested in finding what time of day was most likely to get a post the most upvotes, and I decided to do that through a python program and the PRAW reddit api. The IDs and times of posts are saved as they are posted, and the program waits 12 hours before logging the result of the post and it's upvote counts.

  The data is dumped into a pickle file as well as a CSV file. Since I had to start and stop the program a number of times through data collection, I used the pickle file to create a brand new CSV file at the end (script provided). Other people have done similar studies which have yielded silimar results. 

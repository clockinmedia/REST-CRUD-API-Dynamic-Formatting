I started by reading the tiny Flask example and watching the video, then cloned the code and made the two required changes: I added Mind Gym and The 48 Laws of Power to the hard-coded JSON and renamed every /books endpoint to /goodbooks. Next, I built a front end that uses fetch() to GET the data, shows a spinner while loading, displays an error message if the request fails, and highlights ratings of 4 or higher.

Two things surprised me. First, Flask returned the JSON keys in alphabetical order, so my table showed "author" before "id" until I set the column order myself. Second, the app would not run on my Mac because macOS uses port 5000 for AirPlay.

My code evolved from a basic script into something more reliable. I moved to port 5001, added a launcher file, and returned errors as JSON instead of HTML.

I now better understand HTTP status codes, statelessness, and how the client and server stay separate. I would like to learn more about connecting this API to a real database.

# System Documentation

| Authors | Date | Course |
| ------- | ---- | ------ |
| Adam Ivarsson & Lukas Michanek | 8th of October 2015 | TDP003 |

![](The simple diagram img URL)

This application uses quite a simple model. The user makes requests to the web server, which in this case is Flask, and then Flask works with the database to fetch the requested data. Jinja will turn the HTML templates into real HTML documents with the data that Flask got from the data layer, and a response will be made that lets the user see the webpage.

To further understand how this works, please look at the following UML diagram. It specifies in a simplified form what happens when you load and use the `/list` page, the most complicated part of the application.

![](The UML diagram img URL)

This is how functions in the presentation layer work:

Placeholder text.

All web requests and stack traces are also logged to a file on disk for easy debugging. This file contains the same type of information that you'd normally see in the console when running the server.

We also have a bit of error handling...

Placeholder.

The system was built to comply with this [system specification](), and additionally, all functions in the data layer are documented very well. If you have any doubts what so ever, reading the documented code will be of great help to you.

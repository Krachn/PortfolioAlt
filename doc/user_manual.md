# User Manual

This user manual will walk through the structure of the blog out and how to use it.

## Layout Structure

All pages inherit the base blog layout. This layout has a few elements that stay concistent throughout all pages:
* The sidebar, which contains information **about** the webpage. The sidebar has:
  * A picture of the blog owner.
  * Short info about the owner.
  * Navigation list with links to:
    * The start page.
    * The list page.
    * The techniques page.
* The blog logo and the blog title.

## Blog Structure

The front-end of your blog will consist of 4 pages (see list below):

* The Startpage (`/`)
  * Contains a "featured" post.
  * This page should look about the same as a project page.
* The List Page (`/list`)
  * Contains a list of all projects where each row consists of the following information:
    * The project name.
    * **The project date?**
    * **Technique tags?**
    * An image from the post.
    * A short description.
  * Has search functionality for filtering by text and techniques (any or all of the selected) with functions for sorting (ascending or decending date).
  * Clicking on the title of a post will bring you to the project page for that project.
* The Project Page (`/project/id`)
  * Presents all available information about a project to the user. This includes, but is not limited to:
    * The project name.
    * The project date (day, month, year).
    * All involved parties (ex. team members).
    * Techniques used, as a list of clickable tags. Clicking on one tag should bring you to the `/list` page, filtered by the tag you clicked on.
* The Techniques Page (`/techniques`)
  * Contains a list of all techniques used throughout all projects, followed by a list of all project that use that certain technique.
  * Clicking a project name will take you to that project's project page.
  * Clicking a technique name will take you to the list page filtered by the technique you clicked.

## Searching and Filtering

The list page contains a form to request blog posts matching your search and filtering criteria. Once requested the server will retrieve all matches, sort them, and then send them back to you. To do this you'd have to fill out the search and filtering form.

The form itself is divied up in two sections where the first section filters results based on selected techniques (checkboxes), and where the second section lets you select a sorting method and search blog posts by text. This is roughly what the form looks like:

![](http://i.imgur.com/alI9klf.png)

Checking the `Any` radio button and one or more techniques would match and return all blog posts that uses **any** of the selected techniques. Similarly, checking the `All` radio button and one or more techniques would match and return all blog posts that uses **all** of the selected techniques.

These posts may then be sorted by date using the dropdown list and choosing either `Ascending` or `Decending`.

Additionaly, there is a text search box if you'd rather prefer that.

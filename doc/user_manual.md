# User Manual

This user manual will walk through the structure of the blog out and how to use it.

Key rule: If it looks like a link, smells like a link, walks like a link, then it probably is a link, and that probably means that it is a link to either a blog post, or a certain technique that was used.

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
  * **This page should look identical to a project page?**
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
  * Clicking a technique name will take you to the list page filtered by the technique you clicked. Why you'd do that is way past me.

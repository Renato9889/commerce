<h1 align="center">Harvard University CS50 Commerce Project - Renato's Project (e-commerce) </h1>

<p align="justify"> This git repository contains an design of an e-commerce auction site that allowed users to post 
  auction listings, bid on listings, comment on those listings, and add listings to a “watchlist”. This project primarily centered around utilizing a database to store 
  and manage various website data, including user logins, items, comments, values, and additional information</p>

  <img src="https://github.com/Renato9889/commerce/assets/38532053/e57f271f-b7f8-42f5-90f3-1007f8e73ae2">
  <img src="https://github.com/Renato9889/commerce/assets/38532053/7e7b654e-d624-42a3-a400-e756883deea7">
  <img src="https://github.com/Renato9889/commerce/assets/38532053/34f44a30-162f-4633-870b-792adeb55cde">
  <img src="https://github.com/Renato9889/commerce/assets/38532053/493f5f53-be17-44c8-b621-396a250442ac">

<h2>Specification and details</h2>
<a href="[https://youtu.be/mbwFpwo3gHU](https://youtu.be/9ouauawwXZ4?si=vDAWZzQ6ugRTgNDD)">Click here to view the project execution video</a>
<ul>
  <li>Django site name: mymy-commerce</li>
  <li>Shows auction listings from the site, in the active listing each item is displayed showing title, description, current price, date posted and photo.</li>
  <li>Categories, page that displays a list of all listing categories. By clicking on any category, the user is taken to a page that displays all active listings in that category.</li>
  <li>The web pages Watchlist, Bids, Creating  Listing can only be accessed when logged in.</li>
  <li>User login.</li>
  <li>Watchlist, logged-in users can visit a watchlist page that displays all the listings they have added to their watchlist.</li>
  <li>When clicking on a listing, it takes the user to a specific page for that listing. On this page, users can view all the details about the listing, including the current listing price.  If the user is logged in, they can add the item to their 'watchlist.' If the item is already in the watchlist, the user can remove it. </li>
  <li> If the user is logged in, they can place a bid on the item. The bid must be at least as large as the initial bid and must be higher than any other bids that have been placed (if any). If the bid does not meet these criteria, the user will receive an error.</li>
  <li>The user can post comments on the listing page. The listing page displays all comments made on the listing.</li>
  <li>User bids higher than the item's current bid.</li>
  <li>Page shows bid details and status of all user items.</li>
  <li>The logged in user can “close” the auction of their posted items.</li>
  <li>User Register</li>
  <li>The user creates a new listing. Must specify a title for the listing, a text-based description, the category of the listing, an image url, and the starting bid.</li>
  <li>Error if you do not fill in all the fields correctly when creating a new listing.</li>
  <li> Page informs that item was closed by the user who posted it, making it impossible to bid further.</li>
  <li>Django Admin Interface: Through the Django Admin Interface, a site administrator is able to view, add, edit, and delete any listings, comments, and bids made on the site.</li>
</ul>

## ✔️ Techniques and technologies used
- ``Python3``
- ``Data Base``
- ``SQL``
- ``HTML``
- ``Django``
- ``CSS``
- ``JavaScript``
- ``VisualStudioCode``

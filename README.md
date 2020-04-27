Chategories
===========
Chategories is a prototype implementation of a multi-player SMS game.
It is similar to the board game, Scattergories® with slightly different possibilities and scoring.

### Pre-requisites
1. AT&T Marketplace Account, with a purchased Local Number.
2. A host to run this application with a "publicly routable FQDN"

NOTE: Item 2 can be satisfied by running this application on a laptop behind a NAT/firewall, and installing a tunnelling utility such as *ngrok*.  This utility registers a temporary FQDN on their public server, and routes traffic via a secure tunnel to your app running on localhost.  See https://ngrok.com

### Deployment Instructions
1. Clone this repo
2. Run the application  (e.g. python3 Chategories).  
NOTE: By default, Flask http server listens on port 5000.
3. Verify the application is running by attempting to access it using a browser.  e.g. URL is http://localhost:5000/
4. If using a utility like ngrok, start it now.  Make a note of the public https endpoint it reports.

### Configuration

#### App Setup

Ideally, this step should only need to be done once, and may need to be repeated if the server or app needs to be restarted.

Using a browser, navigate to the SMSbot Home screen http://localhost:5000/
Select App Setup from the navigation menu.
Fill in the SMSbot Configuration form:
- Private Project Key is the value from your AT&T API Marketplace Account.
- Private Project Secret is the value from your AT&T API Marketplace Account.
- Projet TN is a Telephone Number resource you have reserved in the AT&T API Marketplace Account and assigned to the Project.
- APIM URL is the URL of the AT&T API Marketplace server.  (generally, keep the default value)
- Public URL is the URL that APIM server will use to call the webhook in this application.  When using ngrok, this is the value produced in Step 4 of Deployment Instructions above. 

#### Customize Categories
The app is deployed with a starter set of categories.
You can add more categories or de-activate any of the existing categories.
Using a browser, navigate to the SMSbot Home screen http://localhost:5000
Select the Customize Categories Menu from the navigation menu.

The form presents the set of  *category* items that make up the possibilities.
Use this form to:
- modify the position value
- modify the category  value
- activate or deactivate a particular  item
- add a new category item 

Remember to click on Submit to make your changes take effect.

#### Customize Alphabet
The form presents the set of *position* and *letter* items that make up the alphabet possibilities.
Use this form to:
- modify the position value  (begins with or ends with)
- modify the letter  value.  Note: can be more than 1 letter.
- activate or deactivate a particular  item
- add a new alphabet item 

Remember to click on Submit to make your changes take effect.
### Game Logic
The game composes a question by randomly pairing a Category item with an Alphabet item, and sending the question to all players.
Each player submits their answer to the question.
An answer that is invalid scores -1.
An answer that matches another player scores 0.
A unique correct answer scores 1.

### Commands

A message from a player can be either a command or an answer.  Commands are one of the following key words, followed by a colon (:).

| Command Key Word | Arguments | Description |
| ------------------ | ---------- | ------------- |
| join:            | name      | adds player *name* to the game |
| drop:            |           | removes the player from the game |
| new:             |           | initiates a new game |
| reset:           |           | reset scores of all players to 0 |

#### Example Play

| Player | Message Content |  Player 1 sees | Player 2 sees| Player 3 sees|
| ----- | ---------------- | ---------- | ---------| -------- |
|  1  | join: Doug | Doug joined |                 |          |
| 2   | join: Carl | Carl joined | Carl joined     |          |
| 3   | join: Dom  | Dom joined  | Dom joined      | Dom joined |
| 3   | new:       | New game! names of streets that begins with M | New game! names of streets that begins with M | New game! names of streets that begins with M |
| 1   | Main       | Noted       |                 |          |
| 2   | Maple      |             | Noted           |          |
| 3   | Broad      | Unique response Main from Doug. Unique response Maple from Carl. Invalid response Broad from Dom.  Current Score: Doug 1, Carl 1, Dom -1.  Next category!  Capitals of states that begin with T |  Unique response Main from Doug. Unique response Maple from Carl. Invalid response Broad from Dom.  Current Score: Doug 1, Carl 1, Dom -1.  Next category!  Capitals of states that begin with T | Unique response Main from Doug. Unique response Maple from Carl. Invalid response Broad from Dom.  Current Score: Doug 1, Carl 1, Dom -1.  Next category!  Capitals of states that begin with T |
| 1   | Topeka     | Noted       |                 |          |
| 2   | Topeka     |             | Noted           |          |
| 3   | Trenton    | Duplicate response Topeka from Doug.  Duplicate response Topeka from Carl.  Unique response Trenton from Dom.  Current Score: Doug 1, Carl 1, Dom 0.  Next category! sport teams that begins with O | Duplicate response Topeka from Doug.  Duplicate response Topeka from Carl.  Unique response Trenton from Dom.  Current Score: Doug 1, Carl 1, Dom 0.  Next category! sport teams that begins with O | Duplicate response Topeka from Doug.  Duplicate response Topeka from Carl.  Unique response Trenton from Dom.  Current Score: Doug 1, Carl 1, Dom 0.  Next category! sport teams that begins with O |
| 3   | drop:      | Dom has left | Dom has left   |          |
| 1   | Orioles    | Noted        |                |          |
| 2   | Oakland    | Unique response Orioles from Doug.  Unique response Oakland from Carl,  Current Score: Doug 2, Carl 2.  Next category!  Colors that being with P | Unique response Orioles from Doug.  Unique response Oakland from Carl,  Current Score: Doug 2, Carl 2.  Next category!  Colors that being with P | |


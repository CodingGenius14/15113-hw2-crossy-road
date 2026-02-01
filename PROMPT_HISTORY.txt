1.)
Strategy: Use Claude to generate the code for this project and prompt it iteratively to make small improvements after each iteration and use descriptive prompts clearly outlining the desired results. Started off by understanding what it needed from me to build out the game.

2.)
Below you will find a list of the prompts that I provided to Claude (Sonnet 4.5) 
The prompts with (*) are prompts that Claude did a good job of implementing

Prompt:
what all information from me do u need to build out a full game of crossy road?

==========================================================================================

Prompt: 
1. Objective
The main goal of Crossy Road is simple:
* Move your character forward as far as possible without dying.
* Score points based on the number of tiles (or “steps”) your character crosses.
* Survival is the main challenge; there is no “end” to the level—just try to go as far as possible.
2. Movement
* The game is grid-based, with movement restricted to one tile at a time.
* Typical movements:
   * Forward (main direction): +1 tile on Y-axis
   * Backward: -1 tile on Y-axis
   * Left/Right: ±1 tile on X-axis
* The character moves one tile per tap/press.
* Characters do not move continuously; movement is discrete.
3. Obstacles
The world consists of repeating lanes of different types. Each lane has specific mechanics:
a) Roads with Vehicles
* Cars, trucks, and other vehicles move horizontally across the lane.
* Colliding with a vehicle kills the character.
* Vehicles can have different speeds and sizes.
b) Rivers/Lakes
* Water lanes contain logs, lily pads, or turtles that move horizontally.
* The player must jump onto these moving objects to cross safely.
* Falling into water kills the character.
c) Train Tracks
* Trains pass horizontally and often very fast.
* The player must wait for a gap or time movement to avoid being hit.
d) Static Obstacles
* Trees, rocks, fences, and other terrain features block movement.
* You cannot move into a tile with an obstacle.
5. Scoring
* 1 point per forward step (tile moved forward).
* Bonus points may occur for:
   * Crossing rivers safely
   * Hopping onto moving platforms
   * Staying alive longer
* High scores are recorded per session.
6. Death & Restart
* Character dies if:
   * Hit by a vehicle
   * Falls in water
   * Collides with certain obstacles (like trains)
* After death, the game resets from the starting position.
7. Environment & Randomization
* The game world is procedurally generated, meaning:
   * Each lane type is random (roads, rivers, grass, train tracks, etc.).
   * Player faces different obstacles and layouts each session.
* This keeps the game unpredictable and replayable.
8. Additional Mechanics
* Safe zones: Some lanes are grass or safe tiles where no hazards exist.
* Character unlocks: Different characters may have cosmetic effects, but gameplay remains the same.
* Progressive difficulty:
   * Vehicles and rivers move faster over time or as you go further.
   * Gaps between obstacles may shrink. | Build the game in pygame and it should be a clean and workable version of crossyroad, it doesnt need to be perfect or exact but should be playable and get all the main functionalities down 

==========================================================================================

Prompt: 
make sure the obstacles go a lot slower and at a normal pace, the score should also reset when the game is over, and the sprite should start at the beginning of the screen, and u dont need to update the readme, just give the code

==========================================================================================

Prompt: 
remmebr start of the screen is south and when the player hits the up arrow the sprite should move north and the sprite can not move backwards only forward and sideways, also pls make the hazards go a lot slower similar to the game

==========================================================================================

* Prompt:
make the sprites go a lot slower than what u currently have, and make the sprite start at the southmost part of the screen rn u have the sprite at the top of the screen it needs to srart at the bottom

==========================================================================================

* Prompt:
this is a lot better, there is only 1 issue though, you have the movement direction mixed up for the sprite. Right now you have the sprite at the top most of the screen which is NOT CORRECT. You need the sprite to start at the bottom and then as the player clicks the up arrow it moves up the screen

==========================================================================================

Prompt:
this is much better! now one thing to note is when the chicken gets on the log it should move in the direction with the log until it moves forward to get off

==========================================================================================

* Prompt:
this is insanely good! Now try making the camera a little smoother so it doesnt feel so choppy every time the chicken moves forward

==========================================================================================

Prompt:
make sure its gradually catching up to the chicken throughout the game not just the initial few moves upward. Also really make sure that the cases for the game ending are met. the game should only end when the chicken makes direct contact with water or is hit by one of the obstacles

==========================================================================================

Prompt:
much better, now just make sure that the bottom of the screeen slowly moves forward catching up  to the chicken where if the chicken ends up staying stationary for too long the screen catches up to it and the game ends.

==========================================================================================

Prompt:
remmebr aftwer i make my first initial movements forward then the bottom of the screen should start moving in following the chicken , also make sure that it is impossible for the cicken to pass through a tree

==========================================================================================

Prompt:
the game should not be over in cases like these as it has not hit any hazard

==========================================================================================

* Prompt:
In Crossy Road, staying still for too long (approximately 5 seconds)  triggers an eagle to swoop down and snatch your character, immediately ending the game. This mechanic prevents stalling and forces constant forward progression





## Character sprites ###########################################################
##
## The sprite files were drawn on canvases of different sizes (Elena's are 900
## pixels tall, everyone else's 1000), so here each one is scaled to a fixed
## height on screen. To make someone taller or shorter, change their height
## below; everything else follows.
##
## Every sprite stands on the bottom of the screen. Use the pos_ transforms
## below to place them, e.g. "show emma at pos_right".

## How tall each full-body sprite is on screen, in pixels (the screen is 1080).
define sprite_height_girls = 940
define sprite_height_guys = 1000

## How tall the close-up (waist-up) sprites are on screen.
define sprite_height_closeup = 1000

image elena = Transform("images/elena.png", zoom=sprite_height_girls / 900.0)
image emma = Transform("images/emma.png", zoom=sprite_height_girls / 1000.0)
image gus = Transform("images/gus.png", zoom=sprite_height_guys / 1000.0)
image zane = Transform("images/zane.png", zoom=sprite_height_guys / 1000.0)

image elenaclassroom = Transform("images/elenaclassroom.png", zoom=sprite_height_closeup / 900.0)
image emmabus = Transform("images/emmabus.png", zoom=sprite_height_closeup / 1000.0)


## Positions ###################################################################
##
## Each one places the middle of the sprite at a point along the bottom of the
## screen.

transform pos_farleft:
    xpos 0.15 xanchor 0.5 ypos 1.0 yanchor 1.0

transform pos_left:
    xpos 0.25 xanchor 0.5 ypos 1.0 yanchor 1.0

transform pos_center:
    xpos 0.5 xanchor 0.5 ypos 1.0 yanchor 1.0

transform pos_right:
    xpos 0.75 xanchor 0.5 ypos 1.0 yanchor 1.0

transform pos_farright:
    xpos 0.85 xanchor 0.5 ypos 1.0 yanchor 1.0

## Emma in the bus seat, sitting a little lower.
transform pos_bus_seat:
    xpos 0.6 xanchor 0.5 ypos 1.0 yanchor 1.0 yoffset 20

## Phone chat ##################################################################
##
## Text messages are shown as chat bubbles inside a phone in the middle of the
## screen. Narration and inner thoughts keep using the normal textbox.
##
## In the script:
##
##     $ phone_open("Emma")   # show the phone with an empty chat
##     b_txt "Hey!"           # message from Emma (left side, Emma's color)
##     p_txt "Hi Emma"        # message from the player (right side)
##     p "(Oh no.)"           # normal dialogue still uses the textbox
##     $ phone_close()        # hide the phone

## Characters that talk through the phone.
define a_txt = PhoneCharacter("Elena", "#E31B61")
define b_txt = PhoneCharacter("Emma", "#0e719e")
define x_txt = PhoneCharacter("Zane", "#B5B9FF")
define p_txt = PhoneCharacter("[player_name]", "#7d00ae", mine=True)

## How long the "..." typing bubble shows before an incoming message.
define phone_typing_delay = 0.7

default phone_contact = ""
default phone_log = []
default phone_typing = None

init -1 python:

    def phone_text_color(color):
        """Dark text on light bubbles, white text on dark ones."""
        r, g, b = Color(color).rgb
        return "#222222" if 0.299 * r + 0.587 * g + 0.114 * b > 0.6 else "#ffffff"

    def phone_bubble_bg(color):
        return Frame(Transform("gui/chat/bubble.png", matrixcolor=TintMatrix(color)), 22, 22)

    def phone_open(contact):
        store.phone_contact = contact
        store.phone_log = [ ]
        store.phone_typing = None
        renpy.show_screen("phone_chat")
        renpy.with_statement(dissolve)

    def phone_close():
        renpy.hide_screen("phone_chat")
        renpy.with_statement(dissolve)

    class PhoneCharacter(ADVCharacter):
        """
        A character whose lines appear as chat bubbles in the phone. Lines from
        the other person are preceded by a short "..." typing bubble.
        """

        def __init__(self, name, bubble, mine=False, **properties):
            properties.setdefault("screen", "phone_say")
            properties.setdefault("color", bubble)
            # Without this the text gets the textbox's say_dialogue position.
            properties.setdefault("what_style", "phone_bubble_text")
            properties.setdefault("what_color", phone_text_color(bubble))
            # Chat messages appear all at once rather than typing out.
            properties.setdefault("what_suffix", "{fast}")
            ADVCharacter.__init__(self, name, show_mine=mine, show_bubble=bubble, **properties)
            self.phone_mine = mine
            self.phone_bubble = bubble

        def __call__(self, what, *args, **kwargs):
            if not self.phone_mine and phone_typing_delay and not renpy.is_skipping():
                # Hide the empty textbox while the "..." bubble shows.
                window = store._window
                store._window = False
                store.phone_typing = self.phone_bubble
                renpy.pause(phone_typing_delay)
                store.phone_typing = None
                store._window = window

            rv = ADVCharacter.__call__(self, what, *args, **kwargs)
            store.phone_log.append((self.phone_mine, self.phone_bubble, what))
            return rv


## The messages so far, plus the "..." bubble while the other person types.
screen phone_history():

    for mine, bubble, msg in phone_log[-15:]:
        frame:
            style "phone_bubble"
            xalign (1.0 if mine else 0.0)
            background phone_bubble_bg(bubble)
            text msg style "phone_bubble_text" color phone_text_color(bubble)

    if phone_typing:
        frame:
            style "phone_bubble"
            background phone_bubble_bg(phone_typing)
            hbox:
                style "phone_typing_dots"
                for i in range(3):
                    add Transform("gui/chat/dot.png", matrixcolor=TintMatrix(phone_text_color(phone_typing))) at phone_dot(i * 0.15)


## Shown for the whole conversation, behind the dialogue.
screen phone_chat():
    zorder -1

    fixed:
        style "phone"
        add "gui/chat/phone_frame.png"
        text "[phone_contact]" style "phone_contact"

        # The message area of the phone's screen. Old messages scroll off the
        # top and are clipped.
        fixed:
            style "phone_area"
            at phone_clip
            vbox:
                style "phone_messages"
                use phone_history


## The say screen used by PhoneCharacter. It draws the same phone on top of
## phone_chat, with the new message as the last bubble.
screen phone_say(who, what, mine=False, bubble="#888888"):

    fixed:
        style "phone"
        add "gui/chat/phone_frame.png"
        text "[phone_contact]" style "phone_contact"

        fixed:
            style "phone_area"
            at phone_clip
            vbox:
                style "phone_messages"
                use phone_history

                frame:
                    style "phone_bubble"
                    xalign (1.0 if mine else 0.0)
                    background phone_bubble_bg(bubble)
                    text what id "what" style "phone_bubble_text" color phone_text_color(bubble)


transform phone_clip:
    crop (0, 0, 339, 541)

transform phone_dot(delay):
    alpha 0.35
    pause delay
    block:
        linear 0.25 alpha 1.0
        linear 0.25 alpha 0.35
        pause 0.25
        repeat

style phone is fixed:
    xysize (490, 805)
    xalign 0.5
    ypos -45

style phone_area is fixed:
    pos (77, 130)
    xysize (339, 541)

style phone_typing_dots is hbox:
    spacing 6
    yalign 0.5

style phone_contact is text:
    pos (132, 84)
    size 26
    bold True
    color "#ffffff"

style phone_messages is vbox:
    xfill True
    yalign 1.0
    spacing 10
    xmargin 12
    ymargin 12

style phone_bubble is frame:
    xmaximum 250
    padding (16, 10, 16, 10)

style phone_bubble_text is text:
    size 22
    line_spacing 2

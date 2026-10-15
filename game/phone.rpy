## Phone chat ##################################################################
##
## Text messages are shown as chat bubbles inside a phone in the middle of the
## screen. The textbox stays visible underneath: for a message it shows the
## sender and the same line, and narration and inner thoughts use it as usual.
##
## In the script:
##
##     $ phone_open("Emma")             # show the phone with an empty chat
##     b_txt "Hey!"                     # message from Emma (left, Emma's color)
##     p_txt "Hi Emma"                  # message from the player (right)
##     p "(Oh no.)"                     # normal dialogue, phone stays up
##     $ phone_typing_start(b_txt)      # show "..." for Emma until she sends
##     $ phone_typing_start(p_txt)      # show "..." for the player
##     $ phone_typing_stop()            # remove all "..." bubbles
##     $ phone_close()                  # hide the phone

## Characters that talk through the phone.
## Elena replies almost instantly; Emma takes her time; Arielle replies slowly. Very slowly.
define a_txt = PhoneCharacter("Elena", "#E31B61", typing_delay=0.35)
define b_txt = PhoneCharacter("Emma", "#0e719e", typing_delay=1.3)
define x_txt = PhoneCharacter("Zane", "#B5B9FF")
define p_txt = PhoneCharacter("[player_name]", "#7d00ae", mine=True)
define ar_txt = PhoneCharacter("Arielle", "#e8a33d", typing_delay=2.0)

## How long the "..." typing bubble shows before an incoming message, unless
## the character sets its own typing_delay.
define phone_typing_delay = 0.7

## Sounds for a message arriving and for the player sending one. They play on
## their own channel (under the sound effects volume) so they don't cut off
## other sounds.
define phone_receive_sound = "audio/sfx/pop.ogg"
define phone_send_sound = "audio/sfx/send.ogg"

init python:
    renpy.music.register_channel("phone", "sfx", loop=False)

default phone_contact = ""
default phone_log = []

## The color of the other person's "..." bubble, or None when they are not
## typing, and whether the player's "..." bubble is showing.
default phone_typing_them = None
default phone_typing_me = False

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
        store.phone_typing_them = None
        store.phone_typing_me = False
        renpy.show_screen("phone_chat")
        renpy.with_statement(dissolve)

    def phone_close():
        renpy.hide_screen("phone_chat")
        renpy.with_statement(dissolve)

    def phone_typing_start(who):
        if who.phone_mine:
            store.phone_typing_me = True
        else:
            store.phone_typing_them = who.phone_bubble

    def phone_typing_stop():
        store.phone_typing_me = False
        store.phone_typing_them = None

    class PhoneCharacter(ADVCharacter):
        """
        A character whose lines appear as chat bubbles in the phone, and in the
        textbox below it. Lines from the other person are preceded by a short
        "..." typing bubble.
        """

        def __init__(self, name, bubble, mine=False, typing_delay=None, **properties):
            properties.setdefault("screen", "phone_say")
            properties.setdefault("color", bubble)
            ADVCharacter.__init__(self, name, show_mine=mine, show_bubble=bubble, **properties)
            self.phone_mine = mine
            self.phone_bubble = bubble
            self.phone_delay = typing_delay

        def get_typing_delay(self):
            if self.phone_delay is None:
                return phone_typing_delay
            return self.phone_delay

        def __call__(self, what, *args, **kwargs):
            if self.phone_mine:
                store.phone_typing_me = False

            elif self.get_typing_delay() and not renpy.is_skipping():
                # Show "..." in the phone, and the sender's name with "..." in
                # the textbox (replacing the empty textbox) while they type.
                store.phone_typing_them = self.phone_bubble
                window = store._window
                store._window = False
                renpy.show_screen("phone_typing_say", who=renpy.substitute(self.name), color=self.phone_bubble)
                renpy.pause(self.get_typing_delay())
                renpy.hide_screen("phone_typing_say")
                store._window = window

            if not self.phone_mine:
                store.phone_typing_them = None

            if not renpy.is_skipping():
                sound = phone_send_sound if self.phone_mine else phone_receive_sound
                renpy.sound.play(sound, channel="phone")

            rv = ADVCharacter.__call__(self, what, *args, **kwargs)
            store.phone_log.append((self.phone_mine, self.phone_bubble, what))
            return rv


## One chat bubble.
screen phone_bubble(msg, mine, bubble):
    frame:
        style "phone_bubble"
        xalign (1.0 if mine else 0.0)
        background phone_bubble_bg(bubble)
        text msg style "phone_bubble_text" color phone_text_color(bubble)


## A "..." bubble.
screen phone_typing_bubble(mine, bubble):
    frame:
        style "phone_bubble"
        xalign (1.0 if mine else 0.0)
        background phone_bubble_bg(bubble)
        hbox:
            style "phone_typing_dots"
            for i in range(3):
                add Transform("gui/chat/dot.png", matrixcolor=TintMatrix(phone_text_color(bubble))) at phone_dot(i * 0.15)


## The phone with the chat so far. `current` is a message that is being said
## right now, which goes after the others.
screen phone_body(current=None, mine=False, bubble=None):

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

                for m, b, msg in phone_log[-15:]:
                    use phone_bubble(msg, m, b)

                if current is not None:
                    use phone_bubble(current, mine, bubble)

                if phone_typing_them:
                    use phone_typing_bubble(False, phone_typing_them)

                if phone_typing_me:
                    use phone_typing_bubble(True, p_txt.phone_bubble)


## Shown for the whole conversation, behind the dialogue.
screen phone_chat():
    zorder -1
    use phone_body


## The say screen used by PhoneCharacter: the phone with the new message as
## its last bubble, on top of phone_chat, plus the usual textbox.
screen phone_say(who, what, mine=False, bubble="#888888"):

    use phone_body(what, mine, bubble)

    window:
        id "window"

        if who is not None:
            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


## The textbox while the other person is typing.
screen phone_typing_say(who, color):
    window:
        style "window"
        window:
            style "namebox"
            text who style "say_label" color color
        text "…" style "say_dialogue"


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
    ypos 20

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

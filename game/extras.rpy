## Content warning #############################################################
##
## Shown at the start of every new game.

screen content_warning():
    modal True

    add Solid("#000")

    vbox:
        style_prefix "warning"
        align (0.5, 0.5)

        text _("Content Warning") style "warning_title"
        text _("This game contains strong language and brief mentions of suicidal thoughts.")
        text _("If you are struggling, please reach out to someone you trust or a local support line.")

        null height 20

        textbutton _("Continue") action Return() xalign 0.5

style warning_vbox is vbox:
    xmaximum 1200
    spacing 40

style warning_text is gui_text:
    color "#ffffff"
    text_align 0.5
    xalign 0.5

style warning_title is warning_text:
    size 60

style warning_button is button
style warning_button_text is gui_button_text:
    size 36
    idle_color "#aaaaaa"
    hover_color "#ffffff"


## Endings #####################################################################
##
## Which endings the player has reached, shown from the main menu.

default persistent.endings_seen = set()

define endings_list = [
    ("elena", _("Elena")),
    ("emma", _("Emma")),
    ("none", _("On My Own")),
    ]

init python:
    def mark_ending(key):
        persistent.endings_seen.add(key)
        renpy.save_persistent()

screen endings():

    tag menu

    $ found = len([k for k, _t in endings_list if k in persistent.endings_seen])
    $ total = len(endings_list)

    use game_menu(_("Endings"), scroll="viewport"):

        style_prefix "endings"

        vbox:
            text _("Endings found: [found] / [total]")

            null height 20

            for key, title in endings_list:
                if key in persistent.endings_seen:
                    label "[title!t]"
                else:
                    label "???" style "endings_locked_label"

style endings_vbox is vbox:
    spacing 20

style endings_text is gui_text
style endings_label is gui_label
style endings_label_text is gui_label_text:
    size 44

style endings_locked_label is endings_label
style endings_locked_label_text is endings_label_text:
    color gui.insensitive_color

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


## Naming saves ###############################################################
##
## Shown when the player clicks a slot on the save screen.

screen save_name_prompt(slot):
    modal True
    zorder 200

    style_prefix "confirm"

    default draft = FileSaveName(slot) or ""

    add "gui/overlay/confirm.png"

    frame:
        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _("Name this save:"):
                style "confirm_prompt"
                xalign 0.5

            input:
                style "save_name_input"
                value ScreenVariableInputValue("draft")
                length 30

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Save") action [ SetVariable("save_name", draft), Hide("save_name_prompt"), FileSave(slot) ]
                textbutton _("Cancel") action Hide("save_name_prompt")

    key "input_enter" action [ SetVariable("save_name", draft), Hide("save_name_prompt"), FileSave(slot) ]
    key "game_menu" action Hide("save_name_prompt")

style save_name_input is gui_text:
    xalign 0.5
    color gui.accent_color
    size 40


## Endings #####################################################################
##
## The endings the player has reached, laid out like the save slots. Clicking
## one replays it.

default persistent.endings_seen = set()
default persistent.last_player_name = "Zack"
default persistent.last_player_name2 = "dream girl"

## (key, title, label to replay, picture)
define endings_list = [
    ("elena", _("Elena"), "elena_ending", "images/rooftop.png"),
    ("emma", _("Emma"), "emma_ending", "images/park2.png"),
    ("none", _("On My Own"), "none_ending", "images/bedroomnight.png"),
    ]

init python:
    def mark_ending(key):
        persistent.endings_seen.add(key)
        renpy.save_persistent()

    def ending_replay_scope():
        return {
            "player_name": persistent.last_player_name,
            "player_name2": persistent.last_player_name2,
            "go_with_elena": True,
            }

screen endings():

    tag menu

    $ found = len([e for e in endings_list if e[0] in persistent.endings_seen])
    $ total = len(endings_list)

    use game_menu(_("Endings")):

        fixed:

            label _("Endings found: [found] / [total]"):
                style "page_label"
                xalign 0.5

            grid len(endings_list) 1:
                style_prefix "slot"
                xalign 0.5
                yalign 0.5
                spacing gui.slot_spacing

                for key, title, start_label, picture in endings_list:

                    if key in persistent.endings_seen:
                        button:
                            action Replay(start_label, scope=ending_replay_scope(), locked=False)
                            has vbox
                            add Transform(picture, size=(config.thumbnail_width, config.thumbnail_height)) xalign 0.5
                            text "[title!t]" style "endings_title"
                            text _("Click to replay") style "slot_time_text"
                    else:
                        button:
                            action NullAction()
                            has vbox
                            add Transform(picture, size=(config.thumbnail_width, config.thumbnail_height), matrixcolor=SaturationMatrix(0.0) * BrightnessMatrix(-0.3), blur=12) xalign 0.5
                            text "???" style "endings_title"
                            text _("Not reached yet") style "slot_time_text"

style endings_title is slot_name_text:
    size 34
    color gui.accent_color

define config.main_menu_music = "audio/calltothesoul.mp3"

default major = ""

define a = Character("Elena", color="#E31B61")
default elena_affection = 0
default go_with_elena = False
define b = Character("Emma", color="#0e719e")
default emma_affection = 0
default try_talk_emaa = False
define lv = Character(None, what_color="#db81ff")
default arielle_stage = 0     
default arielle_gone = False  

define m = Character("[player_name2]",  color="#db81ff")
define p = Character("[player_name]", color="#7d00ae")
define pv = Character(_("He"), color="#7d00ae")
define x = Character("Zane", color="#B5B9FF")
define z = Character("Gus", color="#5C492A")

define l = Character("You",color= "#db81ff")
define q = Character("???")
define s = Character("Both")
define t = Character("Teacher")
define y = Character("Chris")

# Big centered title card used for "DAY 1", "THE DAY", etc.
define daycard = Character(None, kind=centered, what_size=72, what_color="#ffffff", statement_name="say-centered")

label start:
    scene black
    $ quick_menu = False
    call screen content_warning
    $ quick_menu = True
    jump day1

label day1:
    $ player_name = renpy.input(__("Please enter your name:"), length=12, exclude="[]{}")
    $ player_name = player_name.strip()
    if player_name == "":
        $ player_name = "Zack"
    
    scene road
    with dissolve
    play music "audio/peace.mp3" fadein 1.0
    "Not knowing exactly what you're doing, you drive down a highway with no destination in mind."
    $ player_name2 = renpy.input(__("Please enter your dream girl's name:"), length=12, exclude="[]{}")
    $ player_name2 = player_name2.strip()
    if player_name2 == "":
        $ player_name2 = "Angharad"
    $ persistent.last_player_name = player_name
    $ persistent.last_player_name2 = player_name2
    scene shadow
    with dissolve
    m "A penny for your thoughts?"
    p "Just glad you're here with me."
    m "Me, too."
    "You smile at each other."
    "Even without words, there's no awkwardness at all."
    "You know this is the happiest you'll ever be."
    
    scene black
    with fade
    stop music fadeout 1.5
    p "Fuck!"
    daycard "DAY 1"
    scene bedroom
    with dissolve
    "You wake up slowly and start to realize none of it was real."
    "What you would sacrifice just to get back to that dream..."
    "Reality strikes back: you're just a freshman starting college."
    "You're studying:"
    menu:
        "Computer Science":
            $ major = "Computer Science"
        "Economics":
            $ major = "Economics"
        "Physics":
            $ major = "Physics"
        "Chemistry":
            $ major = "Chemistry"
        
    "Life hasn't treated you too badly, but you still have your lows."
    "You're already 18 years old, and you've never been in a relationship."
    "You were never one of the cool kids in school, just a shy kid no one really remembers."
    "There are many reasons you turned out the way you are today:"
    "Maybe some family drama, friend issues, or even being bullied."
    "But none of that really matters anymore."
    "You still had good friends around to support you, at least until now."
    "New college, new environment, new people."
    "You're excited and nervous at the same time."
    "You don't want to screw up, but you also know you're destined to."
    p "(sigh) Guess it's time."
    "You freshen up and get ready to head to school."
    "You put on your headphones and pick the music that represents you the most."
    "You are ready."
    "Perchance?"
    
    scene courtyard
    with dissolve
    play music "audio/indiefolkyears.mp3" fadein 1.0
    "Trying to choose the right song for the vibe, you don't notice someone walking up to you."
    q "Excuse me, can you give me a little help?"
    "Hearing someone call out, you look up and see a girl waving at you."
    show elena at pos_center
    with dissolve
    q "Do you know how to get to classroom 301B in Jordan Building?"
    "Given you're a new student, there's no way you would know the location."
    p "I'm not so sure..."
    "Even though you don't know the location at all, you still try to help."
    "You take out your phone and try to search for information."
    p "I think you need to take a left turn here and go to the second building and that should be it."
    q "Turn left, second building... Got it! Thank you so much!"
    "She thanks you and heads straight for the building before you can say anything."
    p "I'm not that sure though..."
    "Feeling stupid for thinking this simple interaction could turn into something more, you walk faster toward campus, trying to shake off the embarrassment."
    scene black
    with fade
    "Some time later..."
    scene corridor
    with dissolve
    "It's your second class, and you're still thinking about the incident."
    "Thanks to your fast walking, you arrive at the classroom pretty early."
    "Which also means you can choose the seat you want in the classroom."
    "You've tried every possible variation."
    "The back row is usually for the 'players,' the front row is for the 'nerds,' and the middle seats are... nothing special."
    "You're basically a master of seating at this point, and you know there's no point in overthinking it."
    "So you make your choice and take a seat."
    "Not knowing what else to do, you put on your headphones and start playing with your phone."
    scene black
    with fade
    "Some time later..."
    scene back
    with dissolve
    "You notice that the class is about to start."
    "Then you feel someone tap your shoulder from behind."
    q "You again!"
    "You look up and realize she's the girl who asked you for directions earlier."
    show elenaclassroom at pos_center
    with dissolve
    p "Oh hi! I didn't know you were in this class, too."
    q "Well, who would have known, right? HAHA."
    q "I should give you a proper thanks!" 
    q "Though, you know you actually gave me the wrong directions?"
    p "(Crap!)"
    p "Oh shoot, I'm so sorry about that."
    q "It's all good haha."
    q "Your intentions were good."
    "You still feel a bit awkward and sorry at the same time, and perhaps she notices as well."
    a "Anyway... I'm Elena, and you?"
    p "Oh! I'm [player_name]."
    "She sits down next to you as soon as you finish."
    a "Well, [player_name], nice to meet you."
    scene teacher
    with dissolve
    stop music fadeout 1.5
    "You listen to the lecture with your full attention, though sometimes you zone out."
    t "Alright class, before the lecture ends, I want you to know that this course will have a group assignment."
    t "Since you're all freshmen, I will assign the groups myself."
    "You're glad you don't have to pretend to be an extrovert and find some teammates."
    t "I will divide the groups by seat. You'll be paired with the student sitting next to you."
    t "You should know who your partner is now. Let me know if you have any questions."
    "You realize you'll be in the same group as Elena."
    scene back
    show elenaclassroom at pos_center
    with dissolve
    a "Guess that's you and me!"
    p "Yeah!"
    a "We should exchange contact and social media info to discuss the assignment, yeah?"
    p "Sure!"
    "While you're typing in her contact, Elena keeps talking."
    a "The universe really wants us together, huh?"
    "Overthinking that sentence way too much, you freeze for a second."
    p "Yeah, I guess so. HAHA."
    p "(Idiot, get your shit together.)"
    "SOMETIMES I WISH I WAS BETTER."

    scene black
    with fade
    play music "audio/inspiring.mp3" fadein 1.0
    $ renpy.movie_cutscene("movies/iwishiwasbetter.webm", stop_music=False)

    scene bedroomnight
    with dissolve
    "You return home, thinking this day could have gone worse."
    "However, it actually went better than you expected."
    "Replaying the day in your head, you lie on your bed and take a deep breath."
    "You take out the phone and start looking at [player_name2]'s photos."
    "You might have had a chance to be with her, but none of it ever happened."
    "Sometimes you think it's the unknown possibility of that future that makes you regret it and dwell on it so much."
    "So you decide to do something you haven't done in a while."
    "You open the dating app."
    "The one you've opened many times and never have a successful experience with."
    "And you start to look at the profiles."
    "Then you see a girl called Arielle."
    "She looks like your type, so you decide to give it a go."
    menu:
        "Answer her prompts":
            "You answer one of her prompts:"
            "If you could be an animal, what would it be?"
            $ prompt_answer = renpy.input(__("You answer:"), length=25, exclude="[]{}")
            $ prompt_answer = prompt_answer.strip()
            if prompt_answer == "":
                $ prompt_answer = "llama"
            p "[prompt_answer]."
        "Just like":
            "You don't type anything and just give a like."
        "A simple hi":
            "You just type hi!"  
    "Then you close your phone and go to take a bath."
    scene black
    "Some time later..."
    "You get a notification from the dating app."
    "You have a match with Arielle!"
    "She didn't say anything so now it's up to you."
    p "(All right. How should I do this?)"
    $ phone_open("Arielle")
    menu:
        "Wait for her to respond first.":
            "Waiting is also a virtue, right?"
            "So you do nothing."
            $ arielle_gone = True
        "Say hi.":
            p_txt "Hey"
            "You stare at the screen for a while."
            "You just say hey."
            "Pretty much nothing."
            $ arielle_gone = True
        "Ask how her day is going?":
            p_txt "Hi! How's your day going?"  
    "Nothing."
    "Now there's nothing else you can do."
    "But before you go to bed, you somehow decide to check Elena's social media."
    "Concerts. Road trips." 
    "Rooftop parties." 
    "Friends laughing at a joke you'll never hear."
    "Her life looks like a movie." 
    "Yours looks like a loading screen."
    p "(Fuck my life.)"
    "You decide to check the dating app one last time."
    if arielle_gone:
        "The chat is gone."
        "Arielle unmatched you."
        p "(FUCK THIS SHIT)"
    else:
        "To your surprise, you got a message."
        $ phone_typing_start(ar_txt)
        ar_txt "Just finish my classes, and I'm exhausted at the moment:("
        p_txt "I'm sure it will get better haha"
        p_txt "What degree are you in?"
        $ arielle_stage = 1
    "You close the app again."
    "You then have a video chat with your old friends, and get ready for bed."
    p "(Sigh) Sweet dreams, I hope."
    stop music fadeout 1.5

label day2:
    scene black
    with fade
    daycard "DAY 2"
    scene emmasits
    with dissolve
    "Another day, another class."
    "Somehow, you still arrive at class early today."
    play music "audio/ilikeyoualot.mp3" fadein 1.0
    "This time, though, you see a girl who apparently came even earlier than you."
    "She's sitting in the front row."
    "At first glance, she seems like the shy type, and a good student who takes class seriously."
    "Maybe you should get closer to her and see what happens."
    "Which sounds like a weird idea, even in your head."
    "Trying not to creep her out, you take the seat behind her."
    "You try to start a conversation with her, but every time you're about to speak, something holds you back."
    "Eventually, you give up and start playing with your phone again."
    scene black
    "Some time later..."
    scene emmasits
    with dissolve
    "You notice a guy coming towards the girl."
    "The guy sits next to her, and they start chatting."
    "You can hear the girl laughing out loud, which kind of surprises you, since you thought she was the shy type."
    "At the same time, you can't help feeling lonely."
    p "(That guy must be her boyfriend. I mean, of course. She's beautiful, so it's normal for her to have a boyfriend.)"
    "You're drowning in your thoughts until the professor comes in and starts the class."
    scene black
    "Some time later..."
    scene professor
    with dissolve
    stop music fadeout 1.5
    "You listen to the lecture with your full attention, though you zone out now and then."
    t "Alright class, before we finish, I want you to know that this course will have a group project, due the week after next."
    t "So you should probably start to discuss your project early."
    t "Since you're all freshmen, I will assign the groups myself."
    "Once again, you're glad you don't have to find teammates yourself."
    t "I will divide the groups by seat. Each group will have four members."
    t "You should know which group you're in now, let me know if you have any questions."
    "You realize you'll be in the same group with the girl and the guy."
    scene classroom2
    with dissolve
    "Since you're all in the same group, you figure you should take the initiative and greet your teammates."
    "You exchange contact, social media and learn each other's names."
    "The guy's name is Gus, the other one is Chris, and of course, the girl."
    show emmabus at pos_center
    with dissolve
    play music "audio/ilikeyoualot.mp3" fadein 1.0
    b "My name is Emma, nice to meet you."
    p "Nice to meet you too."
    p "I'm [player_name]."
    stop music fadeout 1.5

    scene bedroom
    with dissolve
    play music "audio/happytosad.mp3" fadein 1.0
    "You get back home."
    "Today wasn't that bad."
    "Out of curiosity, you decide to check Emma's social as well."
    "There aren't many posts or selfies."
    "Just some sceneries like windows in the rain, a book page with one sentence underlinedand, and a lake at sunset, captioned only with a date."
    "This is the kind of contents that you feel more familiar with."
    "You kind of like it."
    "Then again, who gives a shit if you like it or not?"
    play sound "audio/sfx/message.ogg"
    "You get a meesage."
    $ phone_open("Elena")
    a_txt "PARTNER"
    a_txt "did u read the assignment brief yet"
    p_txt "Oh not yet, sorry about that."
    a_txt "all good me neither"
    a_txt "we're gonna be so good at this"
    p_txt "I hope so haha"
    $ phone_close()
    "You laugh a bit."
    "Better just go freshen up and go to sleep."
    "But this time, you don't feel like doing that yet."
    "You have an urge to just go out and go for a walk."
    "So you do."
    "You put on your headphones once again, pick the right song, and head out."

    scene browsing
    with dissolve
    "You just do some random stuff:"
    scene coffee
    with dissolve
    "You go out and buy drinks."
    scene departmentstore
    with dissolve
    "You browse the department store, looking at all kinds of things."
    scene park
    with dissolve
    "You go to the park and watch kids playing together."
    scene streets
    with dissolve
    "You walk slowly through the streets, taking in the lights and buildings of the city."
    "You feel peaceful, even though nothing significant happened at all."
    "You just cherish the moment."
    "You're always a little weirded out by how much you enjoy this."
    "But that doesn't matter now."
    "In fact, nothing matters now."
    "All you feel is satisfied, spiritually."
    "(And you also decide to post a story with all the pictures you took today.)"
    stop music fadeout 1.5

label day3:
    scene black
    with fade
    daycard "DAY 3"
    scene classroom3
    with dissolve
    "You're in classes."
    "Then you get a message."
    play sound "audio/sfx/message.ogg"
    $ phone_open("Elena")
    "Turns out it's Elena replying to your story."
    a_txt "niceee where did you go??"
    a_txt "u a night walk person??"
    p_txt "Kind of, haha. Just walking around after class."
    a_txt "respect"
    $ phone_close()
    p "(Cool...?)"
    "Since you didn't expect she would reply to your story at all."
    scene black
    with fade
    "Some time later..."
    "Class just finished."
    "You remember you're working on the project with your group later."
    "Gus messaged you last night asking when you're free."
    "In the end, you all decided to work on it this afternoon."
    "So you grab a quick meal at a restaurant."
    "Then you head to the place the group agreed on over the phone yesterday."

    scene library
    play music "audio/cozylofirelax.mp3" fadein 1.0
    show emma at pos_center
    with dissolve
    "Turns out Emma is still exactly as you expected (at least for now):"
    "She's polite to strangers (which is currently you)."
    "She takes the project seriously."
    "Though she's not in charge or anything."
    "She just follows everyone's instructions and does her best."
    "Which is insanely similar to you."
    menu:
        "Try to chat with her a little bit.":
            $emma_affection-=1
            $try_talk_emaa = True
            "You try to talk to her, but she's clearly too focused on the project to chat."
        "Keep up the hard work":
            $emma_affection+=1
            "Feeling her attitude toward the project, you know this is not the time for chit chat."
            "So you work as hard as you can, too."
            "And maybe, just maybe, Emma notices that, too."
    scene black
    with fade
    "Some time later..."
    scene library
    with dissolve
    y "Alright guys, I think we should call it a day. I have some stuff to do later."
    p "Yeah, no problem."
    y "We can figure out when to meet next over the phone."
    y "I really gotta go, bye for now!"
    p "Bye!"
    z "Bye!"
    b "Bye!"
    "Since the group work is done, you figure you should leave too."
    "(Especially so you don't interrupt these two.)"
    show gus at pos_center
    show emma at pos_right
    with dissolve
    z "Hey man, wait up!"
    "You stop."
    p "Yeah?"
    z "You're too fast man, wait for us!"
    "Then you realize he wants to leave together."
    "You're kind of confused, but you wait for him anyway."
    p "Oh sorry man, didn't notice that."
    z "It's okay, let's go now."
    scene black
    with fade
    "Some time later..."
    scene street
    show gus at pos_center
    show emma at pos_right
    with dissolve
    "The three of you walk home, and Gus does most of the talking."
    z "So, [player_name], what makes you want to study [major]?"
    p "I think it was the most interesting option I had."
    z "So you'll choose what you like over what you're good at?"
    p "I think so, but when you put it this way..."
    b "I think both ways have their ups and downs, right?"
    "Emma suddenly speaks up."
    show gus at pos_right
    show emma at pos_center
    with dissolve
    p "Yeah, I agree."
    p "So what about you two, why study [major]?"
    z "Because that's probably the one subject I don't suck at. HAHA."
    "Emma takes a while to think, then answers."
    b "I think...the same reason as [player_name]?"
    menu:
        "Ask her more.":
            $ emma_affection += 1
            p "Was it hard for you to decide?"
            b "It definitely took some time, I guess."
            b "There were... lots of discussions at the time."
            "You sense she might not want to talk about this more, so you change the subject."
        "Leave it at that.":
            pass
    p "Well, I think that's the most common way people choose their majors."
    p "People are still kind of confused about what they really like."
    p "So they just choose something that's not the least interesting?"
    b "I guess you have a point!"
    "You guys just chat about these things, nothing personal, just casual conversation."
    "Then Emma reaches her home and says goodbye."
    hide emma
    show gus at pos_center
    with dissolve
    "You and Gus then continue on your way."
    p "So are you and Emma together?"
    "You're pretty sure of the answer, but you still ask, just to be polite."
    z "What? Bro! Do you think we're together haha!"
    "That's not what you expected him to say."
    p "Sorry, it's just that you guys gave me that impression."
    z "I'm crying bro that's hilarious."
    z "Nope, I've known her for a while now. We're just close friends."
    p "Oh!"
    "You suddenly imagine what it would be like to be with Emma."
    "However, another thought strikes you."
    "Just because Emma isn't with Gus doesn't mean she doesn't have a boyfriend."
    "You could ask Gus about it, of course, but your intentions would be way too obvious."
    "So you don't ask."
    scene black
    "Some time later..."
    "To your surprise, Gus is really easy to talk to."
    "You guys just keep chatting."
    "And of course, somehow the conversation turns NSFW."
    "You didn't expect to get along with Gus this fast."
    "Then again, why not?"
    "He's just such an extroverted person."
    stop music fadeout 1.5
    if not arielle_gone:
        scene bedroomnight
        with dissolve
        play sound "audio/sfx/message.ogg"
        "When you get home, there's a notification on the dating app again."
        $ phone_open("Arielle")
        ar_txt "sorry i'm slow at replying btw, pottery class ate my whole week"
        ar_txt "I'm studying bachelor of art(as you can guess haha) at the moment!"
        ar_txt "and my bowl collapsed AGAIN"
        p "(Pottery. Okay. Say something normal.)"
        menu:
            "Ask her questions.":
                p_txt "Pottery? That's cool! How long have you been doing it?"
                p_txt "Do you like art in the first place?"
                p_txt "What's the best thing you've made so far?"
                $ arielle_gone = True
            "Simple reply.":
                p_txt "that's sad."
                "And you're done."
                $ arielle_gone = True
            "One question, one story.":
                p_txt "That's unfortunate:( Is pottery your favorite form of art?"
                p_txt "I tried making a mug once in high school. It doesn't look good HAHA."
                ar_txt "No, I actually enjoy painting a lot better."
                ar_txt "I'm sure it's not that bad!"
                p_txt "Oh really? Paintings are my favorite form of art as well, especially portraits and landscape!"
                p_txt "I do try to draw from time to time, but it still needs practice :("
                $ arielle_stage = 2
        $ phone_close()
        if arielle_gone:
            "Ten minutes later, the chat is gone."
            "Arielle unmatched you."
            p "(Two days of waiting for that.)"
            p "(Great job, [player_name].)"
        "You go to sleep."
    
label day4:
    scene black
    with fade
    daycard "DAY 4"
    scene classroom4
    with dissolve
    "You slept pretty well last night."
    "You kept thinking about the promising start with Emma (and sure, Gus)."
    "You hope you'll become friends."
    "Then you decide to check your social media again."
    "Then you see Emma's story."
    "A cup of tea balanced on her knee."
    "You type 'Oh nice! Where's this?'"
    "Delete."
    "You type 'Is that green tea?'"
    "Delete."
    "You just like it."
    p "(Pussy.)"
    "With a lot on your tiny brain, you head to school as soon as you're fully awake."
    "And of course you come to school early."
    "Maybe you should make coming to school early a habit."
    "Or not."
    "Unlike last time, though, you're the first one here."
    "You start to play with your phone once again."
    "Trying to let yourself drown in your thoughts."
    scene black
    "Some time later..."
    scene classroom4
    with dissolve
    play music "audio/joyful.mp3" fadein 1.0
    a "Hey, good morning!"
    "You find someone sitting down next to you."
    show elena at pos_center
    with dissolve
    p "Oh hi, Elena!"
    "To your surprise, Elena is a lot earlier than last time."
    menu:
        "Wow, you're unexpectedly early today.":
            p "(STUPID!)"
            a "Yeah, I must have left the wrong impression. I'm actually a good student who's always on time. HAHA."
            p "No, no no, I'm sure you are."
            a "I will believe you for now."
            p "I don't usually got to school this early in high school."
            a "Is that so?"
        "Hey, good to see you again.":
            $ elena_affection += 1
            a "Good to see you, too."
            a "So, are you always this early for school?"
            p "Sometimes yes, sometimes really close to being late."
            a "Back in high school?"
            p "Yeah."
    a "So what were you like in high school?"
    p "Nothing special I think."
    p "I was the kind of guy you probably wouldn't remember when you look back."
    a "I'm sure you're exaggerating. HAHA."
    a "Someone will definitely remember you."
    a "Or at least, I bet you made someone laugh somehow."
    p "Yeah, maybe you're right."
    a "You're not the kind of person who leaves people in pain, right?"
    p "I sincerely hope so."
    a "We should hang out sometime!"
    a "I'm sure I can make you more positive!"
    p "You can certainly try."
    a "And I will!"
    a "Oh, and we should talk about the assignment."
    a "Feel free to fill me in by texting me. I'll do the same."
    p "Yeah, got it."
    "Class is about to start, so you stop talking."
    stop music fadeout 1.5
    scene black
    with fade
    "Some time later..."
    scene classroom4
    show elena at pos_center
    with dissolve
    "Class is over, and Elena says goodbye."
    "You thought you'd leave together, but then you see her with some other people."
    "Of course she has friends, idiot."
    "You then leave the classroom as well, feeling a bit sad."

    scene basketball
    play music "audio/bowling.mp3" fadein 1.0
    show gus at pos_right
    with dissolve
    "To your surprise, even though you were hoping to get along with Emma, you end up getting along with Gus pretty well."
    "He asks you to hang out after class, and you guys have a great time."
    "Gus likes all kinds of sports."
    "And you're not good at most of them."
    "But he's fine with it."
    "He just appreciates the company."
    "And right now, you're taking a break after some rounds of basketball."
    z "So, did you get to know new people these days?"
    p "Yeah, a few. Not a lot, but I think it's progress."
    z "Well, maybe you should hang out with me and Emma more, I mean we're also in the same group."
    p "Yeah maybe."
    z "Don't worry! Emma is a great person, it just takes some time for her to warm up."
    z "She's actually pretty outgoing and fun around her friends."
    z "She's just shy around people she doesn't know much."
    z "Once you get to know her, you'll understand."
    p "(Kind of sounds like me.)"
    p "How long did you say you've known her again?"
    z "We went to the same high school, same class, so... 3 years?"
    p "Hmm..."
    z "Don't worry man, I'll help break the ice."
    play sound "audio/sfx/vibrate.ogg"
    "Gus's phone buzzes, and he picks it up."
    z "...And speak of the devil!"
    z "She just asked me when we're working on the project again."
    z "Let me reply to her first..."
    z "So, when are you free to do the project?"
    p "Tomorrow? I don't have class in the afternoon."
    z "Got it!"
    "..."
    z "Emma said she's cool, too."
    z "I'll ask Chris later."
    p "Appreciate the help, man."
    z "No problem."
    stop music fadeout 1.5

    scene restaurant
    show zane at pos_center
    with dissolve
    play music "audio/restaurant.mp3" fadein 1.0
    "You have lunch with Zane."
    "He's a student you met in another class."
    "He might be the first friend you made in this school."
    "You guys get along pretty well; you have common interests:"
    "You both like video games and share the same taste in movies."
    x "...so that's why I like Pixels."
    p "Yeah, that movie has its flaws, but I think it's definitely worth a watch."
    x "So... how's your day?"
    x "Feels like the class is already too hard for me. HAHA."
    p "I guess it's okay for now. I have a group project, though."
    x "How is it?"
    p "Don't like group projects, but I think I'll do better this time."
    x "Why?"
    p "Just feel like the team is getting along."
    x "Who's in it?"
    p "Come on, even if I say the name you wouldn't know who they are."
    x "Try me."
    p "Fine. There's Emma, Gus, and Chris."
    p "We just happened to end up in the same group."
    x "So, tell me about Emma, is she single or not? Your type? Or are you..."
    p "Hold it, Jesus! I can't answer all of them at the same time."
    p "Not sure, maybe, and you didn't even finish that sentence before I stopped you."
    "Zane rolls his eyes."
    p "But yeah, I think we're getting along."
    x "You lucky bastard. In school for a few days and you already know a girl."
    "You kind of want to correct him."
    "But then you realize there's really nothing to brag about, so you stop."
    "But Zane has already noticed."
    x "Wait a minute, you're trying to say something."
    p "Nothing serious, just want to say I know TWO girls, that's it."
    x "Holy shit dude, how in the hell have you never had a girlfriend?" 
    x "This is ridiculous, it's only the fourth day of school!"
    p "Relax, there's nothing going on at all, and I suspect nothing will."
    x "Dude, you've got to give yourself some credit, man."
    x "If you were such a bad person, no one would approach you at all."
    x "You don't have the confidence and never take the initiative, huh?"
    x "I bet that's why you've been single your whole life."
    p "Bro, what the fuck is that supposed to mean? And get out of my head!"
    if arielle_gone:
        p "(Thanks for the reminder. I literally got unmatched this week.)"
    else:
        if arielle_stage >= 2:
            p "(Well at least I'm talking to someone on a dating app at the moment.)"
            p "(Sort of. She replies pretty slow though.)"
    x "HAHA, you're like an open book. Way too easy to read."
    x "But seriously, have some faith."
    x "Don't think too much about it."
    x "Just play it cool, and I'm sure you've got this, whatever this is."
    p "Sure."
    stop music fadeout 1.5

label day5:
    scene black
    with fade
    daycard "DAY 5"
    scene classroom3
    with dissolve
    "Nothing interesting happens. You finish your classes."
    "Then you remember it's time to work on the project with your group again."
    "So you grab a quick meal at a restaurant."
    "Then you head to the place where the group agreed to meet."
    scene library
    play music "audio/cozylofirelax.mp3" fadein 1.0
    show emma at pos_center
    with dissolve
    "Everything is basically the same."
    "Emma is still polite and still takes the project seriously."
    if try_talk_emaa:
        "And this time, you've learned not to try talking to her while she's working."
    else:
        "And you're still working hard on the project, too, taking it seriously."
    "However, she chats with you a little now and then."
    "It makes you wonder if you're getting closer."
    "During breaks, you laugh with her at Gus's stupid jokes."
    "They're still just ordinary interactions, but you can feel her walls getting thinner."
    scene black
    with fade
    "Some time later..."
    scene library
    show gus at pos_center
    with dissolve
    z "I think we're done!"
    z "That took a while."
    y "Alright guys, good job!"
    y "But I gotta go now."
    z "What! Again?"
    z "I thought we were gonna celebrate!"
    y "It's fine, you guys go ahead. I'll be on my way now. Bye!"
    "You figure Chris either has a girlfriend or is a serious introvert."
    p "Bye!"
    z "Bye!"
    b "Bye!"
    "You're not sure if you're walking home together this time."
    "So you move slowly in case they're coming, while also leaving yourself an exit."
    "Then Gus comes over again."
    z "Hey man, even though Chris is gone, we still think we should celebrate. You're joining us, right?"
    "Caught off guard by the sudden invitation, of course, you hesitate."
    p "Well..."
    z "Come on man! It will be fun, I promise!"
    z "And don't worry man, I already asked Emma and she said she's cool with it, too."
    z "There's nothing to worry about."
    "The clock is ticking, and so is your mind."
    "It feels like it takes forever as you calculate every possibility, and finally,"
    p "Fine."
    p "Where are we going?"
    stop music fadeout 1.5

    scene arcade
    with dissolve
    play music "audio/retroarcade.mp3" fadein 1.0
    "Surprised, but also not surprised at all, you find yourself in an arcade."
    "You used to go to places like this a lot."
    "But for no real reason, you just stopped."
    p "Nice place!"
    show gus at pos_center
    show emma at pos_right
    with dissolve
    z "I know, right?"
    z "Enough talking, let's play!"
    "The three of you start playing all kinds of games."
    "Racing games, claw machine, basketball machine, you feel like you're 10 again."
    scene black
    with fade
    "Some time later..."
    p "No way!"
    z "What's up, bro?"
    scene darts
    with dissolve
    p "Holy shit, they have a dart machine here!?"
    "Back in high school, you always played darts with your old friends."
    b "You wanna play?"
    p "You don't have to ask me twice!"
    "You get so excited you forget you're supposed to be the shy guy."
    p "You guys want to play teams or solo?"
    z "Teams, of course! Oh, and [player_name], you're with Emma."
    z "I'm too competitive to team up with Emma and lose."
    b "What? How dare you!"
    p "It's ok, I'm fine with Emma."
    "You insert the coins and start the game."
    "Since you've played this a lot before, you think you have the upper hand."
    "But Gus turns out to be extremely good at it (as expected), even though he's never played before."
    "And Emma? Well, let's just say Gus was right not to team up with her."
    menu:
        "Cheer every time Emma does well":
            $emma_affection+=1
            "She cheers for you right back every time."
        "Cheer every time Gus does well":
            "He cheers for you right back every time."
    "You roll on the floor whenever you mess up or get a low score."
    "You're having such a good time that nobody else exists except the three of you."
    scene black
    with fade
    "Some time later..."
    scene darts
    with dissolve
    "You think you did pretty well, given how strong your opponent is."
    "The score is close, but eventually you lose."
    b "Shoot! I'm sorry we lost."
    menu:
        "It's okay":
            $emma_affection+=1
            p "It's fine."
            p "When I play with my friends, I usually end up being the one who loses."
            p "So I'm kind of getting used to it."
            p "Also, I don't care about winning that much (maybe a little), I enjoy the company here."
            b "Glad you feel that way, me too!"
            p "(Wait, does she mean she doesn't care about winning, or that she enjoys the company, too?)"
            "And yes, just like that, you're back to your 'usual' self."
        "Such a shame":
            p "Damn, we almost got it, such a shame."
            b "Now I feel really bad."
            p "Oh no, no no. It's fine."
            p "When I play with my friends, I usually end up being the one who loses."
            p "So I'm kind of getting used to it."
            p "Also, I enjoy the company here."
            b "Glad you feel that way, me too!"
            p "(Wait, does she mean she's used to losing, or that she enjoys the company, too?)"
            "And yes, just like that, you're back to your 'usual' self."
    stop music fadeout 1.5
 
    scene walk
    with dissolve
    play music "audio/awalkonasummerevening.mp3" fadein 1.0
    "Every show has to end, and so does this hangout."
    show gus at pos_left
    show emma at pos_right
    with dissolve
    "The three of you walk home together again, chatting and laughing."
    "This time, Gus reaches his house first."
    "The two of you say goodbye to Gus and keep walking."
    hide gus
    with dissolve
    "Yes, only the two of you."
    show emma at pos_center
    with dissolve
    "You can already feel the awkwardness in the air, and that feels like shit."
    p "(God damn it, Gus, why are you the first to leave?)"
    "You have two choices:"
    "You could make up an excuse, say you need to catch the metro, and escape before it gets awkward."
    "Or get your shit together and you may have some great conversation."
    "So?"
    menu:
        "Try to have a chat":
            $emma_affection+=1
            "You decide to say something first to break the ice."
            s "So..."
            s "Sorry, you go first."
            "Realizing you keep talking over each other, you make sure to speak first this time."
            p "It's alright, you can go first."
            b "I don't mean this in a bad way, but you're kind of a different person when we're playing darts."
            p "Yeah, I can certainly feel it myself, too. HAHA."
            p "I think it's just because I really like darts, one of my interests."
            p "Like video games, movies that kind of stuff."
            b "Oh what kind of movies do you like?"
            p "Most genres are fine by me, but I do have a favorite movie."
            $ favorite_movie = renpy.input(__("What's your favorite movie:"), length=50, exclude="[]{}")
            $ favorite_movie = favorite_movie.strip()
            if favorite_movie == "":
                $ favorite_movie = "Portrait Of A Lady On Fire"
            p "It's [favorite_movie]."
            $emma_affection+=1
            b "NO WAY! I love that movie as well!"
            b "Not my favorite but I do love it!"
            b "I mean the movie just did a very great job on..."
            "You're kind of surprised that Emma suddenly has so much to say."
            scene black
            "Some time later..."
            scene walk
            show emma at pos_center
            with dissolve
            b "To this day, that movie still has a huge impact on me!"
            p "Yeah, I agree! That's why I've watched it around 10 times now, haha."
            b "Not that many times for me, but agreed!"
            "You guys laugh and keep walking."
            p "Another reason I like the movie so much is that it has sentimental value, just like darts."
            b "What do you mean?"
            p "Like darts, it brings back some good memories from high school."
            p "I used to play darts with my high school friends a lot."
            p "This is gonna sound a little sad, but it's one of those rare memories that makes me feel happy when I think about high school."
            b "What happened in high school, if I may ask?"
            p "Nothing."
            b "Nothing?"
            p "I think that's the point. Nothing happened." 
            p "I didn't know a lot of people, and I didn't join many activities."
            p "I was just... there."
            p "So I'm really thankful for my friends there."
            p "They made my time in high school more meaningful."
            p "Not trying to be ungrateful. I know there were definitely people who had it worse than me there."
            p "It's just the thought of people living better than me sometimes really gets me."
            b "I get it, I sometimes think about that, too."
            b "At least you had some good times back then, and now, right?"
            p "Yeah, I guess." 
            b "Hey, thanks for sharing this side of you."
            p "What side?"
            b "That you can be crazy fun and sentimental sometimes."
            "You want to say something, but you don't know what."
            "So you ask her questions to continue the conversation."
            "You usually walk pretty fast, but this time, both of you walk a lot slower."
            "Like the world is on fast-forward, or you just don't want to leave."
            p "So what were you like in high school?..."
            
        "Make an excuse":
            p "Hey, I actually have to catch the metro, here..."
            p "So I'll see you later?"
            b "Yeah sure, no problem!"
            b "See you!"
    stop music fadeout 1.5

    if not arielle_gone:
        scene bedroomnight
        with dissolve
        "You get home and another notification on the dating app."
        $ phone_open("Arielle")
        ar_txt "sorry again for the late reply, I don't turn on notifications most of the time"
        ar_txt "NO WAY Portraits are my favorite kind of painting!"
        ar_txt "If you don't mind I can be the judge of that lol"
        "You think things are actually going pretty well?"
        "What should you do next?"
        menu:
            "Keep talking":
                p_txt "Don't worry it's all good!"
                p_txt "I know right portraits are really awesome to see, I try to feel every painter's perspective on different people."
                p_txt "It's all good I think I still need to improve a lot more."
                p_txt "Do you draw yourself as well?"
                $ arielle_gone = True
            "Ask for her social media.":
                p_txt "Don't worry it's all good!"
                p_txt "I know! I like to feel every painter's perspective on different people."
                p_txt "If you don't mind seeing something really amateur then sure!"
                p_txt "Though I think I can't send pictures here, do you have social?"
                ar_txt "oh of course!"
                ar_txt "it's @arielle.makes.paintings"
                "You laugh out loud (literally.)"
                "You follow her."
                p_txt "Nice, just followed you!"
                "A minute later, she follows you back."
                "You decide to start the conversation in social."
                p_txt "This is [player_name] saying hi from another place now haha"
                ar_txt "Hello to you from here as well!"
                ar_txt "I'm going to sleep, we'll talk later?"
                p_txt "Of course! Have a good night!"
                "She liked the message."
                $ arielle_stage = 3
            "Just agree with her.":
                p_txt "Don't worry it's all good!"
                p_txt "I know right portraits are really awesome!"
                p_txt "It's fine I think I should practice more first."
                "You wait for her to say something else."
                "She doesn't."
                "You don't either."
                "And just like that, the conversation stops."
                $ arielle_gone = True
        if arielle_gone:
            "Ten minutes later, the chat is gone."
            "Arielle unmatched you."
            p "(Sometimes you really sucks, [player_name].)"        
        $ phone_close()

label day6:
    scene black
    with fade
    daycard "DAY 6"
    scene bedroom
    with dissolve
    play music "audio/future.mp3" fadein 1.0
    "You got home exhausted yesterday."
    "So much has happened in just a few days."
    "You're pretty sure more has happened this week than in all of high school."
    if arielle_stage >= 3:
        "You decide to have a look on Arielle's Instagram as well."
        "Though you guys have never met(yet), you feel like you've known her for a while."
        "You think you should probably take some actions."
        "So you do."
        $ phone_open("Arielle")
        p_txt "Hey do you wanna grab some coffee or do something together?"
        $ phone_close()
        "You throw your phone away."
        "You really FUCKING DO IT."
        "Now it's all up to her."
        "Still that doesn't make you feel better."
        "You're still nervous as fuck."
    play sound "audio/sfx/message.ogg"
    "As you drown in your thoughts, your phone chimes."
    $ phone_open("Emma")
    "It's a message and it's from Emma."
    b_txt "last night was really fun :)"
    p_txt "Yeah!"
    menu:
        "We should do that more often.":
            $emma_affection+=1
            p_txt "We should do that more often."
            "You realize that sentence can have multiple meanings."
            p "(Fuck!)"
            "Then a message comes in."
            b_txt "can't agree more haha"
            p "(Wait, does she mean she likes hanging out, or the walk?)"
            p "(Dumbass! Why make a statement even you can't understand?)"
        "You know where to find me.":
            "Not knowing exactly what to write, you type the first thing that comes to mind."
            "Send."
            p_txt "You know where to find me."
            p "(Shit, why would I say that? What the fuck does that mean?)"
            "Emma replies."
            b_txt "haha"
            b_txt "i might take you up on that :)"
    p "(Wait, is she flirting?)"
    p "(Hold your horses, el tigre. You don't even know if she's single or not.)"
    p "(Maybe she's just being polite, or wants to be friends.)"
    p "(Yeah, that's gotta be it.)"
    $ phone_close()
    "Then you turn off your phone."
    scene black
    with fade
    "A few moments later..."
    scene bedroom
    with dissolve
    $ phone_open("Elena")
    play sound "audio/sfx/message.ogg"
    "You get another message."
    "But this time, it's Elena."
    a_txt "heyyy whatcha doing rn??"
    p_txt "Nothing currently."
    a_txt "wanna hang out??"
    p "(What's with people and their sudden invitations?)"
    p "(Thank god I don't have a life.)"
    "Your brain goes into overdrive."
    "If you were socially capable, this could be the kind of night you'd never forget."
    "On the other hand, you might screw up everything and make her think you're an idiot."
    "After all, what's stopping you?"
    "So, what's it gonna be?"
    menu:
        "Yeah, sure!":
            $go_with_elena = True
            $ elena_affection += 3
            p_txt "Yeah, sure!"
            a_txt "YESSS"
            a_txt "sending u my location, meet me there in 30!!"
            $ phone_close()
            scene place
            with dissolve
            "You go to the place Elena told you about and wait."
            "Some time later..."
            "You see a car coming to you, and someone rolls down the window."
            a "Hey, get in!"
            "The driver is Elena, so you get in."
            scene car
            with dissolve
            menu:
                "Nice car!":
                    $ elena_affection += 1
                    a "Thanks!"
                    p "So, where are we going?"
                    a "Just wait and you'll see."
                "Where are we going?":
                    a "Just somewhere random."
                    p "Sure."
            play music "audio/indie.mp3" fadein 1.0
            "With music playing on the drive, you feel like maybe you should chat a little."
            p "So what kind of music do you listen to?"
            "(That's the best question you can think of?)"
            a "All kinds I think, but I like the surprise of indie music."
            a "You never know what kind of amazing masterpiece you'll get."
            p "Yeah, I get that."
            p "There's this band called Far Caspian. Their music is just so inspiring."
            a "Really? Guess I'll have to listen sometime."
            "On the way, you chit-chat about little things like this."
            "You don't feel the need to carry the conversation."
            "You ask questions when it feels right, and she asks some, too."
            "There's no awkwardness at all."
            "Then Elena asks you a question."
            a "So... I've heard you've never been in a relationship before, huh?"
            stop music
            $ renpy.music.play("audio/djdrop.mp3", channel="music", loop=0)
            p "(WHERE THE FUCK IS THIS COMING FROM!)"
            a "Sorry, HAHA. I just really want to know if it's true or not."
            p "How did you know that?"
            a "I have my ways."
            a "But, a little bird named Gus told me."
            p "(What the fuck, Gus!)"
            p "(Damn it! I can't even remember when I told him that.)"
            p "(Wait, does that mean that son of a bitch told Emma too?)"
            p "(That might explain some of her nice gestures.)"
            p "(She was probably just being friendly, or taking pity on me.)"
            p "(Fuck you and your lousy mouth, Gus!)"
            a "Hello, earth to [player_name]?"
            "You realize all that thinking took a lot longer than a second."
            p "Oh sorry, just thinking for a second."
            p "Wait, how do you know Gus?"
            a "He's in another class with me."
            a "We got to talking, and he found out I knew you."
            a "So he spilled some information about you."
            p "God damn it."
            a "It's okay, HAHA."
            a "So what if you've never been in a relationship before?"
            a "Everyone starts out single."
            a "You've just been at it... a little longer."
            p "Thanks, that definitely makes me feel BETTER."
            a "HAHA, I'm sorry."
            a "But look, I used to date other people, too."
            a "And look at me, still single."
            p "(She's single?)"
            p "Still, that makes you far more experienced than me."
            a "Maybe, but so what?"
            a "I don't think that matters much if you meet the right person."
            "Probably too annoyed or embarrassed, you don't even overthink the possible hidden meaning in what she just said."
            p "Perhaps."
            a "(Sigh) How about this: I'll tell you a secret, to even out your embarrassing situation."
            p "No, no. You don't have to do this."
            p "Not your fault in the first place."
            a "It's okay, I want to."
            p "If you insist."
            a "Oh right!"
            play music "audio/dancinginthesunmastertrack.mp3" fadein 1.0
            "She suddenly makes a U-turn."
            p "Whoa, what was that?"
            a "I was gonna take you to play pool or some shit."
            a "But now, to my secret hideout, to even out your embarrassing situation!"
            p "Okay, I don't think you need to say 'your embarrassing situation' every time."
            a "Copy that. On the way to my secret hideout, to even out [player_name]'s embarrassing situation!"
            p "God damn it."
            p "(I'm gonna fucking kill you, Gus.)"
            stop music fadeout 1.5

            scene destination
            with dissolve
            play music "audio/aquiettime.mp3" fadein 1.0
            "After some time, you finally arrive at the destination."
            show elena at pos_center
            with dissolve
            a "This is the place!"
            "You get out of the car and find yourself at a beach."
            p "A beach, huh?"
            a "Yeah, this is one of my favorite spots, I like the beach at night."
            p "Why?"
            a "There's something really calm about it, you know?"
            a "It's great at daytime, but at night, it's just so quiet and you feel like you're the only one around."
            a "Also, the magnificence of the sea just humbles you."
            p "Yeah, I get what you're saying."
            p "It's really...peaceful."
            a "Right?"
            "You don't expect Elena to have this side."
            "You always thought of her as a party girl or something."
            "And maybe you're wrong."
            hide elena
            with dissolve
            "Elena sits down on the sand, and you sit next to her."
            show elenabeach
            with dissolve
            "Since she mentioned the quietness of the beach, you just sit and watch the scenery without saying anything."
            "The two of you just sit on the beach and enjoy the view."
            scene black
            "Some time later..."
            show elenabeach
            with dissolve
            "You don't know how long you've been watching the ocean."
            "You're both just drawn in."
            "Then Elena speaks."
            a "You know how I found this place in the first place?"
            p "How?"
            a "It was my first breakup. I don't know exactly what went wrong, but my ex broke up with me."
            a "I was devastated. I ran out, and I kept running until I couldn't, then I walked."
            "You know you definitely should not say anything now."
            a "I ended up at this beach, and it felt like it was talking to me."
            a "So I just sat here, the exact spot."
            a "I just watched the waves moving."
            p "It's like the sea won't judge."
            "You don't know why you said that, but you also know it's exactly the kind of thing you would say."
            a "Yeah, something like that..."
            "You can feel she's looking at you, but you just keep looking at the sea, until she doesn't."
            "Then you go back to looking at the sea quietly."
            "Doing nothing, but getting everything."
            stop music fadeout 1.5

        "Maybe next time.":
            $go_with_elena = False
            p_txt "Maybe next time."
            a_txt "boooo"
            a_txt "ok fine, catch u later!!"
            $ phone_close()
    stop music fadeout 1.5


label day7:
    scene black
    with fade
    daycard "DAY 7"
    if go_with_elena:
        scene bedroom
        with dissolve
        "You wake up not knowing exactly when you went to bed."
        "But you do know everything that happened yesterday was certainly not a dream."
        "You guys didn't get intimate or do anything weird."
        "Just two souls connecting."
        "Nothing special but you feel alive."
        play music "audio/joyful.mp3" fadein 1.0
        menu:
            "Text Elena: 'Thanks for last night, I really appreciate it.'":
                $ phone_open("Elena")
                $ elena_affection += 1
                p_txt "Thanks for last night, I really appreciate it!"
                a_txt "anytime!! i enjoyed the company too ngl"
                "You can't help smiling, and you try to hide it like an idiot."
                "You hope whatever this is, it better not end badly."
                $ phone_close()
                scene black
                with fade
                "Some time later..."
                "Since you messaged Elena, you wonder whether you should message Emma, too."
            "Don't text, that's kind of weird.":
                $ phone_open("Elena")
                play sound "audio/sfx/message.ogg"
                "You get a text from Elena:"
                a_txt "heyyy thanks for last night!!"
                a_txt "u were good company ngl"
                p_txt "No problem, always at your service."
                "You can't help smiling, and you try to hide it like an idiot."
                "You hope whatever this is, it doesn't end badly."
                $ phone_close()
                scene black
                with fade
                "Some time later..."
                "Since Elena messaged you, you wonder whether you should message Emma, too."
        jump emma_message
    else:
        pass
        scene bedroom
        with dissolve
        "Today you actually have nothing to do."
        "(At least until someone suddenly invites you somewhere again.)"
        "But for now, you just lie on your bed and play with your phone."
        play sound "audio/sfx/message.ogg"
        "Then, you get a message."
        $ phone_open("Elena")
        a_txt "HEYYY"
        play music "audio/joyful.mp3" fadein 1.0
        "It's Elena."
        a_txt "so about last night"
        a_txt "u said MAYBE NEXT TIME??"
        "Ouch."
        p_txt "Yeah, I'm sorry. I had things to do at the time."
        a_txt "nah it's fine HAHA"
        a_txt "but i need to make sure of something"
        a_txt "are u free next friday?"
        p_txt "Maybe. Why?"
        a_txt "just checking"
        a_txt "making sure u actually show up next time"
        menu:
            "Promise":
                $ elena_affection += 1
                p_txt "Hey, I promise next time you ask me to hang out, I'll say yes no matter what, okay?"
                p_txt "Unless my family dies or something."
                a_txt "HAHAHA ur so stupid"
                a_txt "but u better keep that promise"
            "Don't promise":
                p_txt "Not so sure, probably will have things to do."
                p_txt "But I'll try to make room for you."
                a_txt "HAHA ok ok"
                a_txt "i'm counting that as a promise btw"
        a_txt "i'm keeping my eye on u"
        $ phone_close()
        "You put your phone down, smiling."
        p "(She really wants to hang out with me that bad?)"
        p "(Weird.)"
        scene black
        with fade
        "Some time later..."
        scene bedroom
        with dissolve
        "Since Elena messaged you, you wonder whether you should message Emma, too."
        jump emma_message

label emma_message:
    scene bedroom
    with dissolve
    $ phone_open("Emma")
    $ phone_typing_start(p_txt)
    "You open your chat with Emma and try typing whatever comes to mind."
    "But none of them feels good enough."
    $ phone_typing_start(b_txt)
    "Then you see the typing indicator pop up."
    play music "audio/ilikeyoualot.mp3" fadein 1.0
    p "(Oh shit! She's online, too!)"
    "But she doesn't send anything either."
    p "(Fuck, she definitely knew I was online.)"
    p "(I need to type in something ASAP to make sure I don't look like a weirdo.)"
    "So you do."
    p_txt "Hey, so do you think the project is okay or do we need to fix it?"
    p "(THAT'S THE BEST YOU GOT??)"
    b_txt "i think it's good?"
    b_txt "why, did you find something wrong?"
    p_txt "No! I think it's all good, just double checking."
    b_txt "ok"
    p "(This doesn't look good.)"
    p_txt "So how's your day?"
    b_txt "nothing much"
    "Then you see her typing for a while, like she's deciding if she should type this."
    b_txt "actually, I'm writing a script now"
    b_txt "what about you?"
    "You don't expect that."
    p_txt "That's so cool! What is it about?"
    p_txt "I'm just playing with my phone here, haha."
    b_txt "it's a fantasy one, the plot is talking about what if you're the only one on earth?"
    b_txt "it's still in the early stages, but i'll keep you posted!"
    b_txt "why not hang out with gus or something then?"
    "You know she didn't mean it that way, but somehow you feel kind of offended."
    p_txt "Well, I think I just want to have a me-day today."
    p_txt "Speaking of which, do you know where Gus is?"
    p_txt "Partying or something?"
    b_txt "not sure"
    b_txt "why? do you need him for something?"
    p_txt "Just asking."
    $ phone_typing_start(b_txt)
    "Then Emma types for a while."
    "It looks like she's typing and deleting over and over."
    "Like she's wondering whether she should send it or not."
    b_txt "is this about the never-been-in-a-relationship thing?"
    stop music
    $ renpy.music.play("audio/djdrop.mp3", channel="music", loop=0)
    if go_with_elena:
        p_txt "GOD DAMN IT!"
        p "(So he did tell Emma!)"
        p_txt "How many people did he tell?"
        b_txt "i'm guessing you didn't say he could tell people?"
        p_txt "The hell I did!"
        p "(Fuck you and your lousy mouth again, Gus!)"
    else:
        p "COUGH COUGH"
        "You almost choke."
        p_txt "How did you know that?"
        b_txt "gus told me"
        b_txt "i figured he didn't ask you first"
        p_txt "HELL NO, HE DIDN'T!"
        p_txt "Sorry, I'm just kind of pissed off right now."
        p "(What the fuck, Gus!)"
        p "(Damn it. I can't even remember when I told him that.)"
        "Then you understand something."
        p "(That might explain some of Emma's nice gestures. She was probably just being friendly, or taking pity on me.)"
        p "(Fuck you and your lousy mouth, Gus.)"
    b_txt "hey it's okay"
    b_txt "there's nothing wrong with never dating anyone"
    p_txt "Yeah, easy for you to say."
    p_txt "I bet you've had a lot of boyfriends before."
    b_txt "well first of all, i don't have a boyfriend now"
    play music "audio/ilikeyoualot.mp3" fadein 1.0
    p "(Really?)"
    $ phone_typing_start(b_txt)
    "Emma types for a while again."
    "Like she's wondering whether she should send it or not."
    b_txt "and second"
    b_txt "i've never been in a relationship either"
    b_txt "like ever"
    p_txt "Wait, really?"
    b_txt "yeah"
    b_txt "don't tell anyone, i will deny it"
    "In shock, you once again type without thinking."
    p_txt "Wow, I never would have thought a pretty girl like you has never had a boyfriend before."
    "You quickly realize what you just typed."
    p "(Did I just FUCKING TYPE THAT SHIT?)"
    b_txt "wait"
    b_txt "you think i'm pretty?"
    menu:
        "Yes, of course!":
            $ emma_affection += 2
            p_txt "I think you look good both inside and outside, at least from what I know so far, haha."
            b_txt "oh"
            b_txt "thank you :)"
            "You're not so sure, but you think she's happy."
        "Why wouldn't I?":
            $ emma_affection += 1
            p_txt "I mean you're definitely prettier than lots of girls."
            b_txt "oh"
            b_txt "thank you :)"
            "You're not so sure, but you think she's happy."
    "Embarrassed by what you just did, you wrap up the conversation quickly."
    p_txt "I'll let you get back to your writing."
    p_txt "I'm gonna get some rest now. Bye!"
    b_txt "you weren't bothering me btw"
    b_txt "bye :)"
    $ phone_close()
    "You turn off your phone."
    "You think you're done for now."
    "So you spend the rest of the day playing video games."
    stop music fadeout 1.5

label day8:    
    scene black 
    with fade
    daycard "DAY 8"
    scene back
    with dissolve
    "Another day of school."
    "And yes, you're still early."
    if arielle_stage >= 3:
        "Before class, you check Instagram. Arielle still hasn't opened your last message."
        "It's been two days."
        "You start to wonder what you've done wrong along the way."
    "Then you notice Elena."
    "She really meant what she said about coming earlier."
    "So you sit next to her."
    show elenaclassroom at pos_center
    with dissolve
    play music "audio/joyful.mp3" fadein 1.0
    a "Oh hey, surprised to see me this early again?"
    p "Surprised, yeah. But in a good way."
    p "But if you don't mind me asking, why come to school so early?"
    a "I can ask the same about you."
    p "I don't think I really have a reason."
    a "Please. Whenever people say there's no reason, there's definitely a reason."
    a "You either don't want to talk about it or you don't even notice."
    a "And it's definitely not because of your personality, or you would have said you like being punctual."
    "You're kind of shocked she has observed so much."
    p "Maybe I didn't notice yet."
    p "Then, do you have a reason?"
    a "Trying to find mine, just like you."
    p "Guess we're alike in that way, then."
    a "Yeah, yeah I think so."
    a "So how are you these days?"
    p "Good, I think?"
    "Then you remember that asshole Gus."
    p "And there's Gus."
    "Class is about to start, so Elena cuts you off."
    a "Hey, let's talk about this later, cafeteria?"
    p "Sure."
    "Then you prepare for class."
    scene black
    with fade
    "Some time later..."
    scene back
    with dissolve
    "The class is over."
    "So you head to the cafeteria."
    scene lunch
    show elena at pos_center
    with dissolve
    a "So, what happened?"
    p "Gus happened."
    if go_with_elena:
        a "You're still mad about that, huh?"
        p "I wouldn't be if he didn't give me another reason."
        a "What happened?"
        p "Turns out he told more people about my personal issues."
        a "No surprise. After all, I barely know him and he still told me."
        p "That's just ridiculous!"
        p "He really doesn't have the right to say any of that!"
        a "Hey, if you want, I can go fight him with you."
        p "No, it's fine, I don't wanna bother you."
        p "And I think I would do better if I handle it myself."
    else:
        a "Gus? Wait, big guy, brown eyes, kind of dumb, the one who told me you've never been in a relationship?"
        p "Yeah..."
        p "..."
        p "......"
        p "........."
        p "Wait, WHAT THE FUCK!?"
        p "YOU KNOW TOO!?"
        a "Yeah, HAHA."
        a "His issue is that he spills too much."
        a "I was only asking if he knew you or not, he just said everything like a fucking novel or something."
        p "God damn it."
        a "It's okay, HAHA."
        a "So what if you've never been in a relationship?"
        a "Everyone starts out single."
        a "You've just been at it... a little longer."
        p "Thanks, that definitely makes me feel better."
        a "HAHA, I'm sorry."
        a "Look, I don't think that matters much if you meet the right person."
        "Probably too annoyed or embarrassed, you don't even notice the possible hidden meaning in what she just said."
        p "Perhaps."
        a "(Sigh) How about this: I'll tell you a secret, to even out your embarrassing situation."
        p "No, no. You don't have to do this."
        p "Not your fault in the first place."
    a "Fair enough."
    a "Though I think you should find him and talk about this."
    p "That's my intention."
    scene black
    with fade
    stop music fadeout 1.5
    "You're still kind of pissed, so you don't talk too much."
    "Some time later..."
    scene restaurant
    play music "audio/bowling.mp3" fadein 1.0
    show gus at pos_center
    with dissolve
    z "I think Elena really likes you, bro."
    p "(God damn it, how the hell are we talking about this!?)"
    p "(I should be pissed at him.)"
    p "That's not relevant now."
    p "Jesus fucking Christ, why would you tell Elena and Emma that I've never been in a relationship?"
    p "In fact, how many people did you tell?"
    p "You know what? I don't want to know the answer."
    z "Whoa bro, chill."
    z "I was just having conversations with them, and I think it's not that big of a deal."
    z "And, no, I didn't tell anyone else."
    p "Why would you think it's not a big deal?"
    p "It's really personal information here!"
    z "I'm sorry, bro."
    z "I didn't know it was that sensitive for you, or that I shouldn't tell anyone."
    z "I won't tell anyone from now on."
    "You sigh."
    p "It's fine. I probably should have told you not to tell anyone in the first place."
    p "Just...think about what can be said and what can't carefully next time, okay?"
    z "Of course, bro."
    z "I'm really sorry."
    z "Look, dinner's on me. Eat whatever you like."
    p "Thanks, man. But you don't have to do this."
    z "OH NO NO, I INSIST!"
    "He shouts so loudly that people start staring at you two."
    p "Okay, all right, all right! Jesus!"
    z "Still friends?"
    p "Of course."
    z "So, let's get back to business, Elena."
    p "Again, I don't think she likes me."
    z "Dude, you're either stupid or you just don't want to admit there's a chance with Elena."
    p "I don't believe anything you just said."
    "Deep down, you actually believe him a little."
    "He's probably right."
    "You start to feel really weird in your stomach."
    "Great, now you'll be nervous forever."
    "Which can potentially be a giant fuck-up."
    z "Yeah, man. Maybe I'm wrong, just don't put too much pressure on yourself."
    p "(Yeah, right after what you just said.)"
    z "Be yourself, and you'll be fine."
    p "(Question is, I don't know if I can be 'myself' right now.)"
    stop music fadeout 1.5

label day9:    
    scene black 
    with fade
    daycard "DAY 9"
    scene classroom2
    with dissolve
    "Yep, going to school early is now one of your traits."
    "You sit down in one of the chairs, ready to play on your phone, since you assume you're the earliest again."
    "You get yourself ready, go to the bathroom, and so on."
    "Then you see a familiar figure."
    "And unlike last time, you get up and sit next to her."
    play music "audio/ilikeyoualot.mp3" fadein 1.0
    p "Hey, Emma!"
    show emmabus at pos_center
    with dissolve
    b "Good morning, [player_name]!"
    "She greets you with a sweet smile."
    p "So how did your script go?"
    b "It's on the way, I actually have a lot of ideas after we talked about it!"
    p "That's great!"
    "And, once again, class is about to begin."
    p "Well, I should get back to my seat. Nice talking to you, though."
    "You're about to stand up and leave."
    b "WAIT!"
    "You stop."
    b "You can sit next to me if you want."
    "Kind of surprised, you stop for a second."
    p "Yeah, sure. Let me get my stuff first."
    "So you go grab your stuff and sit next to her."
    p "Hello again!"
    b "Hello to you, too, haha."
    "She smiles."
    hide emmabus
    scene professor
    with dissolve
    "Class begins, and of course, you stop talking and listen to the lecture."
    "Every now and then, your eyes meet and you both just smile."
    "Nothing special, but it still feels so unique."
    scene black
    with fade
    "Some time later..."
    scene classroom2
    with dissolve
    "Class is finished, and it's time to leave."
    b "Hey, I gotta go, got classes to catch!"
    p "Of course! I'll see you around."
    "She waves as she leaves."
    "A little bummed there's nothing more, you leave, too."
    stop music fadeout 1.5

label day10:
    scene black
    with fade
    daycard "DAY 10"
    scene classroom2
    with dissolve
    if arielle_stage >= 3:
        "You notice you've stopped checking whether Arielle opened your message."
        "You're not sure when that happened."
    "And back to school again."
    "This time, you go straight to the seat next to Emma."
    "And you guys talk about whatever you can think of."
    play music "audio/ilikeyoualot.mp3" fadein 1.0
    p "So, how many new friends did you make?"
    show emmabus at pos_center
    with dissolve
    b "Yeah! I met a few interesting people, there's Claire, Cathy, Xavier..."
    b "Oh, and of course, you."
    "You laugh."
    p "Well, I appreciate that."
    scene black
    with fade
    "Some time later..."
    scene classroom2
    with dissolve
    "Class is finished, and it's time to leave."
    "You don't know what to say to conclude the interaction, so you just pretend to be busy and pack up your bag slowly."
    "And it works."
    "Emma's already done."
    show emmabus at pos_center
    with dissolve
    b "Hey, what are your plans for the weekend?"
    p "Nothing at the moment. What's up?"
    b "I was thinking maybe we could hang out?"
    p "Sure!"
    p "(Does she mean just the two of us?)"
    b "How about Saturday afternoon?"
    p "Sure!"
    b "Great! I guess we'll... keep in touch?"
    p "No problem!"
    "You both feel a little embarrassed, so you wrap up the conversation and go your separate ways."
    p "(This can't possibly be a date, right?)"
    stop music fadeout 1.5
    scene black
    with fade
    "Some time later..."
    scene restaurant
    show zane at pos_center
    with dissolve
    play music "audio/restaurant.mp3" fadein 1.0
    "You have dinner with Zane."
    x "So let me get this straight:"
    x "You're going on a date with Emma, and you've also been hanging out with Elena."
    p "Not a date."
    p "But something like that."
    x "Dude, I haven't seen you for, what? Four days?"
    x "And you've just become a fucking chick magnet or something?"
    p "What? You're being ridiculous, we don't even know what will happen."
    x "Yeah, you told me that last time, and back then you guys barely knew each other."
    p "HA! I knew you didn't think I had a chance last time."
    x "Of course not! I was trying to support you."
    x "But look at you now, I start to think I'm the one that needs support."
    p "Nah, man, come on. You had girlfriends before, I don't."
    p "You already win."
    x "Maybe."
    p "Come on man, let's not talk about this now."
    p "How about we talk about 'that game'?"
    x "You mean the one that's coming out soon?"
    p "Damn straight!"
    x "Oh man, I can't wait for it to come out..."
    stop music fadeout 1.5

label day11:
    scene black
    with fade
    daycard "DAY 11"
    scene bedroom
    with dissolve
    "Unsurprisingly, you barely slept last night, and you look like a piece of shit right now."
    "You spent all night thinking about the endless possibilities for the date."
    "Some are great, some are shit-bad, and they can all be true."
    "You need to get out and get your shit together."
    scene classroom4
    with dissolve
    "Early, yeah, whatever."
    "Elena is here, again."
    "For a girl that is so random, she sure seems fixed on this."
    p "Hey."
    play music "audio/joyful.mp3" fadein 1.0
    show elena at pos_center
    with dissolve
    a "Hey to you!"
    "Elena looks at you, shocked."
    a "Whoa, you don't look so good. Bad sleep?"
    p "Yeah, kind of."
    p "(If she's going to ask me the reason why, I better come up with something now.)"
    p "(It'd be stupid to just say, 'Hey, I'm going on a potential date with a girl!')"
    a "Guess it didn't go well with Gus?"
    a "You cut him off or something?"
    p "Nah. We talked about it and we're good."
    a "Really? I thought you would have a big fight or something."
    p "Nah, I don't like conflicts."
    p "Besides, I know he didn't do it on purpose. His intentions were... kind of good?"
    p "Also, it's a little bit on me for not telling him to keep quiet."
    p "Just a little bit."
    a "You're way too kind, you know."
    p "Maybe a little."
    scene black
    with fade
    "Some time later..."
    scene classroom4
    with dissolve
    "Class is finished, and you should leave too."
    a "Hey, I got something to do, gotta go."
    a "Talk to you soon?"
    p "No problem."
    "You already had a feeling she'd disappear on her own adventure and pop up again out of nowhere."
    "So you don't feel sad or angry anymore."
    "You're kind of getting used to her vibe."
    "Which is good?"
    stop music fadeout 1.5

label day12:
    scene black
    with fade
    daycard "DAY 12"
    scene bedroom
    with dissolve
    "Yep, you still didn't sleep well last night, and you still look like a piece of shit right now."
    "You spent another night thinking about the endless possibilities for the date."
    "You feel even worse now."
    play sound "audio/sfx/ringtone.ogg" loop
    "Then your phone rings."
    p "(Who would be calling me now?)"
    "Kind of annoyed, you don't even check the name on the screen and just pick up."
    stop sound fadeout 0.2
    p "Hello?"
    play music "audio/joyful.mp3" fadein 1.0
    a "Hey, sleepy head, time to wake up!"
    p "Oh shit, Elena!?"
    a "Yeah, it's me in the flesh."
    a "Why are you so surprised, you're having sex right now or something?"
    p "WHAT?"
    a "Just kidding! HAHA!"
    a "So what're you doing now?"
    p "Just woke up and getting myself a cup of tea."
    a "Then what are you doing later?"
    p "Nothing, I guess?"
    a "Cool, wanna hang out with me?"
    "You just woke up, and your head is buzzing."
    "Honestly, it's a miracle you even answered the phone."
    p "Yeah, sure. Just give me like, an hour."
    a "Nice! It's a date then."
    p "Yeah."
    "After you hang up the phone..."
    "......"
    "........."
    "..........."
    p "(Wait...)"
    $ renpy.music.play("audio/djdrop.mp3", channel="music", loop=0)
    p "(OH, SHIT, OH SHIT, OH SHIT SHIT SHIT!)"
    p "(DID SHE JUST SAY IT'S A DATE!?)"
    p "(She's joking, right? RIGHT?)"
    p "(She's got to be joking.)"
    p "(But if she's not, now I have two dates in two days. Does that count as cheating?)"
    p "(And now, I have a date in one hour.)"
    p "(STUPID! Why couldn't you just say you needed more than one fucking hour!?)"
    p "FUCK THIS--"

    scene  place
    with dissolve
    "You don't know how you do it. Maybe your life just switched to autopilot for a minute."
    if go_with_elena:
        "Somehow you get your shit together and show up at the exact spot where you waited for her last time."
        "Then you see a car approaching, and you already know it's Elena."
        a "Come on, hop in!"
        scene road2
        with dissolve
        "Once again, you're in her car."
    else:
        "Somehow you get your shit together and show up at the spot Elena told you about."
        "Then you see a car approaching, and the driver rolls down the window."
        "It's Elena."
        a "Come on, hop in!"
        scene road2
        with dissolve
    play music "audio/peace.mp3" fadein 1.0
    "This time, you can't shake a feeling of deja vu."
    "You realize that right now feels like the dream you had before."
    "But you can't really tell why you feel this way."
    menu:
        "Mention the dream.":
            $ elena_affection -= 1
            p "You know, I had a dream kind of like this. Just driving down a wide road like this one."
            p "It's one of the best dreams I've ever had."
            a "Yeah? Anyone with you on that journey?"
            p "Yeah... someone who meant something to me."
            "That's the best answer you can come up with on the spot without ruining the mood."
            p "(Probably shouldn't have mentioned that dream at all, damn!)"
            a "You wanna talk about it?"
            p "Maybe next time."
        "Don't mention the dream.":
            p "(Might be a bad idea to mention that.)"
    play music "audio/road.mp3" fadein 1.0
    if go_with_elena:
        "You know she likes the surprises indie music can bring."
        "So you just sit back and enjoy the music and the view."
        "Also, you're pretty sure even if you ask where you're going, she won't answer."
    else:
        p "So where are we going?"
        a "Wait and you'll see!"
        p "Fair enough."
        "Then you realize something."
        "It's still debatable whether this is a real date, but it occurs to you that you never asked if she's single."
        p "Hey, I hope this doesn't sound rude, but you don't have a boyfriend now, right?"
        a "No, I don't. You think I would go out with you alone if I'm in a relationship?"
        p "(She has a point...)"
        p "(Wait, so is this actually a real date!?)"
    "Lost in thought, you don't notice you've arrived."
    a "Hey, we're here!"
    p "Drive-in?"
    stop music fadeout 1.5

    scene drivein
    with dissolve
    play music "audio/cinema.mp3" fadein 1.0
    "A drive-in theater, where you watch movies from your car. They're pretty rare these days."
    p "Wow, I never knew you were this kind of person."
    a "What? Old?"
    p "More like retro."
    a "HAHA, fuck you!"
    p "Seriously though, it's pretty cool."
    p "I didn't know drive-ins still existed."
    p "How did you find this place?"
    a "That's another story for another time."
    a "For now... to the popcorn and drinks!"
    scene black
    with fade
    "Some time later..."
    scene drivein
    with dissolve
    "After the debate of the century over salty versus sweet popcorn, you're both in the car and ready for the movie."
    p "So... What's the movie about?"
    a "I have no idea."
    p "You have no idea?"
    a "I mean, the experience is more important, right?"
    p "Yeah, yeah. But if it's a horror film, I'm leaving."
    a "You don't like being scared shitless?"
    p "HAHA, very funny."
    a "Don't worry, if it's a horror film, you have my permission to hold my hand."
    "She says it while showing her hand."
    "You laugh."
    p "You'd better keep your word."
    a "Of course I will!"
    scene black
    with fade
    "Some time later..."
    scene drivein
    with dissolve
    "Luckily (or maybe not) for you, it's just some normal romance movie."
    "The plot isn't that good, but Elena was right."
    "The experience definitely makes the movie better."
    "You guys watch the movie without talking."
    "You laugh when you're supposed to laugh."
    "It feels very special."
    "At last, the movie ends, and the credits start to roll."
    "Then Elena talks."
    a "You know, I've never brought anyone here before."
    if go_with_elena:
        p "(At this point, she's taken me to way too many places she's never taken anyone else.)"
        p "(I'd be fucking stupid to think this means nothing.)"
        p "(If there's a next time, I should definitely take her to my special place, too.)"
    else:
        p "(Okay, this is definitely a date.)"
        p "(If there's a next time, I should definitely take her to my special place, too.)"
    p "And I'm really glad you brought me here."
    scene black
    with fade
    "Some time later..."
    scene road3
    with dissolve
    "After this extraordinary adventure, she drives you home."
    "Neither of you talks much. You can tell something is up."
    "Then she drops you off."
    scene placenight
    with dissolve
    "But before she leaves, she talks to you."
    a "Hey!"
    p "Yeah?"
    a "Do you... wanna try this?"
    p "What?"
    a "You and me?"
    play sound "audio/sfx/heartbeat.ogg"
    "You kind of saw this coming, but you're still in shock when it happens."
    a "Don't worry, take your time to think about it. No pressure."
    "She drives away before you can say anything."
    "Leaving you there, standing like a statue, still in shock."
    stop music fadeout 1.5

    scene black 
    with fade
    pause
    scene bedroomnight
    with dissolve
    "Shocked by what Elena said, you know you're destined to stay awake all night."
    "Which is not a surprise."
    "Especially since you still have a date with Emma."
    "Which kind of feels wrong now."
    "Not knowing what to do, you text Zane for advice."
    "Since Gus's credibility isn't exactly high right now."
    $ phone_open("Zane")
    x_txt "Hey man, what's up?"
    play music "audio/lahth.mp3" fadein 1.0
    p_txt "Hypothetical question, does it count as cheating if I go on two dates?"
    x_txt "'Hypothetical', huh?"
    x_txt "I'll have to get the full picture of the situation first."
    x_txt "Did they put a label on it, like you're officially dating?"
    p_txt "No, I don't think so. But I think they're really getting to that point."
    x_txt "If that's the case, I think two dates are fine."
    x_txt "BUT."
    x_txt "The fact that you're wondering if it's cheating means that deep down, a small part of you already feels it's wrong."
    p_txt "Hey, I didn't say it was me."
    x_txt "Yeah, and I'm the president of the United States. I'm not that stupid."
    x_txt "My suggestion: go on both dates, and you'd better make up your mind after that."
    x_txt "Because you're getting to the point where someone might get their heart broken."
    p_txt "Thanks, dude. Now I feel SO relaxed, and not under SO much pressure that I'm going to freak out."
    x_txt "Dude, you asked for my advice, not my comfort."
    x_txt "I'm being genuine here."
    p_txt "Yeah, I get it."
    p_txt "I really appreciate the help."
    x_txt "Hey, cut yourself some slack. Just play it cool for now."
    x_txt "Nothing has happened yet."
    x_txt "Before that crucial point, you're still safe."
    p_txt "Thanks, man. I needed that."
    x_txt "No problem."
    $ phone_close()
    "You turn off your phone and try to go to sleep."
    "And of course, it doesn't work."
    stop music fadeout 1.5

label day13:
    scene black
    with fade
    daycard "DAY 13"
    scene bedroom
    with dissolve
    "Another day, another beginning."
    "You spend half the day getting ready."
    "The more you prepare, the more you feel you're fucked."
    "Eventually, it's time."
    "So you head out."
    scene busstation
    with dissolve
    play music "audio/theladyofthelake.mp3" fadein 1.0
    "It's a weird place for Emma to choose as a meeting spot."
    "Even so, that's still not what worries you the most."
    "And this time, you're actually earlier than her."
    "You wonder what happened."
    "Then she shows up carrying two packages."
    show emma at pos_center
    with dissolve
    b "Hey! Hope I didn't keep you waiting for so long."
    p "Nah, I just got here."
    "Which is kind of not true."
    p "So what are those?"
    b "You'll find out later."
    scene black
    with fade
    "Some time later..."
    scene lake
    with dissolve
    "You find yourself at the lake."
    "A very particular choice, you might add."
    "She notices you're thinking about something."
    b "Hey, don't worry."
    b "We're not gonna swim."
    b "There's a cabin where we can chill, it's my aunt's."
    b "She's out of town for a few days."
    p "(Wow, her family owns a cabin? Guess they are pretty rich.)"
    p "So what are we doing today?"
    b "Nothing."
    p "Nothing?"
    b "And something."
    p "(And something...)"
    b "But first, let's head inside and relax a bit."
    "You follow her."
    scene cabin
    with dissolve
    "It's kind of hilarious that even though there are seats inside, you both just sit outside and enjoy the view."
    "Then Emma speaks."
    b "I used to come here a lot when I was a kid. I loved how wide the lake looked."
    b "It seemed so big and sparkling when I was young."
    b "But the older I got, the less we came here."
    p "Why?"
    b "Distance? Change? Life? You name it."
    b "Sometimes, nothing happens, we just...grow up."
    "To your surprise, even though Elena and Emma are completely different people, they're really similar in some ways."
    "You wonder what it would be like if they were friends."
    "Maybe that will happen in time, or maybe you should introduce them to each other?"
    "Nope. That's stupid, at least for now."
    b "Anyway, there's something I wanna do, and I think it's time."
    "Finally, you're going to find out what's in the packages. You've been dying to know."
    "And the mystery is revealed..."
    b "Paper lanterns!"
    b "But the kind that floats on water!"
    p "Paper lanterns?"
    "You're surprised, but somehow it comes out sounding pretty disappointed."
    b "You don't like that?"
    p "(Fuck you and your voice, [player_name].)"
    p "No! I think it's pretty special."
    p "But why do you want to do it?"
    b "For good luck, I think."
    b "Also, it's pretty cool to experience all kinds of cultures."
    p "Well, I won't say no to that."
    b "But first, we have to make them ourselves."
    "You've never been that into DIY."
    scene black
    with fade
    "Some time later..."
    scene table
    with dissolve
    "After some struggling, some laughing at your expense, and even some help, you finally finish."
    p "All right, I think we're good to go!"
    p "Though I remember you can write wishes on the lantern, right?"
    b "Impressive! Indeed we should!"
    b "Just write something that comes to your mind."
    "You see Emma has already started writing something."
    p "What are you writing?"
    b "It's a secret! No peeking!"
    p "Fine, fine!"
    "You get back to your lantern."
    $ player_wish = renpy.input(__("What should you wish for?"), length=40, exclude="[]{}")
    $ player_wish = player_wish.strip()
    if player_wish == "":
        $ player_wish = "Become someone you like"
    "You hope it comes true."
    p "All right, I'm done. You good to go?"
    b "Yep, let's go!"
    scene lantern
    with dissolve
    "You don't know why, but you're taking this more seriously than you expected."
    "You don't play around or talk. You just walk to the lake and release the lantern."
    "So does Emma."
    "You just watch the two lanterns float away."
    "It's so beautiful that you don't understand why you've never done this before."
    "In just these few days, you've learned so many things people don't usually say."
    "And seen places you never cared about or even noticed."
    "Every new person is like a new book and you can only know the story if you open it first."
    p "(Next time, I should leave my book open.)"
    "Once the lanterns are out of sight, you pack up and get ready to leave."
    scene black
    with fade
    "Some time later..."
    scene bus
    show emmabus at pos_bus_seat
    with dissolve
    "Pretty tired, neither of you says much on the way home. You just rest."
    "Then Emma speaks."
    b "Hey, I really appreciate you doing this with me."
    p "No problem."
    "She opens her mouth, then closes it."
    "Then she opens her mouth again."
    b "You know I like you a lot, right?"
    play sound "audio/sfx/heartbeat.ogg"
    p "(Oh shit!)"
    "She can definitely tell you're overthinking."
    b "Hey, don't overthink this, okay?"
    b "I just feel like I need to say this or I probably will regret it."
    b "You don't have to say anything now, but let me know how you feel soon, okay?"
    p "Okay, I promise you."
    stop music fadeout 1.5
    scene black
    with fade
    "Some time later..."
    scene bedroomnight
    with dissolve
    "Okay, this is definitely getting out of hand."
    "Two girls have just confessed their feelings to you."
    "And worst of all, you have feelings for both of them."
    "This is starting to feel wrong."
    "You need to decide, and you need to decide now!"
    
label theday:
    scene black
    with fade
    daycard "THE DAY"
    scene bedroom
    play music "audio/choice.mp3" fadein 1.0
    show zane at pos_farleft
    show gus at pos_farright
    with dissolve
    "After you tell Zane and Gus what happened, they come to your place ASAP."
    z "Look at my boy here, he's becoming the real winner!"
    x "Dude, can't you see he's bothered as fuck right now?"
    p "It's ok, Zane. I just never thought this kind of shit would happen to me."
    p "I mean, look at me."
    p "What quality do I have to make two girls like me at the same time?"
    p "Did I save someone's life in a previous life or something?"
    p "I can't find any explanation."
    x "Bro, chill."
    x "Like I said before, have some confidence in yourself."
    x "You're a good guy. There's nothing wrong with two girls falling for you at the same time."
    z "I can't agree with Zane more."
    z "You got this."
    z "Now the question is, who will you choose?"
    z "Oh, this is so exciting!"
    x "GUS!"
    p "I mean, Elena brings out a side of me even I didn't know about. It's always exciting with her."
    p "On the other hand, I feel so comfortable with Emma. We're so much alike, it's kind of scary."
    x "Hey, man, listen. I know this will sound cliche as fuck."
    x "But follow your heart."
    p "You're right."
    p "It's cliche as fuck."
    x "Fine."
    x "But listen."
    x "After all this time, who can you imagine being in a relationship with?"
    x "Or which one makes you happier?"
    x "Think about that."
    x "Also, I'm gonna have to be honest with you."
    x "If you don't have the answer after I ask you those questions, then perhaps you shouldn't choose either of them."
    z "Wait, why?"
    x "Because that means [player_name] doesn't have stronger feelings for either of them."
    x "If that's the case, then neither of them feels right enough for [player_name] to say yes."
    x "The fact that [player_name] asks us to help is already kind of a bad sign."
    x "But I get it, this is kind of a big decision."
    x "It's normal to freak out."
    z "Dude, you're so good at this stuff."
    x "I know, right?"
    x "That being said, I think I've bought you enough time, [player_name]."
    x "So, what's it gonna be?"
    menu:
        "Elena" if elena_affection >= 3:
            p "I have my answer, I'm gonna meet her now."
            jump elena_ending
        "Emma" if emma_affection >= 8:
            p "I have my answer, I'm gonna meet her now."
            jump emma_ending
        "None" if emma_affection >= 8 or elena_affection >= 3:
            p "You know what? You're right."
            p "If I'm still sitting here thinking about it, it means I don't like either of them more."
            p "Maybe my feelings for them are just not strong enough."
            p "I should let both of them go, it's better this way."
            z "I salute you my friend. You're a god damn legend."
            x "I trust your choice. This is gonna hurt, but it'll be worth it in time."
            jump none_ending
        "None (score too low)" if emma_affection <= 7 and elena_affection <= 2:
            p "You know what? You're right."
            p "If I'm still sitting here thinking about it, it means I don't like either of them more."
            p "I'm not even sure either of them likes me that much."
            p "I should let both of them go, it's better this way."
            z "I salute you my friend. You're a god damn legend."
            x "I trust your choice. This is gonna hurt, but it'll be worth it in time."
            jump none_ending
    stop music fadeout 1.5

label reject_emma:
    scene parkafternoon
    with dissolve
    "You wait for Emma at the park."
    "You keep rehearsing what to say."
    "You don't even notice Emma arriving."
    "She looks so happy and so innocent, with no idea what's coming."
    b "Hey!"
    "You finally notice her."
    show emma at pos_center
    with dissolve
    p "Oh hey!"
    "You hug each other and then sit on the bench."
    b "So, what are we doing today?"
    p "Nothing."
    b "Nothing?"
    "You can't keep stalling. The longer you wait, the worse it'll be!"
    p "Actually, I have something to say."
    "Emma turns to face you."
    b "What is it?"
    "Once again, you brace yourself for what you're about to say."
    p "I really like you, Emma. I do."
    p "But we shouldn't be together."
    "You watch Emma's smile fade as confusion sets in."
    "She tries to process what you're saying."
    b "Okay... but why? Did I do something wrong?"
    p "No, no, no. It's not because of anything you did."
    p "And I like you, I really do."
    p "And you're a good person, you are."
    p "But the problem is me."
    p "What I feel right now isn't strong enough to make me sure we should be together."
    p "I hesitate."
    p "You are fully prepared, but I'm not."
    p "And I certainly can't ask you to wait."
    p "What if I still said no after all that?"
    p "That would hurt you even more."
    p "I don't want to leave you hanging in uncertainty."
    "She stays quiet for a while."
    b "It's okay, I kind of get what you're saying."
    b "And I'm glad you told me."
    "Tears start to fall."
    b "But it's just not fair."
    b "You don't know how much I like you."
    "You look at her."
    "There's no one to blame but yourself for making her feel this way."
    b "At least I tried, right?"
    p "Yes, yes you did."
    p "And I'll always remember that."
    "You know she's way too mature for her age."
    "You know exactly what you're giving up."
    "You say nothing and just hold her."
    "You let her cry until she's done."
    "You feel like you're the biggest piece of shit in the world."
    "Finally, Emma pulls herself together."
    b "Well, this sucks."
    b "At least you let me know sooner."
    b "Now I have time to heal."
    "You want to ask if you can still be friends, but you know that's too much to ask right now."
    b "I'll see you around, [player_name]."
    "Then she stands up and leaves."
    hide emma
    with dissolve
    "It hurts to make such a wonderful girl cry like that. This is one of the hardest decisions you've ever made."
    "But you know it's the right thing to do."
    return

label reject_elena:
    scene beach
    with dissolve
    "Here you are."
    "You asked Elena if you could talk."
    "She told you to meet her at the beach."
    "This is gonna suck, but you still have to do it."
    "You see Elena."
    show elena at pos_center
    with dissolve
    "She's waving at you."
    "You have the urge to say nothing and pretend it's all right."
    "But your moral compass wins."
    a "Hey, how are you doing?"
    p "Yeah, I'm fine."
    a "Really?"
    p "Actually no, I feel like shit."
    a "Why? What happened?"
    "You stay silent for a while."
    "You think she already knows where this is going."
    "She waits for you to continue."
    "You take one big fucking breath."
    p "I don't think we should date each other."
    "Elena pauses for a second, like she's thinking it all through."
    "Then she speaks."
    a "You really sure about this?"
    p "Yes."
    a "Okay then."
    p "Okay?"
    a "Yeah."
    "You're surprised her reaction is way calmer than you expected, and YOU had imagined EVERY possibility."
    a "What? You thought I was gonna give you a hard time or something?"
    p "Actually, yes."
    a "Well, I'm not that type of person."
    a "It's clear you've thought this through and made up your mind."
    a "And you even told me in person, which is already better than a lot of people."
    a "If this is what you want, I won't stop you."
    "This is going way too well."
    a "Though you might regret what you'll miss."
    "She winks at you."
    p "I'm sure this decision will haunt me every day."
    "You smile."
    "Silence falls, until Elena holds out her hand."
    a "Hey, but we can still be friends, right?"
    "You shake her hand."
    p "Of course, friends."
    a "Friends."
    "Then she hugs you and shouts as she leaves."
    a "Let me know if you wanna hang out or something."
    a "Don't just ghost me because of this."
    p "Never!"
    hide elena
    with dissolve
    "You shout after her as she walks farther and farther away."
    "You then sigh."
    "It actually went better than you expected, but you still feel sad inside."
    "But you know this is the right thing to do."
    return

label elena_ending:
    "Before you go to Elena, there are still things you need to do."
    "And one of them is painful."
    call reject_emma
    "You feel like shit, but you're also happy it's time."
    "Time to do what you've been waiting to do for a long time."
    "On the way, you open the dating app one last time."
    "Then you delete it."
    "You don't need it anymore."
    stop music fadeout 1.5

    scene black
    with fade
    play music "audio/elena.mp3" fadein 1.0
    lv "YOU SUDDENLY REALIZE SOMETHING."
    scene place
    with dissolve
    lv "It's the first time you've had to wait at this spot."
    lv "He texted you to wait at the same spot where you had him wait before."
    lv "And it's kind of funny and frustrating at the same time."
    lv "Then a car approaches, and its window rolls down."
    pv "Come on, what are you waiting for?"
    l "Yeah, coming!"
    scene black
    with fade
    lv "You get in the car."
    scene playercar
    with dissolve
    l "If I'd known you had a car, I wouldn't have been driving you around this whole time."
    pv "Well, you never asked."
    l "Fair enough."
    lv "You look out the window and just vibe with the music."
    l "Nice songs, what are these?"
    if go_with_elena:
        pv "Remember that band I told you about?"
        l "Oh, I remember it! It's fear...care?"
        pv "Close enough. Far Caspian."
        l "Well, they're really good."
        pv "Told you."
    else:
        pv "An indie band called Far Caspian."
        l "Cool! I always have a thing for indie music."
        pv "Is that so? Noted."
    lv "He winks, and you didn't see that coming."
    l "Someone's in a good mood."
    l "What's the good news?"
    pv "You'll see."
    scene black
    with fade
    lv "Some time later..."
    scene stairs
    with dissolve
    lv "You follow him into a building."
    l "What's this place?"
    pv "It's actually my apartment."
    lv "You're a little surprised and laugh out loud."
    l "Whoa, I didn't know you were this kind of person. So eager."
    pv "Oh, no, no, that's not what I meant, I... "
    pv "You're messing with me, aren't you?"
    lv "You nod and smile."
    pv "Well played."
    scene rooftop
    with dissolve
    lv "You keep climbing, and finally, you're there."
    l "Rooftop?"
    pv "Yep."
    l "Look, if you're mad, I'm sorry..."
    pv "Oh, no, no. The rooftop is where I wanted to take you in the first place."
    l "Why?"
    if go_with_elena:
        pv "Remember when you told me you love how quiet the beach is at night, and I said it was peaceful?"
        l "Yeah."
        pv "This is one of the places that makes me feel peaceful."
        lv "You realize he's about to share something personal, so you stay quiet, sit down on a chair, and take in the view."
    else:
        lv "You realize he's about to share something personal, so you stay quiet, sit down on a chair, and take in the view."
    pv "When I was in high school, the school was being renovated, so some places that weren't supposed to be open were, well, open."
    pv "Yeah, and I found a spot."
    pv "Turns out the door that led to the rooftop was unlocked."
    pv "So that place kind of became my personal space."
    pv "It's not that high, but it kind of makes you feel like you're flying, up there in the sky."
    pv "Just you, looking down on the world."
    pv "I know this sounds stupid, but sometimes I look down and wonder how painful it would be to jump down."
    lv "You don't see this coming at all."
    l "Hey, it's not stupid."
    pv "It is, and I know it."
    pv "But don't worry, I'm not planning to kill myself or anything. HAHA."
    lv "You go quiet for a while."
    lv "He probably realizes that wasn't the right thing to say, so he changes the subject."
    pv "And that rooftop has a garden."
    pv "Sometimes I didn't give a damn about my clothes and just lay down on the grass, looking up at the sky."
    lv "You picture a young [player_name] lying on the grass. You can picture it pretty well. He looks happy."
    pv "And it still feels amazing, even now."
    lv "You can see him smile."
    pv "But you know, eventually people found out about the place, and more and more of them started showing up."
    pv "And eventually, the school found out and locked the door."
    pv "Just like that, I never got to feel that again."
    pv "Until I found this rooftop."
    lv "You take in the view again."
    pv "I mean, you definitely can't compare this to what I had before, but this rooftop is still pretty unique to me."
    pv "But mostly, I think it gives me the peace I've been longing for."
    pv "And..."
    pv "You're the first one to know about this."
    lv "After hearing this, you just stop giving a fuck."
    lv "You stand up, get close to him and just kiss him."
    lv "You can tell he's surprised (and inexperienced), but he still gives it his best."
    lv "You pull back."
    l "Sorry, I just feel like doing that."
    pv "Nothing to be sorry about. I like it."
    l "Though you never answered my question..."
    lv "He realizes what you mean, and then he notices something."
    pv "Wait a minute, are you blushing?"
    lv "Now that he's pointed it out, you definitely realize it, too."
    l "The fuck I am!"
    lv "You definitely blush even harder now."
    pv "Okay, okay."
    lv "He laughs, then turns serious."
    pv "Yes."
    l "What?"
    pv "Yes, I would like to try."
    pv "You and me."
    lv "You've been in relationships before, but you've never felt this nervous and this happy."
    lv "You'll never tell him, but the wait between asking him and getting an answer scared you a lot."
    lv "And the fact that he took this long to answer must mean he thought it through."
    lv "Or he's just an idiot who doesn't know how much you really like him."
    lv "So you jump into his arms, and he's so surprised he almost drops you."
    lv "But you don't give a fuck."
    lv "You just want to kiss him like there's no tomorrow."
    stop music fadeout 1.5
    $ mark_ending("elena")
    jump tomorrow

label emma_ending:
    "Before you go to Emma, there are still things you need to do."
    "And one of them is painful."
    play music "audio/end.mp3" fadein 1.0
    call reject_elena
    "You feel a little relieved, and you're also happy it's time."
    "Time to do what you've been waiting to do for a long time."
    "On the way, you open the dating app one last time."
    "Then you delete it."
    "You don't need it anymore."
    stop music fadeout 1.5

    scene black
    with fade
    play music "audio/emma.mp3" fadein 1.0
    lv "YOU REALIZE SOMETHING."
    scene cafe 
    with dissolve
    lv "This is the first time he's asked you out since you told him how you feel."
    lv "You're scared of what is gonna happen."
    lv "But you're also hopeful for what's going to happen."
    lv "Which is why you got to the cafe way too early and are just sitting here."
    lv "You wonder why he chose this specific cafe."
    lv "The view is not that bad but it's also not that good."
    lv "You hope this is not a bad sign."
    lv "If you said you weren't nervous, you'd definitely be lying."
    lv "But even if he rejects you, you get it."
    lv "You believe you can take it."
    lv "After all, it's just a heart being broken, right?"
    lv "You're so deep in your own head that you don't notice him coming."
    pv "Hey, I'm sorry for keeping you waiting."
    l "No, no, no, it's fine, I came too early myself."
    pv "Well then, I should have expected that and come earlier."
    lv "He gives you a smile."
    lv "You're kind of blushing, so you try to change the subject."
    l "So, what are we doing today?"
    pv "I was thinking we could grab a drink first, then go for a walk, if that's all right?"
    l "Of course!"
    l "(That's a really simple plan for a date.)"
    lv "You don't like the feeling of what's coming next."
    pv "So... What would you like?"
    lv "'You' almost slips out of your mouth, and that's not like you at all."
    l "Green tea will be fine, thanks."
    scene black
    with fade
    pause
    scene cafe
    with dissolve
    lv "By the time he brings the drinks, your head is already spinning like crazy."
    lv "And now he's sitting next to you."
    lv "He seems nervous, too, like he's about to say something bad."
    lv "Then he decides to break the ice first."
    pv "You know, I used to come here a lot."
    l "Huh?"
    lv "Not expecting that, you blurt out the first thing that comes to mind."
    lv "And you feel so rude."
    lv "You can tell he's trying to explain."
    pv "My high school is close by."
    lv "You start to come back to your senses."
    lv "He hasn't said anything important yet. There's still hope."
    l "You love this place?"
    pv "Not really."
    lv "You're kind of surprised."
    pv "Remember when I said there were only a few memories from high school that make me happy?"
    l "And this is also one of them?"
    pv "Yeah."
    l "Why?"
    pv "My old friends and I used to hang out here after school."
    pv "Not for long, since we all had to go home."
    pv "You see the seats outside?"
    pv "That's where we always sat."
    lv "Maybe you shouldn't have come so early. You should have let him pick the seats."
    pv "Sometimes we'd just watch funny videos."
    pv "Sometimes we'd eat some snacks."
    pv "And sometimes we'd just talk."
    pv "About stupid things, weird things, everything."
    pv "We didn't really fit in with our class, but we had our own world."
    pv "And this,"
    lv "He shows you the drink."
    pv "Is what I always had back in the day."
    lv "You don't know what you should say now."
    lv "You feel kind of sad for him..."
    l "I'm sure it's very delicious."
    lv "You smile."
    pv "It's okay, I think?"
    lv "He smiles back."
    lv "You've already forgotten you were nervous in the first place."
    pv "You wanna get out of here?"
    l "Only if you want to."
    scene black
    with fade
    pause
    scene downtown
    with dissolve
    lv "You head out and walk together."
    lv "He's trying to figure out how to continue the conversation, you think."
    pv "Umm... So, about this walk."
    lv "He finally gets to the point."
    pv "My parents used to drive me to school early, so I'd always be in the classroom early, too."
    lv "He's stalling. Is he going to reject you?"
    pv "Problem was, I didn't like that feeling."
    pv "I didn't have many friends back then, and I barely knew my classmates."
    pv "So when I was in the classroom, I just felt isolated, like I was in prison."
    pv "Then one day, my parents dropped me off early as usual."
    pv "But this time, instead of going through the school gate, I walked the other way."
    pv "That was one of the best decisions I made in high school."
    lv "Does that mean he dropped out of high school?"
    lv "You feel like asking, but also feel like you should let him finish first."
    lv "So you just listen."
    pv "There was nothing really special about it, though."
    pv "I just walked around the streets near the school."
    pv "It was kind of surprising how many different buildings were around my school."
    pv "Hospitals, department stores, that cafe from earlier, and also, look!"
    pv "A park."
    pv "You wanna go and have a seat?"
    l "Sure."
    scene black
    with fade
    pause
    scene park2
    with dissolve
    lv "You sit on the bench in the park and enjoy the view."
    pv "So yeah, where were we?"
    lv "Here it comes."
    pv "Right, all kinds of buildings."
    l "(Damn it!)"
    pv "So, I didn't have much time before school started, but I still had time to look around."
    lv "So he didn't drop out."
    pv "It was too early for most stores to be open, and I actually liked that."
    pv "I'd just buy some tea or juice or whatever at the convenience store, put on my headphones, and wander around."
    pv "It was way quieter in the morning."
    pv "And there was just something so freeing about it."
    pv "It actually made getting through the school day a lot easier."
    l "Hey, I'm sure you were a wonderful guy in high school, too!"
    pv "Thanks, I needed that."
    lv "The two of you stay quiet for a while."
    lv "Then he speaks."
    pv "Anyway, the reason I'm telling you all this is that I figured it'd be easier to relax if I shared a secret first."
    pv "And also, I think I should share a place that's important to me, too."
    pv "And I trust you enough to tell you."
    lv "Wait, did he just say he trusts you enough?"
    lv "He takes a breath."
    pv "I really like you, too."
    lv "You think your heart just stopped beating for a second."
    pv "I want to try this, US, dating."
    lv "Then you realize why he's been doing all this. Everything he just said was important."
    lv "You're touched that he trusts you enough to tell you all this, and happy that he feels the same."
    lv "And it hits you: he feels the same."
    l "Really?"
    lv "You're smiling way too much."
    pv "Yes, I'm sure."
    lv "Without thinking, you kiss him on the cheek."
    l "Hey, I really appreciate that you shared that with me."
    pv "I wanted to."
    lv "Then you reach for his hand."
    lv "He notices, and holds yours back."
    pv "Want to walk a little?"
    l "Absolutely!"
    lv "You both stand up, still holding hands."
    lv "Then you go for a walk, and yes, still holding hands like there's no tomorrow."
    stop music fadeout 1.5
    $ mark_ending("emma")
    jump tomorrow

label none_ending:
    scene bedroom
    with dissolve
    play music "audio/end.mp3" fadein 1.0
    "You've made up your mind and are ready to do what needs to be done."
    "This will hurt, but at least you can choose who to talk to first."
    "Your last choice, though both will happen eventually."
    menu:
        "Go to Elena":
            call reject_elena
            "You feel a little relieved, but you're not done yet."
            "Time to find Emma."
            call reject_emma

        "Go to Emma":
            call reject_emma
            "You feel like shit, but you're not done yet."
            "Time to find Elena."
            call reject_elena
    scene bedroom
    with dissolve
    "You never knew it could be this painful to reject someone, let alone two people."
    "You hate yourself for having to do this."
    "But you've finally done it."
    "In time, you believe all of you will heal."
    "But for now, you just want to lie in bed and do nothing."
    "Thinking about all the decisions in your life that have led you to this moment."
    "[player_name2], Elena, Emma, Zane, Gus, Arielle..."
    if arielle_stage >= 3:
            play sound "audio/sfx/message.ogg"
            "Then your phone buzzes."
            "IT'S Arielle."
            $ phone_open("Arielle")
            ar_txt "omg hi"
            ar_txt "i'm SO sorry. my social got hacked and i lost literally everything"
            ar_txt "just restore it and remembered i never replied to you"
            "You stare at the screen."
            "Maybe it's true. Maybe it isn't."
            "You'll never know."
            ar_txt "anyway, are you still up for getting coffee sometime?"
            "HOW ABOUT TOMORROW?"
    else:
            "BEEEEEEEEEEE"
            p "Now what??"
            "EMERGENCY! GO TO THE NEAREST EXIT"
            p "Jesus! Fine."
            "You get dressed."
            "You go out."
            "You look at everything."
            "The couple, the friends, the loner, the tree, the rain, the sun."
            "They all still lived after today."
            "They all will be here tomorrow."
    stop music fadeout 1.5
    $ mark_ending("none")

label tomorrow:
    scene black
    with fade
    play music "audio/tomorrow.mp3" fadein 1.0
    "Yes, tomorrow."
    scene day
    with dissolve
    "Where there are endless outcomes."
    "Endless realities."
    scene browsing
    with dissolve
    "It's all up to you."
    "You, to make them happen."
    scene night
    with dissolve
    "And before it happens, anything is possible."
    "Anything."
    scene black
    with dissolve
    "Who knows?"
    "Maybe what you wish for will come true:"
    "[player_wish]."
    scene black
    with fade
    daycard "TOMORROW."
    scene black
    with fade
    pause
    pause
    return
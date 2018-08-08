screen differences_scr:
    
    ##### Timer
    timer 1.0 action [Return("smth_2"), If (diff_timer > 1, SetVariable("diff_timer", diff_timer - 1), Jump("diff_game_lose") ) ] repeat True
    
    text str(diff_timer) xalign 0.5 yalign 0.05
    
    ##### Two screens with practically identical images
    use left_scr(x=pic_name)
    use right_scr(x=pic_name)

    
screen left_scr:
    
    # Screen at left has all differences
    fixed:
        xpos 50 ypos 100
        button:
            background None
            $ base_pic = ("base_image_%s.png" % x)
            add base_pic
            action SetVariable ("diff_timer", diff_timer -1)
            mouse "left"
        
        for spot in differences_list:
            $ pic_1 = ("spot_%d_1_%s.png" % (spot["s_number"], x) )          # changed spot 
            $ pic_2 = ("spot_%d_0_%s.png" % (spot["s_number"], x ))          # normal spot
            $ pic_3 = ("spot_%d_done_%s.png" % (spot["s_number"], x) )       # done mark
            
            if spot["is_difference"]:
                button:
                    background None
                    add pic_1 
                    action [SetDict(differences_list[spot["s_number"]], "is_solved", True), Return("smth") ]
                    focus_mask True
                    mouse "left"
                
            else:
                button:
                    background None
                    add pic_2 
                    action None
                    focus_mask True
                    mouse "left"
                    
            if spot["is_solved"]:
                button:
                    background None
                    add pic_3 
                    action None
                    focus_mask True
                    mouse "left"
            



screen right_scr:
    
    # Screen at right has all the normal spots
    fixed:
        xpos 300 ypos 100
        button:
            background None
            $ base_pic = ("base_image_%s.png" % x)
            add base_pic
            action SetVariable ("diff_timer", diff_timer -1)
            mouse "right"
        
        for spot in differences_list:
            $ pic_1 = ("spot_%d_0_%s.png" % (spot["s_number"], x) )          # normal spot
            $ pic_2 = ("spot_%d_0_%s.png" % (spot["s_number"], x) )          # normal spot
            $ pic_3 = ("spot_%d_done_%s.png" % (spot["s_number"], x) )       # done mark
            
            if spot["is_difference"]:
                button:
                    background None
                    add pic_1 
                    action [SetDict(differences_list[spot["s_number"]], "is_solved", True), Return("smth") ]
                    focus_mask True
                    mouse "right"
                
            else:
                button:
                    background None
                    add pic_2 
                    action None
                    focus_mask True
                    mouse "right"
                    
            if spot["is_solved"]:
                button:
                    background None
                    add pic_3 
                    action None
                    focus_mask True
                    mouse "right"


init:
    
    # Should set the mouse cursor, 'cause we'll need the left and right ones
    # Those cursors have two arrows and the distance between them is (picture width + gap between left and right screen)
    # So in this example the left one has active point at (0, 0) and right - at (250, 0)
    $ config.mouse = {"default": [("cur.png", 0, 0)], "left": [("left_cur.png", 0, 0)], "right": [("right_cur.png", 250, 0)]}

    python:
        def spots_shuffle(x):
            renpy.random.shuffle(x)
            return x

label differences_game1:
    
    #####
    #
    # At first, let's set the number of possible differences and how many of them the player should find 
    $ differences_list = [] 
    $ differnces_total_number = 3
    $ differnces_number = 2
    $ values_l = []
    
    # And make the differences_list that describes all the spots
    python:
        for i in range (0, differnces_number):
            values_l.append (True)
        for i in range (0, (differnces_total_number - differnces_number) ):
            values_l.append (False)
        
        values_l = spots_shuffle(values_l)
        
        for i in range (0, differnces_total_number):
            differences_list.append({"s_number":i, "is_difference":values_l[i], "is_solved":False} )
    
            
    
    # Before start the game, let's set the timer
    $ diff_timer = 20
    
    # Shows the game screen with the named image.
    # Images must be named as
    # "base_image_[different names for each image].png" - image itself
    # "spot_0_0_[different names for each image].png" - first spot of an image in normal state _0_0_
    # "spot_2_1_[different names for each image].png" - third spot of an image in different state _2_1_
    # "spot_3_done)_[different names for each image].png" - done mark for fourth spot of an image _3_done_

    # There is only one image in this example, so just put it twice to show how it should work
    $ chosen_pic = renpy.random.choice( ("girl1", "girl1") )

    show screen differences_scr(pic_name=chosen_pic)
    

    # The game loop
    label diff_loop:
       $ result = ui.interact()
       $ diff_timer = diff_timer
       python:
           for i in range (0, len(differences_list)-1 ):
               one_of_spots = differences_list[i]
               # Loop will exist till at least one of differences doesn't found
               if one_of_spots["is_difference"] and not one_of_spots["is_solved"]:
                   renpy.jump("diff_loop")
                   
       jump diff_game_win
        
label diff_game_lose:
    hide screen differences_scr
    $ renpy.pause (0.1, hard = True)
    $ renpy.pause (0.1, hard = True)
    "You lose! Try again."
    jump differences_game2

label diff_game_win:
    $ renpy.pause (1.0, hard = True)
    hide screen differences_scr
    $ renpy.pause (0.1, hard = True)
    $ renpy.pause (0.1, hard = True)
    "You win!"
	jump differences_game2
	
	
label differences_game2:
    
    #####
    #
    # At first, let's set the number of possible differences and how many of them the player should find 
    $ differences_list = [] 
    $ differnces_total_number = 3
    $ differnces_number = 2
    $ values_l = []
    
    # And make the differences_list that describes all the spots
    python:
        for i in range (0, differnces_number):
            values_l.append (True)
        for i in range (0, (differnces_total_number - differnces_number) ):
            values_l.append (False)
        
        values_l = spots_shuffle(values_l)
        
        for i in range (0, differnces_total_number):
            differences_list.append({"s_number":i, "is_difference":values_l[i], "is_solved":False} )
    
            
    
    # Before start the game, let's set the timer
    $ diff_timer = 20
    
    # Shows the game screen with the named image.
    # Images must be named as
    # "base_image_[different names for each image].png" - image itself
    # "spot_0_0_[different names for each image].png" - first spot of an image in normal state _0_0_
    # "spot_2_1_[different names for each image].png" - third spot of an image in different state _2_1_
    # "spot_3_done)_[different names for each image].png" - done mark for fourth spot of an image _3_done_

    # There is only one image in this example, so just put it twice to show how it should work
    $ chosen_pic = renpy.random.choice( ("girl2", "girl2") )

    show screen differences_scr(pic_name=chosen_pic)
    

    # The game loop
    label diff_loop:
       $ result = ui.interact()
       $ diff_timer = diff_timer
       python:
           for i in range (0, len(differences_list)-1 ):
               one_of_spots = differences_list[i]
               # Loop will exist till at least one of differences doesn't found
               if one_of_spots["is_difference"] and not one_of_spots["is_solved"]:
                   renpy.jump("diff_loop")
                   
       jump diff_game_win
        
label diff_game_lose:
    hide screen differences_scr
    $ renpy.pause (0.1, hard = True)
    $ renpy.pause (0.1, hard = True)
    "You lose! Try again."
    jump differences_game3

label diff_game_win:
    $ renpy.pause (1.0, hard = True)
    hide screen differences_scr
    $ renpy.pause (0.1, hard = True)
    $ renpy.pause (0.1, hard = True)
    jump differences_game3

label differences_game3:
    
    #####
    #
    # At first, let's set the number of possible differences and how many of them the player should find 
    $ differences_list = [] 
    $ differnces_total_number = 3
    $ differnces_number = 2
    $ values_l = []
    
    # And make the differences_list that describes all the spots
    python:
        for i in range (0, differnces_number):
            values_l.append (True)
        for i in range (0, (differnces_total_number - differnces_number) ):
            values_l.append (False)
        
        values_l = spots_shuffle(values_l)
        
        for i in range (0, differnces_total_number):
            differences_list.append({"s_number":i, "is_difference":values_l[i], "is_solved":False} )
    
            
    
    # Before start the game, let's set the timer
    $ diff_timer = 20
    
    # Shows the game screen with the named image.
    # Images must be named as
    # "base_image_[different names for each image].png" - image itself
    # "spot_0_0_[different names for each image].png" - first spot of an image in normal state _0_0_
    # "spot_2_1_[different names for each image].png" - third spot of an image in different state _2_1_
    # "spot_3_done)_[different names for each image].png" - done mark for fourth spot of an image _3_done_

    # There is only one image in this example, so just put it twice to show how it should work
    $ chosen_pic = renpy.random.choice( ("girl3", "girl3") )

    show screen differences_scr(pic_name=chosen_pic)
    

    # The game loop
    label diff_loop:
       $ result = ui.interact()
       $ diff_timer = diff_timer
       python:
           for i in range (0, len(differences_list)-1 ):
               one_of_spots = differences_list[i]
               # Loop will exist till at least one of differences doesn't found
               if one_of_spots["is_difference"] and not one_of_spots["is_solved"]:
                   renpy.jump("diff_loop")
                   
       jump diff_game_win
        
label diff_game_lose:
    hide screen differences_scr
    $ renpy.pause (0.1, hard = True)
    $ renpy.pause (0.1, hard = True)
    "You lose! Try again."
    jump differences_game3

label diff_game_win:
    $ renpy.pause (1.0, hard = True)
    hide screen differences_scr
    $ renpy.pause (0.1, hard = True)
    $ renpy.pause (0.1, hard = True)
    jump theending
	
label theending:
	"It is over!"
    return

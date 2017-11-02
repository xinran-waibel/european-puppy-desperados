import animation


boss1_image = d_animation.animated_image( "graphics/boss1.png", 69, 69 )
boss1_walk = d_animation.animation( boss1_image, [0], True, 3 )
boss1_kick = d_animation.animation( boss1_image, [0,1,2,1,0], False, 3 )

boss1_smash_image = d_animation.animated_image( "graphics/boss1_smash.png", 69, 138 )
boss1_smash = d_animation.animation( boss1_smash_image, [0,1,2,3,4,3,2,1,2,3,4,3,2,1,2,3,4,3,2,1,0], False, 3 )

player_image = d_animation.animated_image( "graphics/player.png", 48, 48 )
player_walk = d_animation.animation( player_image, [0], True, 3 )
player_stab = d_animation.animation( player_image, [1,2,1], False, 3 )
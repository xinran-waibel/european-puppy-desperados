import player
import mice
import shootmice
import shoot
import cheese
import level
import values
import levels

class entity_manager:
    def __init__( self ):
        self.entities = []
        self.player = None
        self.level = None

    ### removes all entities from the manager
    def clear( self ):
        self.entities = []
        self.player = None

    ### takes in a function and applies it to all of the entities
    ### An additonal piece of data can be provided
    ### The function must take in an entity and an additional piece of data
    def do_this_for_all( self, function, data = None ):
        x = 0
        while(x < len(self.entities)):
            function( self.entities[x], data )
            x+=1

    ### removes any entities with remove_self flagged
    def cull( self ):
        def remove( entity, self ):
            if entity.remove_self is True:
                if entity.is_player:
                    values.entity_manager.reload_level()
                else:
                    if self.level.sprite_layers[1].contains_sprite( entity.sprite ):
                        self.level.sprite_layers[1].remove_sprite( entity.sprite )

                    self.entities.remove(entity)

        self.do_this_for_all( remove, self )
        
    ### handles collison detection of the entities
    def collide( self, level ):
        for entity in self.entities:
            entity.clear_collisions()
            level.collide(entity)

        x = 0
        while x < len( self.entities ):
            y = x + 1
            while y < len( self.entities ):
                if not self.entities[x].ghost and not self.entities[y].ghost:
                    if self.entities[x].group is self.entities[y].group or isinstance(self.entities[x], shoot.shoot) or isinstance(self.entities[y], shoot.shoot):
                        self.entities[x].overlap( self.entities[y] )
                    else:
                        self.entities[x].collide_with(self.entities[y])
                y+=1
            x+=1

    ### add an entity to the manager
    def add( self, entity ):
        self.entities.append( entity )
       
    ### spawns the entities in the level
    def spawn_entities( self, lvl ):
        spawn_layer = lvl.sprite_layers[4]
        xmin = 0 #int((lvl.cam_pos_x) / lvl.tile_width)
        #if xmin < 0:
        #        xmin = 0
        xmax = lvl.width #int((lvl.cam_pos_x + lvl.cam_width) / lvl.tile_width)
        #if xmax >= lvl.width:
        #        xmax = lvl.width - 1
        ymin = 0 #int((lvl.cam_pos_y) / lvl.tile_height)
        #if ymin < 0:
        #        ymin = 0
        ymax = lvl.height #int((lvl.cam_pos_y + lvl.cam_height) / lvl.tile_height)
        #if ymax >= lvl.height:
        #        ymax = lvl.height - 1

        for y in range(ymin, ymax):
            for x in range (xmin, xmax):
                if spawn_layer.content2D[y][x] is not None:
                    if spawn_layer.content2D[y][x].key[0] == level.spawn_type['player']:
                        self.player = player.player( x * lvl.tile_width, y * lvl.tile_height )
                        self.add( self.player )
                        lvl.sprite_layers[1].add_sprite(self.player.sprite)
                        spawn_layer.content2D[y][x] = None
                    elif spawn_layer.content2D[y][x].key[0] == level.spawn_type['miceleft']:
                        mouse = mice.mice(x * lvl.tile_width, y * lvl.tile_height)
                        mouse.heading = -1
                        mouse.velocity.x = -mouse.speed
                        self.add(mouse)
                        lvl.sprite_layers[1].add_sprite(mouse.sprite)
                        spawn_layer.content2D[y][x] = None
                    elif spawn_layer.content2D[y][x].key[0] == level.spawn_type['miceright']:
                        mouse = mice.mice(x * lvl.tile_width, y * lvl.tile_height)
                        mouse.heading = 1
                        mouse.velocity.x = mouse.speed
                        self.add(mouse)
                        lvl.sprite_layers[1].add_sprite(mouse.sprite)
                        spawn_layer.content2D[y][x] = None
                    elif spawn_layer.content2D[y][x].key[0] == level.spawn_type['shootmiceleft']:
                        shootmouse = shootmice.shootmice(x * lvl.tile_width, y * lvl.tile_height)
                        shootmouse.heading = -1
                        self.add(shootmouse)
                        lvl.sprite_layers[1].add_sprite(shootmouse.sprite)
                        spawn_layer.content2D[y][x] = None
                    elif spawn_layer.content2D[y][x].key[0] == level.spawn_type['shootmiceright']:
                        shootmouse = shootmice.shootmice(x * lvl.tile_width, y * lvl.tile_height)
                        shootmouse.heading = 1
                        self.add(shootmouse)
                        lvl.sprite_layers[1].add_sprite(shootmouse.sprite)
                        spawn_layer.content2D[y][x] = None
                    elif spawn_layer.content2D[y][x].key[0] == level.spawn_type['cheese']:
                        cheddar = cheese.cheese(x * lvl.tile_width, y * lvl.tile_height)
                        self.add(cheddar)
                        #lvl.sprite_layers[1].add_sprite(cheddar.sprite)
                        spawn_layer.content2D[y][x] = None

             
    ### calls for the level to be reloaded
    ### basically a temp soltuion
    def reload_level( self ):  
        self.clear()
        values.level = level.Level(levels.levels[levels.levelIndex], values.screen)
        self.level = values.level
        self.spawn_entities(self.level)

    ### calls for the next level to be reloaded
    ### basically a temp soltuion
    def load_next_level( self ):  
        levels.levelIndex += 1
        if levels.levelIndex >= len(levels.levels):
            levels.levelIndex = 0
        self.reload_level()

        
    ### calls all of the enitties update procedures
    def update( self ):
        def update_all( entity, unused ):
            entity.update()

        self.do_this_for_all( update_all )
        
        #self.spawn_entities( values.level )
        self.cull()

    ### calls all of the enitties draws procedures
    def draw( self, screen ):
        def draw_all( entity, screen ):
            entity.draw( screen )

        self.do_this_for_all( draw_all, screen )

#__revision__ = "$Rev: 115 $"
#__version__ = "3.0.0." + __revision__[6:-2]
#__author__ = 'DR0ID @ 2009-2011'


import sys
import os
import pygame
import math
import vector

try:
    import _path
except:
    pass

import tiledtmxloader

spawn_type = {'player': 1, 'miceright': 2, 'miceleft': 3, 'shootmiceleft': 5, 'shootmiceright': 4, 'cheese': 6}

class Level:
    def __init__( self, file = None, screen = None ):
      
        self.world_map = None

        self.pixel_width = 0
        self.pixel_height = 0

        self.tile_width = 0
        self.tile_height = 0

        self.width = 0
        self.height = 0

        self.layers = None
        self.number_of_layers = 0

        self.renderer = None

        self.cam_pos_x = 0
        self.cam_pos_y = 0
        self.cam_width = 0
        self.cam_height = 0

        self.sprite_layers = None

        if( not file is None ):
            self.load( file, screen )

    ### loads a level from a file name, requires the screen that the level is to be displayed on
    def load( self, file, screen ):
        """
        Main method.
        """
        args = sys.argv[1:]
        if len(args) < 1:
            path_to_map = os.path.join(os.pardir, file)
            print(("usage: python %s your_map.tmx\n\nUsing map '%s'\n" % \
                (os.path.basename(__file__), path_to_map)))
        else:
            path_to_map = args[0]

        # parser the map (it is done here to initialize the
        # window the same size as the map if it is small enough)
        self.world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(path_to_map)

        # let see how many pixels it will use
        self.pixel_width = self.world_map.pixel_width
        self.pixel_height = self.world_map.pixel_height

        # let see the tilesize
        self.tile_width = self.world_map.tilewidth
        self.tile_height = self.world_map.tileheight

        # number of tiles
        self.width = self.world_map.width
        self.height = self.world_map.height

        # map layers
        self.layers = self.world_map.layers
        self.number_of_layers = len( self.world_map.layers )

        # load the images using pygame
        resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
        resources.load( self.world_map )

        # prepare map rendering
        assert self.world_map.orientation == "orthogonal"

        # renderer
        self.renderer = tiledtmxloader.helperspygame.RendererPygame()

        # cam_offset is for scrollingaa
        self.cam_pos_x = 0
        self.cam_pos_y = 0

        # set initial cam position and size
        self.renderer.set_camera_position_and_size( self.cam_pos_x, self.cam_pos_y, \
                                            screen.get_width(), screen.get_height(), "topleft" )

        self.cam_width = self.renderer._cam_rect.width
        self.cam_height = self.renderer._cam_rect.height

        # retrieve the layers
        self.sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)

    ### checks if entity collides on the map
    def collide( self, entity ):

        coll_level = self.sprite_layers[3]
        #for sprite_layer in self.sprite_layers:
         #   if sprite_layer.name is "collision" or sprite_layer.name is "Collision":
          #      coll_level = sprite_layer
           #     break
        
        if coll_level is None:
            return

        for y in range( int( ( entity.body.top + entity.velocity.y ) / self.tile_height ), \
                        int( ( entity.body.bottom + entity.velocity.y ) / self.tile_height ) + 1 ):
            for x in range( int( ( entity.body.left + entity.velocity.x ) / self.tile_width ), \
                            int( ( entity.body.right + entity.velocity.x ) / self.tile_width ) + 1):
                if  y < self.height and x < self.width and y >= 0 and x >= 0 and not ( coll_level.content2D[y][x] is None ):
                    block = pygame.Rect( x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height )
                    entity.collide_with( coll_level.content2D[y][x].rect )

    ### returns the value of the collision tile at a given position
    def get_collision_tile_at( self, position ):
        x = int( position.x / self.tile_width )
        y = int( position.y / self.tile_height )

        if(self.sprite_layers[3].content2D[y][x] is not None):
            return self.sprite_layers[3].content2D[y][x].rect
        return None


    ### set the position of the camera
    def set_cam_pos( self, x, y ):
        self.cam_pos_x = x
        self.cam_pos_y = y
        
        if( self.cam_pos_x < self.cam_width / 2 ):
            self.cam_pos_x = self.cam_width / 2

        if( self.cam_pos_y < self.cam_height / 2):
            self.cam_pos_y = self.cam_height / 2
        
        if( self.cam_pos_x > self.pixel_width - self.cam_width / 2 ):
            self.cam_pos_x = self.pixel_width - self.cam_width / 2
        
        if( self.cam_pos_y > self.pixel_height - self.cam_height / 2 ):
            self.cam_pos_y = self.pixel_height - self.cam_height / 2

    ### draws the map and entities stored in it
    def draw( self, screen ):
        self.renderer.set_camera_position( self.cam_pos_x, self.cam_pos_y, "center" )

        # render the map
        for sprite_layer in self.sprite_layers:
            if sprite_layer.is_object_group:
                # we dont draw the object group layers
                # you should filter them out if not needed
                continue
            else:
                self.renderer.render_layer(screen, sprite_layer)

    # Takes in two vectors, one which represents the start of the raycast and one that represents the end
    # It returns a vector which represents how far the line goes without colliding into any wall 
    # or how far it goes without going past the end
    def raycast( self, start, end ):
        y_diff = end.y - start.y
        x_diff = end.x - start.x
                    
        line_length = math.sqrt( x_diff * x_diff + y_diff * y_diff )
        
        if x_diff == 0:
            x_diff = 1
        
        if y_diff == 0:
            y_diff = 1

        delta_x = math.sqrt( self.tile_width * self.tile_width + (self.tile_height * self.tile_height) * ( y_diff * y_diff ) / ( x_diff * x_diff ) )
        delta_y = math.sqrt( self.tile_height * self.tile_height + (self.tile_width * self.tile_width) * ( x_diff * x_diff ) / ( y_diff * y_diff ) )
        
        x_step = 1
        if x_diff < 0: x_step = -1
        
        y_step = 1
        if y_diff < 0: y_step = -1

        x_off = 0
        y_off = 0

        if ( x_step > 0 ):
            x_off = start.x - math.floor( start.x / self.tile_width ) * self.tile_width;
        else: 
            x_off = math.ceil( start.x / self.tile_width ) * self.tile_width - start.x;

        x_off *= math.fabs( y_diff / x_diff );

        if ( y_step > 0 ):
            y_off = start.y - math.floor( start.y / self.tile_height ) * self.tile_height;
        else: 
            y_off = math.ceil( start.y / self.tile_height ) * self.tile_height - start.y;

        y_off *= math.fabs( x_diff / y_diff );

        length_traveled = 0
        
        x = math.floor( start.x / self.tile_width )
        y = math.floor( start.y / self.tile_height )
        
        while ( length_traveled < line_length ):
            if not ( self.sprite_layers[3].content2D[y][x] is None ):
                return vector.Vector2( x * self.tile_width, y * self.tile_height );

            if ( delta_x - x_off < delta_y - y_off ):
                y_off += ( delta_x - x_off );
                length_traveled += ( delta_x - x_off );
                x += x_step;
                x_off = 0;
            else:
                x_off += ( delta_y - y_off );
                length_traveled += ( delta_y - y_off );
                y += y_step;
                y_off = 0;
        return end
 
    def raycast_succeeds( self, start, end ):
        resulting_ray = self.raycast( start, end )
        return ( resulting_ray.x == end.x ) and ( resulting_ray.y == end.y )

    def get_tile_position( self, x, y ):
        return vector.Vector2( x * self.tile_width + self.tile_width / 2, y * self.tile_height + self.tile_height / 2 )
    
    def get_offsetted_position( self, position ):
        return vector.Vector2( position.x - self.cam_pos_x + self.cam_width / 2, position.y - self.cam_pos_y  + self.cam_height / 2 )

    def is_tile_visible( self, tile ):
        left = int( (self.cam_pos_x - self.cam_width / 2) / self.tile_width )
        right = int( (self.cam_pos_x + self.cam_width / 2) / self.tile_width )
        top = int( (self.cam_pos_y - self.cam_height / 2) / self.tile_height )
        bottom = int( (self.cam_pos_y + self.cam_height / 2) / self.tile_height )

        if( tile.x < left or tile.x > right or tile.y < top or tile.y > bottom ):
            return False
        return True

    def getNumberOfEntity(self, type):
        spawn_layer = self.sprite_layers[4]
        count = 0
        for y in range( len( spawn_layer.content2D ) ):
            for x in range (len (spawn_layer.content2D[y] ) ):
                if spawn_layer.content2D[y][x] is not None:
                    if spawn_layer.content2D[y][x].key[0] == type:
                        count += 1
        return count
    
    def getNumberOfMice(self):
        spawn_layer = self.sprite_layers[4]
        count = 0
        for y in range( len( spawn_layer.content2D ) ):
            for x in range (len (spawn_layer.content2D[y] ) ):
                if spawn_layer.content2D[y][x] is not None:
                    if spawn_layer.content2D[y][x].key[0] == spawn_type['miceleft'] or spawn_layer.content2D[y][x].key[0] == spawn_type['miceright'] \
                        or spawn_layer.content2D[y][x].key[0] == spawn_type['shootmiceleft'] or spawn_layer.content2D[y][x].key[0] == spawn_type['shootmiceright']:
                        count += 1
        return count

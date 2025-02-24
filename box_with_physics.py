import pygame
import math
import time
import sys

frequency = 1/120
cursor_mass = 0.7
window_width = 1400
window_height = 800
pixels_in_a_meter = 100

block_position = [2,1.5]
block_velocity = [0,0]
block_rotation = (math.pi/4+0.2)*0
block_angular_velocity = 0
block_size = [2,2]
block_mass = 10

ground_position = [7, 0.5]
ground_size =[14, 1]

def rotate_vector(vector, theta):
    return [vector[0]*math.cos(theta)-vector[1]*math.sin(theta), vector[0]*math.sin(theta)+vector[1]*math.cos(theta)]

def vector_projection_of_a_onto_b(a, b):
    scalar = (a[0]*b[0]+a[1]*b[1])/(b[0]*b[0]+b[1]*b[1])
    return [scalar*b[0], scalar*b[1]]

def normalize_vector(vector):
    length = math.sqrt(vector[0]**2+vector[1]**2)
    return [vector[0]/length, vector[1]/length]

def get_axis(theta):
    return normalize_vector(rotate_vector([1,0], theta)), normalize_vector(rotate_vector([0,1], theta))

def get_corners(rect_pos, rect_size, rect_rot):
    rect_axis = get_axis(rect_rot)
    corners = []

    for corner_i in [-1,1]:
        for corner_j in [-1,1]:
            corner = [rect_pos[0] + rect_axis[0][0]*corner_i * rect_size[0]/2 + rect_axis[1][0]*corner_j*rect_size[1]/2, rect_pos[1] + rect_axis[0][1]*corner_i * rect_size[0]/2 + rect_axis[1][1]*corner_j*rect_size[1]/2]
            corners.append(corner)

    return corners

def projection_collision(rect_pos, rect_size, rect_rot, on_rect_pos, on_rect_size, on_rect_rot, surface):
    on_rect_axis = get_axis(on_rect_rot)

    for axis in range(2):
        minimum_distance = None
        maximum_distance = None

        half_on_rect_size = on_rect_size[axis] / 2

        for corner in get_corners(rect_pos, rect_size, rect_rot):
            line_to_corner = [corner[0] - on_rect_pos[0], corner[1] - on_rect_pos[1]]

            projection_of_vector_onto_axis = vector_projection_of_a_onto_b(line_to_corner, on_rect_axis[axis])

            positive_direction = projection_of_vector_onto_axis[0]*on_rect_axis[axis][0] + projection_of_vector_onto_axis[1]*on_rect_axis[axis][1] > 0
            
            sign = 1
            if not(positive_direction):
                sign = -1

            projection_distance = math.sqrt(projection_of_vector_onto_axis[0]**2 + projection_of_vector_onto_axis[1]**2)
            signed_projection_distance = projection_distance*sign

            if (not(minimum_distance) or signed_projection_distance < minimum_distance):
                minimum_distance = signed_projection_distance
            
            if (not(maximum_distance) or signed_projection_distance > maximum_distance):
                maximum_distance = signed_projection_distance
        
    if not(minimum_distance < 0 and maximum_distance > 0 or abs(minimum_distance) < half_on_rect_size or abs(maximum_distance) < half_on_rect_size):
        return False
    
    return True

def rectangle_collision(rect_pos, rect_size, rect_rot, on_rect_pos, on_rect_size, on_rect_rot, surface):
    return projection_collision(rect_pos, rect_size, rect_rot, on_rect_pos, on_rect_size, on_rect_rot, surface) and projection_collision(on_rect_pos, on_rect_size, on_rect_rot, rect_pos, rect_size, rect_rot, surface)

def is_point_inside_rectangle(point_x, point_y, pos, size, rot):
    # Translate point coordinates relative to the rectangle center
    translatedX = point_x - pos[0]
    translatedY = point_y - pos[1]
    
    # Rotate point coordinates to align with the rectangle's orientation
    cos_theta = math.cos(-rot)
    sin_theta = math.sin(-rot)
    rotatedX = translatedX * cos_theta - translatedY * sin_theta
    rotatedY = translatedX * sin_theta + translatedY * cos_theta
    
    # Check if the point is within the rectangle bounds
    if -size[0] / 2 <= rotatedX <= size[0] / 2 and -size[1] / 2 <= rotatedY <= size[1] / 2:
        return True  # Point is hovering over the rectangle
    return False

def line_equation(x1,y1,x2,y2):
    A, B, C = (0,0,0)

    if x1 == x2:
        A=1
        B=0
        C=-x1
    else:
        m = (y2-y1)/(x2-x1)
        A=m
        B=-1
        C=y1-m*x1

    return A, B, C

def cursor_collision(last_cursor_position, cursor_position):
    cursor_acceleration = [(cursor_position[0] - last_cursor_position[0]) / frequency**2, (cursor_position[1] - last_cursor_position[1]) / frequency**2]
    cursor_force = [cursor_acceleration[0]*cursor_mass, cursor_acceleration[1]*cursor_mass]

    net_force = [0,0]
    torque = 0
    
    block_corners = []

    for corner in [[-1,1],[1,1],[1,-1],[-1,-1]]:
        corner_relative_position = [corner[0]*block_size[0]/2, corner[1]*block_size[1]/2]
        corner_relative_position_rotated = [0,0]
        corner_relative_position_rotated[0] = corner_relative_position[0]*math.cos(block_rotation)-corner_relative_position[1]*math.sin(block_rotation)
        corner_relative_position_rotated[1] = corner_relative_position[0]*math.sin(block_rotation)+corner_relative_position[1]*math.cos(block_rotation)
        corner_position = [block_position[0] + corner_relative_position_rotated[0], block_position[1] + corner_relative_position_rotated[1]]
        block_corners.append(corner_position)

    if is_point_inside_rectangle(cursor_position[0], cursor_position[1], block_position, block_size, block_rotation):
        minimum_distance = None
        border_A, border_B, border_C = (0,0,0)

        for i in range(4):
            corner = i
            next_corner = (i + 1) % 4
            
            A, B, C = line_equation(block_corners[corner][0], block_corners[corner][1], block_corners[next_corner][0], block_corners[next_corner][1])

            distance = abs(A*cursor_position[0]+B*cursor_position[1]+C)/math.sqrt(A**2+B**2)

            if minimum_distance == None or distance < minimum_distance:
                minimum_distance = distance
                
                border_A=A
                border_B=B
                border_C=C
        
        A,B,C = line_equation(cursor_position[0], cursor_position[1], cursor_position[0] + cursor_force[0], cursor_position[1] + cursor_force[1])

        if (A*border_B-border_A*B) != 0 and (A*border_B-border_A*B) != 0:
            point_of_intersection = [(B*border_C-border_B*C)/(A*border_B-border_A*B), (C*border_A-border_C*A)/(A*border_B-border_A*B)]

            if is_point_inside_rectangle(point_of_intersection[0], point_of_intersection[1], block_position, block_size, block_rotation):
                r = [point_of_intersection[0]-block_position[0], point_of_intersection[1]-block_position[1], 0]
                distance_from_block_center = math.sqrt(r[0]**2 + r[1]**2)

                # Angle between force and border
                if (A*border_A+B*border_B) != 0:
                    net_force = cursor_force
                    cursor_force = [cursor_force[0], cursor_force[1], 0]

                    torque = cross_product(r, cursor_force)[2]

    return net_force, torque

def cross_product(A, B):
    return [
        A[1] * B[2] - A[2] * B[1],
        A[2] * B[0] - A[0] * B[2],
        A[0] * B[1] - A[1] * B[0]
    ]

def friction_torque(width,height,mass, rotation_angle_rad, velocity):
    rotation_angle_rad = rotation_angle_rad % (math.pi/2)

    friction_force = -velocity[0]*0.7*9.8*block_mass/abs(velocity[0])
    distance = math.sqrt((width/2)**2+(height/2)**2)
    torque = distance*friction_force*math.sin(rotation_angle_rad)

    return torque



def normal_torque(width, height, mass, rotation_angle_rad):
    rotation_angle_rad = rotation_angle_rad % (math.pi/2)
    
    distance = math.sqrt((width/2)**2+(height/2)**2)
    force = -9.8*mass
    angle=(math.pi/4)-rotation_angle_rad
    torque = distance*force*math.sin(angle)

    return torque



pygame.init()
next_time = 0
last_cursor_position = pygame.mouse.get_pos()
surface = pygame.display.set_mode((window_width,window_height))
  
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if time.perf_counter() > next_time:
        surface.fill((255,255,255))

        next_time = time.perf_counter() + frequency

        cursor_screen_position = pygame.mouse.get_pos()
        cursor_position = (cursor_screen_position[0] / pixels_in_a_meter, (window_height-cursor_screen_position[1]) / pixels_in_a_meter)
        cursor_acceleration = [(cursor_position[0] - last_cursor_position[0]) / frequency**2, (cursor_position[1] - last_cursor_position[1]) / frequency**2]

        net_force_from_cursor, torque_from_cursor = cursor_collision(last_cursor_position, cursor_position)
        last_cursor_position = cursor_position

        net_force = [net_force_from_cursor[0], net_force_from_cursor[1]-9.8*block_mass]

        block_position[1] -= 1/pixels_in_a_meter

        _friction_torque = 0

        if (block_velocity[0] != 0) and rectangle_collision(ground_position, ground_size, 0, block_position, block_size, block_rotation,surface):
            friction = 0.7*9.8*block_mass

            sign = 0
            if block_velocity[0] != 0:
                sign = block_velocity[0]/abs(block_velocity[0])
            else:
                sign = net_force[0]/abs(net_force[0])

            friction = -friction*sign
            net_force[0] += friction
            _friction_torque = friction_torque(block_size[0], block_size[1], block_mass, block_rotation, block_velocity)

        gravity_torque = normal_torque(block_size[0], block_size[1],block_mass,block_rotation)

        net_torque = torque_from_cursor + gravity_torque + _friction_torque
        angular_acceleration = net_torque/((1/12)*block_mass*(block_size[0]**2+block_size[1]**2))

        previous_block_rotation_above_ground = block_rotation % (math.pi/2)

        block_angular_velocity += angular_acceleration * frequency
        block_angular_velocity=block_angular_velocity*(1-5*frequency)

        block_rotation += block_angular_velocity * frequency
        block_rotation_above_ground = block_rotation % (math.pi/2)

        block_position[1] += 1/pixels_in_a_meter

        block_acceleration = [net_force[0]/block_mass, net_force[1]/block_mass]
        
        block_velocity[0] += block_acceleration[0] * frequency
        block_velocity[1] += block_acceleration[1] * frequency

        block_position[0] += block_velocity[0] * frequency
        block_position[1] += block_velocity[1] * frequency

        block_position[0] = max(min(block_position[0], -0.5+window_width/pixels_in_a_meter),0.5)

        block_image = pygame.Surface((pixels_in_a_meter*block_size[0],pixels_in_a_meter*block_size[1]))
        block_image.set_colorkey((0,0,0))
        block_image.fill((0,0,255))
        block_image = pygame.transform.rotate(block_image, (block_rotation * 360 / (2*math.pi))%360)

        pygame.draw.rect(surface, (255,0,0), pygame.Rect(pixels_in_a_meter*(ground_position[0]-ground_size[0]/2), window_height - pixels_in_a_meter*(ground_position[1]+ground_size[1]/2), pixels_in_a_meter*ground_size[0], pixels_in_a_meter*ground_size[1]))

        x_offset = 0
        y_offset = 0

        for corner in get_corners(block_position, block_size, block_rotation):
            relative_corner_position = [corner[0]-block_position[0], corner[1]-block_position[1]]
            if relative_corner_position[0] < x_offset:
                x_offset = relative_corner_position[0]
            
            if relative_corner_position[1] > y_offset:
                y_offset = relative_corner_position[1]
        
        surface.blit(block_image, (pixels_in_a_meter*(block_position[0]+x_offset), window_height - (block_position[1]+y_offset)*pixels_in_a_meter))

        while(rectangle_collision(ground_position, ground_size, 0, block_position, block_size, block_rotation, surface)):
            block_velocity[1] = 0
            block_position[1] += 0.001

        pygame.display.flip()
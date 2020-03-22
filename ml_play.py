"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
        else:
            ball_x = scene_info.ball[0]
            ball_y = scene_info.ball[1]
            platform_x = scene_info.platform[0]
            platform_y = scene_info.platform[1]
            ball_next = scene_info.ball[0]
            ball_hit = False
            if ball_x == 0 and ball_y >= 200:
                ball_next = 0 + platform_y - ball_y
                ball_hit = True
            elif ball_x == 200 and ball_y >= 200:
                ball_next = 200 - (platform_y - ball_y)
                ball_hit = True
            if ball_next > platform_x and ball_hit == True:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            elif ball_next < platform_x and ball_hit == True:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            else :
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            """
            ball_x = scene_info.ball[0]
            platform_x = scene_info.platform[0]
            if ball_x > platform_x :
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            elif ball_x < platform_x :
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            else :
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            """
            
            

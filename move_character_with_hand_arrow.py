from pico2d import *
import time
import math

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)

TUK_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
hand = load_image('hand_arrow.png')

def handle_events():
    global running
    global character_x, character_y, hand_x, hand_y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            hand_x, hand_y = event.x, TUK_HEIGHT - 1 - event.y

def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

running = True
character_x, character_y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0
hide_cursor()

hand_x, hand_y = -100, -100  # 초기화 시 화면 밖에 위치

prev_time = time.time()

while running:
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)

    # 화살표와 캐릭터 간의 거리 계산
    distance = get_distance(character_x, character_y, hand_x, hand_y)

    # 캐릭터 이동
    move_x, move_y = 0, 0
    if character_x < hand_x:
        move_x = 1
    elif character_x > hand_x:
        move_x = -1
    if character_y < hand_y:
        move_y = 1
    elif character_y > hand_y:
        move_y = -1

    # 대각선으로 이동
    character_x += move_x
    character_y += move_y

    if move_x != 0 or move_y != 0:
        if move_x > 0:
            character.clip_draw(frame * 100, 100 * 1, 100, 100, character_x, character_y)
        else:
            character.clip_composite_draw(frame * 100, 100 * 1, 100, 100, 0, 'h', character_x, character_y, 100, 100)
    else:
        character.clip_composite_draw(frame * 100, 100 * 1, 100, 100, 0, 'h', character_x, character_y, 100, 100)

    if distance < 10.0:
        # 화살표가 캐릭터에 도달하면 위치 초기화
        hand_x, hand_y = -100, -100

    update_canvas()
    frame = (frame + 1) % 8

    handle_events()

close_canvas()

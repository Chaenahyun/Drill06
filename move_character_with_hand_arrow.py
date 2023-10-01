from pico2d import *
import time
import math

# 화면 크기 설정
TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)

# 이미지 로드
TUK_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
hand = load_image('hand_arrow.png')

def handle_events():
    global running
    global character_x, character_y
    global arrow_list, move_arrow_x, move_arrow_y

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            move_arrow_x, move_arrow_y = event.x, TUK_HEIGHT - 1 - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            # 화살표 리스트에 클릭한 위치 추가
            arrow_list.append((event.x, TUK_HEIGHT - 1 - event.y))

def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# 초기화
running = True
character_x, character_y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0

# 커서 이미지 로드 및 초기화
cursor_image = load_image('hand_arrow.png')
hand_x, hand_y = TUK_WIDTH // 2, TUK_HEIGHT // 2
arrow_list = []
move_arrow_x, move_arrow_y = hand_x, hand_y
prev_time = time.time()
move_x, move_y = 0, 0

while running:
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)

    for arrow_x, arrow_y in arrow_list:
        hand.draw(arrow_x, arrow_y)

    # 커서 이미지를 마우스 위치 그리기
    cursor_image.draw(move_arrow_x, move_arrow_y)
    hand_x, hand_y = move_arrow_x, move_arrow_y

    if arrow_list:
        target_x, target_y = arrow_list[0]
        distance = get_distance(character_x, character_y, target_x, target_y)
        if character_x < target_x:
            move_x = 1
        elif character_x > target_x:
            move_x = -1
        else:
            move_x = 0
        if character_y < target_y:
            move_y = 1
        elif character_y > target_y:
            move_y = -1
        else:
            move_y = 0
        character_x += move_x
        character_y += move_y
        if distance < 10.0:
            arrow_list.pop(0)

    if move_x != 0 or move_y != 0:
        if move_x > 0:
            character.clip_draw(frame * 100, 100 * 1, 100, 100, character_x, character_y)
        else:
            character.clip_composite_draw(frame * 100, 100 * 1, 100, 100, 0, 'h', character_x, character_y, 100, 100)
    else:
        character.clip_composite_draw(frame * 100, 100 * 1, 100, 100, 0, 'h', character_x, character_y, 100, 100)

    update_canvas()
    frame = (frame + 1) % 8

    handle_events()

close_canvas()

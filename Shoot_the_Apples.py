import os
import pygame

pygame.init()

# 화면 크기 설정
screen_width = 880  # 가로
screen_height = 650  # 세로
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Shoot the Apples!!")

# FPS
clock = pygame.time.Clock()
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

# 배경 이미지
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 캐릭터 불러오기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size  # 이미지 크기
character_width = character_size[0]  # 가로
character_height = character_size[1]  # 세로
character_x_pos = (screen_width / 2) - (character_width / 2)  # 화면 가로 절반 크기
character_y_pos = screen_height - character_height  # 화면 가장 아래에

# 이동할 좌표
to_x = 0
to_y = 0

character_speed = 0.4

# 무기
arrow = pygame.image.load(os.path.join(image_path, "arrow.png"))
arrow_size = arrow.get_rect().size
arrow_width = arrow_size[0]

arrows = []

arrow_speed = 15

# 사과 이미지 및 속도
apple_images = [
    pygame.image.load(os.path.join(image_path, "apple1.png")),
    pygame.image.load(os.path.join(image_path, "apple2.png")),
    pygame.image.load(os.path.join(image_path, "apple3.png"))
]

apple_speed_y = [-15, -11, -8]

# 사과 객체 리스트
apples = []

apples.append({
    "pos_x": 50,
    "pos_y": 50,
    "img_idx": 0,
    "to_x": 3,
    "to_y": apple_speed_y[0],
    "init_spd_y": apple_speed_y[0]
})

# 폰트 정의
game_font = pygame.font.Font(None, 40)
#게임 종료 메시지
game_result = "Game Over"

# 총 시간
total_time = 100
# 시작 시간
start_ticks = pygame.time.get_ticks()


# 이벤트 루프
running = True
while running:
    dt = clock.tick(60)  # 프레임 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
            elif event.key == pygame.K_SPACE:
                arrow_x_pos = character_x_pos + (character_width / 2) - (arrow_width / 2)
                arrow_y_pos = character_y_pos
                arrows.append([arrow_x_pos, arrow_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

    character_x_pos += to_x * dt
    character_y_pos += to_y * dt

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    arrows = [[a[0], a[1] - arrow_speed] for a in arrows]
    arrows = [[a[0], a[1]] for a in arrows if a[1] > 0]

    # 사과 위치 정의
    for apple_idx, apple_val in enumerate(apples):
        apple_pos_x = apple_val["pos_x"]
        apple_pos_y = apple_val["pos_y"]
        apple_img_idx = apple_val["img_idx"]

        apple_size = apple_images[apple_img_idx].get_rect().size
        apple_width = apple_size[0]
        apple_height = apple_size[1]

        if apple_pos_x < 0 or apple_pos_x > screen_width - apple_width:
            apple_val["to_x"] = apple_val["to_x"] * -1

        if apple_pos_y < 0:  # 사과가 천장에 닿으면
            apple_val["to_y"] = apple_val["to_y"] * -1 # Y축 속도 반전

        if apple_pos_y >= screen_height - apple_height:
            apple_val["to_y"] = apple_val["init_spd_y"]
        else:
            apple_val["to_y"] += 0.1

        apple_val["pos_x"] += apple_val["to_x"]
        apple_val["pos_y"] += apple_val["to_y"]

    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    # 충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for apple_idx, apple_val in enumerate(apples):
        apple_pos_x = apple_val["pos_x"]
        apple_pos_y = apple_val["pos_y"]
        apple_img_idx = apple_val["img_idx"]

        apple_rect = apple_images[apple_img_idx].get_rect()
        apple_rect.left = apple_pos_x
        apple_rect.top = apple_pos_y

        if character_rect.colliderect(apple_rect):
            # 사과와 캐릭터가 일정 범위 이상 겹칠 때만 충돌로 처리
            overlap_rect = character_rect.clip(apple_rect)
            if overlap_rect.width * overlap_rect.height > (character_width * character_height * 0.25):  # 겹치는 영역이 전체 영역의 25% 이상일 때
                running = False
                break

    # 무기와 사과 삭제
    arrows_to_remove = -1
    apples_to_remove = -1

    for arrow_idx, arrow_val in enumerate(arrows):
        arrow_x_pos = arrow_val[0]
        arrow_y_pos = arrow_val[1]

        arrow_rect = arrow.get_rect()
        arrow_rect.left = arrow_x_pos
        arrow_rect.top = arrow_y_pos

        for apple_idx, apple_val in enumerate(apples):
            apple_pos_x = apple_val["pos_x"]
            apple_pos_y = apple_val["pos_y"]
            apple_img_idx = apple_val["img_idx"]

            apple_rect = apple_images[apple_img_idx].get_rect()
            apple_rect.left = apple_pos_x
            apple_rect.top = apple_pos_y

            if arrow_rect.colliderect(apple_rect):
                arrows_to_remove = arrow_idx
                apples_to_remove = apple_idx

                if apple_img_idx <len(apple_images) - 1:
                    apple_width = apple_rect.size[0]
                    apple_height = apple_rect.size[1]

                    small_apple_rect = apple_images[apple_img_idx +1].get_rect()
                    small_apple_width = small_apple_rect.size[0]
                    small_apple_height = small_apple_rect.size[1]
            
                    #왼쪽으로 튕겨
                    apples.append({
                        "pos_x": apple_pos_x + (apple_width / 2) - (small_apple_width / 2),
                        "pos_y": apple_pos_y + (apple_height / 2) - (small_apple_height /2),
                        "img_idx": apple_img_idx + 1,
                        "to_x": -3,
                        "to_y": apple_speed_y[0],
                        "init_spd_y": apple_speed_y[apple_img_idx+1] })
                    
                    #오른쪽으로 튕겨
                    apples.append({
                        "pos_x": apple_pos_x + (apple_width / 2) - (small_apple_width / 2),
                        "pos_y": apple_pos_y + (apple_height / 2) - (small_apple_height /2),
                        "img_idx": apple_img_idx + 1,
                        "to_x": 3,
                        "to_y": apple_speed_y[0],
                        "init_spd_y": apple_speed_y[apple_img_idx+1] })
                break

        if arrows_to_remove != -1:
            del arrows[arrows_to_remove]
            arrows_to_remove = -1

        if apples_to_remove != -1:
            del apples[apples_to_remove]
            apples_to_remove = -1

        if len(apples) == 0:
            game_result = "Mission Complete"
            running = False

    screen.blit(background, (0, 0))  # 배경 그리기

    for arrow_x_pos, arrow_y_pos in arrows:
        screen.blit(arrow, (arrow_x_pos, arrow_y_pos))

    for idx, val in enumerate(apples):
        apple_pos_x = val["pos_x"]
        apple_pos_y = val["pos_y"]
        apple_img_idx = val["img_idx"]
        screen.blit(apple_images[apple_img_idx], (apple_pos_x, apple_pos_y))

    screen.blit(character, (character_x_pos, character_y_pos))  # 캐릭터 그리기

    # 타이머
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (0, 0, 0))
    screen.blit(timer, (10, 10))

    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()  # 게임 화면 다시 그리기!

msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000)

# pygame 종료
pygame.quit()

import pygame
import sys
import math
import random

# ******************** 画像の読み込み ********************
img_title_board = pygame.image.load("image/title_board.png")
img_text = [
    pygame.image.load("image/klask.png"),
    pygame.image.load("image/easy.png"),
    pygame.image.load("image/normal.png"),
    pygame.image.load("image/hard.png"),
    pygame.image.load("image/flick_off.png"),
    pygame.image.load("image/score_goal.png"),
    pygame.image.load("image/score_double_biscuit.png"),
    pygame.image.load("image/score_klask.png"),
    pygame.image.load("image/you_win.png"),
    pygame.image.load("image/you_lose.png"),
    pygame.image.load("image/how_to_play.png"),
    pygame.image.load("image/next.png"),
    pygame.image.load("image/back.png"),
    pygame.image.load("image/title.png")
]
img_board = pygame.image.load("image/board.png")
img_hole = pygame.image.load("image/hole.png")
img_striker = [
    pygame.image.load("image/striker_0.png"),
    pygame.image.load("image/striker_1.png"),
    pygame.image.load("image/striker_2.png"),
    pygame.image.load("image/striker_3.png")
]
img_ball = pygame.image.load("image/ball.png")
img_biscuit = pygame.image.load("image/biscuit.png")
img_power_bar = pygame.image.load("image/power_bar.png")
img_rule = [
    None,
    pygame.image.load("image/rule_1.png"),
    pygame.image.load("image/rule_2.png"),
    pygame.image.load("image/rule_3.png"),
    pygame.image.load("image/rule_4.png"),
    pygame.image.load("image/rule_5.png"),
    pygame.image.load("image/rule_6.png"),
    pygame.image.load("image/rule_7.png"),
    pygame.image.load("image/rule_8.png")
]

# ******************** 効果音 ********************
snd_smash = None        # スマッシュの音
snd_collision = None    # ボールとビスケットが当たった音
snd_bound = None        # ボールが壁に当たった音
snd_stick = None        # ビスケットがストライカーにひっついた音
snd_point_pl = None     # プレイヤーの得点時の音
snd_point_com = None    # コンピュータの得点時の音
snd_pl_win = None       # プレイヤーの勝利
snd_pl_lose = None      # プレイヤーの負け

# ******************** 変数／定数 ********************
# =============== COLOR ===============
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# =============== SIZE ===============
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000
SCREEN_SCORE_BOARD = 100
BOARD_HEIGHT_CENTER = (SCREEN_HEIGHT-SCREEN_SCORE_BOARD)/2+SCREEN_SCORE_BOARD
# =============== GAME ===============
idx = 0     # ゲームの状態管理
tmr = 0     # タイマー
level = 0   # コンピュータのレベル

power_set = False   # フリックオフのパワーセット
power_gauge = 0     # フリックオフのパワーゲージ

COMPUTER = 0    # コンピュータのインデックス
PLAYER = 1      # プレイヤーのインデックス
turn = [False, False]   # ターンのトリガー(0:OFF/1:ON)
goal = [0, 0]   # ゴール時にフリックの点滅

point_pl = 0    # プレイヤーの得点
point_com = 0   # コンピュータの得点
POINT_WIN = 6   # ゲームの決着時のポイント
text_goal = 0   # ゴール内容(5~7)
POWER = 3       # ボールを弾くパワー
E = 1           # 反発係数
# =============== PLAYER ===============
pl_x = 0    # x座標
pl_y = 0    # y座標
pl_vx = 0   # x方向の速度(移動量)
pl_vy = 0   # y方向の速度(移動量)
pl_bis= 0   # ついているビスケットの数
# =============== COMPUTER ===============
com_x = 0   # x座標
com_y = 0   # y座標
com_vx = 0  # x方向の速度(移動量)
com_vy = 0  # y方向の速度(移動量)
com_a = 0   # 角度(°)
com_bis = 0 # ついているビスケットの数
# =============== BALL ===============
BALL_MASS = 5   # 質量
ball_x = 0      # x座標
ball_y = 0      # y座標
ball_vx = 0     # x方向の速度(移動量)
ball_vy = 0     # y方向の速度(移動量)
# =============== BISCUIT ===============
BISCUIT_NUM = 3             # ビスケットの数
BISCUIT_MASS = 1            # 質量
BISCUIT_POWER = 5           # ビスケットパワー
bis_f = [True]*BISCUIT_NUM  # ストライカーについていないビスケット
bis_x = [0]*BISCUIT_NUM     # x座標
bis_y = [0]*BISCUIT_NUM     # y座標
bis_vx = [0]*BISCUIT_NUM    # x方向の速度(移動量)
bis_vy = [0]*BISCUIT_NUM    # y方向の速度(移動量)
bis_a = [0]*BISCUIT_NUM     # 角度(°)
# =============== HOLE ===============
HOLE_COM_X = 120                        # コンピュータ側の穴のx座標
HOLE_PL_X = SCREEN_WIDTH - HOLE_COM_X   # プレイヤー側の穴のx座標
HOLE_Y = BOARD_HEIGHT_CENTER            # 穴のy座標
# =============== FLICK ===============
FLICK_MASS = 1  # 質量
FLICK_Y = 50    # y座標
flick_pl_x = 0  # x座標：プレイヤー
flick_pl_v = 0  # 速度(移動量)：プレイヤー
flick_com_x = 0 # x座標：コンピュータ
flick_com_v = 0 # 速度(移動量)：コンピュータ


# ============================================================
#                           DRAW
# ============================================================

# ******************** 文字の表示 ********************
def draw_text(sc, txt, x, y, siz, col):
    fnt = pygame.font.Font(None, siz)
    sur = fnt.render(txt, True, col)
    # 中央揃え
    x = x - sur.get_width()/2
    y = y - sur.get_height()/2
    # 文字表示
    sc.blit(sur, [x, y])


# ******************** ボードの表示 ********************
def draw_board(sc):
    # 画像：テーブル／ホール
    sc.blit(img_board, [0, SCREEN_SCORE_BOARD])
    sc.blit(img_hole, [HOLE_COM_X - img_hole.get_width()/2, HOLE_Y - img_hole.get_height()/2])
    sc.blit(img_hole, [HOLE_PL_X - img_hole.get_width()/2, HOLE_Y - img_hole.get_height()/2])

    # 点数表示
    for i in range(2):
        if goal[i] > 0:
            goal[i] -= 1
    # フリック表示(得点時 -> フリックが点滅)
    if goal[0]%10 < 5:
        pygame.draw.circle(sc, BLUE, [SCREEN_WIDTH/2-(80+point_com*100), FLICK_Y], 35)
    if goal[1]%10 < 5:
        pygame.draw.circle(sc, BLUE, [SCREEN_WIDTH/2+(80+point_pl*100), FLICK_Y], 35)
    # スコアボードの数字表示
    for i in range(0, 7):
        draw_text(sc, str(i), (SCREEN_WIDTH/2)-(80+i*100), SCREEN_SCORE_BOARD/2, 50, WHITE)
        draw_text(sc, str(i), (SCREEN_WIDTH/2)+(80+i*100), SCREEN_SCORE_BOARD/2, 50, WHITE)

    # 画像：ビスケット／ボール
    for i in range(BISCUIT_NUM):
        if bis_f[i] == True:
            sc.blit(img_biscuit, [bis_x[i]-img_biscuit.get_width()/2, bis_y[i]-img_biscuit.get_height()/2])
    sc.blit(img_ball, [ball_x-img_ball.get_width()/2, ball_y-img_ball.get_height()/2])

    # 画像：ストライカー(プレイヤー／コンピュータ)
    sc.blit(img_striker[pl_bis], [pl_x-img_striker[pl_bis].get_width()/2, pl_y-img_striker[pl_bis].get_height()/2])
    sc.blit(img_striker[com_bis], [com_x-img_striker[com_bis].get_width()/2, com_y-img_striker[com_bis].get_height()/2])


# ============================================================
#                       PLAYER / COMPUTER
# ============================================================

# ******************** プレイヤーのストライカー ********************
def striker_player(mx, my):
    global idx, tmr, text_goal, point_com
    global pl_x, pl_y, pl_vx, pl_vy

    # 速度(移動量)／座標
    pl_vx = mx - pl_x
    pl_vy = my - pl_y
    pl_x = mx
    pl_y = my
    # 移動(座標)制限
    if pl_x < SCREEN_WIDTH/2 + img_striker[pl_bis].get_width()/2:
        pl_x = SCREEN_WIDTH/2 + img_striker[pl_bis].get_width()/2
    if pl_x > SCREEN_WIDTH - img_striker[pl_bis].get_width()/2:
        pl_x = SCREEN_WIDTH - img_striker[pl_bis].get_width()/2
    if pl_y < SCREEN_SCORE_BOARD + img_striker[pl_bis].get_height()/2:
        pl_y = SCREEN_SCORE_BOARD + img_striker[pl_bis].get_height()/2
    if pl_y > SCREEN_HEIGHT - img_striker[pl_bis].get_height()/2:
        pl_y = SCREEN_HEIGHT - img_striker[pl_bis].get_height()/2
    # 自陣の穴に落ちる
    if get_dis(HOLE_PL_X, HOLE_Y, pl_x, pl_y) < img_hole.get_width()/2 * img_hole.get_height()/2:
        snd_point_com.play()
        point_com += 1
        turn[PLAYER] = True
        goal[COMPUTER] = 60
        text_goal = 7
        idx = 3
        tmr = 0


# ******************** コンピュータのストライカー ********************
def striker_computer():
    global idx, tmr, text_goal, point_pl
    global com_x, com_y, com_vx, com_vy, com_a

    # 移動量
    dots = 20 + level * 10
    # 移動前の座標
    x = com_x
    y = com_y
    # ボールとコンピュータの距離 -> 角度の算出
    x_dis = ball_x - com_x
    y_dis = ball_y - com_y
    com_a = math.degrees(math.atan2(y_dis, x_dis))
    
    # ボールと接触 -> ボールから離れる
    if get_dis(com_x, com_y, ball_x, ball_y) < 50**2:
        if com_y < ball_y:
            com_y -= dots
        if com_y > ball_y:
            com_y += dots
        if com_x < ball_x:
            com_x -= dots
        if com_x > ball_x:
            com_x += dots
    # ボールの位置：コンピュータ エリア側 -> ボールに向かって移動
    elif ball_x <= SCREEN_WIDTH/2:
        move_x = com_x + dots*math.cos(math.radians(com_a))
        move_y = com_y + dots*math.sin(math.radians(com_a))
        com_x = move_x
        com_y = move_y            
    # ボールの位置：プレイヤー エリア側 -> 自陣のゴール前に移動
    else:
        com_x += ((120-img_hole.get_width()/2 + 150) - com_x) / (16-level*6)
        com_y += (BOARD_HEIGHT_CENTER - com_y) / (16-level*6)
        
    # 移動制限
    if com_x < img_striker[com_bis].get_width()/2:
        com_x = img_striker[com_bis].get_width()/2
    if com_x > SCREEN_WIDTH/2 - img_striker[com_bis].get_width()/2:
        com_x = SCREEN_WIDTH/2 - img_striker[com_bis].get_width()/2
    if com_y < SCREEN_SCORE_BOARD + img_striker[com_bis].get_height()/2:
        com_y = SCREEN_SCORE_BOARD + img_striker[com_bis].get_height()/2
    if com_y > SCREEN_HEIGHT - img_striker[com_bis].get_height()/2:
        com_y = SCREEN_HEIGHT - img_striker[com_bis].get_height()/2

    com_vx = com_x - x
    com_vy = com_y - y

    # 自陣の穴に落ちる
    if get_dis(HOLE_COM_X, HOLE_Y, com_x, com_y) < img_hole.get_width()/2 * img_hole.get_height()/2:
        snd_point_pl.play()
        point_pl += 1
        turn[COMPUTER] = True
        goal[PLAYER] = 60
        text_goal = 7
        idx = 3
        tmr = 0
        
# ============================================================
#                       BALL / BISCUIT
# ============================================================

# ******************** ボール ********************
def ball():
    global idx, tmr, text_goal, point_pl, point_com
    global ball_x, ball_y, ball_vx, ball_vy

    # ボールの半径
    ball_r = img_ball.get_width()/2
    # ボールの座標：ボールの速度(移動量)から計算
    ball_x += ball_vx
    ball_y += ball_vy
    
    # ボールがボードの端に当たった時
    if ball_y < SCREEN_SCORE_BOARD + ball_r and ball_vy < 0:    # ボード：下
        snd_bound.play()
        ball_vy = -ball_vy
    if ball_y > SCREEN_HEIGHT - ball_r and ball_vy > 0:         # ボード：上
        snd_bound.play()
        ball_vy = -ball_vy
    if ball_x < ball_r and ball_vx < 0:                         # ボード：左
        snd_bound.play()
        ball_vx = -ball_vx
    if ball_x > SCREEN_WIDTH - ball_r and ball_vx > 0:          # ボード：右
        snd_bound.play()
        ball_vx = -ball_vx
        
    # ボールの座標がボード外 -> ボードの端へ
    if ball_y < SCREEN_SCORE_BOARD + ball_r:    # ボード：下
        ball_y = SCREEN_SCORE_BOARD + ball_r
    if ball_y > SCREEN_HEIGHT - ball_r:         # ボード：上
        ball_y = SCREEN_HEIGHT - ball_r
    if ball_x < ball_r:                         # ボード：左
        ball_x = ball_r
    if ball_x > SCREEN_WIDTH - ball_r:          # ボード：右
        ball_x = SCREEN_WIDTH - ball_r
        
    # ボールの速度(移動量)：減速
    ball_vx *= 0.95
    ball_vy *= 0.95
    
    # 接触：プレイヤー／コンピュータ -> ボール
    if get_dis(ball_x, ball_y, pl_x, pl_y) < (img_ball.get_width()/2 + img_striker[pl_bis].get_width()/2)**2:   # ボールとプレイヤー
        snd_smash.play()
        ball_vx = pl_vx * POWER
        ball_vy = pl_vy * POWER
    if get_dis(ball_x, ball_y, com_x, com_y) < (img_ball.get_width()/2 + img_striker[com_bis].get_width()/2)**2: # ボールとコンピュータ
        snd_smash.play()
        ball_vx = com_vx * POWER
        ball_vy = com_vy * POWER
        
    # 得点：コンピュータ側の穴に入った場合 -> プレイヤー +1
    if get_dis(ball_x, ball_y, HOLE_COM_X, HOLE_Y) < (img_hole.get_width()/2 - 2) * (img_hole.get_height()/2 - 2): # ボールと穴
        ball_vx *= 0.5
        ball_vy *= 0.5
        if abs(ball_vx) < 1 and abs(ball_vy) < 1:
            snd_point_pl.play()
            point_pl += 1
            turn[COMPUTER] = True
            goal[PLAYER] = 60
            text_goal = 5
            idx = 3
            tmr = 0
    # 得点:プレイヤー側の穴に入った場合 -> コンピュータ +1
    if get_dis(ball_x, ball_y, HOLE_PL_X, HOLE_Y) < (img_hole.get_width()/2 - 2) * (img_hole.get_height()/2 - 2): # ボールと穴
        ball_vx *= 0.5
        ball_vy *= 0.5
        if abs(ball_vx) < 1 and abs(ball_vy) < 1:
            snd_point_com.play()
            point_com += 1
            turn[PLAYER] = True
            goal[COMPUTER] = 60
            text_goal = 5
            idx = 3
            tmr = 0

     
# ******************** ビスケット ********************
def biscuit():
    global idx, tmr, text_goal, point_pl, point_com
    global bis_x, bis_y, bis_vx, bis_vy, bis_a
    global ball_vx, ball_vy
    global pl_bis, com_bis
    
    # ビスケットの半径
    bis_r = img_biscuit.get_width()/2
    
    for i in range(BISCUIT_NUM):
        if bis_f[i] == True:
            # ビスケットの座標：ビスケットの速度(移動量)から計算
            bis_x[i] += bis_vx[i]
            bis_y[i] += bis_vy[i]
            
            # ビスケットがボードの端に当たった時
            if bis_y[i] < SCREEN_SCORE_BOARD + bis_r and bis_vy[i] < 0: # ボード：下
                bis_vy[i] = -bis_vy[i]
            if bis_y[i] > SCREEN_HEIGHT - bis_r and bis_vy[i] > 0:      # ボード：上
                bis_vy[i] = -bis_vy[i]
            if bis_x[i] < bis_r and bis_vx[i] < 0:                         # ボード：左
                bis_vx[i] = -bis_vx[i]
            if bis_x[i] > SCREEN_WIDTH - bis_r and bis_vx[i] > 0:          # ボード：右
                bis_vx[i] = -bis_vx[i]
                
            # ボールの座標がボード外 -> ボードの端へ
            if bis_y[i] < SCREEN_SCORE_BOARD + bis_r:  # ボード：下
                bis_y[i] = SCREEN_SCORE_BOARD + bis_r
            if bis_y[i] > SCREEN_HEIGHT - bis_r:       # ボード：上
                bis_y[i] = SCREEN_HEIGHT - bis_r
            if bis_x[i] < bis_r:                       # ボード：左
                bis_x[i] = bis_r
            if bis_x[i] > SCREEN_WIDTH - bis_r:        # ボード：右
                bis_x[i] = SCREEN_WIDTH - bis_r
                
            # ビスケットの速度(移動量)：減速
            bis_vx[i] *= 0.8
            bis_vy[i] *= 0.8
            
            # 接近：プレイヤーとビスケット
            if get_dis(bis_x[i], bis_y[i], pl_x, pl_y) < ((img_biscuit.get_width()/2 + BISCUIT_POWER*10) + img_striker[pl_bis].get_width()/2)**2:
                # プレイヤーとビスケットの距離 -> 角度の算出
                x_dis = pl_x - bis_x[i]
                y_dis = pl_y - bis_y[i]
                bis_a[i] = math.degrees(math.atan2(y_dis, x_dis))
                # 移動：プレイヤー方向
                bis_x[i] = bis_x[i] + BISCUIT_POWER * math.cos(math.radians(bis_a[i]))
                bis_y[i] = bis_y[i] + BISCUIT_POWER * math.sin(math.radians(bis_a[i]))                
                # 接触：プレイヤーとビスケット -> ビスケットがくっつく
                if get_dis(bis_x[i], bis_y[i], pl_x, pl_y) < (img_biscuit.get_width()/2 + img_striker[pl_bis].get_width()/2)**2:
                    snd_stick.play()
                    pl_bis += 1
                    bis_f[i] = False
                    if pl_bis >= 2:
                        snd_point_com.play()
                        point_com += 1
                        turn[PLAYER] = True
                        goal[COMPUTER] = 60
                        text_goal = 6
                        idx = 3
                        tmr = 0
                        
            # 接近：コンピュータとビスケット
            if get_dis(bis_x[i], bis_y[i], com_x, com_y) < ((img_biscuit.get_width()/2 + BISCUIT_POWER*10) + img_striker[pl_bis].get_width()/2)**2:
                # コンピュータとビスケットの距離 -> 角度の算出
                x_dis = com_x - bis_x[i]
                y_dis = com_y - bis_y[i]
                bis_a[i] = math.degrees(math.atan2(y_dis, x_dis))
                # 移動：コンピュータ方向
                bis_x[i] = bis_x[i] + BISCUIT_POWER * math.cos(math.radians(bis_a[i]))
                bis_y[i] = bis_y[i] + BISCUIT_POWER * math.sin(math.radians(bis_a[i]))
                # 接触：コンピュータとビスケット -> ビスケットがくっつく
                if get_dis(bis_x[i], bis_y[i], com_x, com_y) < (img_biscuit.get_width()/2 + img_striker[com_bis].get_width()/2)**2:
                    snd_stick.play()
                    com_bis += 1
                    bis_f[i] = False
                    if com_bis >= 2:
                        snd_point_pl.play()
                        point_pl += 1
                        turn[COMPUTER] = True
                        goal[PLAYER] = 60
                        text_goal = 6
                        idx = 3
                        tmr = 0
                        
            # 接触：ボールとビスケット -> ビスケットとボールがぶつかった時の速度を反発係数とエネルギー保存の法則から求める
            if get_dis(bis_x[i], bis_y[i], ball_x, ball_y) <= (img_biscuit.get_width()/2 + img_ball.get_width()/2)**2:
                snd_collision.play()
                # x,y方向の速度(移動量)：ボールとビスケット
                bis_vx[i], ball_vx = object_collision(BISCUIT_MASS, bis_vx[i], BALL_MASS, ball_vx)
                bis_vy[i], ball_vy = object_collision(BISCUIT_MASS, bis_vy[i], BALL_MASS, ball_vy)
            

# ============================================================
#                           CALC
# ============================================================

# ******************** 2点間の距離を求める  ********************
def get_dis(x1, y1, x2, y2):
    return (x1-x2)**2 + (y1-y2)**2


# ******************** 2物体の衝突 ********************
def object_collision(m1, v1, m2, v2):
    v1_ = ((m1-m2*E)*v1 + m2*(1+E)*v2) / (m1+m2)
    v2_ = (m1*(1+E)*v1 + (-m1*E+m2)*v2) / (m1+m2)
    return v1_, v2_


# ============================================================
#                           GAME
# ============================================================

# ******************** フリックオフ ********************
def flick_off(sc, key):
    global power_gauge, power_set
    global flick_pl_x, flick_pl_v, flick_com_x, flick_com_v

    # 画像：テーブル／ホール
    sc.blit(img_board, [0, SCREEN_SCORE_BOARD])
    sc.blit(img_hole, [HOLE_COM_X - img_hole.get_width()/2, HOLE_Y - img_hole.get_height()/2])
    sc.blit(img_hole, [HOLE_PL_X - img_hole.get_width()/2, HOLE_Y - img_hole.get_height()/2])

    # スペースキーの押し待ち
    if power_set == False:
        if key[pygame.K_SPACE] == 1:
            # パワーゲージ
            power_gauge = tmr%21
            # フリックの速度：プレイヤーとコンピューター
            flick_pl_v = -power_gauge * 5
            flick_com_v = random.randint(50, 100)
            power_set = True
            
    # スペースキーを押した後
    if power_set == True:
        # x方向の位置
        flick_pl_x += flick_pl_v
        flick_com_x += flick_com_v
        # 減速
        flick_pl_v *= 0.9
        flick_com_v *= 0.9
        # 速度0の判定
        if abs(flick_pl_v) < 0.1:
            flick_pl_v = 0
        if abs(flick_com_v) < 0.1:
            flick_com_v = 0

        # 衝突判定
        if get_dis(flick_pl_x, FLICK_Y, flick_com_x, FLICK_Y) <= 35**2:
            flick_pl_v, flick_com_v = object_collision(FLICK_MASS, flick_pl_v, FLICK_MASS, flick_com_v)
            
        # 画像：パワーゲージ
        sc.blit(img_power_bar, [SCREEN_WIDTH/2 - img_power_bar.get_width()/2, BOARD_HEIGHT_CENTER - img_power_bar.get_height()/2])
        pygame.draw.rect(sc, (64,32,32), [400, 500, 800-power_gauge*40, 100])
    # スペースキーを押す前
    else:
        # 画像：パワーゲージ
        sc.blit(img_power_bar, [SCREEN_WIDTH/2 - img_power_bar.get_width()/2, BOARD_HEIGHT_CENTER - img_power_bar.get_height()/2])
        pygame.draw.rect(sc, (64,32,32), [400, 500, 800-(tmr%21)*40, 100])

    # フリック表示：プレイヤーとコンピュータ
    pygame.draw.circle(sc, BLUE, [flick_com_x, FLICK_Y], 35) # コンピュータ
    pygame.draw.circle(sc, RED, [flick_pl_x, FLICK_Y], 35) # プレイヤー
    
    # スコアボードの数字表示
    for i in range(0, 7):
        draw_text(sc, str(i), (SCREEN_WIDTH/2)-(80+i*100), SCREEN_SCORE_BOARD/2, 50, WHITE)
        draw_text(sc, str(i), (SCREEN_WIDTH/2)+(80+i*100), SCREEN_SCORE_BOARD/2, 50, WHITE)


# ******************** キックオフ ********************
def kick_off(mb):
    global ball_x, ball_y
    global com_x, com_y
    global img_ball

    # ターン：コンピュータ
    if turn[COMPUTER] == True:
        # キックオフの位置：ランダム -> 0：左上 ／ 1：右上
        rand_num = random.randint(0, 1)
        # 角度：20°~70°
        rand_a = random.randint(30, 60)
        
        # キックオフの位置：左上
        if rand_num == 0:
            # x,y座標：ボール
            ball_x = 140 * math.cos(math.radians(rand_a))
            ball_y = SCREEN_SCORE_BOARD + 140 * math.sin(math.radians(rand_a))
            # x,y座標：ストライカー
            com_x = img_ball.get_width()/2
            com_y = SCREEN_SCORE_BOARD + img_ball.get_height()/2
        # キックオフの位置：右上
        elif rand_num == 1:
            # x,y座標：ボール
            ball_x = 140 * math.cos(math.radians(rand_a))
            ball_y = SCREEN_HEIGHT - 140 * math.sin(math.radians(rand_a))
            # x,y座標：ストライカー
            com_x = img_ball.get_width()/2
            com_y = SCREEN_HEIGHT - img_ball.get_height()/2
        return True

    # ターン：プレイヤー
    elif turn[PLAYER] == True:
        # マウスのx,y座標 -> ボールのx,y座標
        ball_x, ball_y = pygame.mouse.get_pos()

        # 移動制限
        if ball_y < SCREEN_SCORE_BOARD + img_ball.get_height()/2:
            ball_y = SCREEN_SCORE_BOARD + img_ball.get_height()/2
        if ball_y > SCREEN_HEIGHT - img_ball.get_height()/2:
            ball_y = SCREEN_HEIGHT - img_ball.get_height()/2
        if ball_x < SCREEN_WIDTH/2 + img_ball.get_width()/2:
            ball_x = SCREEN_WIDTH/2 + img_ball.get_width()/2
        if ball_x > SCREEN_WIDTH - img_ball.get_width()/2:
            ball_x = SCREEN_WIDTH - img_ball.get_width()/2

        # 画像：透明度の調整
        img_ball.set_alpha(255)
        # 枠内 + クリック -> ボールをセット
        if get_dis(ball_x, ball_y, SCREEN_WIDTH, SCREEN_SCORE_BOARD+5) <= 140**2:
            if mb == True:
                return True
        elif get_dis(ball_x, ball_y, SCREEN_WIDTH, SCREEN_HEIGHT-5) <= 140**2:
            if mb == True:
                return True
        else:
            img_ball.set_alpha(150)

    return False


# ******************** ゲーム開始時のボードをセット ********************
def board_set():
    global pl_x, pl_y, pl_vx, pl_vy, pl_bis
    global com_x, com_y, com_vx, com_vy, com_bis
    global ball_vx, ball_vy
    global bis_x, bis_y, bis_vx, bis_vy

    # プレイヤー
    pl_x = SCREEN_WIDTH - 300
    pl_y = BOARD_HEIGHT_CENTER
    pl_vx = 0
    pl_vy = 0
    pl_bis = 0
    # コンピュータ
    com_x = 300
    com_y = BOARD_HEIGHT_CENTER
    com_vx = 0
    com_vy = 0
    com_bis = 0
    # ボール
    ball_vx = 0
    ball_vy = 0
    # ビスケット
    for i in range(BISCUIT_NUM):
        bis_f[i] = True
        bis_x[i] = SCREEN_WIDTH/2
        bis_y[i] = 300 + i*250
        bis_vx[i] = 0
        bis_vy[i] = 0


# ******************** タイトル画面 ********************
def title_screen(sc, mx, my, mb):
    global idx, tmr, level
    
    # 画像：背景／文字
    sc.blit(img_title_board, [0, 0])            
    sc.blit(img_text[0], [SCREEN_WIDTH/2 - img_text[0].get_width()/2, SCREEN_HEIGHT/2 - 300])

    # 画像：EASY
    if 280 - img_text[1].get_width()/2 < mx < 280 + img_text[1].get_width()/2 and \
        650 < my < 650 + img_text[1].get_height():
        if tmr%10 < 5:
            sc.blit(img_text[1], [280 - img_text[1].get_width()/2, 650])
        if mb == True:
            # タイトル音楽：停止 ／ プレイ中音楽：開始
            pygame.mixer.music.stop()
            pygame.mixer.music.load("music/Digital_Ghosts-Unicorn_Heads.mp3")
            pygame.mixer.music.play(-1)

            level = 0
            idx = 1
            tmr = 0
    else:
        sc.blit(img_text[1], [280 - img_text[1].get_width()/2, 650])
        
    # 画像：NORMAL
    if SCREEN_WIDTH/2 - img_text[2].get_width()/2 < mx < SCREEN_WIDTH/2 + img_text[2].get_width()/2 and \
        650 < my< 650 + img_text[2].get_height():
        if tmr%10 < 5:
            sc.blit(img_text[2], [SCREEN_WIDTH/2 - img_text[2].get_width()/2, 650])
        if mb == True:
            # タイトル音楽：停止 ／ プレイ中音楽：開始
            pygame.mixer.music.stop()
            pygame.mixer.music.load("music/Digital_Ghosts-Unicorn_Heads.mp3")
            pygame.mixer.music.play(-1)
                    
            level = 1
            idx = 1
            tmr = 0
    else:
        sc.blit(img_text[2], [SCREEN_WIDTH/2 - img_text[2].get_width()/2, 650])
        
    # 画像：HARD
    if (SCREEN_WIDTH - 280) - img_text[3].get_width()/2 < mx < (SCREEN_WIDTH - 280) + img_text[3].get_width()/2 and \
        650 < my < 650 + img_text[3].get_height():
        if tmr%10 < 5:
            sc.blit(img_text[3], [(SCREEN_WIDTH - 280) - img_text[3].get_width()/2, 650])
        if mb == True:
            # タイトル音楽：停止 ／ プレイ中音楽：開始
            pygame.mixer.music.stop()
            pygame.mixer.music.load("music/Digital_Ghosts-Unicorn_Heads.mp3")
            pygame.mixer.music.play(-1)
                    
            level = 2
            idx = 1
            tmr = 0
    else:
        sc.blit(img_text[3], [(SCREEN_WIDTH - 280) - img_text[3].get_width()/2, 650])

    # 画像：ルール(遊び方)
    if 700 < mx < 700 + img_text[10].get_width() and 850 < my < 850 + img_text[10].get_height():
        if tmr%10 < 5:
            sc.blit(img_text[10], [700, 850])
        if mb == True:
            idx = -1
            tmr = 0
    else:
        sc.blit(img_text[10], [700, 850])
    

# ******************** ルール画面(遊び方説明) ********************
def rule_screen(sc, mx, my, mb):
    global idx, tmr
    
    # 画像：各説明内容
    sc.blit(img_rule[-1 * idx], [0, 0])
    # 画像：NEXT(次の画面)
    if idx > -8:
        if 1350 < mx < 1350 + img_text[11].get_width() and 930 < my < 930 + img_text[11].get_height():
            if tmr%10 < 5:
                sc.blit(img_text[11], [1350, 930])
            if mb == True and tmr > 30:
                idx -= 1
                tmr = 0
        else:
            sc.blit(img_text[11], [1350, 930])

    # 画像：BACK(前の画面)
    if idx < -1:
        if 50 < mx < 50 + img_text[12].get_width() and 930 < my < 930 + img_text[11].get_height():
            if tmr%10 < 5:
                sc.blit(img_text[12], [50, 930])
            if mb == True and tmr > 30:
                idx += 1
                tmr = 0
        else:
            sc.blit(img_text[12], [50, 930])

    # 画像：TITLE(タイトル画面)
    if 730 < mx < 730 + img_text[13].get_width() and 930 < my < 930 + img_text[13].get_height():
        if tmr%10 < 5:
            sc.blit(img_text[13], [730, 930])
        if mb == True and tmr > 30:
            idx = 0
    else:
        sc.blit(img_text[13], [730, 930])
        

# ============================================================
#                           MAIN
# ============================================================

# ******************** メインループ ********************
def main():
    global idx, tmr, level, turn, point_pl, point_com, power_set
    global flick_pl_x, flick_pl_v, flick_com_x, flick_com_v
    global snd_smash, snd_collision, snd_bound, snd_stick, snd_point_pl, snd_point_com, snd_pl_win, snd_pl_lose
    
    pygame.init()
    pygame.display.set_caption("KLACK GAME")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # 効果音
    snd_smash = pygame.mixer.Sound("sound/smash.mp3")
    snd_collision = pygame.mixer.Sound("sound/collision.mp3")
    snd_bound = pygame.mixer.Sound("sound/bound.mp3")
    snd_stick = pygame.mixer.Sound("sound/stick.mp3")
    snd_point_pl = pygame.mixer.Sound("sound/point_player.mp3")
    snd_point_com = pygame.mixer.Sound("sound/point_computer.mp3")
    snd_pl_win = pygame.mixer.Sound("sound/player_win.mp3")
    snd_pl_lose = pygame.mixer.Sound("sound/player_lose.mp3")
    
    tmr = 0
    
    while True:
        tmr = tmr + 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        key = pygame.key.get_pressed()

        # マウスのx,y座標とクリックの有無
        mouseX, mouseY = pygame.mouse.get_pos()
        mBtn_1, mBtn_2, mBtn_3 = pygame.mouse.get_pressed()


        # 遊び方 説明画面
        if idx < 0:
            rule_screen(screen, mouseX, mouseY, mBtn_1)
            
        # タイトル画面：レベル選択
        if idx == 0:
            if tmr == 1:
                # タイトル音楽：開始
                pygame.mixer.music.load("music/Stellar_Wind-Unicorn_Heads.mp3")
                pygame.mixer.music.play(-1)
            # タイトル画面
            title_screen(screen, mouseX, mouseY, mBtn_1)
                
        # フリックオフ：先攻／後攻を決める
        elif idx == 1:
            # 初期化
            if tmr == 1:
                board_set()
                draw_board(screen)
                # 得点の初期化
                point_pl = 0
                point_com = 0
                # フリック関係の初期化
                power_set = False
                flick_pl_x = SCREEN_WIDTH - 120
                flick_pl_v = 0
                flick_com_x = 120
                flick_com_v = 0

            # 文字の表示
            if tmr < 120:
                draw_board(screen)
                if tmr%30 < 20:
                    screen.blit(img_text[4], [SCREEN_WIDTH/2 - img_text[4].get_width()/2, 300])
                    
            # フリックオフ
            if tmr >= 120:
                flick_off(screen, key)
                # 文字の表示
                if tmr%50 < 40:
                    draw_text(screen, "Press  [SPACE]  to  stop!", SCREEN_WIDTH/2, 400, 70, BLACK)
                draw_text(screen, "PLAYER", SCREEN_WIDTH - 400, 200, 65, RED)
                draw_text(screen, "COMPUTER", 400, 200, 65, BLUE)

                # フリックを弾いた後、互いのフリックが止まった場合
                if power_set == True and flick_pl_v == 0 and flick_com_v == 0:
                    power_set = False
                    # 先攻：遠くまでフリックを飛ばせた側
                    if SCREEN_WIDTH - flick_pl_x > flick_com_x:
                        # 先攻：プレイヤー
                        turn[PLAYER] = True
                        idx = 2
                        tmr = 0
                    elif SCREEN_WIDTH - flick_pl_x < flick_com_x:
                        # 後攻：コンピュータ
                        turn[COMPUTER] = True
                        idx = 2
                        tmr = 0
                    else:
                        # 同じ場合はもう一度
                        tmr = 0

        # ゲームプレイ
        elif idx == 2:
            # 初期位置
            if tmr == 1:
                board_set()

            # キックオフ：先攻 ／ 得点された側
            if turn[COMPUTER] == True or turn[PLAYER] == True:
                if kick_off(mBtn_1) == True:
                    turn[COMPUTER] = False
                    turn[PLAYER] = False
                    tmr = 1
            # 操作：ゲームプレイ
            elif turn[COMPUTER] == False and turn[PLAYER] == False and tmr > 60:        
                striker_player(mouseX, mouseY)
                striker_computer()
                ball()
                biscuit()
                
            draw_board(screen)

        # 得点内容の表示
        elif idx == 3:
            draw_board(screen)
            # 文字：得点内容
            screen.blit(img_text[text_goal], [SCREEN_WIDTH/2 - img_text[text_goal].get_width()/2, BOARD_HEIGHT_CENTER - img_text[text_goal].get_height()/2])
            # キックオフへ
            if tmr == 60:
                idx = 2
                tmr = 0
                # 決着がつく：得点が6点になった時
                if point_pl == POINT_WIN or point_com == POINT_WIN:
                    idx = 4
                    tmr = 0

        # ゲーム終了
        elif idx == 4:
            # 効果音：勝敗決定
            if tmr == 1:
                if point_pl == POINT_WIN:
                    snd_pl_win.play()
                elif point_com == POINT_WIN:
                    snd_pl_lose.play()
                    
            draw_board(screen)
            # 文字：結果表示
            if tmr%50 < 40:
                if point_pl == POINT_WIN:
                    screen.blit(img_text[8], [SCREEN_WIDTH/2 - img_text[8].get_width()/2, BOARD_HEIGHT_CENTER - img_text[8].get_height()/2])
                elif point_com == POINT_WIN:
                    screen.blit(img_text[9], [SCREEN_WIDTH/2 - img_text[9].get_width()/2, BOARD_HEIGHT_CENTER - img_text[9].get_height()/2])
            # タイトルへ
            if tmr == 180:
                idx = 0
                tmr = 0

            
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()

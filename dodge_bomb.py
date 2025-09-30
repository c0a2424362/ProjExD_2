import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：タプル（縦、横）
    画面内ならTrue,画面外ならFalse
    """
    yoko,tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:  # 横
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:  # 縦
        tate = False
    return yoko, tate

def gemeover(screen:pg.Surface) -> None:  # ゲームオーバー
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # 画面設定
    gemeover_bg = pg.Surface((WIDTH, HEIGHT))  # ゲームオーバー背景
    gemeover_bg.fill((0, 0, 0))  # 黒で塗りつぶし
    gemeover_bg.set_alpha(200)  # 透明度設定
    font = pg.font.Font(None, 150)
    txt = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(txt, [300, 200])
    gemeover_img = pg.image.load("fig/8.png")
    screen.blit(gemeover_img, [0, 0])  # ゲームオーバー背景描画
    screen.blit(gemeover_bg, [0, 0])  # ゲームオーバー文字描画
    pg.display.update()
    time.sleep(5)  # 5秒間表示
    pg.quit()
    sys.exit()

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []  # 爆弾画像リスト
    bb_acclee = []  # 爆弾加速度リスト
    for r in range(1, 11):  # 10個の爆弾
        bb_img = pg.Surface((20*r, 20*r))  # 爆弾用の空Surface
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)  # 赤い爆弾円
        bb_imgs.append(bb_img)  # 爆弾画像リストに追加
    bb_acclee = [a for a in range(1, 11)]  # 爆弾加速度リストに追加
    bb_img = pg.Surface((20, 20))  # 爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い爆弾円
    bb_img.set_colorkey((0, 0, 0))  # 四隅の黒い部分を透過 
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾横座標
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾縦座標
    return bb_imgs, bb_acclee  # 爆弾画像リスト、爆弾Rectリストを返す


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い爆弾円
    bb_img.set_colorkey((0, 0, 0))  # 四隅の黒い部分を透過
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾横座標
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾縦座標
    vx, vy = +5, +5  # 爆弾の速度
    init_bb_imgs, bb_rcts = init_bb_imgs()  # 爆弾画像リスト、爆弾Rectリスト
    bb_imgs = init_bb_imgs  # 爆弾画像リスト
    avx, avy = vx, vy  # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])
        if kk_rct.colliderect(bb_rct):
            gemeover(screen)  # geme over
        
        


        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 横方向の移動量を加算
                sum_mv[1] += mv[1]  # 縦方向の移動量を加算
        # if key_lst[pg.K_w]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rect.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx, avy)  # 爆弾移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 爆弾描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
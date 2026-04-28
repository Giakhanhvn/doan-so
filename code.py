#gọi thư viện pygame
import pygame
pygame.init()
pygame.mixer.init()

#tiếng đánh chữ
gõ_phím = pygame.mixer.Sound("gõ-phím.mp3")

#tải nhạc nền
nhạc_nền = pygame.mixer.music.load("nhạc-nền.mp3")
pygame.mixer.music.play(-1)   #phát nhạc nền liên tục
pygame.mixer.music.set_volume(0.1)   #điều chỉnh âm lượng nhạc nền

#tạo cửa sổ
pygame.display.set_caption("Đoán số!")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800, 600))

#tải ảnh nền
bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg, (800, 600))

#biến
tick = 0       #đếm số lần lặp
a = 255        #độ trong suốt của hu1
x = 85          #tọa độ x của hu1 và hu2
x_max = 0     #tọa độ x tối đa
y = 5          #tọa độ y của hu1 và hu2
dòng = 1       #số thứ tự dòng
ẩn_hiện_nút = False    #ẩn/hiện nút tiếp tục
nhạc = True      #bật/tắt nhạc
bảng = 1         #số thứ tự bảng
số_cần_tìm = 0     #số cần tìm
alpha_ket_qua = 0  #độ trong suốt của kết quả
click = False       #biến kiểm tra click chuột

#tải ảnh hiệu ứng
hu1 = pygame.image.load("hieu-ung-1.png")
hu1 = pygame.transform.scale(hu1, (5, 25))
hu2 = pygame.image.load("hieu-ung-2.png")
hu2 = pygame.transform.scale(hu2, (1000, 25))

#thêm nút tiếp tục
tiep = pygame.image.load("tiep.png")
tiep = pygame.transform.scale(tiep, (30, 30))

#thêm NPC
npc = pygame.image.load("huong-dan.png")
npc = pygame.transform.scale(npc, (80, 80))

#nút v
nut_v = pygame.image.load("v.png")
nut_v = pygame.transform.scale(nut_v, (70, 70))

#nút x
nut_x = pygame.image.load("x.png")
nut_x = pygame.transform.scale(nut_x, (70, 70))

#kết quả
kq = pygame.image.load("kt.png")
kq_width, kq_height = kq.get_size()
kq = pygame.transform.scale(kq, (kq_width * 3, kq_height * 3))

#nút tiếp tục
bảng_images = [
    pygame.transform.scale(pygame.image.load(f"bang-{i}.png"), (400, 300))
    for i in range(1, 7)
]
line_images = [
    pygame.transform.scale(pygame.image.load(f"dong-{i}.png"), (875, 25))
    for i in range(1, 7)
]

#chỉnh FPS
clock = pygame.time.Clock()

#vòng lặp chính
running = True
while running:
    click = False
    #kết thúc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        
    clock.tick(30)     #30 FPS

    screen.blit(bg, (0, 0))   #hiện nền

    #hiện NPC
    screen.blit(npc, (10, 10))

    #lấy tọa độ
    chuột = pygame.mouse.get_pos()
    chuột_x = chuột[0]
    chuột_y = chuột[1]

    #hiện nút tiếp tục
    if ẩn_hiện_nút == True and dòng != 6:
        tiep.set_alpha(255)
        if chuột_x >= 750 and chuột_x <= 780 and chuột_y >= 40 and chuột_y <= 70:
            if click == True:
                dòng += 1
                x = 85
                a = 255
                ẩn_hiện_nút = False
    else:
        tiep.set_alpha(0)
    screen.blit(tiep, (750, 40))

    #đổi dòng
    if 1 <= dòng <= 6:
        dong_hien = line_images[dòng - 1]
    if dòng == 1:
        x_max = 190
    elif dòng == 2:
        x_max = 500
    elif dòng == 3:
        x_max = 600
    elif dòng == 4:
        x_max = 800
    elif dòng == 5:
        x_max = 170
    elif dòng == 6:
        x_max = 450

    #hiện dòng hiện
    screen.blit(dong_hien, (90, 5))

    #hiện hiệu ứng
    if bảng < 7:
        screen.blit(hu1, (x, y))
        hu1 = hu1.copy()
        hu1.set_alpha(a)      

        #cập nhật biến
        tick += 1
        if tick >= 1:
            tick = 0
            if x <= x_max:
                if a == 255:
                    a = 0
                else:
                    a = 255
                x += 5
                if nhạc == True:
                    gõ_phím.play()
                    nhạc = False
            else:
                a = 0
                ẩn_hiện_nút = True
                nhạc = True
                gõ_phím.stop()

        screen.blit(hu2, (x + 5, y))
    
    #cập nhật hiệu ứng kết quả
    if bảng == 7 and alpha_ket_qua < 255:
        if tick % 3 == 0:  # chậm lại hiệu ứng
            alpha_ket_qua += 5
            if alpha_ket_qua > 255:
                alpha_ket_qua = 255
            kq.set_alpha(alpha_ket_qua)
            số_1_hiện_copy = số_1_hiện.copy()
            số_1_hiện_copy.set_alpha(alpha_ket_qua)
            số_2_hiện_copy = số_2_hiện.copy()
            số_2_hiện_copy.set_alpha(alpha_ket_qua)
    
    #đổi bảng
    if 1 <= bảng <= 6:
        bang = bảng_images[bảng - 1]

    #hiện bảng
    if dòng == 6:
        screen.blit(bang, (100, 150))
        screen.blit(nut_v, (600, 220))
        screen.blit(nut_x, (600, 320))
        if chuột_x >= 600 and chuột_x <= 670 and chuột_y >= 220 and chuột_y <= 290 and bảng <= 6:
            if click == True:
                if bảng == 1:
                    số_cần_tìm += 1
                elif bảng == 2:
                    số_cần_tìm += 2
                elif bảng == 3:
                    số_cần_tìm += 4
                elif bảng == 4:
                    số_cần_tìm += 8
                elif bảng == 5:
                    số_cần_tìm += 16
                elif bảng == 6:
                    số_cần_tìm += 32
                bảng += 1
        if chuột_x >= 600 and chuột_x <= 670 and chuột_y >= 320 and chuột_y <= 390 and bảng <= 6:
            if click == True:
                bảng += 1

        if số_cần_tìm <= 9:
            số_2 = số_cần_tìm
            số_1_hiện = pygame.image.load("0.png")
            số_2_hiện = pygame.image.load(str(số_2) + ".png")
        else :
            số_1 = số_cần_tìm // 10
            số_2 = số_cần_tìm % 10
            số_1_hiện = pygame.image.load(str(số_1) + ".png")
            số_2_hiện = pygame.image.load(str(số_2) + ".png")

    if bảng == 7:
        screen.blit(kq, (90, 5))
        số_1_hiện = pygame.transform.scale(số_1_hiện, (16, 20))
        số_2_hiện = pygame.transform.scale(số_2_hiện, (16, 20))
        số_1_hiện_copy = số_1_hiện.copy()
        số_1_hiện_copy.set_alpha(alpha_ket_qua)
        số_2_hiện_copy = số_2_hiện.copy()
        số_2_hiện_copy.set_alpha(alpha_ket_qua)
        screen.blit(số_1_hiện_copy, (300, 9))
        screen.blit(số_2_hiện_copy, (320, 9))
        bang.set_alpha(0)
        nut_v.set_alpha(0)
        nut_x.set_alpha(0)
        dong_hien.set_alpha(0)
        out += 1
        if out >= 100:
            running = False

    pygame.display.update()

pygame.quit()
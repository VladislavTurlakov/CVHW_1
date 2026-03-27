# -----------------------------------------------------------------------
# Разработать программу, которая будет выполнять следующие действия:
# 1.Отображать на экране видео с web камеры или из файла 
#   (источник видео должен передаваться через параметры командной строки)
# 2.Отлавливать нажатия левой клавиши мыши на изображении с камеры и 
#   отображать при помощи отрисовки прямоугольника места нажатий
# 3.По нажатию кнопки С или сбрасывать все отмеченные точки 
#   (после сброса точки не отображаются на экране)
# 4.По нажатию кнопки Q или кнопки tkinter завершать приложение
# -----------------------------------------------------------------------

import cv2
import argparse
import tkinter as tk
import threading
import sys

points = []
rectangle_size = 80
running = True

# Функция обработчика кликов мыши
def mouse_callback(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))

# Функция запуска Tkinter кнопки
def tkinter_window():
    global running

    def quit_app():
        global running
        running = False

    root = tk.Tk()
    root.title("Управление")
    root.geometry("200x100")

    btn = tk.Button(root, text="Выход (Q)", command=quit_app)
    btn.pack(expand=True)

    root.mainloop()

# Главная функция
def main():
    global running, points

    parser = argparse.ArgumentParser(description="OpenCV Video Click Tracker")
    parser.add_argument("--source", type = str, default = "0",
        help = "Источник видео: 0 - камера, или путь к видеофайлу"
    )

    args = parser.parse_args()

    # Определение источника
    if args.source.isdigit():
        cap = cv2.VideoCapture(int(args.source))
    else:
        cap = cv2.VideoCapture(args.source)

    if not cap.isOpened():
        print("Ошибка: Невозможно открыть источник видео")
        sys.exit()

    cv2.namedWindow("Video")
    cv2.setMouseCallback("Video", mouse_callback)

    # Запуск Tkinter в отдельном потоке
    tk_thread = threading.Thread(target=tkinter_window)
    tk_thread.daemon = True
    tk_thread.start()

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        # Отображение прямоугольника
        for (x, y) in points:
            top_left = (x - rectangle_size, y - rectangle_size // 2)
            bottom_right = (x + rectangle_size, y + rectangle_size // 2)
            cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)

        cv2.imshow("Video", frame)

        key = cv2.waitKey(1) & 0xFF

        # C — очистить точки
        if key == ord('c') or key == ord('C'):
            points.clear()

        # Q — выход из программы
        if key == ord('q') or key == ord('Q'):
            break

    running = False
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

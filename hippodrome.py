from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from random import randint


# установка состояния лошадей и погоды
def setupHorse():
    global state01, state02, state03, state04
    global weather, timeDay
    global winCoeff01, winCoeff02, winCoeff03, winCoeff04
    global play01, play02, play03, play04
    global reverse01, reverse02, reverse03, reverse04
    global fastSpeed01, fastSpeed02, fastSpeed03, fastSpeed04
    weather = randint(1, 5)
    timeDay = randint(1, 4)
    state01 = randint(1, 5)
    state02 = randint(1, 5)
    state03 = randint(1, 5)
    state04 = randint(1, 5)
    winCoeff01 = int(100 + randint(1, 30 + state01 * 60)) / 100
    winCoeff02 = int(100 + randint(1, 30 + state02 * 60)) / 100
    winCoeff03 = int(100 + randint(1, 30 + state03 * 60)) / 100
    winCoeff04 = int(100 + randint(1, 30 + state04 * 60)) / 100
    # маркеры ситуаций
    reverse01 = False
    reverse02 = False
    reverse03 = False
    reverse04 = False
    play01 = True
    play02 = True
    play03 = True
    play04 = True
    fastSpeed01 = False
    fastSpeed01 = False
    fastSpeed03 = False
    fastSpeed04 = False


# определение победителя
def winRound(horse):
    global x01, x02, x03, x04, money
    res = "К финешу пришла лошадь "

    if horse == 1:
        res += nameHorse01
        win = summ01.get() * winCoeff01
    elif horse == 2:
        res += nameHorse02
        win = summ02.get() * winCoeff02
    elif horse == 3:
        res += nameHorse03
        win = summ03.get() * winCoeff03
    elif horse == 4:
        res += nameHorse04
        win = summ04.get() * winCoeff04

    if horse > 0:
        res += f"! Вы выиграли {valuta}{int(win)}."
        if win > 0:
            res += "Поздравляем! Средства уже зачислены на ваш счёт!"
            insertText(f"Этот забег принёс вам {valuta}{int(win)}.")
        else:
            res += "К сожалению, ваша лошадь проиграла. Попробуйте ещё раз!"
            insertText("Делайте ставку! Увеличивайте прибыль!")
        messagebox.showinfo("РЕЗУЛЬТАТ", res)
    else:
        messagebox.showinfo(
            "Всё плохо",
            "До финиша не дошол никто. Забег признан несостаявшимся. Все ставки возвращены.",
        )
        insertText("Забег признан несостаявшимся.")
        win = summ01.get() + summ02.get() + summ03.get() + summ04.get()

    money += win
    saveMoney(int(money))
    # сброс переменных
    setupHorse()
    # сброс виджетов
    startButton["state"] = "normal"
    stavka01["state"] = "readonly"
    stavka02["state"] = "readonly"
    stavka03["state"] = "readonly"
    stavka04["state"] = "readonly"
    stavka01.current(0)
    stavka02.current(0)
    stavka03.current(0)
    stavka04.current(0)
    # сброс координат и перерисовка
    x01 = 20
    x02 = 20
    x03 = 20
    x04 = 20
    horsePlaceInWindow()
    # обновление интерфейса
    # обновляет выподающие списки и чекбоксы
    refreshCombo(eventObject="")
    # выводит в чат погоду
    vieWeather()
    # выводит в чат информацию о лошадях
    healthHorse()
    # выводит в чат информацию о доступной сумме
    insertText(f"Ваши средства: {valuta}{int(money)}")
    # закрываем программу, если сумма средств на счету меньше 1
    if money < 1:
        messagebox.showinfo("Стоп!", "На ипподром без средств заходить нельзя.")
        quit(0)


# движенее лошадей
def moveHorse():
    global x01, x02, x03, x04

    if randint(0, 100) < 20:
        problemHorse()

    # расчитываем скорость для каждой лошади
    speed01 = (
        randint(1, timeDay + weather) + randint(1, int((7 - state01)) * 3)
    ) / randint(10, 175)
    speed02 = (
        randint(1, timeDay + weather) + randint(1, int((7 - state02)) * 3)
    ) / randint(10, 175)
    speed03 = (
        randint(1, timeDay + weather) + randint(1, int((7 - state03)) * 3)
    ) / randint(10, 175)
    speed04 = (
        randint(1, timeDay + weather) + randint(1, int((7 - state04)) * 3)
    ) / randint(10, 175)
    multiple = 3
    speed01 *= randint(1, 2 + state01) * (1 + fastSpeed01 * multiple)
    speed02 *= randint(1, 2 + state02) * (1 + fastSpeed02 * multiple)
    speed03 *= randint(1, 2 + state03) * (1 + fastSpeed03 * multiple)
    speed04 *= randint(1, 2 + state04) * (1 + fastSpeed04 * multiple)

    # вправо или влево бежит лошадь?
    if play01:
        if not reverse01:
            x01 += speed01
        else:
            x01 -= speed01
    if play02:
        if not reverse02:
            x02 += speed02
        else:
            x02 -= speed02

    if play03:
        if not reverse03:
            x03 += speed03
        else:
            x03 -= speed03
    if play04:
        if not reverse04:
            x04 += speed04
        else:
            x04 -= speed04

    horsePlaceInWindow()
    # текущая ситуация
    allPlay = play01 or play02 or play03 or play04
    allX = x01 < 0 and x02 < 0 and x03 < 0 and x04 < 0
    allReverse = reverse01 and reverse02 and reverse03 and reverse04

    if not allPlay or allX or allReverse:
        winRound(0)
        return 0

    # если лошадь ещё не добежала до финиша, то каждый раз вызываем moveHorse()
    if x01 < 952 and x02 < 952 and x03 < 952 and x04 < 952:
        root.after(5, moveHorse)
    else:
        if x01 >= 952:
            winRound(1)
        elif x02 >= 952:
            winRound(2)
        elif x03 >= 952:
            winRound(3)
        elif x04 >= 952:
            winRound(4)


def runHorse():
    global money
    startButton["state"] = "disabled"
    stavka01["state"] = "disabled"
    stavka02["state"] = "disabled"
    stavka03["state"] = "disabled"
    stavka04["state"] = "disabled"
    money -= summ01.get() + summ02.get() + summ03.get() + summ04.get()
    moveHorse()


# изменение поведения лошади
def problemHorse():
    global reverse01, reverse02, reverse03, reverse04
    global play01, play02, play03, play04
    global state01, state02, state03, state04
    global fastSpeed01, fastSpeed02, fastSpeed03, fastSpeed04
    # выбираем лошадь для события
    horse = randint(1, 4)
    # чем выше число, тем ниже вероятность наступления события
    maxRand = 3000

    if horse == 1 and play01 == True and x01 > 0:
        if randint(0, maxRand) < state01 * 5:
            # маркер движения в обратный
            reverse01 = not reverse01
            # сообщаем пользователю
            messagebox.showinfo(
                "Ааааа!", f"Лошадь {nameHorse01} развернулась и бежит в другую сторону!"
            )
        elif randint(0, maxRand) < state01 * 5:
            # лошадь остановилась
            play01 = False
            messagebox.showinfo(
                "Никогда такого не было и вот опять",
                f"{nameHorse01} заржала и скинула жокея!",
            )
        elif randint(0, maxRand) < state01 * 5 and not fastSpeed01:
            messagebox.showinfo(
                "Великолепно!", f"{nameHorse01} перестала притворяться и ускорилась"
            )
            # задаём множитель ускорения
            fastSpeed01 = True
    elif horse == 2 and play02 == True and x02 > 0:
        if randint(0, maxRand) < state02 * 5:
            reverse02 = not reverse02
            messagebox.showinfo(
                "Ааааа!", f"Лошадь {nameHorse02} развернулась и бежит в другую сторону!"
            )
        elif randint(0, maxRand) < state02 * 5:
            play02 = False
            messagebox.showinfo(
                "Никогда такого не было и вот опять",
                f"{nameHorse02} заржала и скинула жокея!",
            )
        elif randint(0, maxRand) < state02 * 5 and not fastSpeed02:
            messagebox.showinfo(
                "Великолепно!", f"{nameHorse02} перестала притворяться и ускорилась"
            )
            # задаём множитель ускорения
            fastSpeed02 = True
    elif horse == 3 and play03 == True and x03 > 0:
        if randint(0, maxRand) < state03 * 5:
            reverse03 = not reverse03
            messagebox.showinfo(
                "Ааааа!", f"Лошадь {nameHorse03} развернулась и бежит в другую сторону!"
            )
        elif randint(0, maxRand) < state03 * 5:
            play03 = False
            messagebox.showinfo(
                "Никогда такого не было и вот опять",
                f"{nameHorse03} заржала и скинула жокея!",
            )
        elif randint(0, maxRand) < state03 * 5 and not fastSpeed03:
            messagebox.showinfo(
                "Великолепно!", f"{nameHorse03} перестала притворяться и ускорилась"
            )
            # задаём множитель ускорения
            fastSpeed03 = True
    elif horse == 4 and play04 == True and x04 > 0:
        if randint(0, maxRand) < state04 * 5:
            reverse04 = not reverse04
            messagebox.showinfo(
                "Ааааа!", f"Лошадь {nameHorse04} развернулась и бежит в другую сторону!"
            )
        elif randint(0, maxRand) < state04 * 5:
            play04 = False
            messagebox.showinfo(
                "Никогда такого не было и вот опять",
                f"{nameHorse04} заржала и скинула жокея!",
            )
        elif randint(0, maxRand) < state04 * 5 and not fastSpeed04:
            messagebox.showinfo(
                "Великолепно!", f"{nameHorse04} перестала притворяться и ускорилась"
            )
            # задаём множитель ускорения
            fastSpeed04 = True


def refreshCombo(eventObject):
    summ = summ01.get() + summ02.get() + summ03.get() + summ04.get()
    labelAllMoney["text"] = f"У вас на считу: {valuta}{int(money - summ)}"
    stavka01["values"] = getValues(
        int(money - summ02.get() - summ03.get() - summ04.get())
    )
    stavka02["values"] = getValues(
        int(money - summ01.get() - summ03.get() - summ04.get())
    )
    stavka03["values"] = getValues(
        int(money - summ02.get() - summ01.get() - summ04.get())
    )
    stavka04["values"] = getValues(
        int(money - summ02.get() - summ03.get() - summ01.get())
    )

    if summ > 0:
        startButton["state"] = "normal"
    else:
        startButton["state"] = "disabled"

    if summ01.get() > 0:
        horse01Game.set(True)
    else:
        horse01Game.set(False)

    if summ02.get() > 0:
        horse02Game.set(True)
    else:
        horse02Game.set(False)

    if summ03.get() > 0:
        horse03Game.set(True)
    else:
        horse03Game.set(False)

    if summ04.get() > 0:
        horse04Game.set(True)
    else:
        horse04Game.set(False)


# определение размера ставок
def getValues(summa):
    value = []
    if summa > 9:
        for i in range(0, 11):
            value.append(i * (int(summa) // 10))
        else:
            value.append(0)
            if summa > 0:
                value.append(summa)
    return value


# расположение лошадей на экране
def horsePlaceInWindow():
    horse01.place(x=int(x01), y=20)
    horse02.place(x=int(x02), y=100)
    horse03.place(x=int(x03), y=180)
    horse04.place(x=int(x04), y=260)


# добавление строки в текстовый блок
def insertText(s):
    textDiary.insert(INSERT, s + "\n")
    textDiary.see(END)


# формирование погоды и времени суток
def vieWeather():
    s = "Сейчая на ипподроме "

    if timeDay == 1:
        s += "ночь, "
    elif timeDay == 2:
        s += "утро, "
    elif timeDay == 3:
        s += "день, "
    elif timeDay == 4:
        s += "вечер, "

    if weather == 1:
        s += "льёт сильный дождь."
    elif weather == 2:
        s += "моросит дождик."
    elif weather == 3:
        s += "облочно, на горизонте тучи."
    elif weather == 4:
        s += "безоблочно, прекрасная погода!"

    insertText(s)


# фунция чтения из файла оставшейся суммы
def loadMoney():
    try:
        f = open("money.txt", "r")
        m = int(f.readline())
        f.close()
    except FileNotFoundError:
        print(f"Не найден файл с суммой! Задано значение {valuta}{defaultMoney}")
        m = defaultMoney
    return m


# функция записи в файл с суммой
def saveMoney(m):
    try:
        f = open("money.txt", "w")
        f.write(str(m))
        f.close()
    except FileNotFoundError:
        print("Ошибка создания файла, Казино закрывается!")
        quit()


# определение коэфициента по здоровью
def getHealth(name, state, win):
    s = f"Лошадь {name} "

    if state == 5:
        s += "мучается несворением желудка."
    elif state == 4:
        s += "плохо спала. Подёргивается веко."
    elif state == 3:
        s += "сурова и беспощадна."
    elif state == 2:
        s += "в отличном настроении. Покушала хорошо."
    elif state == 1:
        s += "просто ракета!"

    s += f" ({win}:1)"
    return s


# вывод в чат коэфициента
def healthHorse():
    insertText(getHealth(nameHorse01, state01, winCoeff01))
    insertText(getHealth(nameHorse02, state02, winCoeff02))
    insertText(getHealth(nameHorse03, state03, winCoeff03))
    insertText(getHealth(nameHorse04, state04, winCoeff04))


root = Tk()
# координы лошадей и деньги
x01 = 20
x02 = 20
x03 = 20
x04 = 20
nameHorse01 = "Ананас"
nameHorse02 = "Сталкер"
nameHorse03 = "Прожорливый"
nameHorse04 = "Копытце"
defaultMoney = 10000
money = 0
valuta = "$"
weather = randint(1, 5)
timeDay = randint(1, 4)
# маркеры ситуации
reverse01 = False
reverse02 = False
reverse03 = False
reverse04 = False
play01 = True
play02 = True
play03 = True
play04 = True
fastSpeed01 = False
fastSpeed02 = False
fastSpeed03 = False
fastSpeed04 = False
# состояние лошади и коэфициент выплат
state01 = randint(1, 5)
state02 = randint(1, 5)
state03 = randint(1, 5)
state04 = randint(1, 5)
winCoeff01 = int(100 + randint(1, 30 + state01 * 60)) / 100
winCoeff02 = int(100 + randint(1, 30 + state02 * 60)) / 100
winCoeff03 = int(100 + randint(1, 30 + state03 * 60)) / 100
winCoeff04 = int(100 + randint(1, 30 + state04 * 60)) / 100

# размер окна программы
WIDTH = 1024
HEIGHT = 600

# координаты для расположение экрана по центру монитора
POS_X = root.winfo_screenwidth() // 2 - WIDTH // 2
POS_Y = root.winfo_screenheight() // 2 - HEIGHT // 2

# заголовок
root.title("ИППОДРОМ")

# запрет на изменение экрана
root.resizable(False, False)

# задаём положение экрана
root.geometry(f"{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}")

# хранение изображения в программе
road_image = PhotoImage(file="img/road.png")

# Label отображает изображение
road = Label(root, image=road_image)

# размещаем изображение
road.place(x=0, y=17)

# изображения лошадей
horse01_image = PhotoImage(file="img/horse01.png")
horse01 = Label(root, image=horse01_image)
horse02_image = PhotoImage(file="img/horse02.png")
horse02 = Label(root, image=horse02_image)
horse03_image = PhotoImage(file="img/horse03.png")
horse03 = Label(root, image=horse03_image)
horse04_image = PhotoImage(file="img/horse04.png")
horse04 = Label(root, image=horse04_image)
horsePlaceInWindow()

# кнопка start
startButton = Button(text="START", font="arial 20", width=63, background="#37AA37")
startButton.place(x=24, y=370)
startButton["state"] = "disabled"

# текстовое поле
textDiary = Text(width=66, height=7, wrap=WORD)
textDiary.place(x=475, y=450)
scroll = Scrollbar(command=textDiary.yview, width=20)
scroll.place(x=990, y=450, height=125)
textDiary["yscrollcommand"] = scroll.set


# отображение средств
money = loadMoney()

if money <= 0:
    messagebox.showinfo(
        "STOP!",
        """На ипподром без денег заходить
                    НЕЛЬЗЯ!""",
    )
    quit(0)

labelAllMoney = Label(text=f"Остаток средств: {valuta}{money}.", font="Arial 12")
labelAllMoney.place(x=20, y=565)

# чекбоксы ставок
labelHorse01 = Label(text="Ставка на лошадь №1")
labelHorse01.place(x=20, y=450)
labelHorse02 = Label(text="Ставка на лошадь №2")
labelHorse02.place(x=20, y=480)
labelHorse03 = Label(text="Ставка на лошадь №3")
labelHorse03.place(x=20, y=510)
labelHorse04 = Label(text="Ставка на лошадь №4")
labelHorse04.place(x=20, y=540)
horse01Game = BooleanVar()
horse01Game.set(0)
horseCheck01 = Checkbutton(
    text=nameHorse01, variable=horse01Game, onvalue=1, offvalue=0
)
horseCheck01.place(x=165, y=448)
horse02Game = BooleanVar()
horse02Game.set(0)
horseCheck02 = Checkbutton(
    text=nameHorse02, variable=horse02Game, onvalue=1, offvalue=0
)
horseCheck02.place(x=165, y=478)
horse03Game = BooleanVar()
horse03Game.set(0)
horseCheck03 = Checkbutton(
    text=nameHorse03, variable=horse03Game, onvalue=1, offvalue=0
)
horseCheck03.place(x=165, y=508)
horse04Game = BooleanVar()
horse04Game.set(0)
horseCheck04 = Checkbutton(
    text=nameHorse04, variable=horse04Game, onvalue=1, offvalue=0
)
horseCheck04.place(x=165, y=538)
horseCheck01["state"] = "disabled"
horseCheck02["state"] = "disabled"
horseCheck03["state"] = "disabled"
horseCheck04["state"] = "disabled"

# выпадающий список
stavka01 = ttk.Combobox(root)
stavka02 = ttk.Combobox(root)
stavka03 = ttk.Combobox(root)
stavka04 = ttk.Combobox(root)
stavka01["state"] = "readonly"
stavka01.place(x=290, y=450)
stavka02["state"] = "readonly"
stavka02.place(x=290, y=480)
stavka03["state"] = "readonly"
stavka03.place(x=290, y=510)
stavka04["state"] = "readonly"
stavka04.place(x=290, y=540)

# определение допустимых ставок
summ01 = IntVar()
summ02 = IntVar()
summ03 = IntVar()
summ04 = IntVar()
stavka01["textvariable"] = summ01
stavka02["textvariable"] = summ02
stavka03["textvariable"] = summ03
stavka04["textvariable"] = summ04
stavka01.bind("<<ComboboxSelected>>", refreshCombo)
stavka02.bind("<<ComboboxSelected>>", refreshCombo)
stavka03.bind("<<ComboboxSelected>>", refreshCombo)
stavka04.bind("<<ComboboxSelected>>", refreshCombo)
refreshCombo("")
stavka01.current(0)
stavka02.current(0)
stavka03.current(0)
stavka04.current(0)

startButton["command"] = runHorse
vieWeather()
healthHorse()
root.mainloop()

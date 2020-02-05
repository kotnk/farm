class Animal:
    is_hungry = False
    is_ready = False
    is_alive = True
    food_capacity = 100.0 # Максимальная сытость
    food_currently = 50.0 # Текущая сытость
    food_daily_consume = 20.0 # Тратится в день
    resource_capacity = 100.0 # Максимальное накопление ресурсов для сбора
    resource_currently = 20.0 # Текущее кол-во ресурса
    resource_daily_restore = food_currently / 2 # Восстановление ресурсов в день
    weight = 10.0 # kg


    def __init__(self, name, weight):
        self.name = name
        self.weight = weight


    def feed(self):
        if self.is_alive is False:
            print('Вы пробуете покормить животное. Увы, {} не отвечает.'.format(self.name))
        elif self.food_currently > 80:
            print('О нет, животное лопнуло от перенасыщения!')
            self.is_alive = False
            animal_list.remove(self)
            print('\x1b[1;31;40m', '{} погибает от вашей невнимательности!'.format(self.name), '\x1b[0m')
            pet_selector()
        else:
            self.food_currently += 20
            print('{} прыгает от радости! {} Сытость: {}%.'.format(self.name, self.voice, self.food_currently))
            pet_selector()
        if self.food_currently >= self.food_capacity / 2:
            self.is_hungry = False


    def gather(self):
        if self.is_alive is False:
            print('Нельзя собрать, вечная память {}'.format(self.name))
            pet_selector()
        elif self.resource_currently > 19:
            self.resource_currently -= 20
            print('Успешно собрали {} (x20) c {}'.format(self.source, self.name))
            if self.resource_capacity < 50:
                self.is_ready = False
            pet_selector()
        else:
            print('Животное еще не готово к сбору.')
            pet_selector()


    def end_of_the_day(self):

        if self.food_currently > 0 and self.food_currently < 20:
            self.is_hungry = True
        elif self.food_currently <= 0:
            self.is_alive = False
            animal_list.remove(self)
        self.resource_currently += self.resource_daily_restore
        if self.food_currently >= 50:
            self.weight += (self.weight * 2 / self.food_currently)
        elif self.food_currently < 50:
            self.weight -= self.weight / self.food_currently / 5
        self.food_currently -= self.food_daily_consume
        if self.resource_capacity > 50:
            self.is_ready = True


class Goose(Animal):
    source = 'Перо'
    voice = 'Honk!'
    gathering = 'Ощипать'


class Cow(Animal):
    source = 'Молоко'
    voice = 'Му-у-у!'
    gathering = 'Подоить'


class Sheep(Animal):
    source = 'Шерсть'
    voice = 'Бе-е-е!'
    gathering = 'Остричь'


class Chicken(Animal):
    source = 'Яйцо'
    voice = 'Куд-кудах!'
    gathering = 'Собрать яйца'


class Goat(Animal):
    source = 'Козье молоко'
    voice = 'Ме-е-е!'
    gathering = 'Подоить'


class Duck(Animal):
    source = 'Яйцо'
    voice = 'Кря-кря!'
    gathering = 'Собрать яйца'


goose1 = Goose('Серый', 7)
goose2 = Goose('Белый', 5.5)
cow1 = Cow('Манька', 250)
sheep1 = Sheep('Барашек', 40)
sheep2 = Sheep('Кудрявый', 50)
chicken1 = Chicken('Ко-ко', 2)
chicken2 = Chicken('Кукареку', 1.5)
goat1 = Goat('Рога', 23)
goat2 = Goat('Копыта', 19)
duck1 = Duck('Кряква', 1.2)

animal_list = [goose1, goose2, cow1, sheep1, sheep2, chicken1, chicken2, goat1, goat2, duck1]

def pet_selector():
    target = input('\nК кому пойдем? Введите имя животного (или q чтобы завершить день):\n>').capitalize()
    is_listed = 0
    if target == 'Q':
        return
    for animal in animal_list:
        if target == animal.name:
            is_listed = 1
            print('{}! Вот ты где!'.format(animal.name))
            print('-', animal.voice)
            action(animal)
    if is_listed == 0:
        print('Такого животного нет')
        pet_selector()


def next_day():
    for animals in animal_list:
        animals.end_of_the_day()


def cycle():
    day = 1
    print('\nДобро пожаловать на ферму!')
    print('\nКормите животных, собирайте ресурсы:')
    print('q - покинуть ферму\n')
    # print('Пример - "f Серый"\n')
    while True:
        # print('День {}'.format(day))
        print('*' * 10, 'День {}\n'.format(day))
        if len(animal_list) == 0:
            print('Кажется, вы не очень хорошо ухаживаете за животными.')
            exit()
        else:
            total_weight = 0
            max_weight = 0
            fatty = str()
            for animals in animal_list:
                total_weight += animals.weight
                if animals.weight > max_weight:
                    max_weight = animals.weight
                    fatty = animals.name
                print(animals.name, str(round(animals.weight, 2)) + 'кг', end='', sep = ', ')
                if animals.is_hungry is True:
                    print(' - голодает!')
                elif animals.resource_currently > 50 and animals.is_hungry is False:
                    print(' - пора собирать ресурсы')
                else:
                    print(' - в порядке')
            print('\nОбщий вес зверей: {}кг.\n{} весит больше всех - {}кг!'.format(round(total_weight, 2), fatty, round(max_weight, 2)))
        pet_selector()
        day += 1
        next_day()


def action(n):
    while True:
        todo = input('\nЧто делаем?\nПокормить - f\n{} - g\nУйти - q\n>'.format(n.gathering))
        if todo == 'g':
            n.gather()
            break
        if todo == 'f':
            n.feed()
            break
        elif todo == 'q':
            pet_selector()
            break
        else:
            print('Не понял.')


def main():
    cycle()


main()

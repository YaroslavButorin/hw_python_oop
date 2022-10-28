class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность:{self.duration: .3f} ч.;'
                f' Дистанция:{self.distance: .3f} км;'
                f' Ср. скорость:{self.speed: .3f} км/ч;'
                f' Потрачено ккал:{self.calories: .3f}.')
    # про переменные понял.
    # Боюсь опять головная боль будет с тестами, не буду менять.


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    CALORIES_MEAN_SPEED_GRADE: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(training_type=self.__class__.__name__,
                              duration=self.duration,
                              distance=self.get_distance(),
                              speed=self.get_mean_speed(),
                              calories=self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    # разобрался
    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height / self.CM_IN_M

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed_msec: float = self.get_mean_speed() * self.KMH_IN_MSEC

        spent_calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                           + (mean_speed_msec
                              ** self.CALORIES_MEAN_SPEED_GRADE
                              / self.height)
                           * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                           * self.weight)
                          * self.duration * self.MIN_IN_H)

        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed()
                           + self.CALORIES_MEAN_SPEED_SHIFT)
                          * self.CALORIES_WEIGHT_MULTIPLIER
                          * self.weight * self.duration)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_data = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in training_data.keys():
        is_valid = training_data[workout_type](*data)
        return is_valid
    # тут мы просто проверяем есть ли ключ в словаре
    # но нет инструкций что делать если нету. тобишь esle/elif


# не будет работать потому что мы данные посылаем в определённом формате
# и на каждый тип тренировки у нас есть свой подкласс
# а класса для обработки неизвестных значений у нас нет.
# отсюда и
# AttributeError: 'NoneType' object has no attribute 'show_training_info'
# можно сделать try/except в read_package и в main
# Хотя даже можно обойтись только в main


def main(training: Training) -> None:
    """Главная функция."""
    try:
        print(training.show_training_info().get_message())
    except AttributeError:
        print('Неизвестный пакет')
    # это поможет программе работать дальше
    # если придет неизвестный ключ


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('QWERTY', [9000, 1, 75, 180]),  # неизвестный пакет
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

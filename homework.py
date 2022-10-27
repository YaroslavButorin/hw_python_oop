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
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

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
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def _init__(self,
                action: int,
                duration: float,
                weight: float
                ) -> None:
        super().__init__(action, duration, weight)
        self.LEN_STEP: float = 0.65

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height / self.CM_IN_M
        self.CALORIES_MEAN_SPEED_GRADE = 2

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed_msec: float = self.get_mean_speed() * self.KMH_IN_MSEC

        self.calories: float = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                                 + (mean_speed_msec
                                    ** self.CALORIES_MEAN_SPEED_GRADE
                                    / self.height)
                                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                                 * self.weight)
                                * self.duration * self.MIN_IN_H)

        return  self.calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

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

    return training_data[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

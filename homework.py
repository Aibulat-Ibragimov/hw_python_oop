from __future__ import annotations
from inspect import signature


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; Длительность: '
                f'{self.duration:.3f} ч.; Дистанция: {self.distance:.3f} '
                f'км; Ср. скорость: {self.speed:.3f} км/ч; Потрачено '
                f'ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    M_IN_H: float = 60

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
        raise ValueError('Метод не определён')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K_1: float = 0.035
    K_2: float = 0.029
    S_IN_H: float = 3600
    SM_IN_M: float = 100
    KM_H_IN_M_S: float = 0.278

    def __init__(
            self, action: int, duration: float, weight: float,
            height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.K_1 * self.weight
                 + ((self.get_mean_speed() * self.KM_H_IN_M_S) ** 2
                    / self.height / self.SM_IN_M) * self.K_2
                 * self.weight) * self.duration * self.M_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    K_1: float = 1.1
    SQUARE: float = 2

    def __init__(
            self, action: int, duration: float, weight: float,
            length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.K_1) * self.SQUARE * self.weight)


def get_count_args(obj: type[Training]) -> int:
    """Возвращает количество полей у класса."""
    return len(signature(obj).parameters)


training_classes: dict[str, tuple[type[Training], int]] = {
    'SWM': (Swimming, get_count_args(Swimming)),
    'RUN': (Running, get_count_args(Running)),
    'WLK': (SportsWalking, get_count_args(SportsWalking))}


def read_package(workout_type: str, data) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in training_classes:
        raise ValueError('Неверный идендификатор')
    class_, expected = training_classes[workout_type]
    if len(data) != expected:
        raise ValueError('Некорректное количество аргументов')

    return class_(*data)


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

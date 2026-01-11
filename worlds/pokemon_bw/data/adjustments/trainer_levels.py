from typing import Callable

from .. import TrainerAdjustmentData as TrainerAdjData


adjust_cache: dict[tuple[int, int, int, int], Callable[[int], int]] = {}


def adjust(old_min: int, old_max: int, new_min: int, new_max: int) -> Callable[[int], int]:
    a = (old_min, old_max, new_min, new_max)
    if a not in adjust_cache:
        if old_max == old_min:
            adjust_cache[a] = lambda level: (new_min + new_max) // 2
        else:
            adjust_cache[a] = lambda level: (level - old_min) * (new_max - new_min) // (old_max - old_min) + new_min
    return adjust_cache[a]


adjustments: list[TrainerAdjData] = [
    TrainerAdjData(adjust(34, 35, 3, 4), 531),
    TrainerAdjData(adjust(34, 35, 3, 4), 532),
    TrainerAdjData(adjust(34, 35, 3, 4), 533),

    TrainerAdjData(adjust(32, 35, 2, 5), 432),
    TrainerAdjData(adjust(32, 35, 2, 5), 390),
    TrainerAdjData(adjust(32, 35, 2, 5), 389),
    TrainerAdjData(adjust(32, 35, 2, 5), 413),
    TrainerAdjData(adjust(32, 35, 2, 5), 447),

    TrainerAdjData(adjust(34, 36, 4, 6), 460),
    TrainerAdjData(adjust(34, 36, 4, 6), 439),
    TrainerAdjData(adjust(34, 36, 4, 6), 441),
    TrainerAdjData(adjust(34, 36, 4, 6), 450),
    TrainerAdjData(adjust(34, 36, 4, 6), 445),

    TrainerAdjData(adjust(34, 35, 5, 6), 421),
    TrainerAdjData(adjust(34, 35, 5, 6), 526),

    TrainerAdjData(adjust(63, 65, 9, 11), 419),
    TrainerAdjData(adjust(63, 65, 9, 11), 418),
    TrainerAdjData(adjust(63, 65, 9, 11), 424),
    TrainerAdjData(adjust(63, 65, 9, 11), 417),
    TrainerAdjData(adjust(63, 65, 9, 11), 422),
    TrainerAdjData(adjust(63, 65, 9, 11), 420),
    TrainerAdjData(adjust(63, 65, 9, 11), 423),

    TrainerAdjData(adjust(32, 32, 13, 13), 19),

    TrainerAdjData(adjust(34, 35, 13, 14), 252),
    TrainerAdjData(adjust(34, 35, 13, 14), 253),
    TrainerAdjData(adjust(34, 35, 13, 14), 254),

    TrainerAdjData(adjust(34, 36, 24, 26), 221),
    TrainerAdjData(adjust(34, 36, 24, 26), 222),
    TrainerAdjData(adjust(34, 36, 24, 26), 223),
    TrainerAdjData(adjust(34, 36, 24, 26), 224),
    TrainerAdjData(adjust(34, 36, 24, 26), 225),
    TrainerAdjData(adjust(34, 36, 24, 26), 226),
    TrainerAdjData(adjust(34, 36, 24, 26), 227),

    TrainerAdjData(adjust(33, 34, 30, 31), 255),
    TrainerAdjData(adjust(33, 34, 30, 31), 256),

    TrainerAdjData(adjust(62, 65, 36, 39), 578),
    TrainerAdjData(adjust(62, 65, 36, 39), 262),
    TrainerAdjData(adjust(62, 65, 36, 39), 261),
    TrainerAdjData(adjust(62, 65, 36, 39), 259),
    TrainerAdjData(adjust(62, 65, 36, 39), 260),

    TrainerAdjData(adjust(64, 65, 36, 37), 440),
    TrainerAdjData(adjust(64, 65, 36, 37), 453),
    TrainerAdjData(adjust(64, 65, 36, 37), 437),
    TrainerAdjData(adjust(64, 65, 36, 37), 455),

    TrainerAdjData(adjust(60, 64, 35, 37), 579),
    TrainerAdjData(adjust(60, 64, 35, 37), 580),
    TrainerAdjData(adjust(60, 64, 35, 37), 551),

    TrainerAdjData(adjust(61, 65, 33, 37), 448),
    TrainerAdjData(adjust(61, 65, 33, 37), 452),
    TrainerAdjData(adjust(61, 65, 33, 37), 428),
    TrainerAdjData(adjust(61, 65, 33, 37), 427),
    TrainerAdjData(adjust(61, 65, 33, 37), 451),

    TrainerAdjData(adjust(60, 65, 28, 33), 457),
    TrainerAdjData(adjust(60, 65, 28, 33), 430),
    TrainerAdjData(adjust(60, 65, 28, 33), 416),
    TrainerAdjData(adjust(60, 65, 28, 33), 433),
    TrainerAdjData(adjust(60, 65, 28, 33), 434),
    TrainerAdjData(adjust(60, 65, 28, 33), 446),
    TrainerAdjData(adjust(60, 65, 28, 33), 435),
    TrainerAdjData(adjust(60, 65, 28, 33), 436),
    TrainerAdjData(adjust(60, 65, 28, 33), 449),
    TrainerAdjData(adjust(60, 65, 28, 33), 425),
    TrainerAdjData(adjust(60, 65, 28, 33), 426),
    TrainerAdjData(adjust(60, 65, 28, 33), 414),

    TrainerAdjData(adjust(60, 65, 30, 35), 520),
    TrainerAdjData(adjust(60, 65, 30, 35), 547),
    TrainerAdjData(adjust(60, 65, 30, 35), 524),
    TrainerAdjData(adjust(60, 65, 30, 35), 525),
    TrainerAdjData(adjust(60, 65, 30, 35), 523),
    TrainerAdjData(adjust(60, 65, 30, 35), 548),

    TrainerAdjData(adjust(63, 65, 30, 32), 569),
    TrainerAdjData(adjust(63, 65, 30, 32), 570),
    TrainerAdjData(adjust(63, 65, 30, 32), 571),
    TrainerAdjData(adjust(63, 65, 30, 32), 573),
    TrainerAdjData(adjust(63, 65, 30, 32), 568),
    TrainerAdjData(adjust(63, 65, 30, 32), 572),

    TrainerAdjData(adjust(62, 68, 24, 30), 431),
    TrainerAdjData(adjust(62, 68, 24, 30), 415),
    TrainerAdjData(adjust(62, 68, 24, 30), 577),
    TrainerAdjData(adjust(62, 68, 24, 30), 410),
    TrainerAdjData(adjust(62, 68, 24, 30), 458),
    TrainerAdjData(adjust(62, 68, 24, 30), 411),

    TrainerAdjData(adjust(61, 63, 29, 31), 575),
    TrainerAdjData(adjust(61, 63, 29, 31), 581),
    TrainerAdjData(adjust(61, 63, 29, 31), 574),
    TrainerAdjData(adjust(61, 63, 29, 31), 576),

    TrainerAdjData(adjust(65, 65, 27, 27), 529),
    TrainerAdjData(adjust(65, 65, 27, 27), 530),
    TrainerAdjData(adjust(65, 65, 27, 27), 615),
    TrainerAdjData(adjust(65, 65, 27, 27), 528),

    TrainerAdjData(adjust(30, 67, 26, 31), 463),
    TrainerAdjData(adjust(30, 67, 26, 31), 477),
    TrainerAdjData(adjust(30, 67, 26, 31), 488),
    TrainerAdjData(adjust(30, 67, 26, 31), 471),
    TrainerAdjData(adjust(30, 67, 26, 31), 478),
    TrainerAdjData(adjust(30, 67, 26, 31), 461),
    TrainerAdjData(adjust(30, 67, 26, 31), 472),
    TrainerAdjData(adjust(30, 67, 26, 31), 468),
    TrainerAdjData(adjust(30, 67, 26, 31), 485),
    TrainerAdjData(adjust(30, 67, 26, 31), 481),
    TrainerAdjData(adjust(30, 67, 26, 31), 484),
    TrainerAdjData(adjust(30, 67, 26, 31), 466),
    TrainerAdjData(adjust(30, 67, 26, 31), 487),
    TrainerAdjData(adjust(30, 67, 26, 31), 464),
    TrainerAdjData(adjust(30, 67, 26, 31), 474),
    TrainerAdjData(adjust(30, 67, 26, 31), 490),
    TrainerAdjData(adjust(30, 67, 26, 31), 475),
    TrainerAdjData(adjust(30, 67, 26, 31), 470),
    TrainerAdjData(adjust(30, 67, 26, 31), 479),
    TrainerAdjData(adjust(30, 67, 26, 31), 473),
    TrainerAdjData(adjust(30, 67, 26, 31), 486),
    TrainerAdjData(adjust(30, 67, 26, 31), 483),
    TrainerAdjData(adjust(30, 67, 26, 31), 469),
    TrainerAdjData(adjust(30, 67, 26, 31), 489),
    TrainerAdjData(adjust(30, 67, 26, 31), 465),
    TrainerAdjData(adjust(30, 67, 26, 31), 476),
    TrainerAdjData(adjust(30, 67, 26, 31), 467),
    TrainerAdjData(adjust(30, 67, 26, 31), 462),
    TrainerAdjData(adjust(30, 67, 26, 31), 482),
    TrainerAdjData(adjust(30, 67, 26, 31), 480),

    TrainerAdjData(adjust(62, 65, 23, 26), 429),
    TrainerAdjData(adjust(62, 65, 23, 26), 454),
    TrainerAdjData(adjust(62, 65, 23, 26), 444),
    TrainerAdjData(adjust(62, 65, 23, 26), 456),
    TrainerAdjData(adjust(62, 65, 23, 26), 459),

    TrainerAdjData(adjust(65, 65, 24, 24), 608),
    TrainerAdjData(adjust(65, 65, 24, 24), 609),
]

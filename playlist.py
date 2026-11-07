"""Простой менеджер плейлиста (учебный проект для ЛР2 по ТПОАС)."""
import json
import os
import random


class Track:
    def __init__(self, title, artist, duration):
        if not title or not artist:
            raise ValueError("Название и исполнитель не могут быть пустыми")
        if duration <= 0:
            raise ValueError("Длительность должна быть больше нуля")
        self.title = title
        self.artist = artist
        self.duration = duration  # в секундах

    def to_dict(self):
        return {"title": self.title, "artist": self.artist, "duration": self.duration}

    @staticmethod
    def from_dict(data):
        return Track(data["title"], data["artist"], data["duration"])


def format_duration(seconds):
    """Перевод секунд в строку вида М:СС или Ч:ММ:СС."""
    if seconds < 0:
        raise ValueError("Время не может быть отрицательным")
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


class Playlist:
    def __init__(self, name):
        self.name = name
        self.tracks = []
        self.current = 0
        self.repeat = False

    def add_track(self, track):
        for t in self.tracks:
            if t.title == track.title and t.artist == track.artist:
                return False  # дубликат не добавляем
        self.tracks.append(track)
        return True

    def remove_track(self, index):
        if index < 0 or index >= len(self.tracks):
            raise IndexError("Трека с таким номером нет")
        removed = self.tracks.pop(index)
        if self.current >= len(self.tracks):
            self.current = 0
        return removed

    def total_duration(self):
        return sum(t.duration for t in self.tracks)

    def find_by_artist(self, artist):
        artist = artist.lower()
        return [t for t in self.tracks if t.artist.lower() == artist]

    def next_track(self):
        """Переход к следующему треку. Без повтора в конце списка возвращает None."""
        if not self.tracks:
            return None
        if self.current + 1 < len(self.tracks):
            self.current += 1
        elif self.repeat:
            self.current = 0
        else:
            return None
        return self.tracks[self.current]

    def shuffle(self, seed=None):
        rnd = random.Random(seed)
        rnd.shuffle(self.tracks)
        self.current = 0

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"name": self.name,
                       "tracks": [t.to_dict() for t in self.tracks]},
                      f, ensure_ascii=False, indent=4)

    @staticmethod
    def load(path):
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        pl = Playlist(data["name"])
        for item in data["tracks"]:
            pl.add_track(Track.from_dict(item))
        return pl


if __name__ == "__main__":
    pl = Playlist("Моя музыка")
    pl.add_track(Track("Кукушка", "Кино", 400))
    pl.add_track(Track("Группа крови", "Кино", 286))
    pl.add_track(Track("Звезда", "Ария", 312))
    for i, t in enumerate(pl.tracks, 1):
        print(f"{i}. {t.artist} — {t.title} ({format_duration(t.duration)})")
    print("Общая длительность:", format_duration(pl.total_duration()))

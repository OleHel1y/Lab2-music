import os
import tempfile
import unittest

from playlist import Playlist, Track, format_duration


class TestPlaylist(unittest.TestCase):

    def setUp(self):
        # Перед каждым тестом создаём плейлист из трёх треков
        self.pl = Playlist("Тест")
        self.pl.add_track(Track("Кукушка", "Кино", 400))
        self.pl.add_track(Track("Группа крови", "Кино", 286))
        self.pl.add_track(Track("Звезда", "Ария", 312))

    def test_format_duration_minutes(self):
        self.assertEqual(format_duration(286), "4:46")
        self.assertEqual(format_duration(5), "0:05")

    def test_format_duration_hours(self):
        self.assertEqual(format_duration(3725), "1:02:05")

    def test_track_invalid_duration(self):
        with self.assertRaises(ValueError):
            Track("Песня", "Автор", 0)

    def test_add_duplicate_track(self):
        result = self.pl.add_track(Track("Кукушка", "Кино", 400))
        self.assertFalse(result)
        self.assertEqual(len(self.pl.tracks), 3)

    def test_remove_track(self):
        removed = self.pl.remove_track(1)
        self.assertEqual(removed.title, "Группа крови")
        self.assertEqual(len(self.pl.tracks), 2)

    def test_remove_track_wrong_index(self):
        with self.assertRaises(IndexError):
            self.pl.remove_track(10)

    def test_total_duration(self):
        self.assertEqual(self.pl.total_duration(), 400 + 286 + 312)

    def test_find_by_artist_ignore_case(self):
        found = self.pl.find_by_artist("кИнО")
        self.assertEqual(len(found), 2)

    def test_next_track_with_and_without_repeat(self):
        self.pl.next_track()
        self.pl.next_track()                 # дошли до последнего
        self.assertIsNone(self.pl.next_track())   # без повтора — конец
        self.pl.repeat = True
        self.assertEqual(self.pl.next_track().title, "Кукушка")  # с повтором — в начало

    def test_save_and_load(self):
        path = os.path.join(tempfile.mkdtemp(), "playlist.json")
        self.pl.save(path)
        loaded = Playlist.load(path)
        self.assertEqual(loaded.name, "Тест")
        self.assertEqual([t.title for t in loaded.tracks],
                         [t.title for t in self.pl.tracks])


if __name__ == "__main__":
    unittest.main(verbosity=2)

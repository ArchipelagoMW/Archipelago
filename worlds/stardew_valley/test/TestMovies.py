from .bases import SVTestBase
from .. import SeasonRandomization
from ..data.movies import movies_by_name
from ..options import Moviesanity


class MovieTestBase(SVTestBase):

    def test_all_movies_require_theater_and_season(self):
        if Moviesanity.internal_name not in self.options or self.options[Moviesanity.internal_name] == Moviesanity.option_none:
            return
        self.collect_lots_of_money(0.5)
        [self.collect(snack) for snack in ["Movie Drinks", "Movie Sweet Snacks", "Movie Salty Snacks"]]
        theater_items = [self.create_item("Progressive Movie Theater"), self.create_item("Progressive Movie Theater")]
        [self.remove_one_by_name(season) for season in ["Spring", "Summer", "Fall", "Winter"]]
        for movie_name in movies_by_name:
            movie = movies_by_name[movie_name]
            movie_location = f"Watch {movie_name}"
            self.collect(movie.season)
            with self.subTest(f"{movie_location} requires two movie theaters"):
                self.assert_cannot_reach_location(movie_location)
                self.collect(theater_items[0])
                self.assert_cannot_reach_location(movie_location)
                self.collect(theater_items[1])
                self.assert_can_reach_location(movie_location)
            self.remove_one_by_name(movie.season)
            with self.subTest(f"{movie_location} requires {movie.season}"):
                self.assert_cannot_reach_location(movie_location)
                self.collect(movie.season)
                self.assert_can_reach_location(movie_location)
            self.remove(theater_items)
            self.remove_one_by_name(movie.season)


class TestOneMovie(SVTestBase):
    options = {
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized,
        Moviesanity.internal_name: Moviesanity.option_one
    }

    def test_all_movies_require_theater_and_season(self):
        self.collect_lots_of_money(0.5)
        theater_items = [self.create_item("Progressive Movie Theater"), self.create_item("Progressive Movie Theater")]
        movie_location = f"Watch A Movie"
        with self.subTest(f"{movie_location} requires two movie theaters"):
            self.assert_cannot_reach_location(movie_location)
            self.collect(theater_items[0])
            self.assert_cannot_reach_location(movie_location)
            self.collect(theater_items[1])
            self.assert_can_reach_location(movie_location)


class TestAllMovies(MovieTestBase):
    options = {
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized,
        Moviesanity.internal_name: Moviesanity.option_all_movies
    }


class TestAllMoviesLoved(MovieTestBase):
    options = {
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized,
        Moviesanity.internal_name: Moviesanity.option_all_movies_loved
    }


class TestAllMoviesAndAllSnacks(MovieTestBase):
    options = {
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized,
        Moviesanity.internal_name: Moviesanity.option_all_movies_and_all_snacks
    }


class TestAllMoviesWithLovedSnack(MovieTestBase):
    options = {
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized,
        Moviesanity.internal_name: Moviesanity.option_all_movies_with_loved_snack
    }


class TestAllMoviesAndAllLovedSnacks(MovieTestBase):
    options = {
        SeasonRandomization.internal_name: SeasonRandomization.option_randomized,
        Moviesanity.internal_name: Moviesanity.option_all_movies_and_all_loved_snacks
    }
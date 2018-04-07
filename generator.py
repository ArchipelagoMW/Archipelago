from allocation import Allocation
from analyzer import Analyzer
from difficultyanalysis import DifficultyAnalysis
from utility import fail
import time
import random

class Generator(object):
    def __init__(self, data, settings):
        self.data = data
        self.settings = settings
        self.allocation = Allocation(data, settings)

    def generate_seed(self):
        MAX_ATTEMPTS = self.settings.max_attempts
        success = False

        start_time = time.time()
        for attempts in range(MAX_ATTEMPTS):

            self.shuffle()
            analyzer = Analyzer(self.data, self.settings, self.allocation)
            if analyzer.success:
                if not self.settings.egg_goals:
                    success = True
                shift_success, goal_eggs = self.shift_eggs_to_hard_to_reach(analyzer.reachable, analyzer.hard_to_reach_items)
                if shift_success:
                    analyzer = Analyzer(self.data, self.settings, self.allocation, goals=goal_eggs)
                    if analyzer.success:
                        success = True

            if success:
                difficulty_analysis = None
                if not self.settings.hide_difficulty or self.settings.min_difficulty > 0 or self.settings.max_breakability != None:
                    # Run difficulty analysis
                    if self.settings.egg_goals: goals = analyzer.goals
                    else: goals = analyzer.hard_to_reach_items
                    difficulty_analysis = DifficultyAnalysis(self.data, analyzer, goals)

                if self.settings.min_difficulty > 0:
                    if difficulty_analysis.difficulty_score < self.settings.min_difficulty:
                        success = False

                if self.settings.max_breakability != None:
                    if difficulty_analysis.breakability_score > self.settings.max_breakability:
                        success = False

            if success:
                break
                    

        if not success:
            fail('Unable to generate a valid seed after %d attempts.' % MAX_ATTEMPTS)

        time_taken = time.time() - start_time
        time_string = '%.2f seconds' % (time_taken)

        print('Seed generated after %d attempts in %s' % (attempts+1, time_string))

        # Generate Visualization and Print Output:
        if False:
            Analyzer(self.data, self.allocation, visualize=True)
            self.allocation.print_important_item_locations()

        return self.allocation, analyzer, difficulty_analysis

    def shuffle(self):
        self.allocation.shuffle(self.data, self.settings)

    def shift_eggs_to_hard_to_reach(self, reachable_items, hard_to_reach_items):
        return self.allocation.shift_eggs_to_hard_to_reach(self.data, self.settings, reachable_items, hard_to_reach_items)


from dataparser import KNOWLEDGE_INTERMEDIATE, KNOWLEDGE_ADVANCED, DIFFICULTY_HARD, DIFFICULTY_V_HARD, DIFFICULTY_STUPID
from utility import fail
import statistics

class DifficultyConfig(object):
    def __init__(self, weight, config_flags, score_multiplier_diff=0.5):
        self.weight = weight
        self.config_flags = config_flags
        self.score_multiplier_diff = score_multiplier_diff


DIFFICULTY_CONFIGS = [

    # Level 0 - most basic
    DifficultyConfig(
        weight=0.8,
        config_flags = {
            "ZIP_REQUIRED": False,
            "SEMISOLID_CLIPS_REQUIRED": False,
            "BLOCK_CLIPS_REQUIRED": False,
            "POST_GAME_ALLOWED": False,
            "POST_IRISU_ALLOWED": False,
            "HALLOWEEN_REACHABLE": False,
            "PLURKWOOD_REACHABLE": False,
            "WARP_DESTINATION_REACHABLE": False,
            "DARKNESS_WITHOUT_LIGHT_ORB": False,
            "UNDERWATER_WITHOUT_WATER_ORB": False,
            "EVENT_WARPS_REQUIRED": False,
            KNOWLEDGE_INTERMEDIATE: False,
            KNOWLEDGE_ADVANCED: False,
            DIFFICULTY_HARD: False,
            DIFFICULTY_V_HARD: False,
            DIFFICULTY_STUPID: False,
        },
        score_multiplier_diff=0,
    ),

    # Level 1 - intermediate
    DifficultyConfig(
        weight=1.0,
        config_flags = {
            "ZIP_REQUIRED": False,
            "SEMISOLID_CLIPS_REQUIRED": False,
            "BLOCK_CLIPS_REQUIRED": False,
            "POST_GAME_ALLOWED": False,
            "POST_IRISU_ALLOWED": False,
            "HALLOWEEN_REACHABLE": False,
            "PLURKWOOD_REACHABLE": False,
            "WARP_DESTINATION_REACHABLE": False,
            "DARKNESS_WITHOUT_LIGHT_ORB": False,
            "UNDERWATER_WITHOUT_WATER_ORB": False,
            "EVENT_WARPS_REQUIRED": False,
            KNOWLEDGE_INTERMEDIATE: True,
            KNOWLEDGE_ADVANCED: False,
            DIFFICULTY_HARD: True,
            DIFFICULTY_V_HARD: False,
            DIFFICULTY_STUPID: False,
        },
        score_multiplier_diff=0.1,
    ),

    # Level 2 - intermediate and easy flags
    DifficultyConfig(
        weight=1.0,
        config_flags = {
            "ZIP_REQUIRED": False,
            "SEMISOLID_CLIPS_REQUIRED": False,
            "BLOCK_CLIPS_REQUIRED": True,
            "POST_GAME_ALLOWED": False,
            "POST_IRISU_ALLOWED": False,
            "HALLOWEEN_REACHABLE": False,
            "PLURKWOOD_REACHABLE": True,
            "WARP_DESTINATION_REACHABLE": False,
            "DARKNESS_WITHOUT_LIGHT_ORB": True,
            "UNDERWATER_WITHOUT_WATER_ORB": True,
            "EVENT_WARPS_REQUIRED": False,
            KNOWLEDGE_INTERMEDIATE: True,
            KNOWLEDGE_ADVANCED: False,
            DIFFICULTY_HARD: True,
            DIFFICULTY_V_HARD: False,
            DIFFICULTY_STUPID: False,
        },
        score_multiplier_diff=0.0,
    ),

    # Level 3 - advanced tricks, zips, clips and event warps
    DifficultyConfig(
        weight=1.0,
        config_flags = {
            "ZIP_REQUIRED": True,
            "SEMISOLID_CLIPS_REQUIRED": True,
            "BLOCK_CLIPS_REQUIRED": True,
            "POST_GAME_ALLOWED": False,
            "POST_IRISU_ALLOWED": False,
            "HALLOWEEN_REACHABLE": False,
            "PLURKWOOD_REACHABLE": True,
            "WARP_DESTINATION_REACHABLE": False,
            "DARKNESS_WITHOUT_LIGHT_ORB": True,
            "UNDERWATER_WITHOUT_WATER_ORB": True,
            "EVENT_WARPS_REQUIRED": True,
            KNOWLEDGE_INTERMEDIATE: True,
            KNOWLEDGE_ADVANCED: True,
            DIFFICULTY_HARD: True,
            DIFFICULTY_V_HARD: False,
            DIFFICULTY_STUPID: False,
        },
        score_multiplier_diff=0.3,
    ),

    # Level 4 - VHARD tricks
    DifficultyConfig(
        weight=1.0,
        config_flags = {
            "ZIP_REQUIRED": True,
            "SEMISOLID_CLIPS_REQUIRED": True,
            "BLOCK_CLIPS_REQUIRED": True,
            "POST_GAME_ALLOWED": False,
            "POST_IRISU_ALLOWED": False,
            "HALLOWEEN_REACHABLE": False,
            "PLURKWOOD_REACHABLE": True,
            "WARP_DESTINATION_REACHABLE": False,
            "DARKNESS_WITHOUT_LIGHT_ORB": True,
            "UNDERWATER_WITHOUT_WATER_ORB": True,
            "EVENT_WARPS_REQUIRED": True,
            KNOWLEDGE_INTERMEDIATE: True,
            KNOWLEDGE_ADVANCED: True,
            DIFFICULTY_HARD: True,
            DIFFICULTY_V_HARD: True,
            DIFFICULTY_STUPID: False,
        },
        score_multiplier_diff=0.45,
    ),


    # Level 5 - STUPID and everything else.
    DifficultyConfig(
        weight=0.5,
        config_flags = {
            "ZIP_REQUIRED": True,
            "SEMISOLID_CLIPS_REQUIRED": True,
            "BLOCK_CLIPS_REQUIRED": True,
            "POST_GAME_ALLOWED": True,
            "POST_IRISU_ALLOWED": True,
            "HALLOWEEN_REACHABLE": True,
            "PLURKWOOD_REACHABLE": True,
            "WARP_DESTINATION_REACHABLE": True,
            "DARKNESS_WITHOUT_LIGHT_ORB": True,
            "UNDERWATER_WITHOUT_WATER_ORB": True,
            "EVENT_WARPS_REQUIRED": True,
            KNOWLEDGE_INTERMEDIATE: True,
            KNOWLEDGE_ADVANCED: True,
            DIFFICULTY_HARD: True,
            DIFFICULTY_V_HARD: True,
            DIFFICULTY_STUPID: True,
        },
        score_multiplier_diff=0.7,
    ),
]
MAX_CONFIG_LEVEL = len(DIFFICULTY_CONFIGS)


class DifficultyAnalysis(object):

    def __init__(self, data, analyzer, goals):
        self.data = data
        self.analyzer = analyzer
        self.goals = set(goals)
        self.level_scores = None
        self.current_config_score = None

        self.difficulty_score = self._compute_difficulty()
        self.breakability_score = self._compute_breakability()

    def _compute_difficulty(self):
        total_weight = sum(config.weight for config in DIFFICULTY_CONFIGS)
        self._compute_all_level_scores()

        # We take the weighted mean of the square roots to reduce the weight of outliers.
        total_weighted_score = sum(config.weight*level_score**0.5 for config, level_score in zip(DIFFICULTY_CONFIGS, self.level_scores))
        return (total_weighted_score / total_weight)**2

    def _compute_breakability(self):
        self._compute_all_level_scores()
        #self._compute_current_config_score()
        score = self.difficulty_score

        score_diffs = [score-x for x in self.level_scores]
        score_diffs = [x for x in score_diffs if x > 0]

        breakability_score = 0
        if len(score_diffs) > 0:
            breakability_score = statistics.mean(score_diffs)
        return breakability_score

    def _compute_current_config_score(self):
        if self.current_config_score != None: return
        variables = self.data.generate_variables()
        reachable, unreachable, levels, new_variables = self.analyzer.analyze_with_variable_set(variables)
        self.current_config_score = compute_average_goal_level(self.goals, levels)

    def _compute_all_level_scores(self):
        if self.level_scores != None: return
        self.level_scores = [self._compute_level_score(k) for k in range(MAX_CONFIG_LEVEL)]
        #print_ln(self.level_scores)

    def _compute_level_score(self, base_config_level):
        analyzer = self.analyzer
        goals = self.goals

        variables = self.data.generate_pessimistic_variables()

        score_multiplier = 1
        score = 0
        #print_ln('== Base %d ==' % base_config_level)
        for config_level in range(base_config_level, MAX_CONFIG_LEVEL):
            configure_variables(config_level, variables)
            reachable, unreachable, levels, new_variables = analyzer.analyze_with_variable_set(variables)
            #print_ln('level %d' % config_level)
            if goals.issubset(reachable):
                #print_ln('  pass - levels: %d' % len(levels))
                #print_ln('  average goal level: %f' % compute_average_goal_level(goals, levels))
                #for en, level in enumerate(levels):
                    #print_ln('LEVEL %.1f' % (en/2))
                    #print_ln(level)
                score += compute_average_goal_level(goals, levels)*score_multiplier
                break
            #print_ln('  fail - levels: %d' % len(levels))
            
            if config_level >= MAX_CONFIG_LEVEL-1: fail('Unable to reach goals at max config level')
            score += len(levels)/2 * score_multiplier
            score_multiplier += DIFFICULTY_CONFIGS[config_level+1].score_multiplier_diff
            variables = new_variables
        #print_ln('Final Score: %f' % score)

        return score

def compute_average_goal_level(goals, levels):
    count = 0
    total = 0

    for level, variable_list in enumerate(levels):
        goals_in_level = len(goals.intersection(variable_list))
        count += goals_in_level
        total += goals_in_level*level/2

    return total/count

def configure_variables(config_level, variables):
    config_flags = DIFFICULTY_CONFIGS[config_level].config_flags
    length_check_before = len(variables)
    variables.update(config_flags)
    if len(variables) != length_check_before:
        fail('Unknown config flags detected!')


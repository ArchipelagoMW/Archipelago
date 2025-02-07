# Junk Definitions
one_up_mushroom  = "1-Up Mushroom"
one_coin = "1 coin"
five_coins = "5 coins"
ten_coins = "10 coins"
fifty_coins = "50 coins"

# Collectable Definitions
yoshi_egg = "Yoshi Egg"

# Upgrade Definitions
mario_run           = "Run"
mario_carry         = "Carry"
mario_swim          = "Swim"
mario_spin_jump     = "Spin Jump"
mario_climb         = "Climb"
yoshi_activate      = "Yoshi"
p_switch            = "P-Switch"
p_balloon           = "P-Balloon"
progressive_powerup = "Progressive Powerup"
super_star_active   = "Super Star Activate"

# Switch Palace Definitions
yellow_switch_palace = "Yellow Switch Palace"
green_switch_palace  = "Green Switch Palace"
red_switch_palace    = "Red Switch Palace"
blue_switch_palace   = "Blue Switch Palace"

# Special Zone clear flag definition
special_world_clear = "Special Zone Clear"

# Trap Definitions
ice_trap              = "Ice Trap"
stun_trap             = "Stun Trap"
literature_trap       = "Literature Trap"
timer_trap            = "Timer Trap"
reverse_controls_trap = "Reverse Trap"
thwimp_trap           = "Thwimp Trap"

# Other Definitions
victory   = "The Princess"
koopaling = "Boss Token"

smw_item_groups = {
    "Upgrades": {
        mario_run, mario_carry, mario_swim, mario_spin_jump, mario_climb,
        yoshi_activate, p_switch, p_balloon, progressive_powerup, super_star_active,
    },
    "Switch Palaces": {
        yellow_switch_palace, green_switch_palace, red_switch_palace, blue_switch_palace
    },
    "Collectables": {
        yoshi_egg
    },
    "Junk": {
        one_up_mushroom,
        one_coin, five_coins, ten_coins, fifty_coins,
    },
    "Traps": {
        ice_trap, stun_trap, literature_trap,
        timer_trap, reverse_controls_trap, thwimp_trap,
    },
    "Events": {
        victory, koopaling
    }
}

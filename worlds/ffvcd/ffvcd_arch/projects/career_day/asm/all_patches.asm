; init
print "TEST"
incsrc ../../shared_asm/shared_core/defines.asm
incsrc core_code/init.asm

; priority writes
incsrc core_code/relocate_conditional_events.asm
incsrc ../../shared_asm/data_tables/starting_stats.asm

if !fourjobmode == 1
    if !fourjoblock == 1
        ; four job lock is only for when there are 4 unique jobs. Otherwise disable (for 1, 2 or 3 jobs in "fjf" mode)
        incsrc open_world/4_job_lock.asm
    endif
endif

if !remove_flashes == 1
    incsrc open_world/remove_flashes.asm
endif

if !kuzar_credits_warp == 1
    incsrc open_world/kuzar_credits_warp.asm
endif

; world 1                                   Destinations:
incsrc world1/tycoon_meteor_01_mount.asm
incsrc world1/tycoon_meteor_02_mount.asm
incsrc world1/tycoon_meteor_03_battle.asm
incsrc world1/tycoon_meteor_galuf_wakeup.asm ; 01 Pirate's Hideout
incsrc world1/first_save_point.asm           
incsrc world1/spring.asm
incsrc world1/pass_end.asm
incsrc world1/pass_first_hole.asm
incsrc world1/pirate_button.asm
incsrc world1/pirate_cove_outside.asm
incsrc world1/pirate_ship.asm                            ; 02 Wind Shrine
incsrc world1/pirate_ship_out_window.asm
incsrc world1/sleeping_pirates.asm 
incsrc world1/pirate_cove_outside_return.asm
incsrc world1/boko_resting.asm
incsrc world1/leaving_zokks_house_early.asm

incsrc world1/wind_shrine_chancellor.asm
incsrc world1/wing_raptor.asm           
incsrc world1/wind_crystal.asm
incsrc world1/leaving_wind_shrine.asm                ; 03 Tule

incsrc world1/tule.asm                                     ; 04 Torna Canal
incsrc world1/after_tule_boat_cutscene.asm
incsrc world1/canal_gate.asm                           ; 05 Ship Graveyard        

incsrc world1/faris_is_a_girl.asm                 
incsrc world1/faris_wet.asm
incsrc world1/siren.asm                                    ; 06 Hiryuu Mountain

incsrc world1/magisa.asm
incsrc world1/hiryuu_north_mountain.asm            ; 07 Walse Castle
incsrc world1/carwen_lady.asm  

incsrc world1/walse_tower.asm
incsrc world1/walse_king_post_tower.asm       
incsrc world1/walse_meteor_falls.asm                   ; 08 Walse Tower
incsrc world1/lone_wolf_text.asm
incsrc world1/lone_wolf_cell_trap_disable.asm
incsrc world1/guy_next_to_lone_wolf.asm
incsrc world1/walse_tower_sinking.asm
incsrc world1/water_crystal.asm                          ; 09 Walse Meteor
incsrc world1/whirlpool.asm
incsrc world1/walse_meteor_first_warp.asm           ; 0A Karnak Town

incsrc world1/karnak_arrest.asm                          ; 0B Karnak Steamship
incsrc world1/cid_in_cell.asm
incsrc world1/karnak_queen_fight.asm
incsrc world1/karnak_werewolf.asm
incsrc world1/cid_mid_in_airship.asm                    ; 0C Ancient Library
incsrc world1/cid_on_steamship.asm
incsrc world1/steamship_accelerator.asm
incsrc world1/fire_crystal.asm
incsrc world1/after_karnak_escape.asm
incsrc world1/karnak_escape_boss.asm ; (keep this order for boss after escape here)

incsrc world1/ancient_library.asm
incsrc world1/ifrit.asm
incsrc world1/byblos.asm                                   
incsrc world1/mid_after_byblos.asm					   ; 0D Karnak Pub
incsrc world1/mid_with_book.asm                        ; 0E Karnak Steamship
incsrc world1/mid_cid_wakeup.asm                       
incsrc world1/steamship_repair.asm                     ; 0F Crescent Island

incsrc world1/first_entering_crescent.asm             
incsrc world1/black_chocobo.asm                        ; 10 Ancient Library
incsrc world1/lix.asm
incsrc world1/telling_mid_cid_about_steamship.asm      ; 11 Desert

incsrc world1/sandworm.asm                              
incsrc world1/ruined_city.asm
incsrc world1/teleporter_beneath_ruined_city.asm
incsrc world1/catapult_inn.asm
incsrc world1/steamship_under_crescent.asm 
incsrc world1/airship_discovery.asm
incsrc world1/cid_on_flying_ship.asm          					  ; 11 Desert
incsrc world1/ruined_city_rising.asm							  ; 14 Crescent Island
incsrc world1/cid_mid_after_city_flies.asm    	                   ; 13 Tycoon Meteor
incsrc world1/galuf_opening_meteor.asm
incsrc world1/adamantium_get.asm                               
incsrc world1/adamantoise.asm                                    ; 14 Crescent Island
incsrc world1/upgrading_ship.asm                               ; 12 Lonka Ruins (Ascend)
incsrc world1/sol_cannon.asm

incsrc world1/archeoavis.asm
incsrc world1/earth_crystal.asm                          ; 16 Four Meteors
incsrc world1/tycoon_return.asm
incsrc world1/tycoon_meteor_afterearth.asm         
incsrc world1/walse_meteor_afterearth.asm          
incsrc world1/karnak_meteor_afterearth.asm
incsrc world1/ruins_meteor_afterearth.asm           ; 17 Bahamut Peninsula 


; world 2
incsrc world2/exdeathcastle1_gilgamesh.asm
incsrc world2/bigbridge_gilgamesh2.asm
incsrc world2/bigbridge_endofbridge.asm                ; 19 Moogle Forest

incsrc world2/moogleforest_firstmeet.asm               
incsrc world2/mooglewaterway_afterboss.asm         ; 1A Moogle Village
incsrc world2/mooglewaterway_beforeboss.asm
incsrc world2/mooglevillage_to_castlebal.asm           ; 1B Hiryuu Mountain

incsrc world2/kuzar_firstvisit.asm

incsrc world2/balcastle_leavegates.asm
incsrc world2/kelb_firstvisit.asm
incsrc world2/hiryuuvalley_end.asm                         ; 1C Bal Castle
incsrc world2/bal_revisit.asm 
incsrc world2/bal_hiryuuobtain.asm                         ; 1D Guido Cave
incsrc world2/guido_firstvisit.asm                           ; 1E Zeza Fleet
incsrc world2/zezafleet_battle.asm                         ; 1F Zeza Fleet Cabins
incsrc world2/zezafleet_enter.asm
incsrc world2/zezafleet_sleep.asm
incsrc world2/zeza_entertower.asm                       ; 20 Barrier Tower
incsrc world2/barriertower_inside.asm        
incsrc world2/barriertower_top.asm                       ; 21 Submerged Guido Cave
incsrc world2/guido_chests.asm                          
incsrc world2/guido_firsttalk.asm                          ; 22 Mua Forest
incsrc world2/muaforest_enter.asm
incsrc world2/muaforest_fire.asm  
incsrc world2/muaforest_boss.asm                         ; 23 Exdeath Castle
incsrc world2/exdeathcastle2_gilgamesh.asm
incsrc world2/exdeathcastle2_transform.asm
incsrc world2/exdeathcastle2_keyitems.asm
incsrc world2/exdeathcastle2_boss_w3.asm             ; 24 Tycoon Castle

; world 3
incsrc world3/tycoon_w3_cutscenes.asm                  ; 25 Guido Cave
incsrc world3/boco_w3.asm
incsrc world3/antlion_cutscenes.asm
incsrc world3/boko_after_antlion.asm
incsrc world3/w3_guido.asm                                   ; 26 Pyramid
incsrc world3/guido_text_after_giving_book.asm

incsrc world3/pyramid_enter.asm
incsrc world3/pyramid_top.asm                               ; 27 Airship

incsrc world3/merugene.asm
incsrc world3/w3_airshipget.asm                               ; 28 Cleft / Tablets

incsrc world3/solitaryisland_enter.asm
incsrc world3/secondtablet.asm
incsrc world3/forktower.asm
incsrc world3/w3_getsub.asm
incsrc world3/istoryfalls_end.asm
incsrc world3/istoryfalls_enter.asm
incsrc world3/greattrench_end.asm
incsrc world3/greattrench_enter.asm
incsrc world3/northmountain_bahamut.asm
incsrc world3/phoenixtower.asm
incsrc world3/kuzar.asm

incsrc world3/cleft_apanda.asm
incsrc world3/cleft_calofisteri.asm
incsrc world3/cleft_catastroph.asm
incsrc world3/cleft_enter.asm
incsrc world3/cleft_apocalypse.asm
incsrc world3/cleft_halicarnaso.asm
incsrc world3/cleft_halicarnassus.asm
incsrc world3/cleft_twintania.asm
incsrc world3/cleft_necrophobe.asm

; other patches

incsrc core_code/menu_hook.asm
incsrc core_code/battle_code.asm
incsrc core_code/custom_items.asm
incsrc core_code/utility.asm

incsrc ../../shared_asm/shared_core/reward_manager.asm
incsrc ../../shared_asm/shared_core/new_event.asm
incsrc ../../shared_asm/shared_core/encounter_toggle.asm
incsrc ../../shared_asm/shared_core/walk_speed.asm
incsrc ../../shared_asm/shared_core/chest_magicreward.asm
incsrc ../../shared_asm/shared_core/shop_hook.asm
incsrc ../../shared_asm/shared_core/battle_hook.asm
incsrc ../../shared_asm/balancing/exp_abp_modifier.asm

incsrc ../../shared_asm/recovery/all_inns.asm
incsrc ../../shared_asm/recovery/tent.asm



; optionals
if !learning = 1
	incsrc ../../shared_asm/optionals/learning.asm
endif
if !passages = 1
	incsrc ../../shared_asm/optionals/passages.asm
endif
if !pitfalls = 1
	incsrc ../../shared_asm/optionals/pitfalls.asm
endif
if !double_atb = 1
	incsrc ../../shared_asm/optionals/double_atb.asm
endif


; reward events
incsrc reward_events/piratescave_syldra.asm
incsrc reward_events/balcastle_odin.asm
incsrc reward_events/forktower_holyflare.asm
incsrc reward_events/istory_lovesong.asm
incsrc reward_events/kelb_cornajar.asm
incsrc reward_events/kelb_requiem.asm
incsrc reward_events/lix_temptationsong.asm
incsrc reward_events/miragevillage_miragevest.asm
incsrc reward_events/pirate_potions.asm
incsrc reward_events/piratescave_syldra.asm
incsrc reward_events/rugor_ribbon.asm
incsrc reward_events/surgate_speedsong.asm
incsrc reward_events/tycoon_chancellor_reward.asm
incsrc reward_events/windshrine_potions.asm
incsrc reward_events/ancientlibrary_magicsong.asm
incsrc reward_events/balcastle_odin.asm
incsrc reward_events/crescent_herosong.asm
incsrc reward_events/crescent_lifesong.asm
incsrc reward_events/crescent_powersong.asm
incsrc reward_events/crescent_powerherosongs.asm
incsrc reward_events/exdeathcastle_carbuncle.asm
incsrc reward_events/walse_shiva.asm
incsrc reward_events/watercrystal_obtainshards.asm
incsrc reward_events/chicken_knife_brave_blade.asm
incsrc reward_events/walsetower_gogo.asm
incsrc reward_events/tycoon_hiddenarea.asm
incsrc reward_events/istory_toad.asm
incsrc reward_events/aegis_shield.asm
incsrc reward_events/carwen_lone_wolf_barrel.asm
incsrc reward_events/bal_epee.asm
incsrc reward_events/jacole_thunder_whip.asm
incsrc reward_events/lamia_harp_bal.asm
incsrc reward_events/magic_lamp.asm

; open world
incsrc open_world/canal_fix.asm
incsrc open_world/key_items.asm
incsrc open_world/key_item_locks.asm
incsrc open_world/npc_locks.asm
incsrc open_world/open_world.asm
incsrc open_world/default_airship_down.asm
incsrc open_world/intro_cutscene.asm
incsrc open_world/tutorial_beginner_house.asm
incsrc open_world/world1_to_world2_warp.asm
incsrc open_world/world2_to_world1_warp.asm
incsrc open_world/world3_to_world2_warp.asm
incsrc open_world/pyramid_disable.asm
incsrc open_world/custom_lock_cutscenes.asm
incsrc open_world/warp_area.asm
; incsrc open_world/debug_key_items.asm
incsrc open_world/exdeath_overwrite.asm
incsrc core_code/credits.asm
incsrc open_world/summon_bosses.asm
incsrc open_world/gargoyles_restructure.asm
; incsrc open_world/bal_castle_timerguard.asm
incsrc open_world/phoenix_tower.asm
incsrc open_world/custom_enemies.asm
incsrc open_world/boss_portal.asm
incsrc open_world/enemy_dialogue_hook.asm

; these were first included as source code, but it was a pain in the ass
; since they werent made with asar 
; so now theyre just separate patches 


; incsrc open_world/ff5_sortplus.asm
; incsrc open_world/ff5_lr_menu.asm
; incsrc open_world/ff5_items_total.asm
; incsrc open_world/ff5_hp_color.asm
; incsrc open_world/ff5_optimize.asm
; incsrc open_world/ff5_reequip.asm

incsrc world2/mooglewaterway_encounters.asm


; text tables
incsrc ../../shared_asm/text_tables/destination_table.asm
incsrc ../../shared_asm/text_tables/ability_shop_table.asm
incsrc ../../shared_asm/text_tables/ability_chest_table.asm
incsrc ../../shared_asm/text_tables/job_shop_table.asm
incsrc ../../shared_asm/text_tables/job_chest_table.asm
incsrc ../../shared_asm/text_tables/magic_chest_table.asm
incsrc tables/key_item_tables.asm
incsrc ../../shared_asm/text_tables/misc_text.asm
incsrc tables/misc_open_world_text.asm

; other tables
incsrc ../../shared_asm/data_tables/progressive_ability_table.asm
incsrc ../../shared_asm/data_tables/progressive_magic_table.asm
incsrc ../../shared_asm/data_tables/magic_ability_crystal_shop_prices.asm
incsrc ../../shared_asm/data_tables/original_magic_prices.asm
incsrc ../../shared_asm/data_tables/shop_prices.asm
if !explv50 = 1
    incsrc ../../shared_asm/data_tables/exp_table_lv50_modified.asm
endif

incsrc ../../shared_asm/colors/galuf_mimic.asm



; music

; incsrc music/music_data.asm
; incsrc music/music_patch.asm
; incsrc music/music_switch.asm

; addresses 

!ADDRESS_expmod = $F00300
!ADDRESS_abpmod = $F00100
!ADDRESS_progressiverewards = $F02000
!ADDRESS_chesthook = $F03000
!ADDRESS_chesthook_mib = $F031A0
!ADDRESS_chesthook_mib_disable_on_reward_new_regular_item = $F032A0
!ADDRESS_chesthook_new_reward_had_prior_item = $F03300
!ADDRESS_chesthook_new_reward_had_prior_item2 = $F03350
!ADDRESS_chesthook_new_reward_had_prior_item3 = $F03400
!ADDRESS_reset_unusedram3 = $F03500


!ADDRESS_jobindexing = $F00400
!ADDRESS_magicreward = $F00480
!ADDRESS_double_atb = $F004A0
; !ADDRESS_shoatsound = $F01200
!ADDRESS_customitem1 = $F01640
!ADDRESS_customitem2 = $F01300
!ADDRESS_battlehook = $F01380
!ADDRESS_STARTROM = $FF0000
!ADDRESS_ENDROM = $FFFFFF
!ADDRESS_shopindexing = $F00980
!ADDRESS_encounterhook = $F00000
!ADDRESS_worldmaphook = $F00050
!ADDRESS_innhook = $F00270
!ADDRESS_innhook2 = $F002E0
!ADDRESS_innhook3 = $F00340
!ADDRESS_menuhook = $F00500
!ADDRESS_NEWEVENT_jobsetting = $F00F00
!ADDRESS_NEWEVENT_namevalidation = $F00C80
!ADDRESS_NPC_LOCKS = $F01B00
!ADDRESS_NEWEVENT_conditionalvehicles = $F01100
!ADDRESS_NEWEVENT_conditionaleventflags = $F01180
!ADDRESS_NEWEVENT_conditionalrifttablet = $F01800
!ADDRESS_originalmagicprices = $F80000
!ADDRESS_phoenixtowername = $F80900
!ADDRESS_startingcharstats = $F81000
!ADDRESS_startingcharstatsindex = $F80F00
!ADDRESS_useableitemstable = $F83500
!ADDRESS_shophook = $F00680
!ADDRESS_shopcheckreward = $F00700
!ADDRESS_shopawardreward = $F00800
!ADDRESS_shopmagicsword = $F00900
!ADDRESS_walkspeedhook = $F00180
!ADDRESS_walkspeedtownhook = $F001E0
!ADDRESS_airshipslowdown = $F00200
!ADDRESS_canalfix = $F10000
!ADDRESS_keyitems = $F00A00
!ADDRESS_xycoordhook = $F01900
!ADDRESS_keyitemlocks = $F01400
!ADDRESS_menusummonsfix = $F01200
!ADDRESS_newevent_randomstart = $F01B80
!ADDRESS_PROJECT_DEMI_DUMMYSPACE = $F01C00
!ADDRESS_music_instrument_song_indices = $FC0000
!ADDRESS_music_song_pointers = $FC1000
!ADDRESS_music_instrument_pointers = $FC1B00
!ADDRESS_music_loop_sample_length = $FC1D00
!ADDRESS_music_sample_rate = $FC1E00
!ADDRESS_music_asdr = $FC1F00
!ADDRESS_music_custom_song_data = $FC2000
!ADDRESS_music_custom_sample_data = $FD0000


!RELOCATE_conditional_events = $F04000
!RELOCATE_conditional_events_le = $00, $40, $F0
!RELOCATE_conditional_events_le_offset1 = $01, $40, $F0
!RELOCATE_conditional_events_le_offset2 = $02, $40, $F0
!RELOCATE_conditional_events_le_offset3 = $03, $40, $F0

; ram_values

!unlockedjobs1 = $0840
!unlockedjobs2 = $0841
!unlockedjobs3 = $0842
!eventflags = $0A4A
!rewardid = $12
!typeid = $11
!nonmagicrewardindex = $16A2
!magicrewardindex = $16A3
!rewardconfig = $0970
!loopcounter = $1ED7
!progmagicentry = $1ED8
!progmagicentry2 = $1ED9
!progabilityentry = $1ED8
!progabilityentry2 = $1ED9
!currentability = $1ED6
!progmagictable = $F80400
!progabilitytable = $F80600
!currentmagic = $1ED6
!unlockedmagic = $0950

!unlockedability = $08F7
!1pabilities = $08F7
!2pabilities = $090B
!3pabilities = $091F
!4pabilities = $0933

!1pabilitiescount = $08F3
!2pabilitiescount = $08F4
!3pabilitiescount = $08F5
!4pabilitiescount = $08F6

!pointerloc = $7E0153
!pointerloc2 = $7E0156
!validater = $7E01C7


!input = $7E0114
!input2 = $7E0B03
!configmenucheck = $7E0159 ; when this is #$06, player is in config menu
!configmenucheck2 = $7E017B ; when this is #$f6, player is in config menu
!menutype = $7E0143
!itemmenuvalidater = $7E01E0
!itemmenuloc = $7E0200
!speedvalue = $7E0BC0
!itemboxwriter = $7E7511
!encounterswitch = $7E0973
!lastframesave = $7EF87E
!destinationindex = $7E1E20
!charname1 = $7E1E30
!charname2 = $7E1E31
!charname3 = $7E1E32
!charname4 = $7E1E33
!charname5 = $7E1E34
!charname6 = $7E1E35
!charnamecontrol = $7E1E36
!charnamepass = $7E1E37
!destinationdata1 = $E79400
!destinationdata2 = $E79420
!eventrewardindex = $C0FAB0
!typeid = $11
!rewardid = $12
!unusedram1 = $1F10
!unusedram2 = $1F11
!unusedram3 = $1F12

!worldmapflag = $0B53 ; if this is 1, not in world map
!walkinginput = $0b03
!airshipspeed = #$0020

!rewarditemset = $001E20
!mapid = $0AD6
!xycoordcheck = $0AD8
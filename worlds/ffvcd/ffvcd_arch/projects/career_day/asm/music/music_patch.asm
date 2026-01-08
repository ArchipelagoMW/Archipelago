hirom 

org $c4029f
LDA !ADDRESS_music_instrument_song_indices, X

org $C40222
lda !ADDRESS_music_song_pointers, x
org $C40228
lda !ADDRESS_music_song_pointers+1, x
org $C4022E
lda !ADDRESS_music_song_pointers+2, x

org $C402ED
LDA !ADDRESS_music_instrument_pointers, x
org $C402F3
LDA !ADDRESS_music_instrument_pointers+1, x
org $C402F9
LDA !ADDRESS_music_instrument_pointers+2, x
org $C40438
LDA !ADDRESS_music_instrument_pointers, x
org $C4043E
LDA !ADDRESS_music_instrument_pointers+1, x
org $C40444
LDA !ADDRESS_music_instrument_pointers+2, x



org $C404F4
    ADC !ADDRESS_music_loop_sample_length, X
org $C404FE
    LDA !ADDRESS_music_asdr,x
org $C404E0
    LDA !ADDRESS_music_sample_rate, x
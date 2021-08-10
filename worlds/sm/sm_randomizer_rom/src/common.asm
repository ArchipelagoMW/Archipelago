init_memory:
    lda config_multiworld
    beq +
    jsl init_randolive
    jsl mw_init         ; Init multiworld
+
    ;jsl $8b9146
	rtl
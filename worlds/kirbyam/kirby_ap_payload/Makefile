PREFIX  :=
CC      := arm-none-eabi-gcc
OBJCOPY := arm-none-eabi-objcopy

# Preserve existing local devkitPro defaults when installed at the historical path.
ifneq ("$(wildcard C:/devkitPro/devkitARM/bin/arm-none-eabi-gcc.exe)","")
CC      := C:/devkitPro/devkitARM/bin/arm-none-eabi-gcc.exe
OBJCOPY := C:/devkitPro/devkitARM/bin/arm-none-eabi-objcopy.exe
endif


CFLAGS  := -mthumb -mcpu=arm7tdmi -Os -ffreestanding -fno-builtin -nostdlib -Wall -Wextra
LDFLAGS := -T linker.ld -nostdlib

all: payload.bin

payload.elf: ap_payload.o ap_hook.o
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

ap_payload.o: ap_payload.c
	$(CC) $(CFLAGS) -c -o $@ $<

ap_hook.o: ap_hook.s
	$(CC) $(CFLAGS) -c -o $@ $<

payload.bin: payload.elf
	$(OBJCOPY) -O binary $< $@

clean:
	rm -f *.o payload.elf payload.bin

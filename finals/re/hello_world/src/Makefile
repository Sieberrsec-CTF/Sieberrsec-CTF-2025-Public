elf:
	gcc -Wl,-z,norelro poc.s -o poc 
	python3 partial-strip.py
elf-clean:
	gcc -Wl,-z,norelro poc.s -o poc 
elf-strip:
	gcc -s -Wl,-z,norelro poc.s -o poc
sc:
	gcc -fcf-protection=none poc.c -S -masm=intel


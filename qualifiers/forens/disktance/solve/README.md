# disktance

might polish this up later

1. Run `file` to determine filesystem type

    ```bash
    kairos@pop-os ~/Downloads [1]> file sctf.img 
    sctf.img: Linux rev 1.0 ext4 filesystem data, UUID=d40cb453-b4a0-49b9-baa3-2ab29c4eb2c7, volume name "sctf" (needs journal recovery) (extents) (64bit) (large files) (huge files)
    ```

2. View items in filesystem

    ```bash
    kairos@pop-os ~/Downloads [1]> fls -r -m / sctf.img

    0|/lost+found|11|d/drwx------|0|0|16384|1752852333|1752852333|1752852333|1752852333
    0|/.Trash-1000|24449|d/drwx------|1000|1000|4096|1752852428|1752852428|1752852428|1752852428
    0|/.Trash-1000/info|24450|d/drwx------|1000|1000|4096|1752852488|1752852428|1752852428|1752852428
    0|/.Trash-1000/info/elf.trashinfo|14|r/rrw-------|1000|1000|55|1752852488|1752852428|1752852428|1752852428
    0|/.Trash-1000/files|24451|d/drwx------|1000|1000|4096|1752852488|1752852428|1752852428|1752852428
    0|/.Trash-1000/files/elf|12|r/rrwxrwxr-x|1000|1000|17856|1752852425|1752850211|1752852428|1752852425
    0|/flag.txt|13|r/rrw-rw-r--|1000|1000|35|1752852445|1752852453|1752852453|1752852442
    0|/$OrphanFiles|48897|V/V---------|0|0|0|0|0|0|0
    0|/$OrphanFiles/OrphanFile-15 (deleted)|15|-/rrw-rw-r--|1000|1000|0|1752852445|1752852454|1752852454|1752852445

    ```

3. Get the elf file (flag.txt is a fake flag lol)

    ```bash
    kairos@pop-os ~/Downloads [1]> icat sctf.img 12 > elf
    ```

4. Execute the elf file. Might need to resolve dependencies with `ldd`.

    ```bash
    kairos@pop-os ~/Downloads> chmod +x elf 
    kairos@pop-os ~/Downloads> ./elf 
    ```

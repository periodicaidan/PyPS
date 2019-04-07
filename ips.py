import os
from click import echo
import shutil


def read(ips_file):
    if not os.access(ips_file, os.F_OK):
        print(f"IPS file {ips_file} does not exist")
        raise StopIteration

    if not (os.access(ips_file, os.R_OK) and os.access(ips_file, os.W_OK)):
        print(f"{ips_file} is not readable and writable. Please set the appropriate permissions.")
        raise StopIteration

    if ips_file.split(".")[-1] != "ips":
        print(f"{ips_file} is not an IPS file (proper extension is .ips)")
        raise StopIteration

    with open(ips_file, "rb+") as ips:
        header = ips.read(5)
        if header != b"PATCH":
            print(f"IPS file header invalid: {header}")
            raise StopIteration

        """
        The file contains several patches, each patch is laid out thus:

        - 3-digit base-256 location in the ROM where the patch should go
        - 2-digit base-256 length of the patch
        - The patch

        Without any whitespace or other separators

        If the length of the patch is found to be 0, this has a special meaning: to copy a certain byte some number
        of times. This is useful for setting certain locations to null, for example. This has a different format:

        - 3-digit base-256 location in the ROM to copy the data (as above)
        - Two null bytes (which evaluate to 00)
        - 2-digit base-256 number of times the byte should be copied
        - The byte to be copied
        """

        data = ips.read(3)
        while data != "" and data != b"EOF":
            offset = 0
            for _, c in enumerate(data):
                offset = offset * 256 + int(c)

            data = ips.read(2)
            length = 0
            for _, c in enumerate(data):
                length = length * 256 + int(c)

            if length == 0:
                data = ips.read(2)
                length = 0
                for _, c in enumerate(data):
                    length = length * 256 + int(c)

                byte = ips.read(1)
                data = byte * length
            else:
                data = ips.read(length)

            yield offset, data
            data = ips.read(3)


def patch(rom_file, ips_file, backup):
    if not os.access(rom_file, os.F_OK):
        return f"ROM file {rom_file} not found"

    if not (os.access(rom_file, os.R_OK) and os.access(os.W_OK)):
        return f"ROM file {rom_file} is not readable and/or writeable. Please set the appropriate permissions."

    if backup:
        if not os.access(rom_file + ".bak", os.F_OK):
            shutil.copyfile(rom_file, rom_file + ".bak")

    with open(rom_file, "rb+") as rom:
        try:
            for offset, data in read(ips_file):
                rom.seek(offset)
                rom.write(data)
                echo(f"{len(data)} bytes overwritten at offset {hex(offset)}")
        except StopIteration:
            exit(1)

        return "Done."


def show_patches(ips_file):
    with open(ips_file, "rb+") as ips:
        echo(f"Patches for {ips_file}")

        num_patches = 0
        for offset, data in read(ips_file):
            num_patches += 1
            echo(f"Offset: {hex(offset)}\nPatch:")
            length = len(data)
            i = 0
            while i < length:
                for _ in range(8):
                    print(hex(data[i]).replace("0x", "").rjust(2, '0'), end=" ")
                    i = i + 1
                    if i >= length: break

                print()
            print()
        print(f"Total patches: {num_patches}")

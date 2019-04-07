import os
from click import echo
import shutil


def read(ips_file):
    if not os.access(ips_file, os.F_OK):
        echo("IPS file %s does not exist" % ips_file)
        raise StopIteration

    if not (os.access(ips_file, os.R_OK) and os.access(ips_file, os.W_OK)):
        echo("%s is not readable and writable. Please set the appropriate permissions." % ips_file)
        raise StopIteration

    if ips_file.split(".")[-1] != "ips":
        echo("%s is not an IPS file (proper extension is .ips)" % ips_file)
        raise StopIteration

    with open(ips_file, "rb+") as ips:
        header = ips.read(5)
        if header != b"PATCH":
            echo("IPS file header invalid: %s" % header)
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
        return "ROM file %s not found" % rom_file

    if not (os.access(rom_file, os.R_OK) and os.access(os.W_OK)):
        return "ROM file is not readable and/or writeable. Please set the appropriate permissions." % rom_file

    if backup:
        if not os.access(rom_file + ".bak", os.F_OK):
            shutil.copyfile(rom_file, "%s.bak" % rom_file)

    with open(rom_file, "rb+") as rom:
        try:
            for offset, data in read(ips_file):
                rom.seek(offset)
                rom.write(data)
                echo("%s bytes overwritten at offset %s" % (len(data), hex(offset)))
        except StopIteration:
            exit(1)

        return "Done."


def show_patches(ips_file):
    with open(ips_file, "rb+") as ips:
        echo("Patches for %s" % ips_file)

        num_patches = 0
        for offset, data in read(ips_file):
            num_patches += 1
            echo("Offset %s" % hex(offset))
            length = len(data)
            i = 0
            while i < length:
                for _ in range(8):
                    print(hex(data[i]).replace("0x", "").rjust(2, '0'), end=" ")
                    i = i + 1
                    if i >= length: break

                echo()
            echo()
        echo("Total patches: %s" % num_patches)

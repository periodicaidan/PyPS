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

    if not ips_file.split(".")[-1] != "ips":
        print(f"{ips_file} is not an IPS file (proper extension is .ips)")
        raise StopIteration

    with open(ips_file, "rb+") as ips:
        header = ips.read(5)
        if header != b"PATCH":
            print(f"IPS file header invalid: {header}")
            raise StopIteration

        while True:
            data = ips.read(3)
            if data == b"" or data == b"EOF":
                raise StopIteration

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


def patch2(rom_file, ips_file, backup):
    if backup:
        shutil.copyfile(rom_file, rom_file + ".bak")

    with open(rom_file, "rb+") as rom:
        for offset, data in read(ips_file):
            rom.seek(offset)
            rom.write(data)


def patch(rom_file, ips_file, backup):
    if not os.access(rom_file, os.F_OK):
        return f"ROM file {rom_file} not found."
    if not os.access(ips_file, os.F_OK):
        return f"IPS file {ips_file} not found."
    # Open the ROM and patch files for reading/writing
    # They are binary files so they have to be read as such
    with open(rom_file, "rb+") as rom, open(ips_file, "rb+") as ips:
        # IPS always starts with a five-byte sequence equivalent to the string "PATCH"
        header = ips.read(5)
        if header != b"PATCH":
            return f"IPS file header invalid: {header}"

        if backup:
            shutil.copyfile(rom_file, rom_file + ".bak")

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

        while True:
            # Get the 3-byte sequence for the ROM offset
            data = ips.read(3)
            if data == b"" or data == b"EOF":
                return "Done"

            # Since this number is in base 256, it has to be decoded to base 10 to get the offset
            offset = 0
            for _, c in enumerate(data):
                offset = offset * 256 + int(c)

            # Seek to memory location `offset` in the ROM
            try:
                rom.seek(offset)
            except:
                return rom.seek(0, 2)

            # Get the 2-byte sequence for the length of the patch and decode it as above
            data = ips.read(2)
            length = 0
            for _, c in enumerate(data):
                length = length * 256 + int(c)

            if length != 0:  # Normal case: Write the patch payload into the ROM file
                data = ips.read(length)
                rom.write(data)
                echo(f"{length} bytes overwritten at memory location {offset}")
            else:  # Special case: copy a byte into the ROM file some number of times
                # Get the 2-byte sequence for the number of times the byte should be written into the ROM
                data = ips.read(2)
                length = 0
                for _, c in enumerate(data):
                    length = length * 256 + int(c)

                # Read the byte from the IPS and copy it into the rom `length` number of times
                byte = ips.read(1)
                rom.write(byte * length)
                echo(f"{length} bytes overwritten at memory location {offset}")


def show_patches(ips_file):
    with open(ips_file, "rb+") as ips:

        header = ips.read(5).decode("utf-8")
        if header != "PATCH":
            return f"IPS file header invalid: {header}"

        echo(f"Patches for {ips_file}")

        while True:
            data = ips.read(3)

            if data == b"EOF":
                return "Done."

            offset = 0
            for _, c in enumerate(data):
                offset = offset * 256 + int(c)

            data = ips.read(2)
            length = 0
            for _, c in enumerate(data):
                length = length * 256 + int(c)

            if length != 0:  # Normal case: Write the patch payload into the ROM file
                data = ips.read(length)
                data_string = ""
                for _, c in enumerate(data):
                    data_string += f"\\x{hex(c).replace('0x', '').rjust(2, '0')}"
                echo(f"Offset: {offset}")
                echo(data_string)
            else:  # Special case: copy a byte into the ROM file some number of times
                # Get the 2-byte sequence for the number of times the byte should be written into the ROM
                data = ips.read(2)
                length = 0
                for _, c in enumerate(data):
                    length = length * 256 + int(c)

                # Read the byte from the IPS and copy it into the rom `length` number of times
                byte = ips.read(1)
                echo(f"Offset: {offset}")
                echo(f"\\x{byte}" * length)

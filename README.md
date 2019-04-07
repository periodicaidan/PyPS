# PyPS

#### A simple, lightweight, cross-platform IPS patching tool

## Why PyPS?

I wanted a simple IPS patching tool but there aren't any recent, 
maintained ones out there for Linux, so I made my own and thought others 
out there could use it too.

## Installing

Requirements:

- Python 3.x
- pip
- git

Clone this repository, cd into it, and run `pip install .` (or `python 
-m pip install .`). I know this works on Linux and MacOS. It should run
on Windows too but I haven't tested it.

## Usage

Once installed, the name of the program is simply `patchips` (until I 
come up with a better name, at least). The program contains 3 commands.
You can run `patchips --help` to see a description of them all.

### `patch`
Apply an IPS patch file to a ROM. There are four options this command
can accept:

- `--rom` or `-r`: The path to the ROM file that is to be patched
- `--ips` or `-i`: The path to the IPS file to use for patching
- `--backup` or `-b`: Create a backup for the original ROM (enabled by 
default)
- `--no-backup` or `-B`: Disables the above; you will receive a
confirmation dialogue

Once a patch is applied to a ROM, the changes cannot be undone, so it
is recommended that you create a backup. This program does this by
default, copying the file with a `.bak` extension added to the end of
it.

### `patches`

Show all the patches that would be applied to a ROM by an IPS file.
Accepts a single option: `--ips` or `-i` with the path to the IPS file
you would like to see patches for. It outputs the patches as a series of
bytes in hexadecimal. I plan to continue working on this feature.

### `restore`

Restores a ROM from a backup. Only works if you backed up the ROM when
patching. It accepts one option: `--rom` or `-r` followed by the path to
the ROM file you would like to restore.

## License

Copyright Ⓒ Aidan T. Manning

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the 
"Software"), to deal in the Software without restriction, including 
without limitation the rights to use, copy,  modify, merge, publish, 
distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to 
the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

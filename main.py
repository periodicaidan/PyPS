import click
import ips as PyPS
import os


@click.group()
def ips_patch():
    pass


@ips_patch.command("patch")
@click.option("--rom", "-r", required=True, prompt="Path to ROM", help="Path to the ROM file to patch")
@click.option("--ips", "-i", required=True, prompt="Path to IPS", help="Path to the IPS file to use for patching")
@click.option("--backup/--no-backup", "-b/-B", default=True, help="Whether or not to backup the original ROM file (backs up by default)")
def patch(rom, ips, backup=True):
    """
    Apply an IPS patch file to a ROM file
    """
    if not backup:
        click.confirm(f"The ROM {rom} will be partly overwritten; this process cannot be undone and it is *highly* "
                      f"recommended that you make a backup. Are you sure you wish to proceed without one?",
                      abort=True)

    info = PyPS.patch(rom, ips, backup)
    click.echo(info)


@ips_patch.command("restore")
@click.option("--rom", "-r", required=True, prompt="Path to ROM", help="Path to the ROM file to restore")
def restore_rom(rom):
    """
    Revert a ROM file to its original form
    """
    if os.access(f"{rom}.bak", os.F_OK):
        os.remove(rom)
        os.rename(f"{rom}.bak", rom)
        click.echo(f"Restored {rom} from backup.")
    else:
        click.echo(f"No (writable) backup found for {rom}.")


@ips_patch.command("patches")
@click.option("--ips", "-i", required=True, prompt=True, help="Path to the IPS file to list")
def patches(ips):
    """
    Show the patches in an IPS file
    """
    PyPS.show_patches(ips)

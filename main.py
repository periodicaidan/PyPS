import click
import ips as PyPS
import os


@click.group()
def ips_patch():
    pass


@ips_patch.command("patch")
@click.option("--rom", "-r", required=True, prompt="Path to ROM")
@click.option("--ips", "-i", required=True, prompt="Path to IPS")
@click.option("--backup/--no-backup", "-b/-B", default=True)
def patch(rom, ips, backup=True):
    if not backup:
        click.confirm(f"The ROM {rom} will be partly overwritten; this process cannot be undone and it is *highly* "
                      f"recommended that you make a backup. Are you sure you wish to proceed without one?",
                      abort=True)

    info = PyPS.patch(rom, ips, backup)
    click.echo(info)


@ips_patch.command("restore")
@click.option("--rom", "-r", required=True, prompt="Path to ROM")
def restore_rom(rom):
    if os.access(f"{rom}.bak", os.F_OK):
        os.remove(rom)
        os.rename(f"{rom}.bak", rom)
        click.echo(f"Restored {rom} from backup.")
    else:
        click.echo(f"No (writable) backup found for {rom}.")


@ips_patch.command("patches")
@click.option("--ips", "-i", required=True, prompt=True)
def patches(ips):
    PyPS.show_patches(ips)



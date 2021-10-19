from __future__ import annotations

from pathlib import Path

import mrcfile
import typer
from rich import print
from rich.table import Table
from rich.tree import Tree

cli = typer.Typer()


def human_filesize(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


@cli.command()
def mrchead(file: Path):
    """Display an mrc file header in the terminal."""
    with mrcfile.open(file, header_only=True) as mrc:
        header = mrc.header
        voxel_size = mrc.voxel_size
    size_on_disk = file.stat().st_size

    table = Table(title=f'Header for {file.name}')

    table.add_column("Attribute(s)", style='cyan', justify='right')
    table.add_column("Value(s)", style='magenta', justify='right')

    image_shape_str = f'{header.nx:5d} {header.ny:5d} {header.nz:5d}'
    voxel_size_str = f'{voxel_size.x:.3f} {voxel_size.y:.3f} {voxel_size.z:.3f}'

    table.add_row("size on disk", human_filesize(size_on_disk))
    table.add_row("image shape: nx | ny | nz", image_shape_str)
    table.add_row("spacing (Å): dx | dy | dz", voxel_size_str)

    print('\n', table)

    label_tree = Tree(label='|')
    for row in header.label:
        if len(row) > 0:
            label_tree.add(row.decode('utf-8'))
    print(label_tree)


if __name__ == "__main__":
    typer.run(mrchead)

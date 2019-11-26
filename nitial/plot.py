import ternary
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def ternary_scatter(
    composition,
    value,
    components=['Ni', 'Al', 'Ti'],
    cmap='Blues',
    label=None,
    cticks=None,
    s=50,
    edgecolors='k',
    marker='o',
    vmin=None,
    vmax=None
):
    scale = 1
    grid = plt.GridSpec(10, 10, wspace=2, hspace=1)
    ax = plt.subplot(grid[:,:9])

    if vmin is None and vmax is None:
        filtered = value[np.isfinite(value)]
        vmin, vmax = filtered.min(), filtered.max()

    figure, tax = ternary.figure(scale=scale, ax=ax)
    figure.set_size_inches(6,5.1)
    s = tax.scatter(composition, marker=marker, c=value, cmap=cmap, edgecolors=edgecolors, vmin=vmin, vmax=vmax, s=s)
    tax.boundary(linewidth=2.0)
    tax.gridlines(multiple=0.1, color='k')

    ticksize = 12
    ticks = [0.2, 0.4, 0.6, 0.8, 1.0]
    tax.ticks(ticks, ticks, axis='r', linewidth=1, multiple=0.2, fontsize=ticksize, tick_formats='%0.01f', offset=0.03)
    tax.ticks(ticks, ticks, axis='b', linewidth=1, multiple=0.2, fontsize=ticksize, tick_formats='%0.01f', offset=0.02)
    ticks = np.array([0.2, 0.4, 0.6, 0.8, 1.0])[::-1]
    tax.ticks(list(ticks), list(ticks-0.2), axis='l', linewidth=1, fontsize=ticksize, tick_formats='%0.01f', offset=0.03)
    tax.clear_matplotlib_ticks()
    tax.get_axes().axis('off');

    # tax.right_corner_label(components[0], fontsize=18, position=(1.02,0,0), offset=-0.1)
    tax.right_corner_label(components[0], fontsize=18, position=(1.0,0,0), offset=-0.1)
    # tax.top_corner_label(components[1], fontsize=18, position=(-0.075,1.15,0))
    tax.top_corner_label(components[1], fontsize=18, position=(-0.045,1.1,0))
    # tax.left_corner_label(components[2], fontsize=18, position=(-0.05,0,0))
    tax.left_corner_label(components[2], fontsize=18, position=(0.0,0,0))

    ax.axis('equal')

    ax = plt.subplot(grid[1:-1,9:])
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    # norm = matplotlib.colors.Normalize(vmin=-0.9, vmax=value.max())
    cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation='vertical', label=label)
    cb1.set_label(label=label, size=18)

    if cticks is not None:
        cb1.set_ticks(cticks)
        # cb1.set_tick_labels([-.85, -.7, -0.5])

    plt.subplots_adjust()
    plt.tight_layout()
    tax._redraw_labels()

    return tax

def ternary_contour(G, z_value, tax=None, levels=[0.35, 0.42, 0.5, 0.57], linestyle='-'):

    xx = np.unique(G[:,0])
    yy = np.unique(G[:,1])
    XX, YY = np.meshgrid(xx,yy, indexing='xy')

    ZZ = np.zeros_like(YY)
    ZZ = np.triu(np.ones(80))[:,::-1]
    ZZ[(ZZ > 0)] = z_value

    contour = plt.contour(XX[:-5,:], YY[:-5,:], ZZ[:-5,:], levels=levels, alpha=0.0)

    for level in contour.allsegs:

        for ii, seg in enumerate(level):
            try:
                sel = clip(seg)
                tax.plot(seg[sel], color='w', zorder=200, linestyle=linestyle)
            except:
                tax.plot(seg, color='w', zorder=200, linestyle=linestyle)

    return

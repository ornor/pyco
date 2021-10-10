import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

m = kN = 1

# tekenafspraak positief: naar recht, naar beneden, tegen klok in\n

lengte = 8*m

puntlasten = [
    {'x': 2*m, 'F': 15*kN},
    {'x': 4*m, 'F': -3*kN},
]

puntlasten = sorted([puntlast for puntlast in puntlasten if puntlast['x'] >= 0 and puntlast['x'] <= lengte], key=lambda k: k['x'])

reactiekracht_verticaal_links = -1 * sum([(lengte - puntlast['x'])/lengte * puntlast['F'] for puntlast in puntlasten])
reactiekracht_verticaal_rechts = -1 * sum([puntlast['x']/lengte * puntlast['F'] for puntlast in puntlasten])

V = []
V.append((0, 0))
V_waarde = reactiekracht_verticaal_links
V.append((0, V_waarde))
for puntlast in puntlasten:
    V.append((puntlast['x'], V_waarde))
    V_waarde += puntlast['F']
    V.append((puntlast['x'], V_waarde))
V.append((lengte, -reactiekracht_verticaal_rechts))
V.append((lengte, 0))
V.append((0, 0))

def draw_coords(coords, padx=2, pady=2, linewidth=1):
    codes = [Path.MOVETO, *[Path.LINETO for _ in range(len(coords)-1)]]
    path = Path(coords, codes)
    fig, ax = plt.subplots()
    patch = patches.PathPatch(path, linewidth=linewidth, hatch='/', fill=False, color='blue')
    ax.add_patch(patch)
    ax.grid(color='grey', linestyle='-', linewidth=0.2)
    ax.set_xlim(min([c[0] for c in coords]) - padx, max([c[0] for c in coords]) + padx)
    ax.set_ylim(min([c[1] for c in coords]) - pady, max([c[1] for c in coords]) + pady)
    plt.show()

draw_coords(V)

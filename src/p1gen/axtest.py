
import matplotlib.pyplot as plt
import numpy as np 
import matplotlib.cm as cm 
import matplotlib.colors as colors
import matplotlib as mpl
from matplotlib.axes import Axes




def pressure_data():
    arr_a = np.linspace(-0.2, 0.6/2, 10)
    arr_b = np.linspace(-0.58, -0.44, 10)
    arr_c = np.linspace(-0.7, 0, 10)

    return np.concat([arr_a, arr_b, arr_c]).tolist()


def basic_colorbar():
    fig, ax = plt.subplots(figsize=(6, 1), layout='constrained')
    
    
    cmap = mpl.colormaps["cool"]
    norm = colors.Normalize(vmin=5, vmax=10)
    
    fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),
                cax=ax, orientation='horizontal', label='Some Units')
    

    return fig, cmap, norm

def pressure_colorbar(data: list[float], ax: Axes):
    
    expansion = 1.3
    min_, max_ = min(data)*expansion, max(data)*expansion
    if max_ <= 0:
        norm = colors.Normalize(vmin=min_, vmax=max_)
        cmap=mpl.colormaps["YlOrRd_r"]
    else:
        center = 0
        norm = colors.TwoSlopeNorm(vmin=min_, vcenter=center, vmax=max_)
        cmap = mpl.colormaps["RedYlBu"]
    # norm=colors.SymLogNorm(linthresh=0.5, linscale=1, vmin=min_, vmax=max_, base=10)
    #
    bar = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),
                orientation='horizontal', label='Total Pressure [Pa]', 
                ax=ax),
    return  bar, cmap, norm

def flow_colorbar(data: list[float], ax: Axes):
    cmap = mpl.colormaps["Blues"]
    min_, max_ = min(data), max(data)
    # if max_ == 0:
    #     max_ = 0.00001
    # center = 0
    # norm = colors.TwoSlopeNorm(vmin=min_, vcenter=center, vmax=max_)
    # # norm=colors.SymLogNorm(linthresh=0.5, linscale=1, vmin=min_, vmax=max_, base=10)
    norm = colors.Normalize(vmin=min_, vmax=max_)
    bar = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),
                orientation='vertical', label='Volume Flow Rate [m3/s]', 
                ax=ax),
    return  bar, cmap, norm
    

if __name__ == "__main__":
    d = pressure_data()
    fig, ax = plt.subplots(figsize=(6, 1), layout='constrained')
    bar, cmap, norm = pressure_colorbar(d, ax)
    res = norm(-0.1)
    print(f"({res}, -0.1, {cmap(res)})")
    plt.show()

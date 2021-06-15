import py3Dmol
from ipywidgets import widgets, interact,fixed
from IPython.display import display

def section(fle, begin, end):
    """
    yields a section of a textfile. 
    Used to identify [COORDS] section etc
    """
    with open(fle) as f:
        for line in f:
            # found start of section so start iterating from next line
            if line.startswith(begin):
                for line in f: 
                    # found end so end function
                    if line.startswith(end):
                        return
                    # yield every line in the section
                    yield line.rstrip()    

def parse_molden(filename='default.molden_normal_modes'):
    """
    Extract all frequencies, the base xyz coordinates 
    and the displacements for each mode from the molden file
    """
    all_frequencies = list(section(filename, '[FREQ]', '\n'))
    all_frequencies = [(float(freq),i) for i, freq in enumerate(all_frequencies)]
    coords = list(section(filename, '[FR-COORD]', '\n'))
    normal_modes = []
    for freq in range(len(all_frequencies)):
        if freq+1 != len(all_frequencies):
            normal_modes.append(list(section(filename, f'vibration {freq+1}', 'vibration')))
        else:
            normal_modes.append(list(section(filename, f'vibration {freq+1}', '\n')))
    return all_frequencies, coords, normal_modes

def draw_normal_mode(mode=0, coords=None, normal_modes=None):
    """
    draws a specified normal mode using the animate mode from py3Dmol. 
    Coming from psi4 units need to be converted from a.u to A. 
    """
    fac=0.52917721067121  # bohr to A
    xyz =f"{len(coords)}\n\n"
    for i in range(len(coords)):
        atom_coords = [float(m) for m in  coords[i][8:].split('       ')]
        mode_coords = [float(m) for m in  normal_modes[mode][i][8:].split('       ')]
        xyz+=f"{coords[i][0:4]} {atom_coords[0]*fac} {atom_coords[1]*fac} {atom_coords[2]*fac} {mode_coords[0]*fac} {mode_coords[1]*fac} {mode_coords[2]*fac} \n"
    view = py3Dmol.view(width=400, height=400)
    view.addModel(xyz, "xyz", {'vibrate': {'frames':10,'amplitude':1}})
    view.setStyle({'sphere':{'scale':0.30},'stick':{'radius':0.25}})
    view.setBackgroundColor('0xeeeeee')
    view.animate({'loop': 'backAndForth'})
    view.zoomTo()
    return(view.show())

def show_normal_modes(filename='default.molden_normal_modes'):
    """
    wrapper function that parses the file and initializes the widget.
    """
    all_frequencies, coords, normal_modes =  parse_molden(filename=filename)
    _ = interact(draw_normal_mode, coords=fixed(coords), normal_modes=fixed(normal_modes), mode = widgets.Dropdown(
        options=all_frequencies,
        value=0,
        description='Normal mode:',
        style={'description_width': 'initial'}
    ))
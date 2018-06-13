import matplotlib.pyplot as plt
from src.model.qacd_project import QACDProject


filename = 'test_data/test_data.quack'


project = QACDProject()
project.load_file(filename)
print('State:', project.state)
print('Elements:', project.elements)
print('Ratios:', project.ratios)
print('Presets:', project.get_valid_preset_ratios())

if len(project.ratios) == 0:
    project.create_ratio_map('Mg#', preset='Mg#')
    project.create_ratio_map('Example', elements=('Ca', 'Na'), correction_model='pyroxene')
    print('Ratios:', project.ratios)
else:
    names = ['Mg#', 'Example']
    for i, name in enumerate(names):
        ratio, stats = project.get_ratio(name, want_stats=True)
        plt.subplot(len(names), 1, i+1)
        plt.imshow(ratio)
        plt.colorbar()
        plt.title('{} = {}'.format(stats['name'], stats['formula']))
    plt.show()

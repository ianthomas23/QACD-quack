from src.model.qacd_project import QACDProject, State


def create_test_project_file(filename, state):
    print('Creating test project file', filename, 'with state', state)
    project = QACDProject()

    if state >= State.EMPTY:
        project.set_filename(filename)

    if state >= State.RAW:
        project.import_raw_csv_files('test_data')

    if state >= State.FILTERED:
        project.filter(pixel_totals=True, median=True)

    if state >= State.NORMALISED:
        project.normalise()

    if state >= State.H_FACTOR:
        project.create_h_factor()



for i, state in enumerate([State.EMPTY, State.RAW, State.FILTERED,
                           State.NORMALISED, State.H_FACTOR]):
    # Not using .quack file extension so that files are hidden from GUI.
    create_test_project_file('test_data/out{}'.format(i), state)


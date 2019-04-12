import re, os, glob
from file_read_backwards import FileReadBackwards

condorPath = '/vol/hal/halraid/jantoniadis/HeCores/Condor/full_grid'


def checkOutput(path):
    hasFinished = False
    keyword1 = 'stop because'
    keyword2 = 'termination'
    name = path[-20:]
    with FileReadBackwards(f'{path}/condor.out') as file:
        for line in file:
            if line.startswith(f'{keyword1}') or line.startswith(f'{keyword2}'):
                current_status = f'Model {name} has been terminated!'
                hasFinished = True
                break
            else:
                current_status = f'Model {name} still running!'
                
    return hasFinished, current_status


def main():

    model_paths = [path for path in glob.glob(condorPath + '/*')]
    model_paths.sort()

    finished = 0
    running = 0
    for i in model_paths:
        hasFinished, status = checkOutput(i)

        if hasFinished:
            print(status)
            finished += 1
        else:
            print(status)
            running += 1

    print(f'From {len(model_paths)} models, {finished} have finished, and {running} are still running!')


if __name__ == '__main__':
    main()

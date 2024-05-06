#!/usr/bin/env python
#
# Code obfuscation using pyarmor
import os
import shutil

COMMAND_FOR_PYARMOR = 'pyarmor build --force'
EDGE_SDK_DIR = os.path.basename(os.getcwd())
OBFUSCATED_EDGE_SDK = 'djangosaml2-obfuscated'
PY_ARMOR = 'pyarmor'
PY_TRANSFORM = 'pytransform'
EDGE_SDK = 'djangosaml2'


def main():
    """
    Create a edge-sdk-obfuscated directory and copy the deming-core code to it.
    Run the pyarmor build command by changing the current working directory to edge-sdk/pyarmor.
    Then copy the pytransformer folder to the deming-core-obfuscated/deming folder.
    """

    # cd to the parent directory.
    os.chdir('..')

    if os.path.exists(OBFUSCATED_EDGE_SDK):
        shutil.rmtree(OBFUSCATED_EDGE_SDK)

    shutil.copytree(EDGE_SDK_DIR, OBFUSCATED_EDGE_SDK)

    os.chdir(os.path.join(EDGE_SDK_DIR, PY_ARMOR))
    os.system(COMMAND_FOR_PYARMOR)

    # cd to edge-sdk-obfuscated directory.
    os.chdir(os.path.join('..', '..', OBFUSCATED_EDGE_SDK))

    # Move the pytransformer file inside the deming folder
    shutil.move(PY_TRANSFORM, EDGE_SDK)


if __name__ == '__main__':
    main()

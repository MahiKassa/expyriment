#!/usr/bin/env python
"""
Setup file for Expyriment
"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


import stat
from subprocess import Popen, PIPE
try:
    from setuptools import setup
    from setuptools.command.build_py import build_py
    from setuptools.command.install import install
    from setuptools.command.bdist_wininst import bdist_wininst
except ImportError:
    from distutils.core import setup
    from distutils.command.build_py import build_py
    from distutils.command.install import install
    from distutils.command.bdist_wininst import bdist_wininst
from os import remove, close, chmod, path
from shutil import move, rmtree
from tempfile import mkstemp
from glob import glob


# Settings
packages = ['expyriment',
            'expyriment.control',
            'expyriment.io', 'expyriment.io.extras',
            'expyriment.misc', 'expyriment.misc.extras',
            'expyriment.stimuli', 'expyriment.stimuli.extras',
            'expyriment.design', 'expyriment.design.extras']

package_data = {'expyriment': ['expyriment_logo.png', '_fonts/*.*']}

install_requires = ["pygame>=1.9", "pyopengl>3.0"]

extras_require = ["pyserial>=2.5", "pyparallel>=0.2", "numpy>=1.6", "pillow>1.0", "pyxid>1.0"]

dependency_links = ["http://www.lfd.uci.edu/~gohlke/pythonlibs/"]


# Clear old installation when installing
class Install(install):
    """Specialized installer."""

    def run(self):
        # Clear old installation
        olddir = path.abspath(self.install_lib + path.sep + "expyriment")
        oldegginfo = glob(path.abspath(self.install_lib) + path.sep +
                          "expyriment*.egg-info")
        for egginfo in oldegginfo:
            remove(egginfo)
        if path.isdir(olddir):
            rmtree(olddir)
        install.run(self)


# Clear old installation when installing (for bdist_wininst)
class Wininst(bdist_wininst):
    """Specialized installer."""

    def run(self):
        fh, abs_path = mkstemp(".py")
        new_file = open(abs_path, 'w')
        # Clear old installation
        new_file.write("""
from distutils import sysconfig
import os, shutil
old_installation = os.path.join(sysconfig.get_python_lib(), 'expyriment')
if os.path.isdir(old_installation):
    shutil.rmtree(old_installation)
""")
        new_file.close()
        close(fh)
        self.pre_install_script = abs_path
        bdist_wininst.run(self)


# Manipulate the header of all files (only for building/installing from
# repository)
class Build(build_py):
    """Specialized Python source builder."""

    def byte_compile(self, files):
        for f in files:
            if f.endswith('.py'):
                # Create temp file
                fh, abs_path = mkstemp()
                new_file = open(abs_path, 'w')
                old_file = open(f, 'rU')
                for line in old_file:
                    if line[0:11] == '__version__':
                        new_file.write("__version__ = '" + version_nr + "'" +
                                       '\n')
                    elif line[0:8] == '__date__':
                        new_file.write("__date__ = '" + date + "'" + '\n')
                    else:
                        new_file.write(line)
                # Close temp file
                new_file.close()
                close(fh)
                old_file.close()
                # Remove original file
                remove(f)
                # Move new file
                move(abs_path, f)
                chmod(f,
                      stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        build_py.byte_compile(self, files)

def get_version_from_git():
    version_nr = "{0}"
    proc = Popen(['git', 'describe', '--tags', '--dirty', '--always'], \
                        stdout=PIPE, stderr=PIPE)

    return version_nr.format(proc.stdout.read().lstrip("v").strip())

def get_date_from_git():
        proc = Popen(['git', 'log', '--format=%cd', '-1'],
                     stdout=PIPE, stderr=PIPE)
        return proc.stdout.readline().strip()

def get_version_from_file(filename):
    """Get the version (___version___) from a particular file."""

    with open(filename) as f:
        for line in f:
            if line.startswith("__version__"):
                rtn = line.split("'")
                return rtn[1]
    return ''

if __name__=="__main__":
    # Check if we are building/installing from unreleased code
    version_nr = get_version_from_file("expyriment/__init__.py")
    if version_nr == '':
        # Try to add version_nr and date stamp from Git and build/install
        if True:
            proc = Popen(['git', 'rev-list', '--max-parents=0', 'HEAD'],
                         stdout=PIPE, stderr=PIPE)
            initial_revision = proc.stdout.readline()
            if not 'e21fa0b4c78d832f40cf1be1d725bebb2d1d8f10' in initial_revision:
                raise Exception
            version_nr = get_version_from_git()
            date = get_date_from_git()
            # Build
            x = setup(name='expyriment',
                      version=version_nr,
                      description='A Python library for cognitive and neuroscientific experiments',
                      author='Florian Krause, Oliver Lindemann',
                      author_email='florian@expyriment.org, oliver@expyriment.org',
                      license='GNU GPLv3',
                      url='http://www.expyriment.org',
                      packages=packages,
                      package_dir={'expyriment': 'expyriment'},
                      package_data=package_data,
                      install_requires=install_requires,
                      extras_require=extras_require,
                      dependency_links=dependency_links,
                      cmdclass={'build_py': Build, 'install': Install,
                                'bdist_wininst': Wininst}
            )
    
            print ""
            print "Expyriment Version:", version_nr, "(from repository)"
        else:
            raise RuntimeError("Building from repository failed!")

    # If not, we are building/installing from a released download
    else:
        # Build
        setup(name='expyriment',
              version=version_nr,
              description='A Python library for cognitive and neuroscientific experiments',
              author='Florian Krause, Oliver Lindemann',
              author_email='florian@expyriment.org, oliver@expyriment.org',
              license='GNU GPLv3',
              url='http://www.expyriment.org',
              packages=packages,
              package_dir={'expyriment': 'expyriment'},
              package_data=package_data,
              install_requires=install_requires,
              extras_require=extras_require,
              dependency_links=dependency_links,
              cmdclass={'install': Install, 'bdist_wininst': Wininst}
          )

        print ""
        print "Expyriment Version:", version_nr

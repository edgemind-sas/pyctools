"""pyar3 Setup"""

from setuptools import setup, find_packages

VERSION = "0.0.1"

setup(name='pyctools',
      version=VERSION,
      url='https://github.com/edgemind-sas/pyctools',
      author='Roland Donat',
      author_email='roland.donat@gmail.com, roland.donat@edgemind.net',
      maintainer='Roland Donat',
      maintainer_email='roland.donat@edgemind.net',
      keywords='Modelling',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3.8',
          'Topic :: Scientific/Engineering :: Artificial Intelligence'
      ],
      packages=find_packages(
          exclude=[
              "*.tests",
              "*.tests.*",
              "tests.*",
              "tests",
              "log",
              "log.*",
              "*.log",
              "*.log.*"
          ]
      ),
      description='Tools for PyCATSHOO',
      license='MIT',
      platforms='ALL',
      python_requires='>=3.8',
      install_requires=[
          "pandas>=1.4.4",
          "numpy>=1.23.2",
          "pydantic>=1.10.2",
          "xlsxwriter",
          "plotly>=5.10.0",
          "lxml",
          "colored",
      ],
      zip_safe=False,
      # scripts=[
      #     '<pathtoscript>',
      # ],
      )

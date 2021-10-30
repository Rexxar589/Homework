import setuptools

setuptools.setup(
    include_package_data=True,
    name='rss_reader',
    entry_points={
        'console_scripts': [
            'rss_reader = rss_reader.rss_reader:main',
        ],
    },
    version='1.0.4',
    description='rss_reader',
    author='Aleksey Stefonyak',
    author_email='aleksey.stef@gmail.com',
    packages=setuptools.find_packages(),
    install_requires=['argparse', 'requests', 'bs4', 'tabulate', 'datetime', 'lxml', 'fpdf', 'FB2'],
    long_description='rss_reader - CLI utility that can read and save content of rss pages in different formats',
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

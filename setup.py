import setuptools

with open('README.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name="active-dataclass",
    version='0.2a',
    author="Diego Cardoso Nunes",
    author_email="diego.dcn.dev@gmail.com",
    description="A very simple ORM for small projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Di-Ca-N/dataclass_orm",
    packages=setuptools.find_packages(),
    keywords="orm dataclass database",
    classifiers=[
        "Proggramming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Database :: Front-Ends",
        "Intended Audience :: Developers"
    ],
    python_requires='>=3.7',
)
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="p0ker", # Replace with your own username
    version="0.0.1",
    author="Richie Morrisroe",
    author_email="richie.morrisroe@gmail.com",
    description="simulating poker hands (five card stud)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'hypothesis'],
    python_requires='>=3.6',
)

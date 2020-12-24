from setuptools import setup

setup(
    name="pyautostart",
    version="0.1.0",
    description="Make executable files run after user login",
    py_modules=["pyautostart"],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ]
)

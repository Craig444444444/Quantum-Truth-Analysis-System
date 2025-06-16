from setuptools import setup, find_packages

setup(
    name="quantum_truth",
    version="1.0.0",
    author="Craig Huckerby",
    author_email="contact@example.com",
    description="Quantum Truth Analysis System",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quantum-truth",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "matplotlib>=3.5.0",
        "networkx>=2.8.0",
        "tqdm>=4.64.0",
        "Pillow>=9.0.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: Academic Free License (AFL)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'quantum-truth=quantum_truth.__main__:main',
        ],
    },
)

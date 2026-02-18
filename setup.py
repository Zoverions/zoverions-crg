from setuptools import setup, find_packages

setup(
    name="zoverions-crg",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "networkx",
        "matplotlib",
        "tqdm"
    ],
    author="Zoverions",
    description="The Causal Renormalization Group (CRG) framework for quantifying Effective Information and Causal Emergence across scales.",
    url="https://github.com/Zoverions/zoverions-crg",
)

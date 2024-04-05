from setuptools import setup, find_packages

setup(
    name="graph_visualizer",
    version="0.1",
    packages= find_packages(),
    install_requires=[
        "Django==5.0",
        "asgiref==3.7.2",
        "sqlparse==0.4.4",
    ],
    python_requires=">=3.10",
    entry_points={
        "graph_visualizer": [
            "graph_visualizer=graph_visualizer.apps.GraphExplorerConfig"
        ]
    },
)

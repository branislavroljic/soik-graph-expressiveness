# cd ".."
#.\graph_visualizer\.venv\Scripts\activate
pip install ".\api_soik\"

pip install ".\simple_visualizer\"

pip install ".\block_visualizer\"

#pip install ".\xml_datasource\"

pip install ".\json_datasource\"

pip install ".\platform_soik\"

# cd "graph_visualizer"
python .\graph_explorer\src\graph_explorer\manage.py runserver


@echo off
echo Installing packages in chatbi environment...
call C:\tools\anaconda3\Scripts\conda.exe run -n chatbi pip install chromadb langmem langgraph-checkpoint langgraph-prebuilt rank-bm25 python-levenshtein RestrictedPython pysqlite3 aiosqlite sqlalchemy-trino json5 langchain-chroma langchain-mcp-adapters "pyhive[presto]"
echo Done!
pause

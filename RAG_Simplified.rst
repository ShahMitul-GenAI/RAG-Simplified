.. code:: ipython3

    import os.path
    import pickle
    import streamlit as st
    from dotenv import load_dotenv
    from langchain.agents import Tool
    from langchain.chains import RetrievalQA
    from langchain.tools import WikipediaQueryRun
    from langchain.schema.document import Document
    from langchain.agents.agent_types import AgentType
    from langchain.agents.initialize import initialize_agent
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_community.utilities import WikipediaAPIWrapper 
    from langchain.text_splitter import RecursiveCharacterTextSplitter 
    from langchain_community.vectorstores import DocArrayInMemorySearch

.. code:: ipython3

    # loading API keys from env
    load_dotenv()
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

.. code:: ipython3

    # loading model and defining embedding
    llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')
    embeddings = OpenAIEmbeddings()

.. code:: ipython3

    # importing inputs from UI 
    fslk = open("./notifications/option.txt", "r")
    selection = fslk.read()
    fslk.close()
    
    # determining prompts as per search selection option 
    if selection == "Wikipedia":
        while not os.path.exists("./notifications/wiki_query.txt"):
            time.sleep(5)
        if os.path.exists("./notifications/wiki_query.txt"):
            f1 = open("./notifications/wiki_query.txt", 'r')
            query = f1.read()
            f1.close()
            print(f"wiki prompt after selection is {pquery}")
    elif selection == "Research Paper":
         while not os.path.exists("./notifications/doc_query.txt"):
            time.sleep(5)
        if os.path.exists("./notifications/doc_query.txt"):
            f2 = open("./notifications/doc_query.txt", 'r')
            query = f2.read()
            f2.close()
            print(f"Docu prompt after selection is {query}")
    else:
        while not os.path.exists("./notifications/cmd_qr2.txt.txt"):
            time.sleep(5)
        if os.path("./notifications/cmd_qr2.txt"):
            f3 = open("./notifications/cmd_qr1.txt", 'r')
            query1 = f3.read()
            f4 = open("./notifications/cmd_qr2.txt", 'r')
            query2 = f4.read()
            f3.close()
            f4.close()
            print(f"wiki3 prompt after selection is {query1}")
            print(f"docu3 prompt after selection is {query2}")

.. code:: ipython3

    # setting up info retreival from Wikipedia pages (1st knowledge source)
    if selection == "Wikipedia":
        print(f"wiki prompt insider wrapper is {query}")
        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        wiki_output = wikipedia.run(query)

.. code:: ipython3

    # fragmegting the document content to fit in the number of token limitations
    if selection == "Wikipedia":
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
        new_docs = [Document(page_content=sent) for sent in wiki_output.split('\n')]
    
    # splitted_output = text_splitter.split_documents(new_doc)
        data_set = DocArrayInMemorySearch.from_documents(new_docs, embedding=embeddings)

.. code:: ipython3

    # retreiving the llm response using user query
    if selection == "Wikipedia":
        qa = RetrievalQA.from_chain_type(
            llm =llm,
            chain_type="stuff",
            retriever = data_set.as_retriever(),
            verbose=True,
        )

.. code:: ipython3

    if selection.strip() == "Wikipedia":
        wiki_out = qa.invoke(query)
        with open("./notifications/wiki_out.txt", 'w') as fwk:
            fwk.write(str(wiki_out)['result'])
            pickle.dumps("wiki_out.txt")

.. code:: ipython3

    # Loading research paper from web source (2nd knoledge source)
    
    if selection == "Research Paper":
        loader = PyPDFLoader("./2312.10997v5.pdf")
        docs = loader.load()
    
    # fragmegting the document content to fit in the number of token limitations
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
        splits = text_splitter.split_documents(docs)
    
    # load the 
        data_set = DocArrayInMemorySearch.from_documents(documents=splits, embedding=embeddings)

.. code:: ipython3

    # retreiving the llm response using user query
    
    if selection == "Research Paper":
        qa = RetrievalQA.from_chain_type(
            llm =llm,
            chain_type="stuff",
            retriever = data_set.as_retriever(),
            verbose=True,
        )

.. code:: ipython3

    # get query from U/I now
    if selection == "Research Paper":
        result = qa.invoke(query)
        with open("./notifications/doc_out.txt", 'w') as frp:
            frp.write(str(resul['result']))
        pickle.dumps("doc_out.txt")

.. code:: ipython3

    # combining two RAG knoledge sources together for better performance
    
    if selection == "Both":
        wiki_tool = Tool(
            name = "wikipedia",
            func = wikipedia.run,
            description = "A useful tool to search internet for the requested information",
        )
        
        docsearch_tool = Tool(
            name = "docsearch",
            func = qa.run,
            description = "A tool to search information from the pool of documents",
        )
        
        agent= initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose = False,
            handle_pasring_errors = True,
        )

.. code:: ipython3

    # executing the agent for both knowledgebase options
    
    if selection == "Both":
        result1 = agent.invoke(str(query1))
        result2 = agent.invoke(str(query2))
        
        with open("./notifications/1.txt", 'w') as f1:
            f1.write(str(resul1['output']))
            pickle.dumps("1.txt")
        with open("./notifications/2.txt", 'w') as f2:
            f2.write(str(result2['output']))
            pickle.dumps("2.txt")

.. code:: ipython3

    # exporting program ending indicator
    ffnl = open("./notifications/PROG EXIT.txt", "rb")
    pickle.dumps(123, ffnl)
    ffnl.close()

.. code:: ipython3

    !jupyter nbconvert --to script mycode.ipynb
    with open('mycode.py', 'r') as f:
        lines = f.readlines()
    with open('mycode.py', 'w') as f:
        for line in lines:
            if 'nbconvert --to script' in line:
                break
            else:
                f.write(line)


.. parsed-literal::

    This application is used to convert notebook files (*.ipynb)
            to various other formats.
    
            WARNING: THE COMMANDLINE INTERFACE MAY CHANGE IN FUTURE RELEASES.
    
    Options
    =======
    The options below are convenience aliases to configurable class-options,
    as listed in the "Equivalent to" description-line of the aliases.
    To see all configurable class-options for some <cmd>, use:
        <cmd> --help-all
    
    --debug
        set log level to logging.DEBUG (maximize logging output)
        Equivalent to: [--Application.log_level=10]
    --show-config
        Show the application's configuration (human-readable format)
        Equivalent to: [--Application.show_config=True]
    --show-config-json
        Show the application's configuration (json format)
        Equivalent to: [--Application.show_config_json=True]
    --generate-config
        generate default config file
        Equivalent to: [--JupyterApp.generate_config=True]
    -y
        Answer yes to any questions instead of prompting.
        Equivalent to: [--JupyterApp.answer_yes=True]
    --execute
        Execute the notebook prior to export.
        Equivalent to: [--ExecutePreprocessor.enabled=True]
    --allow-errors
        Continue notebook execution even if one of the cells throws an error and include the error message in the cell output (the default behaviour is to abort conversion). This flag is only relevant if '--execute' was specified, too.
        Equivalent to: [--ExecutePreprocessor.allow_errors=True]
    --stdin
        read a single notebook file from stdin. Write the resulting notebook with default basename 'notebook.*'
        Equivalent to: [--NbConvertApp.from_stdin=True]
    --stdout
        Write notebook output to stdout instead of files.
        Equivalent to: [--NbConvertApp.writer_class=StdoutWriter]
    --inplace
        Run nbconvert in place, overwriting the existing notebook (only
                relevant when converting to notebook format)
        Equivalent to: [--NbConvertApp.use_output_suffix=False --NbConvertApp.export_format=notebook --FilesWriter.build_directory=]
    --clear-output
        Clear output of current file and save in place,
                overwriting the existing notebook.
        Equivalent to: [--NbConvertApp.use_output_suffix=False --NbConvertApp.export_format=notebook --FilesWriter.build_directory= --ClearOutputPreprocessor.enabled=True]
    --no-prompt
        Exclude input and output prompts from converted document.
        Equivalent to: [--TemplateExporter.exclude_input_prompt=True --TemplateExporter.exclude_output_prompt=True]
    --no-input
        Exclude input cells and output prompts from converted document.
                This mode is ideal for generating code-free reports.
        Equivalent to: [--TemplateExporter.exclude_output_prompt=True --TemplateExporter.exclude_input=True --TemplateExporter.exclude_input_prompt=True]
    --allow-chromium-download
        Whether to allow downloading chromium if no suitable version is found on the system.
        Equivalent to: [--WebPDFExporter.allow_chromium_download=True]
    --disable-chromium-sandbox
        Disable chromium security sandbox when converting to PDF..
        Equivalent to: [--WebPDFExporter.disable_sandbox=True]
    --show-input
        Shows code input. This flag is only useful for dejavu users.
        Equivalent to: [--TemplateExporter.exclude_input=False]
    --embed-images
        Embed the images as base64 dataurls in the output. This flag is only useful for the HTML/WebPDF/Slides exports.
        Equivalent to: [--HTMLExporter.embed_images=True]
    --sanitize-html
        Whether the HTML in Markdown cells and cell outputs should be sanitized..
        Equivalent to: [--HTMLExporter.sanitize_html=True]
    --log-level=<Enum>
        Set the log level by value or name.
        Choices: any of [0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']
        Default: 30
        Equivalent to: [--Application.log_level]
    --config=<Unicode>
        Full path of a config file.
        Default: ''
        Equivalent to: [--JupyterApp.config_file]
    --to=<Unicode>
        The export format to be used, either one of the built-in formats
                ['asciidoc', 'custom', 'html', 'latex', 'markdown', 'notebook', 'pdf', 'python', 'qtpdf', 'qtpng', 'rst', 'script', 'slides', 'webpdf']
                or a dotted object name that represents the import path for an
                ``Exporter`` class
        Default: ''
        Equivalent to: [--NbConvertApp.export_format]
    --template=<Unicode>
        Name of the template to use
        Default: ''
        Equivalent to: [--TemplateExporter.template_name]
    --template-file=<Unicode>
        Name of the template file to use
        Default: None
        Equivalent to: [--TemplateExporter.template_file]
    --theme=<Unicode>
        Template specific theme(e.g. the name of a JupyterLab CSS theme distributed
        as prebuilt extension for the lab template)
        Default: 'light'
        Equivalent to: [--HTMLExporter.theme]
    --sanitize_html=<Bool>
        Whether the HTML in Markdown cells and cell outputs should be sanitized.This
        should be set to True by nbviewer or similar tools.
        Default: False
        Equivalent to: [--HTMLExporter.sanitize_html]
    --writer=<DottedObjectName>
        Writer class used to write the
                                            results of the conversion
        Default: 'FilesWriter'
        Equivalent to: [--NbConvertApp.writer_class]
    --post=<DottedOrNone>
        PostProcessor class used to write the
                                            results of the conversion
        Default: ''
        Equivalent to: [--NbConvertApp.postprocessor_class]
    --output=<Unicode>
        Overwrite base name use for output files.
                    Supports pattern replacements '{notebook_name}'.
        Default: '{notebook_name}'
        Equivalent to: [--NbConvertApp.output_base]
    --output-dir=<Unicode>
        Directory to write output(s) to. Defaults
                                      to output to the directory of each notebook. To recover
                                      previous default behaviour (outputting to the current
                                      working directory) use . as the flag value.
        Default: ''
        Equivalent to: [--FilesWriter.build_directory]
    --reveal-prefix=<Unicode>
        The URL prefix for reveal.js (version 3.x).
                This defaults to the reveal CDN, but can be any url pointing to a copy
                of reveal.js.
                For speaker notes to work, this must be a relative path to a local
                copy of reveal.js: e.g., "reveal.js".
                If a relative path is given, it must be a subdirectory of the
                current directory (from which the server is run).
                See the usage documentation
                (https://nbconvert.readthedocs.io/en/latest/usage.html#reveal-js-html-slideshow)
                for more details.
        Default: ''
        Equivalent to: [--SlidesExporter.reveal_url_prefix]
    --nbformat=<Enum>
        The nbformat version to write.
                Use this to downgrade notebooks.
        Choices: any of [1, 2, 3, 4]
        Default: 4
        Equivalent to: [--NotebookExporter.nbformat_version]
    
    Examples
    --------
    
        The simplest way to use nbconvert is
    
                > jupyter nbconvert mynotebook.ipynb --to html
    
                Options include ['asciidoc', 'custom', 'html', 'latex', 'markdown', 'notebook', 'pdf', 'python', 'qtpdf', 'qtpng', 'rst', 'script', 'slides', 'webpdf'].
    
                > jupyter nbconvert --to latex mynotebook.ipynb
    
                Both HTML and LaTeX support multiple output templates. LaTeX includes
                'base', 'article' and 'report'.  HTML includes 'basic', 'lab' and
                'classic'. You can specify the flavor of the format used.
    
                > jupyter nbconvert --to html --template lab mynotebook.ipynb
    
                You can also pipe the output to stdout, rather than a file
    
                > jupyter nbconvert mynotebook.ipynb --stdout
    
                PDF is generated via latex
    
                > jupyter nbconvert mynotebook.ipynb --to pdf
    
                You can get (and serve) a Reveal.js-powered slideshow
    
                > jupyter nbconvert myslides.ipynb --to slides --post serve
    
                Multiple notebooks can be given at the command line in a couple of
                different ways:
    
                > jupyter nbconvert notebook*.ipynb
                > jupyter nbconvert notebook1.ipynb notebook2.ipynb
    
                or you can specify the notebooks list in a config file, containing::
    
                    c.NbConvertApp.notebooks = ["my_notebook.ipynb"]
    
                > jupyter nbconvert --config mycfg.py
    
    To see all available configurables, use `--help-all`.
    
    

.. parsed-literal::

    [NbConvertApp] WARNING | pattern 'mycode.ipynb' matched no files
    

::


    ---------------------------------------------------------------------------

    FileNotFoundError                         Traceback (most recent call last)

    Cell In[1], line 2
          1 get_ipython().system('jupyter nbconvert --to script mycode.ipynb')
    ----> 2 with open('mycode.py', 'r') as f:
          3     lines = f.readlines()
          4 with open('mycode.py', 'w') as f:
    

    File ~\anaconda3\envs\genai\lib\site-packages\IPython\core\interactiveshell.py:310, in _modified_open(file, *args, **kwargs)
        303 if file in {0, 1, 2}:
        304     raise ValueError(
        305         f"IPython won't let you open fd={file} by default "
        306         "as it is likely to crash IPython. If you know what you are doing, "
        307         "you can use builtins' open."
        308     )
    --> 310 return io_open(file, *args, **kwargs)
    

    FileNotFoundError: [Errno 2] No such file or directory: 'mycode.py'


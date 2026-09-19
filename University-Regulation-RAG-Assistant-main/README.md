\# University Regulation RAG Assistant



A Retrieval-Augmented Generation (RAG) based chatbot that answers student questions using information from the university academic regulations.



\## Project Overview



The University Regulation RAG Assistant helps students quickly find information from university regulations without manually searching through lengthy PDF documents.



The chatbot can answer questions related to:



\- Attendance requirements

\- SGPA and CGPA calculation

\- Grading system

\- Supplementary examinations

\- Branch change rules

\- Promotion requirements

\- Course registration

\- Credit requirements

\- Degree requirements



The system retrieves relevant information from the regulation document and uses a Large Language Model to generate a grounded answer.



\## Technologies Used



\- Python

\- FastAPI

\- Ollama

\- Qwen 2.5 3B

\- Sentence Transformers

\- ChromaDB

\- LangChain Text Splitters

\- PyMuPDF

\- HTML

\- CSS

\- JavaScript



\## RAG Pipeline



```text

University Regulation PDF

&#x20;         |

&#x20;         v

&#x20;   PDF Text Extraction

&#x20;         |

&#x20;         v

&#x20;    Text Preprocessing

&#x20;         |

&#x20;         v

&#x20;       Chunking

&#x20;         |

&#x20;         v

&#x20;      Embeddings

&#x20;         |

&#x20;         v

&#x20;      ChromaDB

&#x20;         |

&#x20;         v

&#x20;    User Question

&#x20;         |

&#x20;         v

&#x20;  Query Understanding

&#x20;         |

&#x20;         v

&#x20;Semantic + Keyword Search

&#x20;         |

&#x20;         v

&#x20;   Relevant Chunks

&#x20;         |

&#x20;         v

&#x20;      Qwen LLM

&#x20;         |

&#x20;         v

&#x20;    Grounded Answer

&#x20;         |

&#x20;         v

&#x20;  Answer + Source Pages


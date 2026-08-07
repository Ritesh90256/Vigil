

                     +----------------------+
                     |      AI Agent        |
                     +----------+-----------+
                                |
                                |
                     One-line SDK Integration
                                |
                                v
                     +----------------------+
                     |     Vigil SDK        |
                     |  Trace Collection    |
                     +----------+-----------+
                                |
                                |
                           HTTP POST
                                |
                                v
                     +----------------------+
                     |   FastAPI Backend    |
                     |  /traces Endpoint    |
                     +----------+-----------+
                                |
                                |
                     Store Trace + Metadata
                                |
                                v
                     +----------------------+
                     |     PostgreSQL       |
                     |      Traces DB       |
                     +----------+-----------+
                                |
                                |
                                v
                     +----------------------+
                     | Failure Classifier   |
                     +----------+-----------+
                                |
            +-------------------+--------------------+
            |                   |                    |
            v                   v                    v
     Retry Storm        Infinite Loop        Tool Misuse
            |                   |                    |
            +-------------------+--------------------+
                                |
                                v
                      Context Overflow
                                |
                                v
                     Prompt Injection
                                |
                                v
                      LLM Fallback (GPT)
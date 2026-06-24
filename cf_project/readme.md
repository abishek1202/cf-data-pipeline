
##   WORKFLOW STEPS

### 1.Ingestion
- load CSV
- Load Json
- Load invoice
- Save raw data
- validate data
- run ingestion pipeline..

### 2.TRANSFORMATION
- Import libraries
- Logging setup
- load data from ingestion o/p
- clean data
- Featuring Engineering
- Invoice parsing
- Analytics function
- Prepare text for llm/sheshat
- save processed data
- run transformation pipeline.

### 3.LOAD POSTGRES
- Import libraries
- Loggging setup
- Database connection
- Loal final data from transfromation o/p
- Create fact table
- Create dimension table
- Run analytics queries
- run load postgres pipeline

### 4.PIPELINE
- Import modules
- pipeline function
  - ingestion
  - transformation
  - data warehouse
- run pipeline 

### 5. SHESHAT SETUP
- Import modules
- Create metadata
- Create vector database
- Test search
- Save Retrival report
- run sheshat pipeline

### 6. LLM QUERY
- load vector database
- Retrieve context
- Lad local llm
- Create prompt
- Generate answer
- run llm pipeline

### 7.APP CREATION
- Import modules
- Load vector DB
- Retrieve context
- Simple answer logic
- UI
- Sidebar
  - Ask AI
  - Interactive dashboard
  - Sample queries
  - About project




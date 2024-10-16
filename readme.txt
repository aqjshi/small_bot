List of Modules

    Web Interface(WEB_URL, JSON)
        Locates actionable buttons,  Extracts information from JSON, 
        Return log of all Keys, Mouse, Text-fill-in actions.

    
    Data Parser(LIST_OF_DOCUMENTS)
        Creates language model parsing from uploaded documents
        Return JSON
    
    Web Scraper(LIST_OF_KEYWORDS)
        Finds application websites
        Return WEB_URL

    

Pipeline
    
    State 1: Data Parser reads your inputted documents, generates the json as a file of different categories, which 
    entails your personal information, education, skills, etc

    State 2: Web interface locates the buttons/textfields determines best course of action for the current page. 

    State 3: Web interface determines the best json categories, and fills in button/textfield with contents of json category

    State 4: Web Scrape to generate urls



**Refactoring Request: NC Commons Import Bot**

I need a complete code refactoring plan for my NC Commons to Wikipedia import bot. The current implementation is weak and doesn't meet requirements. I want a new codebase utilizing modern best practices.

**Required Technologies & Libraries:**
- `mwclient` - for MediaWiki API interactions
- `wikitextparser` - for parsing wikitext templates
- `sqlite3` - for generating reports and tracking operations
- Comprehensive logging system

**Current Bot Functionality (to be preserved):**

1. **Language List Retrieval**: Fetch language codes from `User:Mr. Ibrahem/import bot` on nccommons.org
   - Example format: `* {{User:Mr. Ibrahem/import bot/line|af}}`

2. **Template Discovery**: For each language, find all Wikipedia pages containing `{{NC|filename.jpg}}`

3. **File Processing**:
   - Extract file names and captions from NC templates
   - Fetch files from NC Commons
   - Upload to Wikipedia with proper attribution
   - Handle duplicates intelligently

4. **Page Updates**: Replace `{{NC|...}}` templates with the newly uploaded file information

5. **Multi-language Support**: Process all languages iteratively

**Refactoring Requirements:**

✅ **Code Architecture:**
- Modular, object-oriented design
- Separation of concerns (API handling, parsing, database, logging)
- Error handling and retry mechanisms
- Configuration management (external config file)

✅ **Logging:**
- Multi-level logging (DEBUG, INFO, WARNING, ERROR)
- Separate log files for different operations
- Timestamped entries with contextual information
- Rotating file handlers to prevent log bloat

✅ **SQLite3 Reporting:**
- Track all operations (uploads, updates, errors)
- Store metadata: timestamps, language codes, file names, success/failure status
- Generate summary reports: files processed per language, error rates, duplicate handling
- Query interface for analytics

✅ **Best Practices:**
- Type hints throughout
- Comprehensive docstrings
- PEP 8 compliance
- Rate limiting and API throttling
- Proper resource cleanup (database connections, file handles)
- Unit test structure outline

**Deliverable:**

Please provide a **detailed refactoring plan** including:
1. Proposed project structure (file/folder organization)
2. Class design and responsibilities
3. Database schema for SQLite3 reports
4. Logging strategy and configuration
5. Key improvements over current implementation
6. Migration path from old code to new code

Do NOT write the full implementation yet—I need the architectural plan first to review before proceeding with development.

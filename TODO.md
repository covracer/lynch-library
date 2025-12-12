# Lynch Library TODO

## Django Project Setup
- [ ] Run `django-admin startproject config` (settings.py will live in config directory)
- [ ] Note: This is a web server application, not a library for installation by others

## Models (Commit 1)
- [ ] Define `CatalogItem` or `Media` model with:
  - [ ] URL field
  - [ ] Title field
  - [ ] Foreign key to Author model
  - [ ] Foreign key to Publisher model
- [ ] Create Author model
- [ ] Create Publisher model

## Management Command 1 (Commit 2)
- [ ] Write management command to scrape Dave Dubin's "Living with Lynch" podcast
- [ ] Enumerate all episodes on best-effort basis
- [ ] Create CSV file output
- [ ] Use data migration and SQLite feature for loading data from CSV
- [ ] Include tests for management command:
  - [ ] Test happy path success case
  - [ ] Test multiple pages
  - [ ] Test failure cases (404, 503)
  - [ ] Create minimal test cases from trimmed website responses

## GitHub Action (Commit 3)
- [ ] Create GitHub Action scheduled once per week to:
  - [ ] Run the management command
  - [ ] Update the CSV file
  - [ ] Commit the results
  - [ ] Create a pull request

## Management Command 2 (Commit 4)
- [ ] Write second management command to:
  - [ ] Explore one URL
  - [ ] Download its content
  - [ ] Transcribe audio to text
- [ ] Use Django storages with Cloudflare R2 for archiving audio data
- [ ] Create new model for text transcripts that relates to CatalogItem
- [ ] Use Cloudflare or OpenAI Whisper for transcription
- [ ] Save transcription text to R2
- [ ] Link to text from Django admin interface

## Technical Notes
- Use SQLite for database
- Configure Django storages for Cloudflare R2
- Ensure proper error handling for web scraping
- Consider rate limiting for API calls
- Test transcription pipeline thoroughly

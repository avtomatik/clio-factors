# Security and safe execution

ClioFactors does not require credentials, scrape websites, or make network requests for its reference recipe. It reads explicitly named CSV members from packaged ZIP snapshots without extracting executable content. User-selected output directories may be written to or overwritten; choose separate paths for important runs.

Do not run the preserved scripts in `legacy/` without inspecting them and their dependencies. They are out of scope for the supported implementation and may attempt obsolete downloads, read local files or execute plotting code at import time.

If you discover a security vulnerability, contact the repository owner privately. Do not post exploit details or credentials in public issues. Before distributing the repository, audit source-data licensing and any unpublished material inherited from the original archive.

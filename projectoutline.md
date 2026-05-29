1. Scaffold the repo and write CLAUDE.md: Create the project folder, CLAUDE.md, .gitignore, and requirements.txt with initial dependencies (rich, typer). Verify: cat CLAUDE.md reads cleanly and describes the project stack, structure, and commands.

2. Initialize git and make first commit: Run git init, stage all files, and push an initial commit to a new GitHub repo. Verify: git log shows one commit and the repo exists on GitHub.

3. Set up SQLite database and schema: Write a database.py that creates a donations table with columns id, date, location, blood_type, and pints on first run. Verify: Run python database.py and confirm the table exists using a quick sqlite3 shell query: .tables.

4. Build the log command: Add a log CLI command using typer that prompts for date, location, and blood type then inserts a row into the database. Verify: Run python tracker.py log, fill in the prompts, then check the DB with sqlite3 to confirm the row is there.

5. Build the history command: Add a history command that queries all donations and renders them as a formatted rich table in the terminal. Verify: Run python tracker.py history and confirm your logged donation appears in a clean, readable table.

6. Calculate eligibility logic: Write a helper function in a logic.py file that takes the most recent donation date and returns the next eligible date (56 days for whole blood). Verify: Unit test it manually in a Python shell with a known date and confirm the output is exactly 56 days later.

7. Build the status command (eligibility): Add a status command that calls the eligibility helper and prints either "✅ You're eligible now!" or "⏳ Next eligible: [date]" using rich. Verify: Run python tracker.py status and confirm the date math is correct against your logged donation.

8. Add the gallons visual to status: Calculate total pints donated, convert to gallons, and render a rich progress bar and summary line (e.g. 0.875 gal ████████░░░░░░░░). Verify: Run python tracker.py status, confirm the bar fills proportionally, log a second fake donation and confirm it updates.

9. Add "lives saved" counter to status: Add a line to status that multiplies total donations by 3 and displays "🩸 Lives potentially saved: X". Verify: Run python tracker.py status and confirm the number is exactly 3× your donation count.

10. Polish the CLI (help text + error handling): Add typer help strings to every command and a graceful error message if the user runs status or history with no donations logged yet. Verify: Run python tracker.py --help and confirm all commands are described; run status on a fresh DB and confirm it doesn't crash.

11. Final git commit and README: Write a short README.md with setup instructions and the three commands, then commit everything cleanly. Verify: A friend (or you, fresh eyes) could clone the repo and run the app in under 2 minutes following only the README.
## Task 3 — <short name>
- Brief: [link or paste]
- What Claude proposed: [1-2 lines]
- What I changed before approving: [1-2 lines]
- Verification: [what you ran or clicked to confirm it works]
- One thing I learned: ...

## Task 1: Scaffold the repo and write CLAUDE.md: 
- Brief: Create the project folder, CLAUDE.md, .gitignore, and requirements.txt with initial dependencies (rich, typer). Verify: cat CLAUDE.md reads cleanly and describes the project stack, structure, and commands.
- What Claude proposed: File structure, including separating python into 3 dedicated files
- What I changed before approving: Added Basic init for a brand new project, questioned if 3 files were necessary before realizing they had a use
- Verification: Project exists in a folder called capstonedonation on WSL
- One thing I learned: yes all python could be on a single file but separating it makes it easier to isolate different parts of your program

## Task 2: Initialize git and make first commit: 
- Brief: Run git init, stage all files, and push an initial commit to a new GitHub repo. Verify: git log shows one commit and the repo exists on GitHub.
- What Claude proposed: Initialize git 
- What I changed before approving: Added initial commit message
- Verification: Github shows project contents on webpage
- One thing I learned: git log lets you see what git did recently in the repo

## Task 3: Set up SQLite database and schema: 
- Brief: Write a database.py that creates a donations table with columns id, date, location, blood_type, and pints on first run. Verify: Run python database.py and confirm the table exists using a quick sqlite3 shell query: .tables.
- What Claude proposed: Database creation in database.py 
- What I changed before approving: Ensuring all table columns made sense for an app designed for one person at a time
- Verification: sqlite3 donations.db ".tables" to give a list of existing tables (verified donations was in that list)
- One thing I learned: donations.db should only exist locally so needs to be in gitignore

## Task 4: Build the log command: 
- Brief: Add a log CLI command using typer that prompts for date, location, and blood type then inserts a row into the database. Verify: Run python tracker.py log, fill in the prompts, then check the DB with sqlite3 to confirm the row is there.
- What Claude proposed: Suggested use of typer to handle CLI interactions between app and user
- What I changed before approving: Making sure all edge cases would be covered. Used outside source to confrim
- Verification: Attempted a correct run through and a bunch of incorrect with bad inputs, empty states, to ensure nothing broke. After creating a few dates, checked the database to ensure logs are being stored
- One thing I learned: Claude is faster. I have claude, so i can't waste time trying to do this on my own.

## Task 5: Build the history command: 
- Brief: Add a history command that queries all donations and renders them as a formatted rich table in the terminal. Verify: Run python tracker.py history and confirm your logged donation appears in a clean, readable table.
- What Claude proposed: using rich to make easily readable table with all donations
- What I changed before approving: Limits to size of inputs
- Verification: added logs through log feature and then ran history to ensure table showed up with all donations available
- One thing I learned: Think about limits- how far back should dates be allowed? How many donations should be allowed at a time?

## Task 6: Calculate eligibility logic: 
- Brief: Write a helper function in a logic.py file that takes the most recent donation date and returns the next eligible date (56 days for whole blood). Verify: Unit test it manually in a Python shell with a known date and confirm the output is exactly 56 days later.
- What Claude proposed: Using date time to find next eligable date
- What I changed before approving: ensuring no security or bad input vunerabilities exist
- Verification: calling get_next_eligible_date gives me a date that's 56 days after the date I passed into the method
- One thing I learned: Simple solutions are just as elegant

7. Build the status command (eligibility): Add a status command that calls the eligibility helper and prints either "✅ You're eligible now!" or "⏳ Next eligible: [date]" using rich. Verify: Run python tracker.py status and confirm the date math is correct against your logged donation.

8. Add the gallons visual to status: Calculate total pints donated, convert to gallons, and render a rich progress bar and summary line (e.g. 0.875 gal ████████░░░░░░░░). Verify: Run python tracker.py status, confirm the bar fills proportionally, log a second fake donation and confirm it updates.

9. Add "lives saved" counter to status: Add a line to status that multiplies total donations by 3 and displays "🩸 Lives potentially saved: X". Verify: Run python tracker.py status and confirm the number is exactly 3× your donation count.

10. Polish the CLI (help text + error handling): Add typer help strings to every command and a graceful error message if the user runs status or history with no donations logged yet. Verify: Run python tracker.py --help and confirm all commands are described; run status on a fresh DB and confirm it doesn't crash.

11. Final git commit and README: Write a short README.md with setup instructions and the three commands, then commit everything cleanly. Verify: A friend (or you, fresh eyes) could clone the repo and run the app in under 2 minutes following only the README.

### AI Workflow
Which tool you reached for in each lane (planning, executing, polishing, reviewing).
- I used Claude chat especially for brainstorming, coming up with plans, and finding vunerabilities in code. Claude CLI was used primarily for executing code, and applying the designs and briefs to the current codebase and state. Claude code for planning and reviewing, claude cli for executing and polishing
One moment one tool clearly outperformed another.
- I felt like the chat version was a lot easier for me to brainstorm with. Claude chat wasn't constantly getting distracted by the code which allowed it to just focus on the design and planning first.
One moment you switched tools mid-task because the first one was the wrong fit.
- Claude CLI knows the code but Claude chat doesn't so sometimes I would write the plan with chat and then bring it to the cli to compare the plan to the current codebase and find any misunderstandings that occured due to the fact that claude chat just doesn't know the codebase.

### Reflection:
Where did the agentic workflow let you ship things you couldn't have shipped alone in 4 hours?
- A lot of the execution could not have happened in this time without claude. I tried doing some of the execution myself but claude is able to compile and ship everything much faster than I could alone.
Where did you have to step in and override Claude? What did you know that it didn't?
- I stepped in espicially to address security issues and bad values. I wanted to make sure there were no gaps. I knew I didn't have to step in whenever claude made a plan or executed something and then immediately after I asked "So what did you miss? What could go wrong?" and claude ended up thinking for up to 5 minutes before I stopped it because there wasn't anything that was missed. One part where I redirected claude was with just a simple comment when creating the lives saved estimation about how pints can be stored with decimals so multiplying by 3 would give a decimal back so we needed to multiply and then truncate to get a better estimate.
What did this project reveal about your own judgment and your own knowledge gaps? (This is the most important question. Spend the most words here.)
- I feel like it really tested my conceptual knowledge a lot more than my syntax knowledge. I didn't necessairally have to master how the typer functions worked in the console, but I did have to understand how methods are structured and know what some common vunerabilities are, like SQL injection, so that I can catch them when claude doesn't. I really exercised my critical thinking by analyzing what claude was giving me and deciding what direction I wanted to go but in summary it was just a lot more higher level thinking versus the grunt work I'm usually used to.
How will you bring this workflow into your internship? What's the first thing you'll do on day one?
- Definiately gonna take a lot of these lessons with me, like understanding the foundation but letting AI do the heavy lifting of syntax and handling all the different edge cases. I can be a lot more efficient if I'm planning stuff and requesting stuff and letting AI do the tough work than if I tried doing it all myself. I'm going to go into my internship not just knowing how to build but how to orchestrate stuff.
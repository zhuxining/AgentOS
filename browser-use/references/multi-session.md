# Multiple Browser Sessions

## Why use multiple sessions

When you need more than one browser at a time:

- Two different Chrome profiles simultaneously
- Isolated browser for testing that won't affect the user's browsing
- Running a headed browser for debugging while headless runs in background

## How sessions are isolated

Each `--session NAME` gets:

- Its own daemon process
- Its own Unix socket (`~/.browser-use/{name}.sock`)
- Its own PID file and state file
- Its own browser instance (completely independent)
- Its own tab ownership state (multi-agent locks don't cross sessions)

## The `--session` flag

Must be passed on every command targeting that session:

```bash
browser-use --session work open <url>      # goes to 'work' daemon
browser-use --session work state           # reads from 'work' daemon
browser-use state                          # goes to 'default' daemon (different browser)
```

If you forget `--session`, the command goes to the `default` session. This is the most common mistake — you'll interact with the wrong browser.

## Combining sessions with browser modes

```bash
# Session 1: connect to user's Chrome
browser-use --session chrome connect

# Session 2: headed Chromium for debugging
browser-use --session debug --headed open <url>
```

Each session is fully independent. The chrome session talks to the user's Chrome, and the debug session manages its own Chromium — both running simultaneously.

## Listing and managing sessions

```bash
browser-use sessions
```

Output:

```
SESSION          PHASE          PID      CONFIG
chrome           running        12346    cdp
debug            ready          12347    headed
```

PHASE shows the daemon lifecycle state: `initializing`, `ready`, `starting`, `running`, `shutting_down`, `stopped`, `failed`.

```bash
browser-use --session chrome close          # close one session
browser-use close --all                     # close every session
```

## Common patterns

**Throwaway test browser:**

```bash
browser-use --session test --headed open https://localhost:3000
# ... test, debug, inspect ...
browser-use --session test close    # done, clean up
```

**Environment variable:**

```bash
export BROWSER_USE_SESSION=work
browser-use open <url>              # uses 'work' session without --session flag
```

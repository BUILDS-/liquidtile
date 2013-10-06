# pyFireTile

FireTile is a library for interacting with FireTiles made by BUILDS.

Currently there is only one and it is a 3x3 FireTile

## Serial Communications Protocol (v1)

The current serial communications protocol is not very well thought out, but
it is easy to implement and write by hand for debugging. There is no
error checking.

Speed: 19200 baud
No Parity, No Flow Control, 8 bit messages

The message format goes as follows and is all sent in ASCII:

| Name                 | Number of Characters | Description
|----------------------|----------------------|---------------------
| Beginning of Message | 1                    | Send a ":" to start message
| Address or Command   | 1                    | Send a hex character (0-9, a-f) to send address. 'u' to update
| Red Color            | 2 (or 0)             | 2 hex characters to signify the 8 bit value of red. Does not exist for update
| Green Color          | 2 (or 0)             | 2 hex character to signifiy the 8 bit value of green. Does not exist for update.
| Blue  Color          | 2 (or 0)             | 2 hex character to signifiy the 8 bit value of blue. Does not exist for update.
| End of Message       | 1                    | Send a '\n' to end message (the NEWLINE character).

Example message:

```
:0FF00FF\n
```